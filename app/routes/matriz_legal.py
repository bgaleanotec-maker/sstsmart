from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_from_directory
from flask_login import login_required, current_user
from app import db
from app.models.matriz_legal import RequisitoLegal, ValoracionJuridica, EvidenciaLegal, LogMatrizLegal, EstadoRequisito, ProbabilidadSancion
from app.models.usuario import Usuario
from werkzeug.utils import secure_filename
import os
from datetime import datetime

matriz_legal_bp = Blueprint('matriz_legal', __name__, url_prefix='/matriz-legal')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'png'}

@matriz_legal_bp.route('/')
@login_required
def dashboard():
    requisitos = RequisitoLegal.query.order_by(RequisitoLegal.fecha_creacion.desc()).all()
    
    # Calcular KPIs simples
    total = len(requisitos)
    cumplen = sum(1 for r in requisitos if r.estado == EstadoRequisito.CUMPLE)
    pendientes = sum(1 for r in requisitos if r.estado == EstadoRequisito.PENDIENTE)
    
    return render_template('matriz_legal/dashboard.html', 
                         requisitos=requisitos,
                         total=total,
                         cumplen=cumplen,
                         pendientes=pendientes)

@matriz_legal_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def crear_requisito():
    if request.method == 'POST':
        norma = request.form.get('norma')
        articulo = request.form.get('articulo')
        descripcion = request.form.get('descripcion')
        entidad = request.form.get('entidad')
        anio = request.form.get('anio')
        
        nuevo_req = RequisitoLegal(
            norma=norma,
            articulo=articulo,
            descripcion=descripcion,
            entidad=entidad,
            anio=anio
        )
        db.session.add(nuevo_req)
        db.session.commit()
        
        # Forensic Log
        nuevo_req.log_accion(current_user.id, "CREACION", f"Norma: {norma}, Art: {articulo}")
        db.session.commit()
        
        flash('Requisito legal creado correctamente.', 'success')
        return redirect(url_for('matriz_legal.dashboard'))
    
    return render_template('matriz_legal/crear_requisito.html')

@matriz_legal_bp.route('/<int:id>/evaluar', methods=['GET', 'POST'])
@login_required
def evaluar_requisito(id):
    requisito = RequisitoLegal.query.get_or_404(id)
    
    # Solo abogados o admins deberían poder evaluar
    # if current_user.rol not in ['Admin', 'Juridico', 'Abogado']:
    #     flash('No tienes permisos para realizar evaluación jurídica.', 'danger')
    #     return redirect(url_for('matriz_legal.dashboard'))

    if request.method == 'POST':
        puntuacion = int(request.form.get('puntuacion'))
        probabilidad = request.form.get('probabilidad') # Enum name
        impacto = float(request.form.get('impacto') or 0)
        concepto = request.form.get('concepto')
        nuevo_estado = request.form.get('estado')
        
        # Crear Valoración
        valoracion = ValoracionJuridica(
            requisito_id=id,
            usuario_id=current_user.id,
            puntuacion_cumplimiento=puntuacion,
            probabilidad_sancion=ProbabilidadSancion[probabilidad],
            impacto_financiero=impacto,
            concepto_final=concepto
        )
        db.session.add(valoracion)
        
        # Actualizar estado del requisito
        if nuevo_estado:
            # Buscar el enum correcto
            for est in EstadoRequisito:
                if est.value == nuevo_estado:
                    requisito.estado = est
                    break
        
        # Forensic Log
        requisito.log_accion(
            current_user.id, 
            "EVALUACION", 
            f"Puntuación: {puntuacion}, Estado: {nuevo_estado}, Riesgo: {valoracion.nivel_riesgo_total}"
        )
        
        db.session.commit()
        flash('Evaluación jurídica registrada.', 'success')
        return redirect(url_for('matriz_legal.dashboard'))
        
    return render_template('matriz_legal/evaluar.html', requisito=requisito)

@matriz_legal_bp.route('/<int:id>/evidencia', methods=['POST'])
@login_required
def subir_evidencia(id):
    requisito = RequisitoLegal.query.get_or_404(id)
    
    if 'archivo' not in request.files:
        flash('No se seleccionó archivo', 'warning')
        return redirect(url_for('matriz_legal.dashboard'))
        
    file = request.files['archivo']
    if file.filename == '':
        flash('Nombre de archivo vacío', 'warning')
        return redirect(url_for('matriz_legal.dashboard'))
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Versionado simple: timestamp
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        savename = f"{ts}_{filename}"
        
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'legales')
        os.makedirs(upload_path, exist_ok=True)
        
        file.save(os.path.join(upload_path, savename))
        
        # Calcular versión
        ultima_version = EvidenciaLegal.query.filter_by(requisito_id=id).order_by(EvidenciaLegal.version.desc()).first()
        nueva_vers = (ultima_version.version + 1) if ultima_version else 1
        
        evidencia = EvidenciaLegal(
            requisito_id=id,
            usuario_id=current_user.id,
            archivo_path=f"legales/{savename}",
            nombre_archivo=filename,
            version=nueva_vers,
            descripcion_cambio=request.form.get('descripcion_cambio', 'Carga inicial')
        )
        db.session.add(evidencia)
        
        # Log
        requisito.log_accion(current_user.id, "EVIDENCIA", f"Archivo: {filename} (v{nueva_vers})")
        db.session.commit()
        
        flash('Evidencia cargada exitosamente.', 'success')
    else:
        flash('Tipo de archivo no permitido', 'danger')
        
    return redirect(url_for('matriz_legal.detalle', id=id))

@matriz_legal_bp.route('/<int:id>')
@login_required
def detalle(id):
    requisito = RequisitoLegal.query.get_or_404(id)
    return render_template('matriz_legal/detalle.html', requisito=requisito)
