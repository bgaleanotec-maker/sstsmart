# -*- coding: utf-8 -*-
"""Pruebas del panel "Así va tu SG-SST" (rediseno-ui/README.md §9.4)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, timedelta

import pytest

from app import create_app, db
from app.tenancy import set_empresa
from app.services.panel import (puntos_arco, punto_arco, nivel_de,
                                faltan_para_aceptable, datos_panel)
from app.services.vencimientos import proximos_vencimientos
from app.data.hitos_normativos import proxima_fecha, proximo_hito


@pytest.fixture()
def app():
    os.environ['SCHEDULER_ENABLED'] = '0'
    app = create_app('testing')
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False,
                      SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
                      SERVER_NAME='localhost')
    with app.app_context():
        db.create_all()
        yield app
        set_empresa(None)
        db.session.remove()
        db.drop_all()


def _empresa(trab=20, riesgo=2):
    from app.models import Empresa
    e = Empresa(nit='900111222', razon_social='Piloto', num_trabajadores=trab, clase_riesgo=riesgo)
    e.calcular_regimen()
    db.session.add(e)
    db.session.commit()
    set_empresa(e.id)
    return e


# ---------- geometría del medidor ----------

def test_puntos_arco_extremos_y_cortes():
    # Arco r=90: cortes de la especificación §4.2
    assert punto_arco(60) == {'x': 137.8, 'y': 29.4}
    assert punto_arco(85) == {'x': 190.2, 'y': 74.1}
    assert punto_arco(0) == {'x': 20.0, 'y': 115.0}
    assert punto_arco(100) == {'x': 200.0, 'y': 115.0}
    # Aguja r=80: el 72 de la maqueta
    assert puntos_arco(72) == {'x': 161.0, 'y': 53.4}
    assert puntos_arco(0) == {'x': 30.0, 'y': 115.0}
    assert puntos_arco(100) == {'x': 190.0, 'y': 115.0}


def test_puntos_arco_acota_fuera_de_rango():
    assert puntos_arco(-10) == puntos_arco(0)
    assert puntos_arco(140) == puntos_arco(100)


# ---------- nivel y "te faltan" ----------

def test_nivel_y_faltan():
    assert nivel_de(None) is None
    assert nivel_de(59.9)['codigo'] == 'CRITICO'
    assert nivel_de(60)['codigo'] == 'MODERADO'
    assert nivel_de(85)['codigo'] == 'MODERADO'
    assert nivel_de(85.1)['codigo'] == 'ACEPTABLE'
    assert faltan_para_aceptable(72) == 14
    assert faltan_para_aceptable(85) == 1
    assert faltan_para_aceptable(85.5) == 0
    assert faltan_para_aceptable(None) == 0


# ---------- hitos ----------

def test_proxima_fecha_hito():
    assert proxima_fecha(7, 31, date(2026, 3, 1)) == date(2026, 7, 31)
    assert proxima_fecha(7, 31, date(2026, 8, 1)) == date(2027, 7, 31)
    assert proxima_fecha(7, 31, date(2026, 7, 31)) == date(2026, 7, 31)


def test_proximo_hito_respeta_modulos():
    assert proximo_hito(set(), date(2026, 3, 1)) is None
    h = proximo_hito({'autoevaluacion'}, date(2026, 3, 1))
    assert h['codigo'] == 'sgrl_autoevaluacion'
    assert '[VERIFICAR]' in h['titulo']  # hasta que Brian confirme la fuente
    assert proximo_hito({'reportes'}, date(2026, 3, 1)) is None


# ---------- vencimientos ----------

def test_vencimientos_ordenados_y_limitados(app):
    from app.models.sgsst import PlanTrabajoActividad, EntregaEPP
    from app.models.autoevaluacion import Autoevaluacion, AccionMejora
    from app.models import Usuario
    _empresa()
    hoy = date(2026, 11, 7)
    u = Usuario(email='t@t.local', nombre_completo='Trabajador Uno', rol='Empleado')
    u.set_password('x')
    db.session.add(u)
    db.session.flush()
    # vencida, en 12 días, en 75 días, fuera de horizonte (120 días), ejecutada (no cuenta)
    db.session.add_all([
        PlanTrabajoActividad(anio=2026, objetivo='o', actividad='Simulacro', fecha_programada=hoy + timedelta(days=12)),
        PlanTrabajoActividad(anio=2026, objetivo='o', actividad='Lejana', fecha_programada=hoy + timedelta(days=120)),
        PlanTrabajoActividad(anio=2026, objetivo='o', actividad='Hecha', fecha_programada=hoy - timedelta(days=3), estado='Ejecutada'),
        EntregaEPP(trabajador_id=u.id, elemento='Casco', fecha_entrega=hoy - timedelta(days=200),
                   fecha_reposicion=hoy - timedelta(days=69)),
    ])
    a = Autoevaluacion(anio=2026, regimen=21)
    db.session.add(a)
    db.session.flush()
    db.session.add(AccionMejora(autoevaluacion_id=a.id, item_codigo='5.1.1', descripcion='Plan de emergencias',
                                fecha_limite=hoy + timedelta(days=75)))
    db.session.commit()

    with app.test_request_context():
        items = proximos_vencimientos({'sgsst', 'epp', 'autoevaluacion'}, limite=6, dias=90, hoy=hoy)
    titulos = [i['titulo'] for i in items]
    assert titulos[0].startswith('Reposición de Casco')      # vencida primero
    assert 'Simulacro' in titulos[1]
    assert 'Plan de emergencias' in titulos[2]
    assert all('Lejana' not in t and 'Hecha' not in t for t in titulos)
    assert items[0]['dias'] == -69 and items[1]['dias'] == 12 and items[2]['dias'] == 75

    with app.test_request_context():
        assert len(proximos_vencimientos({'sgsst', 'epp', 'autoevaluacion'}, limite=2, dias=90, hoy=hoy)) == 2


# ---------- datos del panel ----------

def test_kpi_ocultos_sin_modulo(app):
    e = _empresa()
    with app.test_request_context():
        datos = datos_panel(e, {'reportes'})
    textos = [k['texto'] for k in datos['kpis']]
    assert 'Reportes de condiciones abiertos' in textos
    assert 'Trabajadores' in textos
    assert 'Acciones de mejora abiertas' not in textos
    assert 'Requisitos legales' not in textos
    assert datos['puntaje'] is None and datos['autoeval'] is None


def test_panel_con_autoevaluacion_cerrada(app):
    from app.services import autoevaluacion_service as svc
    e = _empresa(20, 2)  # régimen 21
    a = svc.crear_autoevaluacion(e, 2026, None)
    for r in a.respuestas:
        r.calificacion = 'NO_CUMPLE' if r.item_codigo in ('5.1.1', '1.1.1') else 'CUMPLE'
    svc.cerrar_autoevaluacion(a)  # 100 - 5 - 0.5 = 94.5
    with app.test_request_context():
        datos = datos_panel(e, {'autoevaluacion', 'reportes', 'matriz_legal'})
    assert datos['puntaje'] == 94.5
    assert datos['nivel']['codigo'] == 'ACEPTABLE'
    assert datos['faltan'] == 0
    # acciones ordenadas por puntos: 5.1.1 (5.0) antes que 1.1.1 (0.5)
    assert [x['codigo'] for x in datos['acciones']] == ['5.1.1', '1.1.1']
    assert datos['provisional'] is False
    assert len(datos['kpis']) == 4


def test_panel_web_renderiza(app):
    from app.models import Usuario
    e = _empresa()
    admin = Usuario(email='a@t.local', nombre_completo='Ana Rojas', rol='Admin', empresa_id=e.id, activo=True)
    admin.set_password('pw12345')
    db.session.add(admin)
    db.session.commit()
    set_empresa(None)
    c = app.test_client()
    c.post('/auth/login', data={'email': 'a@t.local', 'password': 'pw12345'})
    r = c.get('/dashboard/')
    html = r.get_data(as_text=True)
    assert r.status_code == 200
    assert 'Así va tu SG-SST' in html
    assert 'Aún no tienes puntaje' in html          # estado vacío
    assert 'No tienes vencimientos' in html
    assert 'aria-current="page"' in html             # ítem activo del menú
    assert 'AR' in html                              # iniciales del avatar
    assert 'class="dark"' not in html
