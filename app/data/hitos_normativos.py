# -*- coding: utf-8 -*-
"""Hitos normativos con fecha fija del año (rediseno-ui/README.md §5.6).

Todos nacen con verificado=False hasta que Brian confirme la fuente oficial:
mientras tanto la interfaz los muestra con la etiqueta "[VERIFICAR]".
Cada hito aplica a un módulo del catálogo; si el módulo no está activo para la
empresa, el hito no se muestra.
"""
from datetime import date

# (codigo, nombre, nombre_corto, mes, dia_limite, modulo, norma, verificado)
HITOS = [
    ('sgrl_autoevaluacion',
     'Registro de la autoevaluación en la plataforma SGRL',
     'Autoevaluación en SGRL',
     7, 31, 'autoevaluacion',
     'Circular 027/2026 Mintrabajo', False),
    ('pesv_reporte_mintrabajo',
     'Reporte anual del PESV a Mintrabajo (ventana 6-31 de enero)',
     'Reporte PESV',
     1, 31, 'pesv',
     'Circular 0034/2026 Mintrabajo', False),
]


def proxima_fecha(mes, dia, hoy=None):
    """Próxima ocurrencia (incluye hoy) de un día/mes fijo."""
    hoy = hoy or date.today()
    candidata = date(hoy.year, mes, dia)
    if candidata < hoy:
        candidata = date(hoy.year + 1, mes, dia)
    return candidata


def hitos_aplicables(modulos_activos, hoy=None):
    """Hitos cuyo módulo está activo, con su próxima fecha, ordenados por fecha."""
    hoy = hoy or date.today()
    salida = []
    for codigo, nombre, corto, mes, dia, modulo, norma, verificado in HITOS:
        if modulo not in modulos_activos:
            continue
        fecha = proxima_fecha(mes, dia, hoy)
        salida.append({
            'codigo': codigo,
            'titulo': nombre + ('' if verificado else ' [VERIFICAR]'),
            'corto': corto + ('' if verificado else ' [VERIFICAR]'),
            'fecha': fecha,
            'dias': (fecha - hoy).days,
            'modulo': modulo,
            'norma': norma,
            'verificado': verificado,
        })
    salida.sort(key=lambda h: h['fecha'])
    return salida


def proximo_hito(modulos_activos, hoy=None):
    hitos = hitos_aplicables(modulos_activos, hoy)
    return hitos[0] if hitos else None
