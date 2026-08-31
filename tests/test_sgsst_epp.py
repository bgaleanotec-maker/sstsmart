# -*- coding: utf-8 -*-
"""Tests del núcleo SG-SST (política, plan, indicadores) y kardex EPP."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, timedelta

import pytest

from app import create_app, db
from app.tenancy import set_empresa


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


@pytest.fixture()
def cliente(app):
    from app.models import Empresa, Usuario
    e = Empresa(nit='900123456', razon_social='Guía SAS', num_trabajadores=20,
                clase_riesgo=2)
    db.session.add(e)
    db.session.commit()
    admin = Usuario(email='a@g.local', nombre_completo='Admin G', rol='Admin',
                    empresa_id=e.id, activo=True)
    admin.set_password('pw12345')
    db.session.add(admin)
    db.session.commit()
    c = app.test_client()
    c.post('/auth/login', data={'email': 'a@g.local', 'password': 'pw12345'})
    return c


def test_regimen_agropecuario(app):
    """Res. 0312 art. 3 num. 8: agro ≤10 trabajadores riesgo I-III → 21."""
    from app.models import Empresa
    normal = Empresa(nit='1', razon_social='x', num_trabajadores=5, clase_riesgo=1)
    agro = Empresa(nit='2', razon_social='y', num_trabajadores=5, clase_riesgo=1,
                   unidad_agropecuaria=True)
    agro_alto = Empresa(nit='3', razon_social='z', num_trabajadores=5, clase_riesgo=5,
                        unidad_agropecuaria=True)
    assert normal.calcular_regimen() == 7
    assert agro.calcular_regimen() == 21
    assert agro_alto.calcular_regimen() == 60


def test_politica_crear_y_versionar(cliente, app):
    from app.models import PoliticaSST
    r = cliente.get('/sgsst/politica')
    assert r.status_code == 200
    assert 'Guía SAS' in r.get_data(as_text=True)  # plantilla prellenada

    anio = date.today().year
    r = cliente.post(f'/sgsst/politica?anio={anio}', data={
        'contenido': 'Política de prueba', 'firmada_por': 'Gerente',
        'cargo_firmante': 'Representante Legal', 'fecha_firma': date.today().isoformat(),
        'divulgada': 'on', 'fecha_divulgacion': date.today().isoformat(),
    }, follow_redirects=True)
    assert r.status_code == 200
    with app.app_context():
        set_empresa(None)
        pol = PoliticaSST.query.filter_by(anio=anio).first()
        assert pol and pol.version == 1 and pol.divulgada

    # Segunda edición → versión 2
    cliente.post(f'/sgsst/politica?anio={anio}', data={'contenido': 'v2'})
    with app.app_context():
        set_empresa(None)
        assert PoliticaSST.query.filter_by(anio=anio).first().version == 2

    r = cliente.get(f'/sgsst/politica/{anio}/imprimir')
    assert r.status_code == 200


def test_plan_anual_y_vencidas(cliente, app):
    anio = date.today().year
    cliente.post(f'/sgsst/plan?anio={anio}', data={
        'anio': anio, 'objetivo': 'Reducir AT', 'actividad': 'Inspección mensual',
        'fecha_programada': (date.today() - timedelta(days=10)).isoformat(),
    })
    r = cliente.get(f'/sgsst/plan?anio={anio}')
    body = r.get_data(as_text=True)
    assert 'Inspección mensual' in body
    from app.models import PlanTrabajoActividad
    with app.app_context():
        set_empresa(None)
        act = PlanTrabajoActividad.query.first()
        assert act.vencida  # programada en el pasado, no ejecutada
        aid = act.id
    cliente.post(f'/sgsst/plan/{aid}/estado', data={'estado': 'Ejecutada'})
    with app.app_context():
        set_empresa(None)
        act = db.session.get(PlanTrabajoActividad, aid)
        assert act.estado == 'Ejecutada' and act.fecha_ejecucion


def test_epp_kardex_y_alertas(cliente, app):
    from app.models import Usuario, EntregaEPP
    with app.app_context():
        set_empresa(None)
        uid = Usuario.query.first().id
    r = cliente.post('/epp/nueva', data={
        'trabajador_id': uid, 'elemento': 'Casco de seguridad',
        'certificacion': 'ANSI Z89.1', 'vida_util_meses': '12',
        'fecha_entrega': (date.today() - timedelta(days=400)).isoformat(),
        'constancia': 'Acta 001',
    }, follow_redirects=True)
    assert r.status_code == 200
    with app.app_context():
        set_empresa(None)
        e = EntregaEPP.query.first()
        assert e.fecha_reposicion is not None
        assert e.reposicion_vencida  # 400 días > 12 meses
    body = cliente.get('/epp/').get_data(as_text=True)
    assert 'reposición vencida' in body
    assert 'sin capacitación' in body


def test_indicadores(cliente, app):
    from app.models import Evento, Empresa
    with app.app_context():
        set_empresa(None)
        eid = Empresa.query.first().id
        set_empresa(eid)  # los eventos deben pertenecer al tenant
        db.session.add(Evento(tipo='Accidente de trabajo', titulo='AT1',
                              dias_incapacidad=10))
        db.session.add(Evento(tipo='Enfermedad laboral', titulo='EL1',
                              dias_incapacidad=5))
        db.session.commit()
        set_empresa(None)
    r = cliente.get(f'/sgsst/indicadores?anio={date.today().year}')
    body = r.get_data(as_text=True)
    assert r.status_code == 200
    # 1 AT / 20 trabajadores * 100 = 5.0
    assert '5.0' in body
