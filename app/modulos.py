"""Gating de módulos SaaS por empresa.

- Context processor: expone `modulos_activos` y el catálogo a las plantillas
  (la navbar solo muestra lo contratado).
- before_request: si la empresa no contrató el módulo del blueprint pedido,
  redirige al dashboard con aviso. Admin de plataforma (rol Admin) nunca se
  bloquea — él configura la suscripción.
- Empresa sin filas en EmpresaModulo → todos los módulos activos (modo legado /
  demo, para no romper instancias existentes hasta configurarlas).
"""
from flask import flash, redirect, url_for, request
from flask_login import current_user

from app.data.modulos import MODULOS, BLUEPRINT_A_MODULO

BLUEPRINTS_LIBRES = {'auth', 'dashboard', 'admin', None}


def modulos_de_empresa():
    """Set de códigos de módulo activos para la empresa del usuario actual."""
    from app.models.suscripcion import EmpresaModulo
    if not current_user.is_authenticated or not getattr(current_user, 'empresa_id', None):
        return set(MODULOS)  # sin empresa asignada: no bloquear (legado)
    filas = EmpresaModulo.query.filter_by(empresa_id=current_user.empresa_id).all()
    if not filas:
        return set(MODULOS)  # sin configurar: todo activo
    return {f.modulo for f in filas if f.activo}


def init_modulos(app):
    @app.context_processor
    def _inyectar_modulos():
        try:
            activos = modulos_de_empresa() if current_user.is_authenticated else set()
        except Exception:
            activos = set(MODULOS)
        return {'modulos_activos': activos, 'CATALOGO_MODULOS': MODULOS}

    @app.before_request
    def _gate_modulo():
        bp = request.blueprint
        if bp in BLUEPRINTS_LIBRES or bp not in BLUEPRINT_A_MODULO:
            return
        if not current_user.is_authenticated:
            return  # login_required de la vista se encarga
        if current_user.tiene_rol('Admin'):
            return
        codigo = BLUEPRINT_A_MODULO[bp]
        if codigo not in modulos_de_empresa():
            flash(f'El módulo "{MODULOS[codigo]["nombre"]}" no está incluido en tu plan. '
                  'Pide a tu administrador activarlo.', 'warning')
            return redirect(url_for('dashboard.index'))
