from flask import render_template
from flask_login import login_required, current_user
from app.models import CondicionInsegura, Evento, ConsultaJuridica
from app.routes import dashboard_bp

@dashboard_bp.route('/')
@login_required
def index():
    total_reportes = CondicionInsegura.query.count()
    reportes_abiertos = CondicionInsegura.query.filter_by(estado='Abierto').count()
    reportes_corregidos = CondicionInsegura.query.filter_by(estado='Corregido').count()
    eventos_pendientes = Evento.query.filter_by(estado='Abierto').count()
    consultas_juridicas = ConsultaJuridica.query.count()
    consultas_abiertas = ConsultaJuridica.query.filter_by(estado='Abierta').count()
    
    contexto = {
        'total_reportes': total_reportes,
        'reportes_abiertos': reportes_abiertos,
        'reportes_corregidos': reportes_corregidos,
        'eventos_pendientes': eventos_pendientes,
        'consultas_juridicas': consultas_juridicas,
        'consultas_abiertas': consultas_abiertas,
        'usuario': current_user
    }
    
    return render_template('dashboard/index.html', **contexto)
