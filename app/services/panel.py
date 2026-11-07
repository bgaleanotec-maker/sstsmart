# -*- coding: utf-8 -*-
"""Datos del panel principal "Así va tu SG-SST" (rediseno-ui/README.md §4).

Deja `routes/dashboard.py` delgado y permite probar la lógica sin HTTP.
"""
import math
from datetime import date, datetime

from app.data.estandares_0312 import ESTANDARES, clasificar, ACCIONES_POR_CLASIFICACION

# Geometría del medidor: viewBox 220x130, centro (110,115)
_CX, _CY = 110.0, 115.0
_R_ARCO = 90.0
_R_AGUJA = 80.0

NIVELES = {
    'CRITICO': {
        'codigo': 'CRITICO', 'texto': 'Crítico', 'color': 'rojo',
        'rango': 'Menos de 60 puntos',
        'implica': ACCIONES_POR_CLASIFICACION['CRITICO'],
    },
    'MODERADO': {
        'codigo': 'MODERADO', 'texto': 'Moderadamente aceptable', 'color': 'amarillo',
        'rango': 'De 60 a 85 puntos',
        'implica': ACCIONES_POR_CLASIFICACION['MODERADO'],
    },
    'ACEPTABLE': {
        'codigo': 'ACEPTABLE', 'texto': 'Aceptable', 'color': 'verde',
        'rango': 'Más de 85 puntos',
        'implica': ACCIONES_POR_CLASIFICACION['ACEPTABLE'],
    },
}
ORDEN_NIVELES = ['CRITICO', 'MODERADO', 'ACEPTABLE']

_PESO = {e[0]: e[4] for e in ESTANDARES}
_DESC = {e[0]: e[3] for e in ESTANDARES}


def punto_arco(s, radio=_R_ARCO):
    """Punto sobre el arco para un puntaje s (0-100): θ = 180° − 1,8·s."""
    s = max(0.0, min(100.0, float(s)))
    theta = math.radians(180.0 - 1.8 * s)
    return {
        'x': round(_CX + radio * math.cos(theta), 1),
        'y': round(_CY - radio * math.sin(theta), 1),
    }


def puntos_arco(s):
    """Extremo de la aguja del medidor (radio 80) para el puntaje s."""
    return punto_arco(s, _R_AGUJA)


def nivel_de(puntaje):
    if puntaje is None:
        return None
    return NIVELES[clasificar(puntaje)]


def faltan_para_aceptable(puntaje):
    """Puntos que faltan para superar 85. 0 si ya es aceptable."""
    if puntaje is None or puntaje > 85:
        return 0
    return int(math.ceil(85.01 - puntaje))


def acciones_prioritarias(autoeval):
    """Ítems NO_CUMPLE ordenados por los puntos que suma cada uno (propuesta)."""
    if autoeval is None:
        return []
    filas = []
    for r in autoeval.respuestas.filter_by(calificacion='NO_CUMPLE'):
        filas.append({
            'codigo': r.item_codigo,
            'descripcion': _DESC.get(r.item_codigo, r.item_codigo),
            'puntos': _PESO.get(r.item_codigo, 0),
        })
    filas.sort(key=lambda f: -f['puntos'])
    return filas


def _a_fecha(valor):
    if isinstance(valor, datetime):
        return valor.date()
    return valor


def datos_panel(empresa, modulos_activos, hoy=None):
    """Todo lo que necesita dashboard/index.html, en un dict."""
    from app.models import CondicionInsegura, RequisitoLegal
    from app.models.autoevaluacion import Autoevaluacion, AccionMejora
    from app.services.vencimientos import proximos_vencimientos

    hoy = hoy or date.today()
    regimen = None
    if empresa:
        regimen = empresa.regimen_estandares or empresa.calcular_regimen()

    autoeval = None
    puntaje = None
    if 'autoevaluacion' in modulos_activos:
        autoeval = Autoevaluacion.query.order_by(Autoevaluacion.anio.desc()).first()
        if autoeval and autoeval.puntaje_total is not None:
            puntaje = autoeval.puntaje_total
            regimen = autoeval.regimen or regimen

    nivel = nivel_de(puntaje)
    acciones = acciones_prioritarias(autoeval)

    # KPI
    kpis = []
    if 'autoevaluacion' in modulos_activos:
        abiertas = AccionMejora.query.filter(AccionMejora.estado != 'Cerrada').all()
        vencidas = sum(1 for a in abiertas if a.fecha_limite and a.fecha_limite < hoy)
        kpis.append({
            'texto': 'Acciones de mejora abiertas', 'cifra': len(abiertas),
            'sub': f'{vencidas} vencida{"s" if vencidas != 1 else ""}',
            'alerta': vencidas > 0,
            'endpoint': ('autoevaluacion.resultado', {'id': autoeval.id}) if autoeval else ('autoevaluacion.lista', {}),
        })
    if 'reportes' in modulos_activos:
        abiertos = CondicionInsegura.query.filter(
            CondicionInsegura.estado.in_(['Abierto', 'Reportado'])).count()
        del_anio = CondicionInsegura.query.filter(
            CondicionInsegura.fecha_creacion >= datetime(hoy.year, 1, 1)).count()
        kpis.append({
            'texto': 'Reportes de condiciones abiertos', 'cifra': abiertos,
            'sub': f'de {del_anio} en {hoy.year}', 'alerta': False,
            'endpoint': ('reportes.listar', {}),
        })
    if 'matriz_legal' in modulos_activos:
        total = RequisitoLegal.query.count()
        del_mes = RequisitoLegal.query.filter(
            RequisitoLegal.fecha_actualizacion >= datetime(hoy.year, hoy.month, 1)).count()
        kpis.append({
            'texto': 'Requisitos legales', 'cifra': total,
            'sub': f'{del_mes} actualizado{"s" if del_mes != 1 else ""} este mes', 'alerta': False,
            'endpoint': ('matriz_legal.dashboard', {}),
        })
    if empresa:
        kpis.append({
            'texto': 'Trabajadores', 'cifra': empresa.num_trabajadores or 0,
            'sub': f'Régimen de {regimen} estándares' if regimen else 'Régimen sin calcular',
            'alerta': False,
            'endpoint': ('autoevaluacion.perfil_empresa', {}),
        })

    return {
        'empresa': empresa,
        'regimen': regimen,
        'autoeval': autoeval,
        'puntaje': puntaje,
        'nivel': nivel,
        'provisional': bool(autoeval and autoeval.estado != 'CERRADA' and puntaje is not None),
        'faltan': faltan_para_aceptable(puntaje),
        'acciones': acciones,
        'niveles': [NIVELES[c] for c in ORDEN_NIVELES],
        'kpis': kpis,
        'vencimientos': proximos_vencimientos(modulos_activos, limite=6, dias=90, hoy=hoy),
        'hoy': hoy,
    }
