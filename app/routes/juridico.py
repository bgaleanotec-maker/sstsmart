# app/routes/juridico.py
"""
Módulo Jurídico SST - Routes completas
Gestión de consultas jurídicas y normativa SST Colombia
"""
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import ConsultaJuridica, DocumentoLegal, Usuario, CondicionInsegura
from app.services.notificaciones import NotificacionService
from app.routes import juridico_bp
from datetime import datetime, timedelta
from functools import wraps
import logging

logger = logging.getLogger(__name__)

# ============ DECORADOR PARA AUTENTICACIÓN JURÍDICA ============

def juridico_required(f):
    """Requiere que el usuario sea Abogado, Responsable_SST o Admin"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.rol not in ['Admin', 'Responsable_SST', 'Abogado']:
            flash('❌ No tienes permiso para acceder al módulo jurídico', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

def abogado_required(f):
    """Requiere que el usuario sea Abogado o Admin"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.rol not in ['Admin', 'Abogado']:
            flash('⚖️ Solo abogados pueden resolver consultas', 'error')
            return redirect(url_for('juridico.listar'))
        return f(*args, **kwargs)
    return decorated_function

# ============ LISTAR CONSULTAS ============

@juridico_bp.route('/')
@juridico_required
def listar():
    """Listar todas las consultas jurídicas con filtros"""
    
    # Parámetros de filtro
    filtro_estado = request.args.get('estado', 'Todas')
    filtro_tipo = request.args.get('tipo', 'Todas')
    filtro_prioridad = request.args.get('prioridad', 'Todas')
    filtro_riesgo = request.args.get('riesgo', 'Todas')
    pagina = request.args.get('pagina', 1, type=int)
    
    # Query base
    query = ConsultaJuridica.query
    
    # Aplicar filtros
    if filtro_estado != 'Todas':
        query = query.filter_by(estado=filtro_estado)
    if filtro_tipo != 'Todas':
        query = query.filter_by(tipo_consulta=filtro_tipo)
    if filtro_prioridad != 'Todas':
        query = query.filter_by(prioridad=filtro_prioridad)
    if filtro_riesgo != 'Todas':
        query = query.filter_by(riesgo_legal=filtro_riesgo)
    
    # Ordenar por fecha descendente
    consultas = query.order_by(ConsultaJuridica.fecha_creacion.desc()).paginate(page=pagina, per_page=10)
    
    # Estadísticas
    stats = {
        'total': ConsultaJuridica.query.count(),
        'abiertas': ConsultaJuridica.query.filter_by(estado='Abierta').count(),
        'en_revision': ConsultaJuridica.query.filter_by(estado='En revisión').count(),
        'resueltas': ConsultaJuridica.query.filter_by(estado='Resuelta').count(),
        'cerradas': ConsultaJuridica.query.filter_by(estado='Cerrada').count(),
        'riesgo_critico': ConsultaJuridica.query.filter_by(riesgo_legal='Crítico').count(),
    }
    
    contexto = {
        'consultas': consultas,
        'stats': stats,
        'filtro_estado': filtro_estado,
        'filtro_tipo': filtro_tipo,
        'filtro_prioridad': filtro_prioridad,
        'filtro_riesgo': filtro_riesgo,
        'estados': ['Abierta', 'En revisión', 'Resuelta', 'Cerrada'],
        'tipos': ['Laboral', 'Penal', 'Civil', 'Administrativo', 'Cumplimiento Normativo'],
        'prioridades': ['Baja', 'Normal', 'Alta', 'Crítica'],
        'riesgos': ['Bajo', 'Medio', 'Alto', 'Crítico']
    }
    
    return render_template('juridico/listar.html', **contexto)

# ============ CREAR CONSULTA ============

@juridico_bp.route('/nueva', methods=['GET', 'POST'])
@juridico_required
def crear():
    """Crear nueva consulta jurídica"""
    
    if request.method == 'POST':
        try:
            consulta = ConsultaJuridica(
                titulo=request.form.get('titulo'),
                descripcion=request.form.get('descripcion'),
                tipo_consulta=request.form.get('tipo_consulta'),
                condicion_insegura_id=request.form.get('condicion_insegura_id') or None,
                empleado_afectado_id=request.form.get('empleado_afectado_id') or None,
                responsable_creador_id=current_user.id,
                prioridad=request.form.get('prioridad', 'Normal'),
                riesgo_legal=request.form.get('riesgo_legal', 'Medio'),
                normativa_aplicable={
                    'articulos': request.form.get('articulos_aplicables', ''),
                    'decretos': request.form.get('decretos_aplicables', ''),
                    'resoluciones': request.form.get('resoluciones_aplicables', '')
                }
            )
            
            consulta.generar_numero_consulta()
            
            db.session.add(consulta)
            db.session.commit()
            
            logger.info(f"✅ Consulta jurídica creada: {consulta.numero_consulta}")
            
            # Enviar notificación a abogados usando método correcto
            try:
                abogados = Usuario.query.filter_by(rol='Abogado', activo=True).all()
                for abogado in abogados:
                    html = f"""
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <div style="background-color: #6f42c1; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;">
                            <h2 style="margin: 0;">⚖️ Nueva Consulta Jurídica</h2>
                        </div>
                        <div style="background-color: #f5f5f5; padding: 20px; border-radius: 0 0 5px 5px;">
                            <p><strong>📋 Número:</strong> {consulta.numero_consulta}</p>
                            <p><strong>📝 Título:</strong> {consulta.titulo}</p>
                            <p><strong>🏷️ Tipo:</strong> {consulta.tipo_consulta}</p>
                            <p><strong>⚠️ Prioridad:</strong> {consulta.prioridad}</p>
                            <p><strong>⚡ Riesgo Legal:</strong> {consulta.riesgo_legal}</p>
                            <p style="text-align: center; margin-top: 20px;">
                                <a href="http://localhost:5000/juridico/{consulta.id}" style="background-color: #6f42c1; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">Ver Consulta</a>
                            </p>
                        </div>
                    </div>
                    """
                    NotificacionService.enviar_email(
                        abogado.email,
                        f"[SST] Nueva Consulta Jurídica: {consulta.numero_consulta}",
                        html
                    )
                logger.info(f"📧 Notificaciones enviadas a {len(abogados)} abogados")
            except Exception as e:
                logger.warning(f"⚠️ Error al enviar notificaciones (no crítico): {str(e)}")
            
            flash(f'✅ Consulta jurídica creada: {consulta.numero_consulta}', 'success')
            return redirect(url_for('juridico.detalle', id=consulta.id))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ Error al crear consulta: {str(e)}", exc_info=True)
            flash(f'❌ Error al crear consulta: {str(e)}', 'error')
            return redirect(url_for('juridico.crear'))
    
    # GET - Mostrar formulario
    condiciones_inseguras = CondicionInsegura.query.filter_by(estado='Abierto').all()
    empleados = Usuario.query.filter_by(rol='Empleado').all()
    tipos_consulta = ['Laboral', 'Penal', 'Civil', 'Administrativo', 'Cumplimiento Normativo']
    
    contexto = {
        'condiciones_inseguras': condiciones_inseguras,
        'empleados': empleados,
        'tipos_consulta': tipos_consulta,
        'prioridades': ['Baja', 'Normal', 'Alta', 'Crítica'],
        'riesgos': ['Bajo', 'Medio', 'Alto', 'Crítico']
    }
    
    return render_template('juridico/crear.html', **contexto)

# ============ DETALLE DE CONSULTA ============

@juridico_bp.route('/<int:id>', methods=['GET', 'POST'])
@juridico_required
def detalle(id):
    """Ver detalle de consulta y permitir resolución"""
    
    consulta = ConsultaJuridica.query.get_or_404(id)
    
    # Verificar permisos
    if current_user.rol == 'Responsable_SST' and consulta.responsable_creador_id != current_user.id:
        if current_user.rol != 'Admin' and current_user.rol != 'Abogado':
            flash('❌ No tienes permiso para ver esta consulta', 'error')
            return redirect(url_for('juridico.listar'))
    
    if request.method == 'POST':
        try:
            accion = request.form.get('accion')
            
            if accion == 'asignar' and current_user.rol in ['Admin', 'Responsable_SST']:
                abogado_id = request.form.get('abogado_id')
                consulta.abogado_asignado_id = abogado_id
                consulta.estado = 'En revisión'
                consulta.fecha_asignacion = datetime.utcnow()
                
                db.session.commit()
                
                # Usar método correcto de notificación
                abogado = Usuario.query.get(abogado_id)
                NotificacionService.enviar_asignacion_consulta(abogado, consulta)
                
                logger.info(f"✅ Consulta {consulta.numero_consulta} asignada a {abogado.nombre_completo}")
                flash(f'✅ Consulta asignada a {abogado.nombre_completo}', 'success')
            
            elif accion == 'resolver' and current_user.rol in ['Admin', 'Abogado']:
                consulta.resolucion = request.form.get('resolucion')
                consulta.recomendaciones = request.form.get('recomendaciones')
                consulta.estado = 'Resuelta'
                consulta.fecha_resolucion = datetime.utcnow()
                
                db.session.commit()
                
                # Usar método correcto de notificación
                if consulta.empleado_afectado:
                    NotificacionService.enviar_resolucion_consulta(consulta.empleado_afectado, consulta)
                
                # Notificar también al creador
                if consulta.responsable_creador and consulta.responsable_creador_id != consulta.empleado_afectado_id:
                    html = f"""
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <div style="background-color: #28a745; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;">
                            <h2 style="margin: 0;">✅ Consulta Resuelta</h2>
                        </div>
                        <div style="background-color: #e8f5e9; padding: 20px; border-radius: 0 0 5px 5px;">
                            <p>La consulta jurídica <strong>{consulta.numero_consulta}</strong> ha sido resuelta por {current_user.nombre_completo}.</p>
                            <p style="text-align: center; margin-top: 20px;">
                                <a href="http://localhost:5000/juridico/{consulta.id}" style="background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">Ver Resolución</a>
                            </p>
                        </div>
                    </div>
                    """
                    NotificacionService.enviar_email(
                        consulta.responsable_creador.email,
                        f"[SST] Consulta Resuelta: {consulta.numero_consulta}",
                        html
                    )
                
                logger.info(f"✅ Consulta {consulta.numero_consulta} marcada como resuelta")
                flash('✅ Consulta marcada como resuelta', 'success')
            
            elif accion == 'cerrar' and current_user.rol in ['Admin', 'Responsable_SST']:
                consulta.estado = 'Cerrada'
                consulta.fecha_cierre = datetime.utcnow()
                db.session.commit()
                logger.info(f"✅ Consulta {consulta.numero_consulta} cerrada")
                flash('✅ Consulta cerrada', 'success')
            
            elif accion == 'reabrir' and current_user.rol in ['Admin', 'Responsable_SST']:
                consulta.estado = 'Abierta'
                db.session.commit()
                logger.info(f"✅ Consulta {consulta.numero_consulta} reabierta")
                flash('✅ Consulta reabierta', 'success')
            
            return redirect(url_for('juridico.detalle', id=consulta.id))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ Error en operación: {str(e)}", exc_info=True)
            flash(f'❌ Error: {str(e)}', 'error')
            return redirect(url_for('juridico.detalle', id=consulta.id))
    
    # Obtener abogados disponibles
    abogados = Usuario.query.filter_by(rol='Abogado').all()
    
    # Obtener documentos asociados
    documentos = DocumentoLegal.query.filter_by(consulta_id=id).all()
    
    # Calcular SLA
    sla_dias = 0
    sla_excedido = False
    if consulta.estado == 'Abierta':
        horas_transcurridas = (datetime.utcnow() - consulta.fecha_creacion).total_seconds() / 3600
        sla_dias = int(horas_transcurridas / 24)
        # SLA según prioridad (en horas)
        sla_map = {'Baja': 168, 'Normal': 72, 'Alta': 24, 'Crítica': 4}
        sla_excedido = horas_transcurridas > sla_map.get(consulta.prioridad, 72)
    
    contexto = {
        'consulta': consulta,
        'abogados': abogados,
        'documentos': documentos,
        'sla_dias': sla_dias,
        'sla_excedido': sla_excedido,
        'puede_asignar': current_user.rol in ['Admin', 'Responsable_SST'],
        'puede_resolver': current_user.rol in ['Admin', 'Abogado'],
        'puede_cerrar': current_user.rol in ['Admin', 'Responsable_SST']
    }
    
    return render_template('juridico/detalle.html', **contexto)

# ============ CARGAR DOCUMENTO ============

@juridico_bp.route('/<int:id>/documento/cargar', methods=['POST'])
@juridico_required
def cargar_documento(id):
    """Cargar documento legal"""
    
    consulta = ConsultaJuridica.query.get_or_404(id)
    
    try:
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        contenido = request.form.get('contenido')
        
        documento = DocumentoLegal(
            consulta_id=id,
            nombre=nombre,
            tipo=tipo,
            contenido=contenido,
            creado_por_id=current_user.id
        )
        
        db.session.add(documento)
        db.session.commit()
        
        logger.info(f"✅ Documento {nombre} cargado en consulta {consulta.numero_consulta}")
        flash('✅ Documento cargado exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error al cargar documento: {str(e)}", exc_info=True)
        flash(f'❌ Error al cargar documento: {str(e)}', 'error')
    
    return redirect(url_for('juridico.detalle', id=id))

# ============ ELIMINAR DOCUMENTO ============

@juridico_bp.route('/documento/<int:doc_id>/eliminar', methods=['POST'])
@juridico_required
def eliminar_documento(doc_id):
    """Eliminar documento legal"""
    
    documento = DocumentoLegal.query.get_or_404(doc_id)
    consulta_id = documento.consulta_id
    
    # Verificar permisos
    if current_user.id != documento.creado_por_id and current_user.rol not in ['Admin', 'Abogado']:
        flash('❌ No tienes permiso para eliminar este documento', 'error')
        return redirect(url_for('juridico.detalle', id=consulta_id))
    
    try:
        db.session.delete(documento)
        db.session.commit()
        logger.info(f"✅ Documento {documento.nombre} eliminado")
        flash('✅ Documento eliminado', 'success')
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error al eliminar documento: {str(e)}", exc_info=True)
        flash(f'❌ Error al eliminar documento: {str(e)}', 'error')
    
    return redirect(url_for('juridico.detalle', id=consulta_id))

# ============ NORMATIVA - BÚSQUEDA ============

@juridico_bp.route('/normativa')
@juridico_required
def normativa():
    """Listar normativa SST Colombia"""
    
    # Buscar consultas marcadas como normativa
    normativas = ConsultaJuridica.query.filter(
        ConsultaJuridica.numero_consulta.like('NORM-%')
    ).order_by(ConsultaJuridica.fecha_creacion.desc()).all()
    
    contexto = {
        'normativas': normativas,
        'total': len(normativas)
    }
    
    return render_template('juridico/normativa.html', **contexto)

# ============ DESCARGAR REPORTE ============

@juridico_bp.route('/<int:id>/descargar')
@juridico_required
def descargar_reporte(id):
    """Generar y descargar reporte de consulta en PDF"""
    
    consulta = ConsultaJuridica.query.get_or_404(id)
    
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from io import BytesIO
        import uuid
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor='#1e3a8a',
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph("REPORTE CONSULTA JURÍDICA", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Información general
        data = [
            ['Campo', 'Valor'],
            ['Número Consulta', consulta.numero_consulta],
            ['Título', consulta.titulo],
            ['Tipo', consulta.tipo_consulta],
            ['Estado', consulta.estado],
            ['Prioridad', consulta.prioridad],
            ['Riesgo Legal', consulta.riesgo_legal],
            ['Creado', str(consulta.fecha_creacion)],
            ['Resuelto', str(consulta.fecha_resolucion) if consulta.fecha_resolucion else 'N/A'],
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#e0e7ff'),
            ('TEXTCOLOR', (0, 0), (-1, 0), '#1e3a8a'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), '#f0f4ff'),
            ('GRID', (0, 0), (-1, -1), 1, '#cccccc'),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Descripción
        story.append(Paragraph("<b>Descripción:</b>", styles['Heading3']))
        story.append(Paragraph(consulta.descripcion or "N/A", styles['BodyText']))
        story.append(Spacer(1, 0.2*inch))
        
        # Resolución
        if consulta.resolucion:
            story.append(PageBreak())
            story.append(Paragraph("<b>Resolución:</b>", styles['Heading3']))
            story.append(Paragraph(consulta.resolucion, styles['BodyText']))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(f"Generado el: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}", 
                              ParagraphStyle('footer', parent=styles['Normal'], fontSize=8, alignment=2)))
        
        doc.build(story)
        buffer.seek(0)
        
        from flask import send_file
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"Consulta_{consulta.numero_consulta}_{datetime.utcnow().strftime('%Y%m%d')}.pdf"
        )
        
    except ImportError:
        flash('❌ ReportLab no está instalado. Instala con: pip install reportlab', 'error')
        return redirect(url_for('juridico.detalle', id=id))
    except Exception as e:
        logger.error(f"❌ Error al generar reporte: {str(e)}", exc_info=True)
        flash(f'❌ Error al generar reporte: {str(e)}', 'error')
        return redirect(url_for('juridico.detalle', id=id))

# ============ API ENDPOINTS ============

@juridico_bp.route('/api/estadisticas')
@juridico_required
def api_estadisticas():
    """API para obtener estadísticas jurídicas"""
    
    try:
        stats = {
            'total_consultas': ConsultaJuridica.query.count(),
            'por_estado': {
                'Abierta': ConsultaJuridica.query.filter_by(estado='Abierta').count(),
                'En revisión': ConsultaJuridica.query.filter_by(estado='En revisión').count(),
                'Resuelta': ConsultaJuridica.query.filter_by(estado='Resuelta').count(),
                'Cerrada': ConsultaJuridica.query.filter_by(estado='Cerrada').count(),
            },
            'por_tipo': {},
            'por_riesgo': {
                'Bajo': ConsultaJuridica.query.filter_by(riesgo_legal='Bajo').count(),
                'Medio': ConsultaJuridica.query.filter_by(riesgo_legal='Medio').count(),
                'Alto': ConsultaJuridica.query.filter_by(riesgo_legal='Alto').count(),
                'Crítico': ConsultaJuridica.query.filter_by(riesgo_legal='Crítico').count(),
            },
            'promedio_resolucion_horas': calcular_promedio_resolucion()
        }
        
        # Contar por tipo
        tipos = ['Laboral', 'Penal', 'Civil', 'Administrativo', 'Cumplimiento Normativo']
        for tipo in tipos:
            stats['por_tipo'][tipo] = ConsultaJuridica.query.filter_by(tipo_consulta=tipo).count()
        
        return jsonify(stats)
    except Exception as e:
        logger.error(f"❌ Error al obtener estadísticas: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

def calcular_promedio_resolucion():
    """Calcular promedio de tiempo de resolución"""
    try:
        consultas_resueltas = ConsultaJuridica.query.filter(
            ConsultaJuridica.fecha_resolucion.isnot(None)
        ).all()
        
        if not consultas_resueltas:
            return 0
        
        total_horas = 0
        for consulta in consultas_resueltas:
            delta = consulta.fecha_resolucion - consulta.fecha_creacion
            total_horas += delta.total_seconds() / 3600
        
        return round(total_horas / len(consultas_resueltas), 2)
    except Exception as e:
        logger.error(f"❌ Error calculando promedio: {str(e)}")
        return 0