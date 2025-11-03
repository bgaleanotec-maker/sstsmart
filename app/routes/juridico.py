from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import ConsultaJuridica, DocumentoLegal, Usuario
from app.services.notificaciones import NotificacionService
from app.routes import juridico_bp
from datetime import datetime

@juridico_bp.route('/')
@login_required
def listar():
    if current_user.rol not in ['Admin', 'Responsable_SST', 'Abogado']:
        flash('No autorizado', 'error')
        return redirect(url_for('dashboard.index'))
    
    consultas = ConsultaJuridica.query.order_by(ConsultaJuridica.fecha_creacion.desc()).all()
    return render_template('juridico/listar.html', consultas=consultas)

@juridico_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        consulta = ConsultaJuridica(
            titulo=request.form.get('titulo'),
            descripcion=request.form.get('descripcion'),
            tipo_consulta=request.form.get('tipo_consulta'),
            condicion_insegura_id=request.form.get('condicion_insegura_id'),
            empleado_afectado_id=request.form.get('empleado_afectado_id'),
            responsable_creador_id=current_user.id,
            prioridad=request.form.get('prioridad', 'Normal'),
            riesgo_legal=request.form.get('riesgo_legal', 'Medio')
        )
        consulta.generar_numero_consulta()
        
        db.session.add(consulta)
        db.session.commit()
        
        flash('Consulta jurídica creada', 'success')
        return redirect(url_for('juridico.detalle', id=consulta.id))
    
    return render_template('juridico/crear.html')

@juridico_bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def detalle(id):
    consulta = ConsultaJuridica.query.get_or_404(id)
    
    if request.method == 'POST':
        if request.form.get('action') == 'asignar':
            abogado_id = request.form.get('abogado_id')
            consulta.abogado_asignado_id = abogado_id
            consulta.estado = 'En revisión'
            consulta.fecha_asignacion = datetime.utcnow()
            
            db.session.commit()
            
            abogado = Usuario.query.get(abogado_id)
            NotificacionService.enviar_asignacion_consulta(abogado, consulta)
            
            flash('Abogado asignado y notificado', 'success')
        
        elif request.form.get('action') == 'resolver':
            consulta.resolucion = request.form.get('resolucion')
            consulta.recomendaciones = request.form.get('recomendaciones')
            consulta.normativa_aplicable = request.form.getlist('normativa_aplicable')
            consulta.estado = 'Resuelta'
            consulta.fecha_resolucion = datetime.utcnow()
            
            db.session.commit()
            
            if consulta.empleado_afectado:
                NotificacionService.enviar_resolucion_consulta(consulta.empleado_afectado, consulta)
            
            flash('Consulta resuelta', 'success')
        
        elif request.form.get('action') == 'cerrar':
            consulta.estado = 'Cerrada'
            consulta.fecha_cierre = datetime.utcnow()
            
            db.session.commit()
            flash('Consulta cerrada', 'success')
        
        return redirect(url_for('juridico.detalle', id=consulta.id))
    
    abogados = Usuario.query.filter_by(rol='Abogado', activo=True).all()
    documentos = DocumentoLegal.query.filter_by(consulta_id=id).all()
    
    return render_template('juridico/detalle.html', consulta=consulta, abogados=abogados, documentos=documentos)

@juridico_bp.route('/<int:consulta_id>/documento/agregar', methods=['POST'])
@login_required
def agregar_documento(consulta_id):
    consulta = ConsultaJuridica.query.get_or_404(consulta_id)
    
    documento = DocumentoLegal(
        consulta_id=consulta_id,
        nombre=request.form.get('nombre'),
        tipo=request.form.get('tipo'),
        contenido=request.form.get('contenido'),
        creado_por_id=current_user.id
    )
    
    if 'archivo' in request.files:
        archivo = request.files['archivo']
        if archivo.filename:
            import os
            ruta = f"uploads/documentos/{consulta_id}/{archivo.filename}"
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            archivo.save(ruta)
            documento.ruta_archivo = ruta
    
    db.session.add(documento)
    db.session.commit()
    
    flash('Documento agregado', 'success')
    return redirect(url_for('juridico.detalle', id=consulta_id))

@juridico_bp.route('/api/estadisticas')
@login_required
def estadisticas():
    total = ConsultaJuridica.query.count()
    abiertas = ConsultaJuridica.query.filter_by(estado='Abierta').count()
    en_revision = ConsultaJuridica.query.filter_by(estado='En revisión').count()
    resueltas = ConsultaJuridica.query.filter_by(estado='Resuelta').count()
    cerradas = ConsultaJuridica.query.filter_by(estado='Cerrada').count()
    
    criticas = ConsultaJuridica.query.filter_by(riesgo_legal='Crítico').count()
    
    return jsonify({
        'total': total,
        'abierta': abiertas,
        'en_revision': en_revision,
        'resuelta': resueltas,
        'cerrada': cerradas,
        'criticas': criticas
    })
