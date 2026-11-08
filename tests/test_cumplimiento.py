# -*- coding: utf-8 -*-
"""Tests del módulo de cumplimiento (SARLAFT transporte, PTEE, SAGRILAFT, datos personales)."""
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
    app = create_app('testing')
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with app.app_context():
        db.create_all()
        yield app
        set_empresa(None)
        db.session.remove()
        db.drop_all()


def _empresa_con_usuarios(app):
    from app.models import Empresa, Usuario, EmpresaModulo
    e = Empresa(nit='900555111', razon_social='Transportes Norte S.A.S.', num_trabajadores=30, clase_riesgo=4)
    db.session.add(e)
    db.session.commit()
    gerente = Usuario(email='g@n.local', nombre_completo='Gloria Niño', rol='Gerente', empresa_id=e.id, activo=True)
    gerente.set_password('pw12345')
    empleado = Usuario(email='e@n.local', nombre_completo='Elkin Ruiz', rol='Empleado', empresa_id=e.id, activo=True)
    empleado.set_password('pw12345')
    db.session.add_all([gerente, empleado])
    db.session.commit()
    set_empresa(e.id)
    for cod in ('cumplimiento', 'autoevaluacion'):
        db.session.add(EmpresaModulo(modulo=cod, activo=True))
    db.session.commit()
    return e, gerente, empleado


def _login(app, email):
    c = app.test_client()
    c.post('/auth/login', data={'email': email, 'password': 'pw12345'})
    return c


# ---------- catálogo ----------

def test_catalogo_integro():
    from app.data.programas_cumplimiento import PROGRAMAS, requisitos_de, normas_pendientes
    assert set(PROGRAMAS) == {'sarlaft_transporte', 'ptee_transporte', 'sagrilaft', 'datos_personales'}
    completo = {r['codigo'] for r in requisitos_de('sarlaft_transporte', 'completo')}
    rms = {r['codigo'] for r in requisitos_de('sarlaft_transporte', 'simplificado')}
    assert 'oficial_suplente' in completo and 'oficial_suplente' not in rms
    assert 'auditoria' in completo and 'auditoria' not in rms
    assert rms < completo
    # Nada verificado todavía: la interfaz debe marcar [VERIFICAR]
    assert normas_pendientes('sarlaft_transporte')


# ---------- servicio ----------

def test_activar_programa_crea_requisitos_y_reportes(app):
    from app.services import cumplimiento_service as svc
    from app.models.cumplimiento import RequisitoCumplimiento, ReporteCumplimiento
    _empresa_con_usuarios(app)
    hoy = date(2026, 11, 8)
    p = svc.activar_programa('sarlaft_transporte', 'simplificado', hoy=hoy)
    codigos = {r.codigo for r in p.requisitos}
    assert 'politica' in codigos and 'oficial_suplente' not in codigos
    assert RequisitoCumplimiento.query.count() == len(codigos)
    # Reportes trimestrales dentro de los 12 meses siguientes: 10-ene, 10-abr, 10-jul, 10-oct de 2027
    fechas = sorted(r.fecha_limite for r in p.reportes)
    assert fechas == [date(2027, 1, 10), date(2027, 4, 10), date(2027, 7, 10), date(2027, 10, 10)]
    assert all(not r.verificado for r in p.reportes)
    # Idempotente
    svc.activar_programa('sarlaft_transporte', 'simplificado', hoy=hoy)
    assert ReporteCumplimiento.query.count() == 4

    # Cambio de régimen: aparecen los del completo sin perder evidencia
    svc.marcar_requisito(p.requisitos[0], 'cumplido', evidencia='Acta 7', fecha=hoy)
    db.session.commit()
    p.regimen = 'completo'
    svc.sincronizar_requisitos(p)
    db.session.commit()
    codigos = {r.codigo for r in p.requisitos if r.estado != 'no_aplica'}
    assert 'oficial_suplente' in codigos
    assert p.requisitos[0].evidencia == 'Acta 7'


def test_avance_y_periodicidad(app):
    from app.services import cumplimiento_service as svc
    _empresa_con_usuarios(app)
    hoy = date(2026, 11, 8)
    p = svc.activar_programa('datos_personales', 'documental', hoy=hoy)
    a = svc.avance(p, hoy)
    assert a['cumplidos'] == 0 and a['porcentaje'] == 0 and a['nivel'] == 'rojo'
    for r in p.requisitos:
        svc.marcar_requisito(r, 'cumplido', evidencia='ok', fecha=hoy)
    db.session.commit()
    assert svc.avance(p, hoy)['porcentaje'] == 100
    # La capacitación anual queda con revisión a 12 meses y vence después
    cap = next(r for r in p.requisitos if r.codigo == 'capacitacion')
    assert cap.proxima_revision == date(2027, 11, 8)
    assert not cap.vencido(hoy)
    assert cap.vencido(date(2027, 11, 9))
    assert svc.avance(p, date(2027, 11, 9))['vencidos'] >= 1
    # no_aplica no cuenta en el total
    svc.marcar_requisito(cap, 'no_aplica')
    db.session.commit()
    assert svc.avance(p, hoy)['total'] == len(p.requisitos) - 1


def test_diagnostico_umbrales():
    from app.services.cumplimiento_service import diagnostico
    from app.data.programas_cumplimiento import parametro
    umbral = parametro('umbral_sarlaft_uvb') * parametro('uvb')
    grande = {d['codigo']: d for d in diagnostico(vigilada_supertransporte=True, ingresos=int(umbral) + 1, activos=10_000_000_000)}
    assert grande['sarlaft_transporte']['regimen'] == 'completo'
    assert grande['ptee_transporte']['regimen'] == 'oficial'
    assert grande['datos_personales']['regimen'] == 'rnbd'
    chica = {d['codigo']: d for d in diagnostico(vigilada_supertransporte=True, ingresos=800_000_000, activos=500_000_000)}
    assert chica['sarlaft_transporte']['regimen'] == 'simplificado'
    assert chica['ptee_transporte']['regimen'] == 'responsable'
    assert chica['datos_personales']['regimen'] == 'documental'
    # Sin datos de ingresos: probable, no obligatorio con régimen
    sin = {d['codigo']: d for d in diagnostico(vigilada_supertransporte=True)}
    assert sin['sarlaft_transporte']['aplica'] == 'probable'
    # No vigilada: solo datos personales
    base = diagnostico()
    assert [d['codigo'] for d in base] == ['datos_personales']


def test_nivel_riesgo():
    from app.services.cumplimiento_service import nivel_riesgo
    assert nivel_riesgo(1) == 'bajo' and nivel_riesgo(6) == 'bajo'
    assert nivel_riesgo(7) == 'medio' and nivel_riesgo(12) == 'medio'
    assert nivel_riesgo(13) == 'alto' and nivel_riesgo(25) == 'alto'


# ---------- listas restrictivas ----------

XML_ONU = b"""<?xml version="1.0" encoding="UTF-8"?>
<CONSOLIDATED_LIST>
 <INDIVIDUALS>
  <INDIVIDUAL><DATAID>1</DATAID><REFERENCE_NUMBER>QDi.001</REFERENCE_NUMBER>
   <FIRST_NAME>JUAN</FIRST_NAME><SECOND_NAME>PEREZ</SECOND_NAME><THIRD_NAME>GOMEZ</THIRD_NAME>
   <INDIVIDUAL_ALIAS><ALIAS_NAME>EL FLACO</ALIAS_NAME></INDIVIDUAL_ALIAS>
  </INDIVIDUAL>
 </INDIVIDUALS>
 <ENTITIES>
  <ENTITY><DATAID>2</DATAID><REFERENCE_NUMBER>QDe.002</REFERENCE_NUMBER>
   <FIRST_NAME>TRANSPORTES ILICITOS DEL SUR S.A.</FIRST_NAME>
   <ENTITY_ALIAS><ALIAS_NAME>TIS</ALIAS_NAME></ENTITY_ALIAS>
  </ENTITY>
 </ENTITIES>
</CONSOLIDATED_LIST>"""


def test_listas_onu_parseo_y_busqueda():
    from app.services import listas_restrictivas as li
    entradas = li.cargar_onu(XML_ONU)
    nombres = [e[0] for e in entradas]
    assert 'JUAN PEREZ GOMEZ' in nombres and 'EL FLACO' in nombres and 'TIS' in nombres
    # tildes y orden no importan
    assert li.buscar('Juan Pérez Gómez', entradas)[0]['referencia'] == 'QDi.001'
    assert li.buscar('transportes ilicitos del sur', entradas)[0]['tipo'] == 'entidad'
    # nombre distinto no coincide; consultas cortas no se evalúan
    assert li.buscar('Comercializadora Andina S.A.S.', entradas) == []
    assert li.buscar('TI', entradas) == []
    disponible, coincidencias, fuente = li.consultar('Juan Perez Gomez', entradas=entradas)
    assert disponible and coincidencias and 'ONU' in fuente
    # Sin URL ni entradas: no disponible, nunca inventa resultado
    assert li.consultar('X Y Z', url='') == (False, [], None)


# ---------- web ----------

def test_web_flujo_completo(app):
    from app.models.cumplimiento import ProgramaCumplimiento, Contraparte
    e, gerente, empleado = _empresa_con_usuarios(app)
    c = _login(app, 'g@n.local')

    r = c.get('/cumplimiento/')
    html = r.get_data(as_text=True)
    assert r.status_code == 200
    assert 'SARLAFT transporte' in html and 'No activado' in html and '[VERIFICAR]' in html

    # Diagnóstico por GET
    r = c.get('/cumplimiento/?diag=1&supertransporte=on&ingresos=900000000&activos=300000000')
    assert 'Régimen de Medidas Simplificadas' in r.get_data(as_text=True)

    # Activar y abrir
    r = c.post('/cumplimiento/activar/sarlaft_transporte', data={'regimen': 'simplificado'}, follow_redirects=True)
    assert r.status_code == 200
    p = ProgramaCumplimiento.query.filter_by(codigo='sarlaft_transporte').first()
    assert p and p.regimen == 'simplificado'
    html = r.get_data(as_text=True)
    assert 'Requisitos y evidencias' in html and 'Reporte periódico de SARLAFT' in html

    # Oficial y requisito
    c.post(f'/cumplimiento/p/{p.id}/oficial', data={'oficial_nombre': 'Marta Díaz', 'oficial_tipo': 'externo', 'registro_sirel': 'on'})
    req = next(r for r in p.requisitos if r.codigo == 'politica')
    c.post(f'/cumplimiento/p/{p.id}/requisito/{req.id}', data={'estado': 'cumplido', 'evidencia': 'Acta 12 de junta'})
    db.session.refresh(req)
    assert req.estado == 'cumplido' and req.fecha_cumplimiento == date.today()
    html = c.get(f'/cumplimiento/p/{p.id}').get_data(as_text=True)
    assert 'Marta Díaz' in html and 'Acta 12 de junta' in html

    # Riesgo alto
    c.post(f'/cumplimiento/p/{p.id}/riesgos', data={'descripcion': 'Pagos en efectivo sin soporte', 'factor': 'canal',
                                                   'probabilidad': 5, 'impacto': 4})
    html = c.get(f'/cumplimiento/p/{p.id}/riesgos').get_data(as_text=True)
    assert 'Pagos en efectivo sin soporte' in html and '1 alto' in html

    # Contraparte: PEP sube a riesgo alto; verificación manual programa reverificación a 6 meses
    c.post('/cumplimiento/contrapartes/nueva', data={'nombre': 'Carlos Mesa', 'tipo': 'conductor', 'pep': 'on',
                                                    'tipo_documento': 'CC', 'documento': '80123'})
    cp = Contraparte.query.filter_by(nombre='Carlos Mesa').first()
    assert cp.nivel_riesgo == 'alto' and cp.verificacion_vencida()
    c.post(f'/cumplimiento/contrapartes/{cp.id}/verificar', data={'modo': 'manual', 'resultado': 'sin_coincidencia', 'fuente': 'OFAC'})
    db.session.refresh(cp)
    assert cp.resultado_verificacion == 'sin_coincidencia' and not cp.verificacion_vencida()
    assert (cp.proxima_verificacion - date.today()).days in range(170, 190)
    # Coincidencia bloquea
    c.post(f'/cumplimiento/contrapartes/{cp.id}/verificar', data={'modo': 'manual', 'resultado': 'coincidencia', 'fuente': 'ONU'})
    db.session.refresh(cp)
    assert cp.estado == 'bloqueada'
    html = c.get('/cumplimiento/contrapartes').get_data(as_text=True)
    assert 'Bloqueada' in html and 'posible coincidencia' in html
    # Consulta automática sin URL configurada: aviso, sin cambio
    r = c.post(f'/cumplimiento/contrapartes/{cp.id}/verificar', data={'modo': 'automatico'}, follow_redirects=True)
    assert 'no está disponible' in r.get_data(as_text=True)

    # El panel y los vencimientos ven el módulo
    html = c.get('/dashboard/').get_data(as_text=True)
    assert 'Otras obligaciones pendientes' in html
    assert 'Reporte periódico de SARLAFT' in html

    # Empleado: puede leer, no modificar
    ce = _login(app, 'e@n.local')
    assert ce.get('/cumplimiento/').status_code == 200
    r = ce.post('/cumplimiento/activar/ptee_transporte', data={}, follow_redirects=True)
    assert ProgramaCumplimiento.query.filter_by(codigo='ptee_transporte').first() is None
    assert 'Solo el oficial de cumplimiento' in r.get_data(as_text=True)


def test_gating_sin_modulo(app):
    """Sin el módulo contratado, un usuario no Admin es devuelto al panel."""
    from app.models import Empresa, Usuario, EmpresaModulo
    e = Empresa(nit='900777', razon_social='Sin módulo S.A.S.', num_trabajadores=5)
    db.session.add(e)
    db.session.commit()
    u = Usuario(email='x@s.local', nombre_completo='X', rol='Gerente', empresa_id=e.id, activo=True)
    u.set_password('pw12345')
    db.session.add(u)
    db.session.commit()
    set_empresa(e.id)
    db.session.add(EmpresaModulo(modulo='autoevaluacion', activo=True))
    db.session.commit()
    c = _login(app, 'x@s.local')
    r = c.get('/cumplimiento/', follow_redirects=True)
    assert 'no está incluido en tu plan' in r.get_data(as_text=True)


def test_vencimientos_incluye_reportes(app):
    from app.services import cumplimiento_service as svc
    from app.services.vencimientos import proximos_vencimientos
    _empresa_con_usuarios(app)
    hoy = date(2027, 1, 1)
    svc.activar_programa('datos_personales', 'rnbd', hoy=hoy)
    with app.test_request_context():
        items = proximos_vencimientos({'cumplimiento'}, limite=10, dias=120, hoy=hoy)
    titulos = [i['titulo'] for i in items]
    assert 'Reporte semestral de reclamos en el RNBD' in titulos
    assert 'Actualización anual del RNBD' in titulos
    assert items == sorted(items, key=lambda i: i['fecha'])
