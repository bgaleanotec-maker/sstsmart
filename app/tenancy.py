"""Multi-tenancy aplicativa (ADR-2 del dossier: ~150 líneas propias, auditables).

Primera línea de aislamiento: filtro automático por `empresa_id` en cada
SELECT de los modelos que llevan TenantMixin, más asignación/validación del
tenant en cada flush. La red definitiva (Row Level Security) se aplica en
Postgres con `scripts/rls_postgres.sql` — este módulo usa la misma semántica.

Reglas:
- El tenant se resuelve al inicio de CADA request desde el usuario autenticado
  (nunca de un valor heredado del hilo: ContextVar se resetea siempre).
- Sin tenant en contexto (login, scheduler, scripts) no se filtra: los jobs
  de escalamiento necesitan ver todas las empresas. Las rutas de negocio
  siempre corren con usuario autenticado y por tanto con tenant.
- Un objeto nuevo sin empresa_id la hereda del contexto; uno con empresa_id
  de OTRO tenant aborta el flush.
"""
from contextvars import ContextVar

from sqlalchemy import event
from sqlalchemy.orm import Session, with_loader_criteria
from sqlalchemy.ext.declarative import declared_attr

from app import db

current_empresa_id = ContextVar('current_empresa_id', default=None)


class TenantMixin:
    """Añade empresa_id (FK + índice) y activa el filtro automático."""

    @declared_attr
    def empresa_id(cls):
        # Nullable a propósito: fase "expand" (expand/contract, doc 03-arq §3).
        # Tras el backfill en producción se vuelve NOT NULL por migración.
        return db.Column(
            db.Integer,
            db.ForeignKey('empresas.id'),
            nullable=True,
            index=True,
        )


def set_empresa(empresa_id):
    """Fija el tenant del contexto actual. None = sin filtro (sistema)."""
    current_empresa_id.set(empresa_id)


def empresa_actual():
    return current_empresa_id.get()


@event.listens_for(Session, 'do_orm_execute')
def _filtro_tenant(execute_state):
    """Inyecta `empresa_id = <tenant>` en todo SELECT de modelos tenant."""
    eid = current_empresa_id.get()
    if eid is None:
        return
    if not execute_state.is_select:
        return
    if execute_state.is_column_load or execute_state.is_relationship_load:
        return
    execute_state.statement = execute_state.statement.options(
        with_loader_criteria(
            TenantMixin,
            lambda cls: cls.empresa_id == eid,
            include_aliases=True,
        )
    )


@event.listens_for(Session, 'before_flush')
def _asignar_tenant(session, flush_context, instances):
    """Asigna el tenant a objetos nuevos y bloquea escrituras cross-tenant."""
    eid = current_empresa_id.get()
    if eid is None:
        return
    for obj in session.new:
        if isinstance(obj, TenantMixin):
            if obj.empresa_id is None:
                obj.empresa_id = eid
            elif obj.empresa_id != eid:
                raise PermissionError(
                    f"Intento de crear {type(obj).__name__} para la empresa "
                    f"{obj.empresa_id} desde el contexto de la empresa {eid}"
                )
    for obj in session.dirty:
        if isinstance(obj, TenantMixin) and obj.empresa_id not in (None, eid):
            raise PermissionError(
                f"Intento de modificar {type(obj).__name__} de la empresa "
                f"{obj.empresa_id} desde el contexto de la empresa {eid}"
            )


def init_tenancy(app):
    """Middleware: resuelve el tenant por request, sin fallbacks silenciosos."""
    from flask_login import current_user

    @app.before_request
    def _resolver_tenant():
        # Reset SIEMPRE antes de tocar current_user: un ContextVar vive por
        # hilo y sin esto el request heredaría el tenant del request anterior
        # (el error #1 de las guías de RLS, aquí en versión aplicativa).
        current_empresa_id.set(None)
        try:
            if current_user.is_authenticated:
                current_empresa_id.set(getattr(current_user, 'empresa_id', None))
        except Exception:
            current_empresa_id.set(None)

    @app.teardown_request
    def _limpiar_tenant(exc=None):
        current_empresa_id.set(None)
