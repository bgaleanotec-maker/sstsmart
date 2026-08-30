from flask import render_template
from flask_login import login_required, current_user
from app.models import (CondicionInsegura, Evento, ConsultaJuridica,
                        Autoevaluacion, AccionMejora, Control, RequisitoLegal)
from app.routes import dashboard_bp


@dashboard_bp.route('/')
@login_required
def index():
    ultima_autoeval = (Autoevaluacion.query
                       .order_by(Autoevaluacion.anio.desc()).first())
    contexto = {
        'total_reportes': CondicionInsegura.query.count(),
        'reportes_abiertos': CondicionInsegura.query.filter(
            CondicionInsegura.estado.in_(['Abierto', 'Reportado'])).count(),
        'eventos_pendientes': Evento.query.filter_by(estado='Abierto').count(),
        'consultas_abiertas': ConsultaJuridica.query.filter_by(estado='Abierta').count(),
        'acciones_abiertas': AccionMejora.query.filter(
            AccionMejora.estado != 'Cerrada').count(),
        'controles_activos': Control.query.filter_by(activo=True).count(),
        'requisitos_legales': RequisitoLegal.query.count(),
        'ultima_autoeval': ultima_autoeval,
        'usuario': current_user,
    }
    return render_template('dashboard/index.html', **contexto)
