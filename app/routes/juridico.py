# app/routes/juridico.py
"""
RUTAS MÓDULO JURÍDICO - SST SMART
==================================
Incluye:
- Gestión de abogados
- Consultas jurídicas completo
- Gestión documental versioned
- Colaboración en tiempo real
- Auditoría y cumplimiento
"""

from flask import render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from app import db
from app.models import (
    ConsultaJuridica, DocumentoLegal, Abogado, ComentarioConsulta, 
    ComentarioDocumento, AuditoriaConsulta, HistorialDocumento, 
    TablaRetencion, Usuario, Empleado
)
from app.services.notificaciones import NotificacionService
from app.routes import juridico_bp
from datetime import datetime, timedelta
import os
import hashlib
from werkzeug.utils import secure_filename

# ==================== CONFIGURACIÓN ====================

UPLOAD_FOLDER = 'uploads/documentos_juridicos'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'xlsx', 'xls', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== ABOGADOS ====================

@juridico_bp.route('/abogados/pool', methods=['GET'])
@login_required
def listar_abogados():
    """Lista el pool de abogados disponibles"""
    page = request.args.get('page', 1, type=int)
    especializacion = request.args.get('especialidad', None)
    
    query = Abogado.query.filter_by(activo=True)
    
    if especializacion:
        # Buscar abogados con esa especialidad
        query = query.filter(Abogado.especialidades.astext.contains(especializacion))
    
    abogados = query.paginate(page=page, per_page=10)
    
    return render_template('juridico/pool_abogados.html', abogados=abogados)


@juridico_bp.route('/abogados/<int:abogado_id>/perfil', methods=['GET'])
@login_required
def perfil_abogado(abogado_id):
    """Perfil detallado del abogado"""
    abogado = Abogado.query.get_or_404(abogado_id)
    
    # Estadísticas
    consultas_totales = abogado.consultas.count()
    consultas_resueltas = abogado.consultas.filter_by(estado='Resuelta').count()
    calificacion = db.session.query(db.func.avg(
        db.column('puntuacion')
    )).filter(db.column('abogado_id') == abogado_id).scalar() or 0
    
    contexto = {
        'abogado': abogado,
        'consultas_totales': consultas_totales,
        'consultas_resueltas': consultas_resueltas,
        'calificacion': calificacion,
        'disponible': abogado.get_disponibilidad_hoy()
    }
    
    return render_template('juridico/perfil_abogado.html', **contexto)


@juridico_bp.route('/abogados/<int:abogado_id>/horario', methods=['GET', 'POST'])
@login_required
def configurar_horario_abogado(abogado_id):
    """Configura horario de atención del abogado"""
    abogado = Abogado.query.get_or_404(abogado_id)
    
    # Solo el abogado o admin pueden editar
    if current_user.id != abogado.usuario_id and current_user.rol != 'Admin':
        flash('No autorizado', 'error')
        return redirect(url_for('juridico.listar_abogados'))
    
    if request.method == 'POST':
        horario = {}
        for dia in ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']:
            inicio = request.form.get(f'{dia}_inicio')
            fin = request.form.get(f'{dia}_fin')
            if inicio and fin:
                horario[dia] = [inicio, fin]
        
        abogado.horario_atencion = horario
        abogado.horas_disponibles = int(request.form.get('horas_disponibles', 20))
        
        db.session.commit()
        flash('Horario actualizado', 'success')
        return redirect(url_for('juridico.perfil_abogado', abogado_id=abogado_id))
    
    return render_template('juridico/configurar_horario.html', abogado=abogado)


# ==================== CONSULTAS JURÍDICAS ====================

@juridico_bp.route('/')
@login_required
def listar_consultas():
    """Lista consultas jurídicas con filtros avanzados"""
    page = request.args.get('page', 1, type=int)
    estado = request.args.get('estado', None)
    prioridad = request.args.get('prioridad', None)
    riesgo = request.args.get('riesgo', None)
    abogado_id = request.args.get('abogado_id', None)
    
    # Verificar permisos
    if current_user.rol not in ['Admin', 'Responsable_SST', 'Abogado', 'Cliente']:
        flash('No autorizado', 'error')
        return redirect(url_for('dashboard.index'))
    
    query = ConsultaJuridica.query
    
    # Filtro por rol
    if current_user.rol == 'Abogado':
        # Solo ve sus consultas
        query = query.filter_by(abogado_asignado_id=current_user.abogado_profile.id)
    elif current_user.rol == 'Cliente':
        # Solo ve sus consultas
        query = query.filter_by(empleado_afectado_id=current_user.id)
    
    # Filtros
    if estado:
        query = query.filter_by(estado=estado)
    if prioridad:
        query = query.filter_by(prioridad=prioridad)
    if riesgo:
        query = query.filter_by(riesgo_legal=riesgo)
    if abogado_id:
        query = query.filter_by(abogado_asignado_id=abogado_id)
    
    consultas = query.order_by(ConsultaJuridica.fecha_creacion.desc()).paginate(page=page, per_page=15)
    
    # Estadísticas
    stats = {
        'total': ConsultaJuridica.query.count(),
        'abiertas': ConsultaJuridica.query.filter_by(estado='Abierta').count(),
        'en_revision': ConsultaJuridica.query.filter_by(estado='En revisión').count(),
        'con_concepto': ConsultaJuridica.query.filter_by(estado='En concepto').count(),
        'resueltas': ConsultaJuridica.query.filter_by(estado='Resuelta').count(),
        'criticas': ConsultaJuridica.query.filter_by(riesgo_legal='Crítico').count(),
    }
    
    abogados = Abogado.query.filter_by(activo=True).all()
    
    return render_template('juridico/listar.html', 
                         consultas=consultas, 
                         stats=stats, 
                         abogados=abogados)


@juridico_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def crear_consulta():
    """Crear nueva consulta jurídica"""
    if request.method == 'POST':
        try:
            consulta = ConsultaJuridica(
                titulo=request.form.get('titulo'),
                descripcion=request.form.get('descripcion'),
                tipo_consulta=request.form.get('tipo_consulta'),
                prioridad=request.form.get('prioridad', 'Normal'),
                riesgo_legal=request.form.get('riesgo_legal', 'Medio'),
                nivel_confidencialidad=request.form.get('confidencialidad', 'Interno'),
                horas_estimadas=float(request.form.get('horas_estimadas', 0)) or None,
                responsable_creador_id=current_user.id
            )
            
            # Relaciones opcionales
            if request.form.get('empleado_afectado_id'):
                consulta.empleado_afectado_id = int(request.form.get('empleado_afectado_id'))
            
            consulta.generar_numero_consulta()
            
            db.session.add(consulta)
            db.session.flush()  # Para obtener el ID
            
            # Registrar auditoría
            auditoria = AuditoriaConsulta(
                usuario_id=current_user.id,
                consulta_id=consulta.id,
                accion='crear_consulta',
                detalles={'titulo': consulta.titulo}
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash(f'Consulta creada: {consulta.numero_consulta}', 'success')
            return redirect(url_for('juridico.detalle_consulta', consulta_id=consulta.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear consulta: {str(e)}', 'error')
    
    empleados = Empleado.query.all()
    return render_template('juridico/crear.html', empleados=empleados)


@juridico_bp.route('/<int:consulta_id>', methods=['GET'])
@login_required
def detalle_consulta(consulta_id):
    """Detalle completo de consulta con todas sus interacciones"""
    consulta = ConsultaJuridica.query.get_or_404(consulta_id)
    
    # Verificar permisos de lectura
    puede_ver = (
        current_user.rol in ['Admin', 'Responsable_SST'] or
        (current_user.rol == 'Abogado' and consulta.abogado_asignado_id == current_user.abogado_profile.id) or
        (current_user.rol == 'Cliente' and consulta.empleado_afectado_id == current_user.id)
    )
    
    if not puede_ver:
        flash('No tiene permiso para ver esta consulta', 'error')
        return redirect(url_for('juridico.listar_consultas'))
    
    # Obtener datos relacionados
    documentos = DocumentoLegal.query.filter_by(
        consulta_id=consulta_id, 
        es_version_anterior=False
    ).all()
    
    comentarios = ComentarioConsulta.query.filter_by(
        consulta_id=consulta_id,
        responde_a_id=None
    ).order_by(ComentarioConsulta.fecha_creacion.desc()).all()
    
    auditoria = AuditoriaConsulta.query.filter_by(consulta_id=consulta_id).order_by(
        AuditoriaConsulta.fecha.desc()
    ).all()
    
    abogados_disponibles = Abogado.query.filter_by(activo=True).all()
    
    contexto = {
        'consulta': consulta,
        'documentos': documentos,
        'comentarios': comentarios,
        'auditoria': auditoria,
        'abogados': abogados_disponibles
    }
    
    return render_template('juridico/detalle.html', **contexto)


@juridico_bp.route('/<int:consulta_id>/asignar-abogado', methods=['POST'])
@login_required
def asignar_abogado(consulta_id):
    """Asigna abogado a consulta"""
    consulta = ConsultaJuridica.query.get_or_404(consulta_id)
    
    if current_user.rol not in ['Admin', 'Responsable_SST']:
        flash('No autorizado', 'error')
        return redirect(url_for('juridico.detalle_consulta', consulta_id=consulta_id))
    
    try:
        abogado_id = request.form.get('abogado_id')
        abogado = Abogado.query.get_or_404(abogado_id)
        
        consulta.cambiar_estado('En revisión', current_user.id, 
                               razon='Asignación manual de abogado')
        consulta.abogado_asignado_id = abogado.id
        
        auditoria = AuditoriaConsulta(
            usuario_id=current_user.id,
            consulta_id=consulta_id,
            accion='asignacion_abogado',
            detalles={'abogado_id': abogado.id, 'abogado_nombre': abogado.usuario.nombre_completo}
        )
        db.session.add(auditoria)
        db.session.commit()
        
        # Notificar abogado
        try:
            NotificacionService.enviar_asignacion_consulta(abogado.usuario, consulta)
        except:
            pass  # Si falla notificación, continuar
        
        flash(f'Consulta asignada a {abogado.usuario.nombre_completo}', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('juridico.detalle_consulta', consulta_id=consulta_id))


@juridico_bp.route('/<int:consulta_id>/cambiar-estado', methods=['POST'])
@login_required
def cambiar_estado_consulta(consulta_id):
    """Cambia estado de consulta y registra auditoría"""
    consulta = ConsultaJuridica.query.get_or_404(consulta_id)
    
    nuevo_estado = request.form.get('nuevo_estado')
    razon = request.form.get('razon', '')
    
    # Validar permisos según estado
    puede_cambiar = (
        (current_user.rol in ['Admin', 'Responsable_SST']) or
        (current_user.rol == 'Abogado' and 
         consulta.abogado_asignado_id == current_user.abogado_profile.id)
    )
    
    if not puede_cambiar:
        return jsonify({'error': 'No autorizado'}), 403
    
    try:
        consulta.cambiar_estado(nuevo_estado, current_user.id, razon)
        db.session.commit()
        
        return jsonify({'success': True, 'nuevo_estado': nuevo_estado})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@juridico_bp.route('/<int:consulta_id>/emitir-concepto', methods=['POST'])
@login_required
def emitir_concepto(consulta_id):
    """Emite concepto jurídico"""
    consulta = ConsultaJuridica.query.get_or_404(consulta_id)
    
    # Solo el abogado asignado puede emitir concepto
    if current_user.rol != 'Abogado' or consulta.abogado_asignado_id != current_user.abogado_profile.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    try:
        concepto = request.form.get('concepto_legal')
        recomendaciones = request.form.get('recomendaciones')
        normativa = request.form.getlist('normativa_aplicable[]')
        horas_reales = float(request.form.get('horas_reales', 0))
        
        consulta.concepto_legal = concepto
        consulta.recomendaciones = recomendaciones
        consulta.normativa_aplicable = normativa
        consulta.horas_reales = horas_reales
        
        consulta.cambiar_estado('Concepto emitido', current_user.id)
        
        auditoria = AuditoriaConsulta(
            usuario_id=current_user.id,
            consulta_id=consulta_id,
            accion='emision_concepto',
            detalles={'horas_reales': horas_reales}
        )
        db.session.add(auditoria)
        db.session.commit()
        
        return jsonify({'success': True, 'concepto_id': consulta.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== GESTIÓN DOCUMENTAL ====================

@juridico_bp.route('/<int:consulta_id>/documentos/agregar', methods=['POST'])
@login_required
def agregar_documento(consulta_id):
    """Agrega documento a consulta con versionado"""
    consulta = ConsultaJuridica.query.get_or_404(consulta_id)
    
    # Verificar permisos
    puede_agregar = (
        current_user.rol in ['Admin', 'Responsable_SST'] or
        (current_user.rol == 'Abogado' and 
         consulta.abogado_asignado_id == current_user.abogado_profile.id)
    )
    
    if not puede_agregar:
        return jsonify({'error': 'No autorizado'}), 403
    
    try:
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        clasificacion = request.form.get('clasificacion', 'Interno')
        tabla_retencion_id = request.form.get('tabla_retencion_id')
        
        documento = DocumentoLegal(
            consulta_id=consulta_id,
            nombre=nombre,
            tipo=tipo,
            clasificacion=clasificacion,
            creado_por_id=current_user.id,
            tabla_retencion_id=tabla_retencion_id or None
        )
        
        # Manejar archivo
        if 'archivo' in request.files:
            archivo = request.files['archivo']
            if archivo and allowed_file(archivo.filename):
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                filename = secure_filename(archivo.filename)
                timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                
                ruta = os.path.join(UPLOAD_FOLDER, filename)
                archivo.save(ruta)
                
                documento.ruta_archivo = ruta
                documento.tamano_bytes = os.path.getsize(ruta)
                documento.calcular_hash(ruta)
        
        # Manejar contenido de texto
        if request.form.get('contenido'):
            documento.contenido = request.form.get('contenido')
        
        # Calcular fecha de destrucción si aplica
        if documento.tabla_retencion:
            documento.fecha_destruccion = documento.tabla_retencion.calcular_fecha_destruccion(
                datetime.utcnow()
            )
        
        # Registrar usuarios con acceso
        documento.usuarios_con_acceso = [current_user.id]
        if consulta.abogado_asignado_id:
            documento.usuarios_con_acceso.append(consulta.abogado_asignado_id)
        
        db.session.add(documento)
        db.session.flush()
        
        # Registrar en auditoría
        auditoria = AuditoriaConsulta(
            usuario_id=current_user.id,
            consulta_id=consulta_id,
            accion='agregar_documento',
            detalles={'nombre': nombre, 'tipo': tipo}
        )
        db.session.add(auditoria)
        
        # Registrar en historial
        historial = HistorialDocumento(
            documento_id=documento.id,
            usuario_id=current_user.id,
            accion='creacion',
            version_nueva=1
        )
        db.session.add(historial)
        db.session.commit()
        
        flash(f'Documento "{nombre}" agregado', 'success')
        return redirect(url_for('juridico.detalle_consulta', consulta_id=consulta_id))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error al agregar documento: {str(e)}', 'error')
        return redirect(url_for('juridico.detalle_consulta', consulta_id=consulta_id))


@juridico_bp.route('/documento/<int:doc_id>/versiones', methods=['GET'])
@login_required
def historial_documento(doc_id):
    """Muestra historial de versiones de un documento"""
    documento = DocumentoLegal.query.get_or_404(doc_id)
    
    # Obtener todas las versiones
    if documento.documento_padre_id:
        # Este es una versión, obtener el documento padre
        doc_principal = DocumentoLegal.query.get(documento.documento_padre_id)
    else:
        doc_principal = documento
    
    versiones = DocumentoLegal.query.filter_by(
        documento_padre_id=doc_principal.id
    ).order_by(DocumentoLegal.numero_version.desc()).all()
    
    cambios = HistorialDocumento.query.filter_by(
        documento_id=doc_id
    ).order_by(HistorialDocumento.fecha.desc()).all()
    
    return render_template('juridico/historial_documento.html',
                         documento=documento,
                         versiones=versiones,
                         cambios=cambios)


@juridico_bp.route('/documento/<int:doc_id>/crear-version', methods=['POST'])
@login_required
def crear_version_documento(doc_id):
    """Crea nueva versión de documento"""
    documento = DocumentoLegal.query.get_or_404(doc_id)
    
    razon = request.form.get('razon_cambio', '')
    
    try:
        nueva_version = documento.crear_nueva_version(current_user.id, razon)
        
        # Actualizar contenido si lo proporciona
        if request.form.get('contenido'):
            nueva_version.contenido = request.form.get('contenido')
        
        # Actualizar archivo si lo proporciona
        if 'archivo' in request.files:
            archivo = request.files['archivo']
            if archivo and allowed_file(archivo.filename):
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                filename = secure_filename(archivo.filename)
                timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                
                ruta = os.path.join(UPLOAD_FOLDER, filename)
                archivo.save(ruta)
                
                nueva_version.ruta_archivo = ruta
                nueva_version.tamano_bytes = os.path.getsize(ruta)
                nueva_version.calcular_hash(ruta)
        
        db.session.commit()
        
        flash(f'Nueva versión creada: v{nueva_version.numero_version}', 'success')
        return redirect(url_for('juridico.historial_documento', doc_id=nueva_version.id))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear versión: {str(e)}', 'error')
        return redirect(url_for('juridico.historial_documento', doc_id=doc_id))


@juridico_bp.route('/documento/<int:doc_id>/descargar', methods=['GET'])
@login_required
def descargar_documento(doc_id):
    """Descarga documento con auditoría"""
    documento = DocumentoLegal.query.get_or_404(doc_id)
    
    # Verificar permisos
    if current_user.id not in (documento.usuarios_con_acceso or []) and \
       current_user.rol not in ['Admin', 'Responsable_SST']:
        return jsonify({'error': 'No autorizado'}), 403
    
    try:
        # Registrar descarga en auditoría
        auditoria = AuditoriaConsulta(
            usuario_id=current_user.id,
            consulta_id=documento.consulta_id,
            accion='descarga_documento',
            detalles={'nombre': documento.nombre}
        )
        db.session.add(auditoria)
        db.session.commit()
        
        if documento.ruta_archivo and os.path.exists(documento.ruta_archivo):
            return send_file(documento.ruta_archivo, 
                           as_attachment=True,
                           download_name=documento.nombre)
        else:
            return jsonify({'error': 'Archivo no encontrado'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== COMENTARIOS COLABORATIVOS ====================

@juridico_bp.route('/<int:consulta_id>/comentario/agregar', methods=['POST'])
@login_required
def agregar_comentario_consulta(consulta_id):
    """Agrega comentario a consulta"""
    consulta = ConsultaJuridica.query.get_or_404(consulta_id)
    
    try:
        comentario = ComentarioConsulta(
            consulta_id=consulta_id,
            usuario_id=current_user.id,
            contenido=request.form.get('contenido'),
            tipo=request.form.get('tipo', 'Observacion'),
            prioridad=request.form.get('prioridad', 'Normal'),
            responde_a_id=request.form.get('responde_a_id') or None
        )
        
        db.session.add(comentario)
        db.session.commit()
        
        return jsonify({'success': True, 'comentario_id': comentario.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@juridico_bp.route('/comentario-doc/<int:doc_id>/agregar', methods=['POST'])
@login_required
def agregar_comentario_documento(doc_id):
    """Agrega anotación a documento"""
    documento = DocumentoLegal.query.get_or_404(doc_id)
    
    try:
        comentario = ComentarioDocumento(
            documento_id=doc_id,
            usuario_id=current_user.id,
            contenido=request.form.get('contenido'),
            tipo=request.form.get('tipo', 'Revision'),
            linea_inicio=request.form.get('linea_inicio'),
            linea_fin=request.form.get('linea_fin'),
            fragmento_texto=request.form.get('fragmento_texto')
        )
        
        db.session.add(comentario)
        db.session.commit()
        
        return jsonify({'success': True, 'comentario_id': comentario.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== AUDITORÍA Y CUMPLIMIENTO ====================

@juridico_bp.route('/auditoria')
@login_required
def reporte_auditoria():
    """Reporte de auditoría del módulo jurídico"""
    if current_user.rol not in ['Admin', 'Responsable_SST']:
        flash('No autorizado', 'error')
        return redirect(url_for('juridico.listar_consultas'))
    
    page = request.args.get('page', 1, type=int)
    usuario_id = request.args.get('usuario_id', None)
    fecha_desde = request.args.get('fecha_desde', None)
    fecha_hasta = request.args.get('fecha_hasta', None)
    
    query = AuditoriaConsulta.query
    
    if usuario_id:
        query = query.filter_by(usuario_id=usuario_id)
    
    if fecha_desde:
        query = query.filter(AuditoriaConsulta.fecha >= datetime.fromisoformat(fecha_desde))
    
    if fecha_hasta:
        query = query.filter(AuditoriaConsulta.fecha <= datetime.fromisoformat(fecha_hasta))
    
    registros = query.order_by(AuditoriaConsulta.fecha.desc()).paginate(page=page, per_page=50)
    
    return render_template('juridico/auditoria.html', registros=registros)


@juridico_bp.route('/tabla-retencion', methods=['GET'])
@login_required
def tabla_retencion():
    """Gestión de tabla de retención documental"""
    if current_user.rol not in ['Admin', 'Responsable_SST']:
        return jsonify({'error': 'No autorizado'}), 403
    
    tablas = TablaRetencion.query.filter_by(activa=True).all()
    return render_template('juridico/tabla_retencion.html', tablas=tablas)


@juridico_bp.route('/api/estadisticas', methods=['GET'])
@login_required
def estadisticas_juridico():
    """API de estadísticas del módulo jurídico"""
    total = ConsultaJuridica.query.count()
    abiertas = ConsultaJuridica.query.filter_by(estado='Abierta').count()
    en_revision = ConsultaJuridica.query.filter_by(estado='En revisión').count()
    en_concepto = ConsultaJuridica.query.filter_by(estado='En concepto').count()
    resueltas = ConsultaJuridica.query.filter_by(estado='Resuelta').count()
    cerradas = ConsultaJuridica.query.filter_by(estado='Cerrada').count()
    
    criticas = ConsultaJuridica.query.filter_by(riesgo_legal='Crítico').count()
    altas = ConsultaJuridica.query.filter_by(riesgo_legal='Alto').count()
    
    # Tiempo promedio de resolución
    consultas_resueltas = ConsultaJuridica.query.filter(
        ConsultaJuridica.fecha_resolucion != None
    ).all()
    
    tiempos = []
    for consulta in consultas_resueltas:
        tiempo = (consulta.fecha_resolucion - consulta.fecha_creacion).days
        tiempos.append(tiempo)
    
    tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0
    
    return jsonify({
        'total': total,
        'abierta': abiertas,
        'en_revision': en_revision,
        'en_concepto': en_concepto,
        'resuelta': resueltas,
        'cerrada': cerradas,
        'criticas': criticas,
        'altas': altas,
        'tiempo_promedio_resolucion_dias': int(tiempo_promedio)
    })