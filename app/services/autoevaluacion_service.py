"""Lógica de la autoevaluación de Estándares Mínimos (Res. 0312/2019).

Reglas de puntaje (arts. 27-28):
- Ítem exigible CUMPLE o NO_APLICA (justificado) → puntaje pleno del ítem.
- Ítem exigible NO_CUMPLE → 0.
- Ítems NO exigibles para el régimen de la empresa (7 o 21) → puntaje pleno
  automático (no se diligencian).
Clasificación: CRÍTICO <60 · MODERADAMENTE ACEPTABLE 60-85 · ACEPTABLE >85.
"""
from datetime import datetime, timedelta

from app import db
from app.data.estandares_0312 import (
    ESTANDARES, items_para_regimen, clasificar, ACCIONES_POR_CLASIFICACION
)
from app.models.autoevaluacion import (
    Autoevaluacion, RespuestaAutoevaluacion, AccionMejora
)

CATALOGO = {e[0]: {'codigo': e[0], 'ciclo': e[1], 'estandar': e[2],
                   'descripcion': e[3], 'puntaje': e[4]} for e in ESTANDARES}


def crear_autoevaluacion(empresa, anio, usuario_id):
    """Crea la autoevaluación del año con una respuesta PENDIENTE por cada
    ítem exigible del régimen de la empresa."""
    regimen = empresa.calcular_regimen()
    autoeval = Autoevaluacion(
        empresa_id=empresa.id, anio=anio, regimen=regimen,
        creada_por_id=usuario_id,
    )
    db.session.add(autoeval)
    db.session.flush()
    for item in items_para_regimen(regimen):
        db.session.add(RespuestaAutoevaluacion(
            autoevaluacion_id=autoeval.id, item_codigo=item[0],
        ))
    db.session.commit()
    return autoeval


def puntaje_no_exigible(regimen):
    """Suma de puntajes de los ítems que no aplican al régimen (se otorgan)."""
    exigibles = {e[0] for e in items_para_regimen(regimen)}
    return sum(e[4] for e in ESTANDARES if e[0] not in exigibles)


def calcular_puntaje(autoeval):
    """Recalcula el puntaje de cada respuesta y el total. No cierra."""
    total = puntaje_no_exigible(autoeval.regimen)
    for resp in autoeval.respuestas:
        peso = CATALOGO[resp.item_codigo]['puntaje']
        if resp.calificacion in ('CUMPLE', 'NO_APLICA'):
            resp.puntaje_obtenido = peso
        else:  # NO_CUMPLE o PENDIENTE
            resp.puntaje_obtenido = 0.0
        total += resp.puntaje_obtenido
    autoeval.puntaje_total = round(total, 2)
    autoeval.clasificacion = clasificar(autoeval.puntaje_total)
    return autoeval.puntaje_total


def desglose_por_ciclo(autoeval):
    """[(ciclo, obtenido, posible)] contando pleno lo no exigible."""
    exigibles = {r.item_codigo: r for r in autoeval.respuestas}
    ciclos = {}
    for cod, ciclo, _est, _desc, peso, _e7, _e21 in ESTANDARES:
        obtenido, posible = ciclos.get(ciclo, (0.0, 0.0))
        if cod in exigibles:
            obtenido += exigibles[cod].puntaje_obtenido or 0.0
        else:
            obtenido += peso  # no exigible → se otorga
        ciclos[ciclo] = (obtenido, posible + peso)
    orden = ['PLANEAR', 'HACER', 'VERIFICAR', 'ACTUAR']
    return [(c, round(ciclos[c][0], 2), round(ciclos[c][1], 2)) for c in orden]


def cerrar_autoevaluacion(autoeval, dias_plazo=90):
    """Cierra la vigencia y deriva el plan de mejoramiento de los NO_CUMPLE."""
    pendientes = [r.item_codigo for r in autoeval.respuestas
                  if r.calificacion == 'PENDIENTE']
    if pendientes:
        raise ValueError(f"Faltan ítems por calificar: {', '.join(pendientes)}")

    calcular_puntaje(autoeval)
    autoeval.estado = 'CERRADA'
    autoeval.fecha_cierre = datetime.utcnow()

    # El plan de mejora sale de los ítems incumplidos (art. 28)
    plazo = timedelta(days=30 if autoeval.clasificacion == 'CRITICO' else dias_plazo)
    for resp in autoeval.respuestas.filter_by(calificacion='NO_CUMPLE'):
        item = CATALOGO[resp.item_codigo]
        db.session.add(AccionMejora(
            empresa_id=autoeval.empresa_id,
            autoevaluacion_id=autoeval.id,
            item_codigo=resp.item_codigo,
            descripcion=f"[{item['codigo']}] Cumplir: {item['descripcion']}",
            fecha_limite=(datetime.utcnow() + plazo).date(),
        ))
    db.session.commit()
    return autoeval


def texto_accion(clasificacion):
    return ACCIONES_POR_CLASIFICACION.get(clasificacion, '')
