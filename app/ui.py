# -*- coding: utf-8 -*-
"""Ayudas de interfaz disponibles en todas las plantillas (rediseño v2).

Expone: empresa_actual(), iniciales(), fecha_larga(), fecha_corta(),
proximo_hito() y puntos_arco() — lo que necesitan base.html y los componentes.
"""
from datetime import date, datetime

from flask import request
from flask_login import current_user

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
         'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
MESES_CORTOS = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago',
                'sep', 'oct', 'nov', 'dic']


def fecha_larga(d):
    """22 de octubre de 2026"""
    if not d:
        return ''
    if isinstance(d, datetime):
        d = d.date()
    return f'{d.day} de {MESES[d.month - 1]} de {d.year}'


def fecha_corta(d):
    """30 ago 2026"""
    if not d:
        return ''
    if isinstance(d, datetime):
        d = d.date()
    return f'{d.day} {MESES_CORTOS[d.month - 1]} {d.year}'


def iniciales(nombre):
    partes = [p for p in (nombre or '').split() if p]
    if not partes:
        return '?'
    if len(partes) == 1:
        return partes[0][:2].upper()
    return (partes[0][0] + partes[1][0]).upper()


def empresa_actual():
    from app import db
    from app.models import Empresa
    if not current_user.is_authenticated:
        return None
    if getattr(current_user, 'empresa_id', None):
        return db.session.get(Empresa, current_user.empresa_id)
    return Empresa.query.first()


def init_ui(app):
    from app.services.panel import puntos_arco
    from app.data.hitos_normativos import proximo_hito
    from app.modulos import modulos_de_empresa

    app.jinja_env.filters['fecha_larga'] = fecha_larga
    app.jinja_env.filters['fecha_corta'] = fecha_corta
    # Globals (no solo contexto): las macros importadas con {% from %} solo
    # ven globals, no las variables de los context processors.
    app.jinja_env.globals.update(
        puntos_arco=puntos_arco, iniciales=iniciales,
        fecha_larga=fecha_larga, fecha_corta=fecha_corta,
    )

    @app.context_processor
    def _ui():
        empresa = None
        hito = None
        try:
            if current_user.is_authenticated:
                empresa = empresa_actual()
                hito = proximo_hito(modulos_de_empresa(), date.today())
        except Exception:
            empresa = None
        return {
            'empresa_actual': empresa,
            'proximo_hito': hito,
            'puntos_arco': puntos_arco,
            'iniciales': iniciales,
            'fecha_larga': fecha_larga,
            'fecha_corta': fecha_corta,
            'hoy': date.today(),
            'ruta_actual': request.endpoint,
        }
