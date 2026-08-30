# -*- coding: utf-8 -*-
"""Tests de aislamiento entre tenants (docs/03-arquitectura/01 §2.6).

Por cada modelo de dominio con TenantMixin: lo que crea la empresa A no puede
leerse desde el contexto de la empresa B, y un modelo tenant nuevo sin cubrir
aquí debe romper la suite (test de completitud).
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from app import create_app, db
from app.tenancy import TenantMixin, set_empresa


@pytest.fixture()
def app():
    os.environ['SCHEDULER_ENABLED'] = '0'
    app = create_app('development')
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False,
                      SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
    with app.app_context():
        db.create_all()
        yield app
        set_empresa(None)
        db.session.remove()
        db.drop_all()


def _empresas(app):
    from app.models import Empresa
    a = Empresa(nit='900000001', razon_social='Empresa A', num_trabajadores=5)
    b = Empresa(nit='900000002', razon_social='Empresa B', num_trabajadores=5)
    db.session.add_all([a, b])
    db.session.commit()
    return a, b


# Fábricas mínimas por modelo tenant
def _fabricas():
    from app.models import (Usuario, Empleado, CondicionInsegura, Evento,
                            RiesgoMatriz, Control, RequisitoLegal,
                            ConsultaJuridica, Curso, GestionReporte,
                            Autoevaluacion, AccionMejora)

    def usuario(i):
        u = Usuario(email=f'u{i}@t.local', nombre_completo=f'U{i}', rol='Empleado')
        u.set_password('x')
        return u

    def condicion(i):
        c = CondicionInsegura(titulo=f'C{i}')
        c.generar_numero_reporte()
        return c

    def consulta(i):
        c = ConsultaJuridica(titulo=f'Q{i}', descripcion='d')
        c.generar_numero_consulta()
        return c

    def control(i):
        r = RiesgoMatriz(nombre_riesgo=f'R-ctl-{i}')
        db.session.add(r)
        db.session.flush()
        u = usuario(f'resp{i}')
        db.session.add(u)
        db.session.flush()
        return Control(codigo=f'CTL-{i}', nombre='c', riesgo_id=r.id,
                       responsable_id=u.id)

    return {
        'Usuario': usuario,
        'Empleado': lambda i: Empleado(usuario=usuario(f'e{i}')),
        'CondicionInsegura': condicion,
        'Evento': lambda i: Evento(tipo='AT', titulo=f'E{i}'),
        'RiesgoMatriz': lambda i: RiesgoMatriz(nombre_riesgo=f'R{i}'),
        'Control': control,
        'RequisitoLegal': lambda i: RequisitoLegal(norma=f'N{i}', articulo='1', descripcion='d'),
        'ConsultaJuridica': consulta,
        'Curso': lambda i: Curso(titulo=f'K{i}'),
        'GestionReporte': lambda i: GestionReporte(reporte=condicion(f'g{i}')),
        'Autoevaluacion': lambda i: Autoevaluacion(anio=2026, regimen=7),
        'AccionMejora': lambda i: AccionMejora(
            autoevaluacion=Autoevaluacion(anio=2025, regimen=7),
            item_codigo='1.1.1', descripcion='d'),
    }


MODELOS = ['Usuario', 'Empleado', 'CondicionInsegura', 'Evento', 'RiesgoMatriz',
           'Control', 'RequisitoLegal', 'ConsultaJuridica', 'Curso',
           'GestionReporte', 'Autoevaluacion', 'AccionMejora']


@pytest.mark.parametrize('nombre', MODELOS)
def test_aislamiento(app, nombre):
    import app.models as m
    a, b = _empresas(app)
    a_id, b_id = a.id, b.id
    fabricas = _fabricas()
    Modelo = getattr(m, nombre)

    set_empresa(a_id)
    obj = fabricas[nombre](1)
    db.session.add(obj)
    db.session.commit()
    obj_id = obj.id
    assert obj.empresa_id == a_id, "before_flush debe asignar el tenant"

    db.session.expunge_all()

    # Desde B: no lo lee, no lo cuenta
    set_empresa(b_id)
    assert db.session.query(Modelo).filter_by(id=obj_id).first() is None
    assert db.session.query(Modelo).count() == 0

    # Desde B: no puede CREAR un registro marcado como de A
    with pytest.raises(PermissionError):
        intruso = fabricas[nombre](2)
        intruso.empresa_id = a_id
        db.session.add(intruso)
        db.session.flush()
    db.session.rollback()


def test_todo_modelo_tenant_esta_cubierto(app):
    """Un modelo nuevo con TenantMixin debe añadirse a MODELOS (y a la lista
    de backfill/RLS). Si no, este test truena a propósito."""
    tenant_models = {m.class_.__name__ for m in db.Model.registry.mappers
                     if issubclass(m.class_, TenantMixin)}
    faltan = tenant_models - set(MODELOS)
    assert not faltan, (
        f"Modelos tenant sin test de aislamiento: {faltan}. "
        "Añádelos a MODELOS aquí, al backfill de scripts/init_prod_db.py "
        "y a scripts/rls_postgres.sql"
    )


def test_sin_contexto_no_filtra(app):
    """Sin tenant en contexto (scheduler/scripts) se ve todo — documentado."""
    from app.models import RiesgoMatriz
    a, b = _empresas(app)
    set_empresa(a.id)
    db.session.add(RiesgoMatriz(nombre_riesgo='RA'))
    db.session.commit()
    set_empresa(b.id)
    db.session.add(RiesgoMatriz(nombre_riesgo='RB'))
    db.session.commit()
    set_empresa(None)
    assert db.session.query(RiesgoMatriz).count() == 2
