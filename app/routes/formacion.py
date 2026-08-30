from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Curso, Examen, Pregunta, Opcion, IntentoExamen, ProgresoFormacion
from datetime import datetime

formacion_bp = Blueprint('formacion', __name__, url_prefix='/formacion')

# ============ HELPER: CÁLCULO DE SCORE ============
def calcular_ranking_sst(usuario_id):
    """
    Calcula el puntaje SST del usuario basado en cursos completados.
    Fórmula: (Exámenes Aprobados / Total Exámenes Asignados) * 100
    """
    total_cursos = Curso.query.filter_by(estado='Activo').count()
    if total_cursos == 0:
        return 0.0

    intentos_aprobados = IntentoExamen.query.filter_by(
        usuario_id=usuario_id, 
        aprobado=True
    ).with_entities(IntentoExamen.examen_id).distinct().count()
    
    score = (intentos_aprobados / total_cursos) * 100
    
    # Actualizar o Crear registro de progreso
    progreso = ProgresoFormacion.query.filter_by(usuario_id=usuario_id).first()
    if not progreso:
        progreso = ProgresoFormacion(usuario_id=usuario_id)
        db.session.add(progreso)
    
    progreso.total_cursos_asignados = total_cursos
    progreso.total_cursos_completados = intentos_aprobados
    progreso.puntaje_global_sst = round(score, 2)
    progreso.ultimo_calculo = datetime.utcnow()
    
    db.session.commit()
    return progreso.puntaje_global_sst

# ============ RUTAS ============

@formacion_bp.route('/')
@login_required
def catalogo():
    # 1. Obtener todos los cursos activos
    todos_cursos = Curso.query.filter_by(estado='Activo').all()
    
    # 2. Agrupar por Categoría para estilo Netflix
    categorias = {}
    destacado = None
    
    if todos_cursos:
        destacado = todos_cursos[0] # El primero como destacado por ahora
        
        for curso in todos_cursos:
            cat = curso.categoria if curso.categoria else 'General'
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(curso)
    
    # 3. Datos del Usuario
    score = calcular_ranking_sst(current_user.id)
    intentos = IntentoExamen.query.filter_by(usuario_id=current_user.id).all()
    
    # Mapa de aprobados para UI (saber si mostrar check)
    cursos_aprobados_ids = [i.examen.curso_id for i in intentos if i.aprobado and i.examen]
    
    return render_template('formacion/catalogo.html', 
                         categorias=categorias, 
                         destacado=destacado, 
                         score=score, 
                         cursos_aprobados_ids=cursos_aprobados_ids)

@formacion_bp.route('/curso/<int:curso_id>')
@login_required
def ver_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    
    # QA Automation: Smart Embed URL generation
    video_embed_url = None
    if curso.video_url:
        import re
        url = curso.video_url
        
        # YouTube Logic
        youtube_regex = (
            r'(https?://)?(www\.)?'
            r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        yt_match = re.match(youtube_regex, url)
        if yt_match:
            video_id = yt_match.group(6)
            video_embed_url = f"https://www.youtube.com/embed/{video_id}?rel=0"
            
        # Vimeo Logic
        elif 'vimeo.com' in url:
            vimeo_regex = r'vimeo.com/([0-9]+)'
            vm_match = re.search(vimeo_regex, url)
            if vm_match:
                video_id = vm_match.group(1)
                video_embed_url = f"https://player.vimeo.com/video/{video_id}"
        
        # Fallback to direct URL if it looks like a video file or generic
        else:
            video_embed_url = url

    return render_template('formacion/ver_curso.html', curso=curso, video_embed_url=video_embed_url)

@formacion_bp.route('/examen/<int:examen_id>', methods=['GET', 'POST'])
@login_required
def tomar_examen(examen_id):
    examen = Examen.query.get_or_404(examen_id)
    
    if request.method == 'POST':
        puntaje_obtenido = 0
        total_puntos = 0
        
        for pregunta in examen.preguntas:
            total_puntos += pregunta.puntaje
            opcion_seleccionada = request.form.get(f'pregunta_{pregunta.id}')
            if opcion_seleccionada:
                opcion = Opcion.query.get(int(opcion_seleccionada))
                if opcion and opcion.es_correcta:
                    puntaje_obtenido += pregunta.puntaje
        
        aprobado = puntaje_obtenido >= (examen.puntaje_total * (examen.porcentaje_aprobacion / 100))
        
        intento = IntentoExamen(
            usuario_id=current_user.id,
            examen_id=examen.id,
            puntaje_obtenido=puntaje_obtenido,
            aprobado=aprobado
        )
        db.session.add(intento)
        db.session.commit()
        
        # Recalcular score global
        nuevo_score = calcular_ranking_sst(current_user.id)
        
        msg = f'Examen finalizado. Puntaje: {puntaje_obtenido}/{total_puntos}. '
        msg += '✅ Aprobado' if aprobado else '❌ No aprobado'
        flash(msg, 'success' if aprobado else 'warning')
        
        return redirect(url_for('formacion.catalogo'))

    return render_template('formacion/examen.html', examen=examen)

@formacion_bp.route('/certificado/<int:curso_id>')
@login_required
def ver_certificado(curso_id):
    # Verificar si el usuario aprobo el examen de este curso
    curso = Curso.query.get_or_404(curso_id)
    examenes_ids = [e.id for e in curso.examenes]
    
    if not examenes_ids:
         flash('Este curso no tiene exámenes configurados.', 'warning')
         return redirect(url_for('formacion.ver_curso', curso_id=curso_id))

    aprobado = IntentoExamen.query.filter(
        IntentoExamen.usuario_id == current_user.id,
        IntentoExamen.examen_id.in_(examenes_ids),
        IntentoExamen.aprobado == True
    ).order_by(IntentoExamen.fecha_intento.desc()).first()
    
    if not aprobado:
        flash('Debes aprobar el examen del curso para obtener el certificado.', 'warning')
        return redirect(url_for('formacion.ver_curso', curso_id=curso_id))
        
    return render_template('formacion/certificado.html', curso=curso, usuario=current_user, fecha=aprobado.fecha_intento)
