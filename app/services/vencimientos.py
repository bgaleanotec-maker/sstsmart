# -*- coding: utf-8 -*-
"""Próximos vencimientos del SG-SST para el panel (rediseno-ui/README.md §4.5).

Une en una sola lista, ordenada por fecha, lo que vence en los próximos
`dias` días (y lo ya vencido): actividades del plan anual, acciones de mejora,
reposiciones de EPP, seguimientos de controles e hitos normativos. Las
consultas quedan acotadas al tenant por app/tenancy.py.
"""
from datetime import date, timedelta

from flask import url_for

from app.data.hitos_normativos import hitos_aplicables
from app.data.modulos import MODULOS


def _item(fecha, titulo, modulo, url, hoy):
    return {
        'fecha': fecha,
        'dias': (fecha - hoy).days,
        'titulo': titulo,
        'modulo': MODULOS.get(modulo, {}).get('nombre', modulo),
        'modulo_codigo': modulo,
        'url': url,
    }


def proximos_vencimientos(modulos_activos, limite=6, dias=90, hoy=None):
    from app.models.sgsst import PlanTrabajoActividad, EntregaEPP
    from app.models.autoevaluacion import AccionMejora
    from app.models import Control

    hoy = hoy or date.today()
    horizonte = hoy + timedelta(days=dias)
    items = []

    if 'sgsst' in modulos_activos:
        for a in (PlanTrabajoActividad.query
                  .filter(PlanTrabajoActividad.estado != 'Ejecutada',
                          PlanTrabajoActividad.fecha_programada.isnot(None),
                          PlanTrabajoActividad.fecha_programada <= horizonte).all()):
            items.append(_item(a.fecha_programada, a.actividad, 'sgsst',
                               url_for('sgsst.plan', anio=a.anio), hoy))

    if 'autoevaluacion' in modulos_activos:
        for m in (AccionMejora.query
                  .filter(AccionMejora.estado != 'Cerrada',
                          AccionMejora.fecha_limite.isnot(None),
                          AccionMejora.fecha_limite <= horizonte).all()):
            items.append(_item(m.fecha_limite, m.descripcion, 'autoevaluacion',
                               url_for('autoevaluacion.resultado', id=m.autoevaluacion_id), hoy))

    if 'epp' in modulos_activos:
        for e in (EntregaEPP.query
                  .filter(EntregaEPP.fecha_reposicion.isnot(None),
                          EntregaEPP.fecha_reposicion <= horizonte).all()):
            quien = e.trabajador.nombre_completo if e.trabajador else 'trabajador'
            items.append(_item(e.fecha_reposicion, f'Reposición de {e.elemento} ({quien})',
                               'epp', url_for('epp.kardex'), hoy))

    if 'controles' in modulos_activos:
        for c in (Control.query
                  .filter(Control.activo.is_(True),
                          Control.proximo_seguimiento.isnot(None)).all()):
            f = c.proximo_seguimiento.date() if hasattr(c.proximo_seguimiento, 'date') else c.proximo_seguimiento
            if f <= horizonte:
                items.append(_item(f, f'Seguimiento del control {c.codigo}: {c.nombre}',
                                   'controles', url_for('controles.listar_controles'), hoy))

    if 'cumplimiento' in modulos_activos:
        from app.models.cumplimiento import ReporteCumplimiento, RequisitoCumplimiento, Contraparte
        for r in (ReporteCumplimiento.query
                  .filter(ReporteCumplimiento.estado == 'pendiente',
                          ReporteCumplimiento.fecha_limite <= horizonte).all()):
            items.append(_item(r.fecha_limite, r.nombre, 'cumplimiento',
                               url_for('cumplimiento.programa', id=r.programa_id) + '#reportes', hoy))
        for q in (RequisitoCumplimiento.query
                  .filter(RequisitoCumplimiento.estado != 'no_aplica',
                          RequisitoCumplimiento.proxima_revision.isnot(None),
                          RequisitoCumplimiento.proxima_revision <= horizonte).all()):
            items.append(_item(q.proxima_revision, f'Revisión: {q.nombre}', 'cumplimiento',
                               url_for('cumplimiento.programa', id=q.programa_id) + f'#req-{q.id}', hoy))
        for c in (Contraparte.query
                  .filter(Contraparte.estado == 'activa',
                          Contraparte.proxima_verificacion.isnot(None),
                          Contraparte.proxima_verificacion <= horizonte).all()):
            items.append(_item(c.proxima_verificacion, f'Reverificar contraparte {c.nombre}', 'cumplimiento',
                               url_for('cumplimiento.contrapartes') + f'#c-{c.id}', hoy))

    for h in hitos_aplicables(modulos_activos, hoy):
        if h['fecha'] <= horizonte:
            items.append(_item(h['fecha'], h['titulo'], h['modulo'],
                               url_for('autoevaluacion.lista') if h['modulo'] == 'autoevaluacion' else '#',
                               hoy))

    items.sort(key=lambda i: i['fecha'])
    return items[:limite]
