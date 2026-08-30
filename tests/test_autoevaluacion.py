# -*- coding: utf-8 -*-
"""Tests del módulo de autoevaluación Res. 0312/2019."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from app import create_app, db
from app.tenancy import set_empresa
from app.data.estandares_0312 import ESTANDARES, items_para_regimen, clasificar
from app.services import autoevaluacion_service as svc


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


def _empresa(trabajadores, riesgo):
    from app.models import Empresa
    e = Empresa(nit=f'9{trabajadores}{riesgo}', razon_social='Test',
                num_trabajadores=trabajadores, clase_riesgo=riesgo)
    db.session.add(e)
    db.session.commit()
    set_empresa(e.id)
    return e


def test_catalogo_integridad():
    assert len(ESTANDARES) == 60
    assert abs(sum(e[4] for e in ESTANDARES) - 100.0) < 1e-6
    assert len(items_para_regimen(7)) == 7
    assert len(items_para_regimen(21)) == 21
    assert len(items_para_regimen(60)) == 60


def test_regimen_por_empresa(app):
    from app.models import Empresa
    casos = [(5, 1, 7), (10, 3, 7), (11, 1, 21), (50, 3, 21),
             (51, 1, 60), (5, 4, 60), (200, 5, 60)]
    for trab, riesgo, esperado in casos:
        e = Empresa(nit=f't{trab}r{riesgo}', razon_social='x',
                    num_trabajadores=trab, clase_riesgo=riesgo)
        assert e.calcular_regimen() == esperado, (trab, riesgo)


def test_clasificacion():
    assert clasificar(59.9) == 'CRITICO'
    assert clasificar(60) == 'MODERADO'
    assert clasificar(85) == 'MODERADO'
    assert clasificar(85.1) == 'ACEPTABLE'
    assert clasificar(100) == 'ACEPTABLE'


def test_todo_cumple_da_100(app):
    e = _empresa(5, 1)   # régimen 7
    a = svc.crear_autoevaluacion(e, 2026, None)
    assert a.respuestas.count() == 7
    for r in a.respuestas:
        r.calificacion = 'CUMPLE'
    svc.cerrar_autoevaluacion(a)
    assert a.puntaje_total == 100.0
    assert a.clasificacion == 'ACEPTABLE'
    assert a.acciones.count() == 0


def test_no_cumple_resta_y_genera_plan(app):
    e = _empresa(20, 2)  # régimen 21
    a = svc.crear_autoevaluacion(e, 2026, None)
    assert a.respuestas.count() == 21
    for r in a.respuestas:
        r.calificacion = 'NO_CUMPLE' if r.item_codigo == '5.1.1' else 'CUMPLE'
    svc.cerrar_autoevaluacion(a)
    # 5.1.1 pesa 5.0 → 95
    assert a.puntaje_total == 95.0
    assert a.clasificacion == 'ACEPTABLE'
    assert a.acciones.count() == 1
    assert a.acciones.first().item_codigo == '5.1.1'


def test_no_aplica_otorga_puntaje(app):
    e = _empresa(5, 1)
    a = svc.crear_autoevaluacion(e, 2026, None)
    for r in a.respuestas:
        r.calificacion = 'NO_APLICA'
        r.justificacion = 'No aplica por actividad'
    svc.cerrar_autoevaluacion(a)
    assert a.puntaje_total == 100.0


def test_pendientes_bloquean_cierre(app):
    e = _empresa(5, 1)
    a = svc.crear_autoevaluacion(e, 2026, None)
    with pytest.raises(ValueError):
        svc.cerrar_autoevaluacion(a)


def test_flujo_web_completo(app):
    from app.models import Usuario
    e = _empresa(5, 1)
    admin = Usuario(email='a@t.local', nombre_completo='A', rol='Admin',
                    empresa_id=e.id, activo=True)
    admin.set_password('pw12345')
    db.session.add(admin)
    db.session.commit()
    set_empresa(None)

    c = app.test_client()
    c.post('/auth/login', data={'email': 'a@t.local', 'password': 'pw12345'})
    r = c.post('/autoevaluacion/nueva', data={'anio': '2026'}, follow_redirects=False)
    assert r.status_code == 302

    from app.models import Autoevaluacion
    with app.app_context():
        set_empresa(None)
        a = Autoevaluacion.query.filter_by(anio=2026).first()
        assert a is not None
        aid = a.id

    data = {'accion': 'cerrar'}
    for item in items_para_regimen(7):
        data[f'cal_{item[0]}'] = 'CUMPLE'
    r = c.post(f'/autoevaluacion/{aid}/guardar', data=data, follow_redirects=False)
    assert r.status_code == 302 and 'resultado' in r.headers['Location']

    r = c.get(f'/autoevaluacion/{aid}/export.csv')
    assert r.status_code == 200
    assert 'Autoevaluaci' in r.get_data(as_text=True)
