from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import (
    CondicionInsegura, Usuario, Dependencia, TipoReporte, 
    TipoEvidencia, CategoriaArea, GestionReporte
)
from datetime import datetime
from app.routes import reportes_bp
import os
from werkzeug.utils import secure_filename
from app.services.gestion_reportes_service import GestionReportesService

@reportes_bp.route('/', methods=['GET'])
@login_required
def listar():
    """Listar todos los reportes"""
    reportes = CondicionInsegura.query.order_by(CondicionInsegura.fecha_creacion.desc()).all()
    return render_template('reportes/listar.html', reportes=reportes)

@reportes_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    """Crear un nuevo reporte"""
    if request.method == 'POST':
        try:
            # Crear nuevo reporte
            reporte = CondicionInsegura()
            reporte.generar_numero_reporte()
            
            # Información del reportador
            reporte.reportador_nombre = request.form.get('reportador_nombre') or current_user.nombre_completo
            reporte.reportador_cargo = request.form.get('reportador_cargo', '')
            reporte.empleado_reportador_id = current_user.id
            
            # Tipo de reporte y evidencia
            reporte.tipo_reporte_id = request.form.get('tipo_reporte_id')
            reporte.tipo_evidencia_id = request.form.get('tipo_evidencia_id')
            
            # Información del incidente
            fecha_str = request.form.get('fecha_incidente')
            if fecha_str:
                reporte.fecha_incidente = datetime.fromisoformat(fecha_str)
            
            reporte.ubicacion_id = request.form.get('ubicacion_id')
            reporte.ubicacion_especifica = request.form.get('ubicacion_especifica', '')
            
            # Descripción
            reporte.titulo = request.form.get('titulo')
            reporte.descripcion = request.form.get('descripcion')
            
            # Imagen (si se sube)
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file and file.filename != '':
                    filename = secure_filename(f"{reporte.numero_reporte}_{file.filename}")
                    upload_dir = 'uploads/reportes'
                    os.makedirs(upload_dir, exist_ok=True)
                    filepath = os.path.join(upload_dir, filename)
                    file.save(filepath)
                    reporte.imagen_url = filepath
            
            # Estado inicial
            reporte.estado = 'Reportado'
            reporte.fecha_creacion = datetime.utcnow()
            
            db.session.add(reporte)
            db.session.commit()
            
            # ============ ASIGNACIÓN AUTOMÁTICA ============
            gestion = GestionReportesService.asignar_reporte(reporte.id)
            
            if gestion:
                flash(f'✅ Reporte {reporte.numero_reporte} creado y asignado automáticamente a {gestion.gestor_actual.nombre_completo}', 'success')
            else:
                flash(f'⚠️ Reporte {reporte.numero_reporte} creado pero NO se pudo asignar (falta configurar gestores)', 'warning')
            
            return redirect(url_for('reportes.ver', id=reporte.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error al crear reporte: {str(e)}', 'error')
            import traceback
            traceback.print_exc()
    
    # GET - Mostrar formulario
    tipos_reporte = TipoReporte.query.filter_by(activo=True).all()
    tipos_evidencia = TipoEvidencia.query.filter_by(activo=True).all()
    categorias = CategoriaArea.query.filter_by(activa=True).all()
    dependencias = Dependencia.query.filter_by(activa=True).all()
    
    return render_template('reportes/nuevo_mejorado.html',
                         tipos_reporte=tipos_reporte,
                         tipos_evidencia=tipos_evidencia,
                         categorias=categorias,
                         dependencias=dependencias,
                         current_user=current_user)

@reportes_bp.route('/<int:id>', methods=['GET'])
@login_required
def ver(id):
    """Ver detalle de un reporte"""
    reporte = CondicionInsegura.query.get_or_404(id)
    
    # Obtener gestión del reporte
    gestion = GestionReporte.query.filter_by(reporte_id=id).first()
    
    # Verificar permisos
    puede_ver = (
        reporte.empleado_reportador_id == current_user.id or
        current_user.rol in ['Admin', 'Responsable_SST', 'Gerente', 'Abogado'] or
        (gestion and gestion.gestor_actual_id == current_user.id)
    )
    
    if not puede_ver:
        flash('No tienes permiso para ver este reporte', 'error')
        return redirect(url_for('reportes.listar'))
    
    return render_template('reportes/ver.html', reporte=reporte, gestion=gestion)

@reportes_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Editar un reporte"""
    reporte = CondicionInsegura.query.get_or_404(id)
    
    # Solo el reportador o SST puede editar
    if reporte.empleado_reportador_id != current_user.id and current_user.rol != 'Responsable_SST':
        flash('No tienes permiso para editar este reporte', 'error')
        return redirect(url_for('reportes.ver', id=id))
    
    if request.method == 'POST':
        try:
            reporte.titulo = request.form.get('titulo')
            reporte.descripcion = request.form.get('descripcion')
            reporte.ubicacion_id = request.form.get('ubicacion_id')
            reporte.tipo_reporte_id = request.form.get('tipo_reporte_id')
            reporte.tipo_evidencia_id = request.form.get('tipo_evidencia_id')
            
            db.session.commit()
            flash('✅ Reporte actualizado', 'success')
            return redirect(url_for('reportes.ver', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error: {str(e)}', 'error')
    
    tipos_reporte = TipoReporte.query.filter_by(activo=True).all()
    tipos_evidencia = TipoEvidencia.query.filter_by(activo=True).all()
    dependencias = Dependencia.query.filter_by(activa=True).all()
    
    return render_template('reportes/editar.html',
                         reporte=reporte,
                         tipos_reporte=tipos_reporte,
                         tipos_evidencia=tipos_evidencia,
                         dependencias=dependencias)

@reportes_bp.route('/<int:id>/responder', methods=['POST'])
@login_required
def responder(id):
    """Marca que el gestor respondió al reporte"""
    gestion = GestionReporte.query.filter_by(reporte_id=id).first()
    
    if not gestion or gestion.gestor_actual_id != current_user.id:
        flash('No tienes permiso para responder este reporte', 'error')
        return redirect(url_for('reportes.ver', id=id))
    
    try:
        GestionReportesService.marcar_respondido(gestion.id, current_user.id)
        flash('✅ Has respondido al reporte', 'success')
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(url_for('reportes.ver', id=id))

@reportes_bp.route('/<int:id>/resolver', methods=['POST'])
@login_required
def resolver(id):
    """Marca que el gestor resolvió el reporte"""
    gestion = GestionReporte.query.filter_by(reporte_id=id).first()
    
    if not gestion or gestion.gestor_actual_id != current_user.id:
        flash('No tienes permiso para resolver este reporte', 'error')
        return redirect(url_for('reportes.ver', id=id))
    
    try:
        resolucion = request.form.get('resolucion', '')
        if not resolucion:
            flash('❌ Debes escribir la resolución', 'error')
            return redirect(url_for('reportes.ver', id=id))
        
        GestionReportesService.marcar_resuelto(gestion.id, current_user.id, resolucion)
        flash('✅ Reporte resuelto y notificación enviada al reportador', 'success')
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(url_for('reportes.ver', id=id))

@reportes_bp.route('/<int:id>/cerrar', methods=['POST'])
@login_required
def cerrar(id):
    """Cerrar un reporte (solo SST)"""
    reporte = CondicionInsegura.query.get_or_404(id)
    
    if current_user.rol not in ['Responsable_SST', 'Admin']:
        flash('Solo SST puede cerrar reportes', 'error')
        return redirect(url_for('reportes.ver', id=id))
    
    try:
        gestion = GestionReporte.query.filter_by(reporte_id=id).first()
        if gestion:
            GestionReportesService.marcar_cerrado(gestion.id, current_user.id)
        
        reporte.estado = 'Cerrado'
        reporte.fecha_cierre = datetime.utcnow()
        db.session.commit()
        
        flash('✅ Reporte cerrado', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(url_for('reportes.ver', id=id))

# ============== API ENDPOINTS ==============

@reportes_bp.route('/api/categorias/<int:categoria_id>/dependencias', methods=['GET'])
@login_required
def api_dependencias_por_categoria(categoria_id):
    """API para obtener dependencias por categoría"""
    dependencias = Dependencia.query.filter_by(
        categoria_id=categoria_id,
        activa=True
    ).all()
    
    return jsonify([{
        'id': d.id,
        'nombre': d.nombre,
        'direccion': d.direccion,
        'latitud': d.latitud,
        'longitud': d.longitud
    } for d in dependencias])

@reportes_bp.route('/api/dependencias/<int:dep_id>', methods=['GET'])
@login_required
def api_dependencia_detail(dep_id):
    """API para obtener detalles de dependencia"""
    dep = Dependencia.query.get_or_404(dep_id)
    return jsonify({
        'id': dep.id,
        'nombre': dep.nombre,
        'direccion': dep.direccion,
        'latitud': dep.latitud,
        'longitud': dep.longitud,
        'categoria': dep.categoria.nombre if dep.categoria else ''
    })