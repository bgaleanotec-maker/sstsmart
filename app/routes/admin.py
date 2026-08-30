from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from flask import current_app
from datetime import datetime
from app import db
from app.models import (
    CategoriaArea, Dependencia, RolSST, TipoReporte, 
    TipoEvidencia, MetodologiaInvestigacion,
    NivelRiesgo, MatrizRiesgos, GestorResponsabilidades, 
    ReglasEscalonamiento, PasoEscalonamiento,
    Curso, Examen, Pregunta, Opcion, IntentoExamen, ProgresoFormacion,
    Usuario
)
from app.utils.notificaciones import NotificationService
from app.constants import ROL_ADMIN, ROLES_FORMACION_ADMIN, ROLES_TODOS
import string
import random
from functools import wraps
from app.routes import admin_bp

# Decorator para verificar si es admin
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.tiene_rol(ROL_ADMIN):
            flash('No tienes permiso para acceder', 'error')
            return redirect(url_for('reportes.listar'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator para Formación (Admin o Responsable SST)
def formacion_permission_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.tiene_rol(*ROLES_FORMACION_ADMIN):
            flash('No tienes permiso para gestionar formación', 'error')
            return redirect(url_for('reportes.listar'))
        return f(*args, **kwargs)
    return decorated_function

# ============== DASHBOARD ==============

@admin_bp.route('/', methods=['GET'])
@admin_required
def dashboard():
    stats = {
        'categorias': CategoriaArea.query.count(),
        'dependencias': Dependencia.query.count(),
        'tipos_reporte': TipoReporte.query.count(),
        'tipos_evidencia': TipoEvidencia.query.count(),
        'metodologias': MetodologiaInvestigacion.query.count(),
        'niveles_riesgo': NivelRiesgo.query.count(),
        'gestores_configurados': GestorResponsabilidades.query.count(),
        'cursos': Curso.query.count()
    }
    return render_template('admin/dashboard.html', stats=stats)

# ============== MANUAL DEL SISTEMA ==============

@admin_bp.route('/manual', methods=['GET'])
@admin_required
def ver_manual():
    return render_template('admin/manual.html')

@admin_bp.route('/manual/descargar', methods=['GET'])
@admin_required
def descargar_manual():
    # 1. Renderizar el template
    html_content = render_template('admin/manual.html')
    
    # 2. Leer estilos personalizados
    try:
        style_path = os.path.join(current_app.static_folder, 'css', 'style.css')
        with open(style_path, 'r', encoding='utf-8') as f:
            custom_css = f.read()
    except Exception as e:
        custom_css = "/* Error reading style.css */"

    # 3. Reemplazar Links con Inserciones Directas para funcionamiento Offline
    
    # Reemplazar Link a output.css con CDN de Tailwind + Config
    tailwind_cdn = """
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        slate: { 850: '#151f32' }
                    }
                }
            }
        }
    </script>
    """
    
    # Eliminar bloques existentes de CSS/Tailwind en base.html para evitar conflictos/404s
    # NOTA: Esto es un reemplazo simple de strings. Si el base.html cambia drásticamente, ajustar.
    
    # a. Quitar CDN actual si existe para ponerlo limpio o dejarlo si ya es CDN (en base.html lo es, pero aseguramos)
    # b. Quitar style.css link y poner style tag
    
    # Estrategia: Buscar el cierre de </head> e inyectar todo si no podemos hacer reemplazo fino
    # Pero el usuario reporta "fondo blanco", así que los estilos no cargan. 
    # Vamos a reemplazar las líneas específicas de base.html si las encontramos, o inyectar en head.
    
    # Reemplazo del link a style.css
    link_style_tag = '<link rel="stylesheet" href="/static/css/style.css">'
    style_injection = f'<style>\n{custom_css}\n</style>'
    
    # Ajuste por si url_for generó otra cosa (depende de deployment context, pero local es /static/...)
    if link_style_tag in html_content:
        html_content = html_content.replace(link_style_tag, style_injection)
    else:
        # Intento regex o simplemente append to head
        html_content = html_content.replace('</head>', f'{style_injection}\n</head>')

    # Asegurar Tailwind (base.html ya tiene CDN, pero si se descargó mal...)
    # Si base.html tiene <script src="https://cdn.tailwindcss.com"></script>, debería funcionar.
    # El problema 'fondo blanco' sugiere que el script no corrió o style.css falló.
    # Como style.css define variables --primary-bg, si falla, variables son undefined -> fallback white?
    # Sí. style.css define :root { --primary-bg: ... } y body { background-color: var(--primary-bg) }
    
    # CONCLUSIÓN: El fallo principal es style.css local (404). Inyectándolo arriba lo arregla.
    
    # Limpieza final de links rotos (opcional pero limpio)
    
    from flask import Response
    return Response(
        html_content,
        mimetype="text/html",
        headers={"Content-disposition": "attachment; filename=Manual_SST_Smart.html"}
    )

# ============== CATEGORÍAS DE ÁREAS ==============

@admin_bp.route('/categorias', methods=['GET'])
@admin_required
def listar_categorias():
    categorias = CategoriaArea.query.all()
    return render_template('admin/categorias/listar.html', categorias=categorias)

@admin_bp.route('/categorias/crear', methods=['GET', 'POST'])
@admin_required
def crear_categoria():
    if request.method == 'POST':
        categoria = CategoriaArea(
            nombre=request.form.get('nombre'),
            descripcion=request.form.get('descripcion'),
            icono=request.form.get('icono'),
            color=request.form.get('color', '#3b82f6')
        )
        db.session.add(categoria)
        db.session.commit()
        flash('Categoría creada exitosamente', 'success')
        return redirect(url_for('admin.listar_categorias'))
    return render_template('admin/categorias/crear.html')

@admin_bp.route('/categorias/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_categoria(id):
    categoria = CategoriaArea.query.get_or_404(id)
    if request.method == 'POST':
        categoria.nombre = request.form.get('nombre')
        categoria.descripcion = request.form.get('descripcion')
        categoria.icono = request.form.get('icono')
        categoria.color = request.form.get('color')
        categoria.activa = request.form.get('activa') == 'on'
        db.session.commit()
        flash('Categoría actualizada', 'success')
        return redirect(url_for('admin.listar_categorias'))
    return render_template('admin/categorias/editar.html', categoria=categoria)

@admin_bp.route('/categorias/<int:id>/eliminar', methods=['POST'])
@admin_required
def eliminar_categoria(id):
    categoria = CategoriaArea.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoría eliminada', 'success')
    return redirect(url_for('admin.listar_categorias'))

# ============== DEPENDENCIAS ==============

@admin_bp.route('/dependencias', methods=['GET'])
@admin_required
def listar_dependencias():
    dependencias = Dependencia.query.all()
    return render_template('admin/dependencias/listar.html', dependencias=dependencias)

@admin_bp.route('/dependencias/crear', methods=['GET', 'POST'])
@admin_required
def crear_dependencia():
    categorias = CategoriaArea.query.filter_by(activa=True).all()
    roles = RolSST.query.all()
    
    if request.method == 'POST':
        dependencia = Dependencia(
            nombre=request.form.get('nombre'),
            descripcion=request.form.get('descripcion'),
            direccion=request.form.get('direccion'),
            latitud=float(request.form.get('latitud', 0)) if request.form.get('latitud') else None,
            longitud=float(request.form.get('longitud', 0)) if request.form.get('longitud') else None,
            categoria_id=request.form.get('categoria_id')
        )
        
        roles_ids = request.form.getlist('roles')
        for rol_id in roles_ids:
            rol = RolSST.query.get(rol_id)
            if rol:
                dependencia.roles_vinculados.append(rol)
        
        db.session.add(dependencia)
        db.session.commit()
        flash('Dependencia creada exitosamente', 'success')
        return redirect(url_for('admin.listar_dependencias'))
    
    return render_template('admin/dependencias/crear.html', categorias=categorias, roles=roles)

@admin_bp.route('/dependencias/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_dependencia(id):
    dependencia = Dependencia.query.get_or_404(id)
    categorias = CategoriaArea.query.filter_by(activa=True).all()
    roles = RolSST.query.all()
    
    if request.method == 'POST':
        dependencia.nombre = request.form.get('nombre')
        dependencia.descripcion = request.form.get('descripcion')
        dependencia.direccion = request.form.get('direccion')
        dependencia.latitud = float(request.form.get('latitud', 0)) if request.form.get('latitud') else None
        dependencia.longitud = float(request.form.get('longitud', 0)) if request.form.get('longitud') else None
        dependencia.categoria_id = request.form.get('categoria_id')
        dependencia.activa = request.form.get('activa') == 'on'
        
        dependencia.roles_vinculados.clear()
        roles_ids = request.form.getlist('roles')
        for rol_id in roles_ids:
            rol = RolSST.query.get(rol_id)
            if rol:
                dependencia.roles_vinculados.append(rol)
        
        db.session.commit()
        flash('Dependencia actualizada', 'success')
        return redirect(url_for('admin.listar_dependencias'))
    
    return render_template('admin/dependencias/editar.html',
                         dependencia=dependencia,
                         categorias=categorias,
                         roles=roles)

@admin_bp.route('/dependencias/<int:id>/eliminar', methods=['POST'])
@admin_required
def eliminar_dependencia(id):
    dependencia = Dependencia.query.get_or_404(id)
    db.session.delete(dependencia)
    db.session.commit()
    flash('Dependencia eliminada', 'success')
    return redirect(url_for('admin.listar_dependencias'))

# ============== TIPOS DE REPORTE ==============

@admin_bp.route('/tipos-reporte', methods=['GET'])
@admin_required
def listar_tipos_reporte():
    tipos = TipoReporte.query.all()
    return render_template('admin/tipos_reporte/listar.html', tipos=tipos)

@admin_bp.route('/tipos-reporte/crear', methods=['GET', 'POST'])
@admin_required
def crear_tipo_reporte():
    if request.method == 'POST':
        tipo = TipoReporte(
            nombre=request.form.get('nombre'),
            descripcion=request.form.get('descripcion'),
            requiere_investigacion=request.form.get('requiere_investigacion') == 'on'
        )
        db.session.add(tipo)
        db.session.commit()
        flash('Tipo de reporte creado', 'success')
        return redirect(url_for('admin.listar_tipos_reporte'))
    return render_template('admin/tipos_reporte/crear.html')

@admin_bp.route('/tipos-reporte/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_tipo_reporte(id):
    tipo = TipoReporte.query.get_or_404(id)
    if request.method == 'POST':
        tipo.nombre = request.form.get('nombre')
        tipo.descripcion = request.form.get('descripcion')
        tipo.requiere_investigacion = request.form.get('requiere_investigacion') == 'on'
        tipo.activo = request.form.get('activo') == 'on'
        db.session.commit()
        flash('Tipo actualizado', 'success')
        return redirect(url_for('admin.listar_tipos_reporte'))
    return render_template('admin/tipos_reporte/editar.html', tipo=tipo)

# ============== TIPOS DE EVIDENCIA ==============

@admin_bp.route('/tipos-evidencia', methods=['GET'])
@admin_required
def listar_tipos_evidencia():
    tipos = TipoEvidencia.query.all()
    return render_template('admin/tipos_evidencia/listar.html', tipos=tipos)

@admin_bp.route('/tipos-evidencia/crear', methods=['GET', 'POST'])
@admin_required
def crear_tipo_evidencia():
    if request.method == 'POST':
        tipo = TipoEvidencia(
            nombre=request.form.get('nombre'),
            descripcion=request.form.get('descripcion'),
            codigo=request.form.get('codigo')
        )
        db.session.add(tipo)
        db.session.commit()
        flash('Tipo de evidencia creado', 'success')
        return redirect(url_for('admin.listar_tipos_evidencia'))
    return render_template('admin/tipos_evidencia/crear.html')

@admin_bp.route('/tipos-evidencia/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_tipo_evidencia(id):
    tipo = TipoEvidencia.query.get_or_404(id)
    if request.method == 'POST':
        tipo.nombre = request.form.get('nombre')
        tipo.descripcion = request.form.get('descripcion')
        tipo.codigo = request.form.get('codigo')
        tipo.activo = request.form.get('activo') == 'on'
        db.session.commit()
        flash('Tipo actualizado', 'success')
        return redirect(url_for('admin.listar_tipos_evidencia'))
    return render_template('admin/tipos_evidencia/editar.html', tipo=tipo)

# ============== METODOLOGÍAS ==============

@admin_bp.route('/metodologias', methods=['GET'])
@admin_required
def listar_metodologias():
    metodologias = MetodologiaInvestigacion.query.all()
    return render_template('admin/metodologias/listar.html', metodologias=metodologias)

@admin_bp.route('/metodologias/crear', methods=['GET', 'POST'])
@admin_required
def crear_metodologia():
    if request.method == 'POST':
        metodologia = MetodologiaInvestigacion(
            nombre=request.form.get('nombre'),
            descripcion=request.form.get('descripcion')
        )
        db.session.add(metodologia)
        db.session.commit()
        flash('Metodología creada', 'success')
        return redirect(url_for('admin.listar_metodologias'))
    return render_template('admin/metodologias/crear.html')

# ============== NIVELES DE RIESGO ==============

@admin_bp.route('/niveles-riesgo', methods=['GET'])
@admin_required
def listar_niveles_riesgo():
    niveles = NivelRiesgo.query.all()
    return render_template('admin/matriz/niveles_listar.html', niveles=niveles)

@admin_bp.route('/niveles-riesgo/crear', methods=['GET', 'POST'])
@admin_required
def crear_nivel_riesgo():
    if request.method == 'POST':
        nivel = NivelRiesgo(
            nombre=request.form.get('nombre'),
            descripcion=request.form.get('descripcion'),
            color=request.form.get('color', '#00FF00'),
            rango_minimo=int(request.form.get('rango_minimo', 0)),
            rango_maximo=int(request.form.get('rango_maximo', 0)),
            requiere_accion=request.form.get('requiere_accion') == 'on'
        )
        db.session.add(nivel)
        db.session.commit()
        flash('Nivel de riesgo creado', 'success')
        return redirect(url_for('admin.listar_niveles_riesgo'))
    
    return render_template('admin/matriz/nivel_crear.html')

# ============== MATRIZ DE RIESGOS ==============

@admin_bp.route('/matriz-riesgos', methods=['GET'])
@admin_required
def listar_matriz_riesgos():
    matriz = {}
    for p in range(1, 6):
        matriz[p] = {}
        for s in range(1, 6):
            celda = MatrizRiesgos.query.filter_by(
                probabilidad=p, severidad=s, activa=True
            ).first()
            matriz[p][s] = celda
    
    niveles_riesgo = NivelRiesgo.query.all()
    reglas = ReglasEscalonamiento.query.all()
    return render_template('admin/matriz/matriz_listar.html', matriz=matriz, niveles=niveles_riesgo, reglas=reglas)

@admin_bp.route('/matriz-riesgos/editar', methods=['POST'])
@admin_required
def editar_celda_matriz():
    data = request.get_json()
    p = data.get('probabilidad')
    s = data.get('severidad')
    nivel_riesgo_id = data.get('nivel_riesgo_id')
    regla_id = data.get('regla_id')
    
    celda = MatrizRiesgos.query.filter_by(probabilidad=p, severidad=s).first()
    
    if not celda:
        celda = MatrizRiesgos(
            probabilidad=p,
            severidad=s,
            valor_riesgo=p * s,
            activa=True
        )
        db.session.add(celda)
    
    celda.nivel_riesgo_id = nivel_riesgo_id if nivel_riesgo_id else None
    celda.regla_escalonamiento_id = regla_id if regla_id else None
    
    db.session.commit()
    
    return jsonify({'success': True, 'mensaje': 'Celda actualizada'})

# ============== GESTORES RESPONSABLES ==============

@admin_bp.route('/gestores-responsables', methods=['GET'])
@admin_required
def listar_gestores_responsables():
    gestores = GestorResponsabilidades.query.all()
    return render_template('admin/matriz/gestores_listar.html', gestores=gestores)

@admin_bp.route('/gestores-responsables/crear', methods=['GET', 'POST'])
@admin_required
def crear_gestor_responsable():
    if request.method == 'POST':
        gestor = GestorResponsabilidades(
            tipo_reporte_id=request.form.get('tipo_reporte_id') or None,
            nivel_riesgo_id=request.form.get('nivel_riesgo_id') or None,
            rol_principal=request.form.get('rol_principal'),
            rol_backup_1=request.form.get('rol_backup_1') or None,
            rol_backup_2=request.form.get('rol_backup_2') or None,
            departamento=request.form.get('departamento') or None,
            tiempo_respuesta_minutos=int(request.form.get('tiempo_respuesta_minutos', 30)),
            tiempo_resolucion_minutos=int(request.form.get('tiempo_resolucion_minutos', 1440))
        )
        
        notificar_roles = request.form.getlist('notificar_roles')
        gestor.notificar_roles = notificar_roles if notificar_roles else None
        
        db.session.add(gestor)
        db.session.commit()
        flash('Gestor configurado', 'success')
        return redirect(url_for('admin.listar_gestores_responsables'))
    
    tipos_reporte = TipoReporte.query.all()
    niveles_riesgo = NivelRiesgo.query.all()
    roles = RolSST.query.all()
    
    return render_template('admin/matriz/gestor_crear.html',
                         tipos_reporte=tipos_reporte,
                         niveles_riesgo=niveles_riesgo,
                         roles=roles)

@admin_bp.route('/gestores-responsables/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_gestor_responsable(id):
    gestor = GestorResponsabilidades.query.get_or_404(id)
    
    if request.method == 'POST':
        gestor.tipo_reporte_id = request.form.get('tipo_reporte_id') or None
        gestor.nivel_riesgo_id = request.form.get('nivel_riesgo_id') or None
        gestor.rol_principal = request.form.get('rol_principal')
        gestor.rol_backup_1 = request.form.get('rol_backup_1') or None
        gestor.rol_backup_2 = request.form.get('rol_backup_2') or None
        gestor.tiempo_respuesta_minutos = int(request.form.get('tiempo_respuesta_minutos', 30))
        gestor.tiempo_resolucion_minutos = int(request.form.get('tiempo_resolucion_minutos', 1440))
        
        notificar_roles = request.form.getlist('notificar_roles')
        gestor.notificar_roles = notificar_roles if notificar_roles else None
        
        gestor.activo = request.form.get('activo') == 'on'
        
        db.session.commit()
        flash('Gestor actualizado', 'success')
        return redirect(url_for('admin.listar_gestores_responsables'))
    
    tipos_reporte = TipoReporte.query.all()
    niveles_riesgo = NivelRiesgo.query.all()
    roles = RolSST.query.all()
    
    return render_template('admin/matriz/gestor_editar.html',
                         gestor=gestor,
                         tipos_reporte=tipos_reporte,
                         niveles_riesgo=niveles_riesgo,
                         roles=roles)

# ============== REGLAS DE ESCALONAMIENTO ==============

@admin_bp.route('/reglas-escalonamiento', methods=['GET'])
@admin_required
def listar_reglas_escalonamiento():
    reglas = ReglasEscalonamiento.query.all()
    return render_template('admin/matriz/reglas_listar.html', reglas=reglas)

@admin_bp.route('/reglas-escalonamiento/crear', methods=['GET', 'POST'])
@admin_required
def crear_regla_escalonamiento():
    if request.method == 'POST':
        regla = ReglasEscalonamiento(
            nombre=request.form.get('nombre'),
            descripcion=request.form.get('descripcion'),
            nivel_riesgo_minimo=int(request.form.get('nivel_riesgo_minimo', 1)),
            nivel_riesgo_maximo=int(request.form.get('nivel_riesgo_maximo', 25)),
            tiempo_respuesta_minutos=int(request.form.get('tiempo_respuesta_minutos', 30)),
            tiempo_resolucion_minutos=int(request.form.get('tiempo_resolucion_minutos', 1440))
        )
        
        db.session.add(regla)
        db.session.flush()
        
        num_pasos = int(request.form.get('num_pasos', 0))
        for i in range(1, num_pasos + 1):
            paso = PasoEscalonamiento(
                regla_id=regla.id,
                numero_paso=i,
                descripcion=request.form.get(f'paso_{i}_descripcion'),
                rol_destino=request.form.get(f'paso_{i}_rol'),
                minutos_delay=int(request.form.get(f'paso_{i}_minutos', 30))
            )
            db.session.add(paso)
        
        db.session.commit()
        flash('Regla de escalonamiento creada', 'success')
        return redirect(url_for('admin.listar_reglas_escalonamiento'))
    
    roles = RolSST.query.all()
    return render_template('admin/matriz/regla_crear.html', roles=roles)

# ============== API ==============

@admin_bp.route('/api/dependencias', methods=['GET'])
@login_required
def api_dependencias():
    dependencias = Dependencia.query.filter_by(activa=True).all()
    return jsonify([{
        'id': d.id,
        'nombre': d.nombre,
        'categoria': d.categoria.nombre if d.categoria else '',
        'latitud': d.latitud,
        'longitud': d.longitud
    } for d in dependencias])



# ============== EDITAR Y ELIMINAR REGLAS ==============

@admin_bp.route('/reglas-escalonamiento/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_regla_escalonamiento(id):
    regla = ReglasEscalonamiento.query.get_or_404(id)
    
    if request.method == 'POST':
        regla.nombre = request.form.get('nombre')
        regla.descripcion = request.form.get('descripcion')
        regla.nivel_riesgo_minimo = int(request.form.get('nivel_riesgo_minimo', 1))
        regla.nivel_riesgo_maximo = int(request.form.get('nivel_riesgo_maximo', 25))
        regla.tiempo_respuesta_minutos = int(request.form.get('tiempo_respuesta_minutos', 30))
        regla.tiempo_resolucion_minutos = int(request.form.get('tiempo_resolucion_minutos', 1440))
        
        # Eliminar pasos anteriores
        PasoEscalonamiento.query.filter_by(regla_id=regla.id).delete()
        
        # Crear nuevos pasos
        num_pasos = int(request.form.get('num_pasos', 0))
        for i in range(1, num_pasos + 1):
            paso = PasoEscalonamiento(
                regla_id=regla.id,
                numero_paso=i,
                descripcion=request.form.get(f'paso_{i}_descripcion'),
                rol_destino=request.form.get(f'paso_{i}_rol'),
                minutos_delay=int(request.form.get(f'paso_{i}_minutos', 30))
            )
            db.session.add(paso)
        
        regla.activo = request.form.get('activo') == 'on'
        
        db.session.commit()
        flash('Regla actualizada', 'success')
        return redirect(url_for('admin.listar_reglas_escalonamiento'))
    
    roles = RolSST.query.all()
    return render_template('admin/matriz/regla_editar.html', regla=regla, roles=roles)

@admin_bp.route('/reglas-escalonamiento/<int:id>/eliminar', methods=['POST'])
@admin_required
def eliminar_regla_escalonamiento(id):
    regla = ReglasEscalonamiento.query.get_or_404(id)
    db.session.delete(regla)
    db.session.commit()
    flash('Regla eliminada', 'success')
    return redirect(url_for('admin.listar_reglas_escalonamiento'))

# ============== NOTIFICACIONES DE PRUEBA ==============

@admin_bp.route('/usuarios/prueba-notificacion', methods=['GET', 'POST'])
@admin_required
def prueba_notificacion():
    if request.method == 'POST':
        email_destino = request.form.get('email')
        subject = "Prueba de Integración SendGrid - SST Smart"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; color: #333; border: 1px solid #ddd; border-radius: 8px;">
            <h2 style="color: #10b981;">✅ Prueba Exitosa</h2>
            <p>Este es un correo de prueba enviado desde el sistema <strong>SST Smart Solutions</strong>.</p>
            <p>Si estás leyendo esto, la integración con SendGrid está funcionando correctamente.</p>
            <hr>
            <p style="font-size: 12px; color: #666;">Fecha: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """
        
        exito = NotificationService.enviar_email(email_destino, subject, html_content)
        
        if exito:
            flash(f'Correo de prueba enviado a {email_destino}', 'success')
        else:
            flash('Error al enviar el correo. Revisa los logs o la consola.', 'error')
            
        return redirect(url_for('admin.prueba_notificacion'))

    return render_template('admin/usuarios/prueba_notificacion.html')















@admin_bp.route('/api/dependencias/<int:id>', methods=['GET'])
@login_required
def api_dependencia_detail(id):
    dependencia = Dependencia.query.get_or_404(id)
    return jsonify({
        'id': dependencia.id,
        'nombre': dependencia.nombre,
        'direccion': dependencia.direccion,
        'latitud': dependencia.latitud,
        'longitud': dependencia.longitud
    })




# ============== GESTIÓN DE FORMACIÓN (ADMIN) ==============

@admin_bp.route('/formacion/cursos', methods=['GET'])
@formacion_permission_required
def listar_cursos():
    cursos = Curso.query.all()
    return render_template('admin/formacion/listar_cursos.html', cursos=cursos)

@admin_bp.route('/formacion/curso/nuevo', methods=['GET', 'POST'])
@formacion_permission_required
def crear_curso():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        contenido_html = request.form.get('contenido_html')
        duracion_horas = request.form.get('duracion_horas')
        video_url = request.form.get('video_url')
        
        # Nuevos campos
        categoria = request.form.get('categoria')
        tipo_contenido = request.form.get('tipo_contenido') # video/pdf
        
        # --- LOGICA DE ARCHIVOS ---
        import time
        def save_file(file, subdir):
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                # Timestamp prevent overwrites
                filename = f"{int(time.time())}_{filename}"
                path = os.path.join(current_app.config['UPLOAD_FOLDER'], subdir)
                os.makedirs(path, exist_ok=True)
                file.save(os.path.join(path, filename))
                return url_for('static', filename=f'uploads/{subdir}/{filename}')
            return None

        # 1. Imagen Portada (Prioridad: Archivo > URL input)
        imagen_file = request.files.get('imagen_file')
        imagen_portada = request.form.get('imagen_portada')  # campo URL (fallback)
        if imagen_file:
            uploaded_img = save_file(imagen_file, 'cursos/imagenes')
            if uploaded_img:
                imagen_portada = uploaded_img

        # 2. PDF (Prioridad: Archivo > URL input)
        pdf_file = request.files.get('pdf_file')
        pdf_url_input = request.form.get('pdf_url')
        if pdf_file:
            uploaded_pdf = save_file(pdf_file, 'cursos/docs')
            if uploaded_pdf:
                pdf_url = uploaded_pdf
            else:
                pdf_url = pdf_url_input
        else:
             pdf_url = pdf_url_input

        # 3. Video (Prioridad: Archivo > URL input)
        video_file = request.files.get('video_file')
        video_url_input = request.form.get('video_url')
        
        if video_file:
            uploaded_video = save_file(video_file, 'cursos/videos')
            if uploaded_video:
                video_url = uploaded_video
            else:
                video_url = video_url_input
        else:
            video_url = video_url_input

        # Validación básica
        if tipo_contenido == 'video' and not video_url:
            flash('Debes proporcionar una URL de video o subir un archivo MP4.', 'error')
            return redirect(request.url)

        nuevo_curso = Curso(
            titulo=titulo,
            descripcion=descripcion,
            contenido_html=contenido_html,
            duracion_horas=duracion_horas,
            video_url=video_url,
            categoria=categoria,
            tipo_contenido=tipo_contenido,
            imagen_portada=imagen_portada,
            pdf_url=pdf_url
        )
        db.session.add(nuevo_curso)
        db.session.commit()
        flash('Curso creado exitosamente.', 'success')
        return redirect(url_for('admin.listar_cursos'))
    return render_template('admin/formacion/crear_curso.html')

@admin_bp.route('/formacion/curso/<int:curso_id>/examen', methods=['GET', 'POST'])
@formacion_permission_required
def gestionar_examen(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    examen = Examen.query.filter_by(curso_id=curso.id).first()
    
    if request.method == 'POST':
        if not examen:
            examen = Examen(
                curso_id=curso.id,
                titulo=f"Examen Final - {curso.titulo}",
                porcentaje_aprobacion=int(request.form.get('porcentaje_aprobacion', 70))
            )
            db.session.add(examen)
        else:
            examen.porcentaje_aprobacion = int(request.form.get('porcentaje_aprobacion', 70))
        
        db.session.commit()
        
        # Agregar pregunta si viene en el form
        texto_pregunta = request.form.get('nueva_pregunta')
        if texto_pregunta:
            pregunta = Pregunta(
                examen_id=examen.id,
                texto_pregunta=texto_pregunta,
                puntaje=int(request.form.get('puntaje_pregunta', 10))
            )
            db.session.add(pregunta)
            db.session.flush() # Para tener el ID de la pregunta
            
            # Opciones
            correcta_idx = request.form.get('opcion_correcta')
            for i in range(1, 5):
                texto_opcion = request.form.get(f'opcion_{i}')
                if texto_opcion:
                    opcion = Opcion(
                        pregunta_id=pregunta.id,
                        texto_opcion=texto_opcion,
                        es_correcta=(str(i) == correcta_idx)
                    )
                    db.session.add(opcion)
            
            db.session.commit()
            flash('Pregunta agregada correctamente.', 'success')
            
        return redirect(url_for('admin.gestionar_examen', curso_id=curso.id))

    return render_template('admin/formacion/gestionar_examen.html', curso=curso, examen=examen)

@admin_bp.route('/formacion/dashboard', methods=['GET'])
@formacion_permission_required
def dashboard_formacion():
    # 1. KPIs Generales
    total_empleados = Usuario.query.count() # O filtrar por rol 'Usuario'
    total_cursos = Curso.query.filter_by(estado='Activo').count()
    
    # Progreso promedio
    progresos = ProgresoFormacion.query.all()
    avg_score = sum([p.puntaje_global_sst for p in progresos]) / len(progresos) if progresos else 0
    
    # 2. Ranking de Empleados
    ranking = db.session.query(Usuario, ProgresoFormacion).join(ProgresoFormacion, Usuario.id == ProgresoFormacion.usuario_id).order_by(ProgresoFormacion.puntaje_global_sst.desc()).limit(10).all()
    
    # 3. Detalle por Curso (Aprobación)
    cursos_stats = []
    cursos = Curso.query.all()
    for curso in cursos:
        # Contar intentos aprobados únicos para este curso
        aprobados = IntentoExamen.query.join(Examen).filter(Examen.curso_id == curso.id, IntentoExamen.aprobado == True).with_entities(IntentoExamen.usuario_id).distinct().count()
        tasa = (aprobados / total_empleados * 100) if total_empleados > 0 else 0
        cursos_stats.append({
            'titulo': curso.titulo,
            'aprobados': aprobados,
            'tasa': round(tasa, 1)
        })
        
    return render_template('admin/formacion/dashboard.html', 
                         total_empleados=total_empleados,
                         total_cursos=total_cursos,
                         avg_score=round(avg_score, 1),
                         ranking=ranking,
                         cursos_stats=cursos_stats)

@admin_bp.route('/formacion/pregunta/eliminar/<int:pregunta_id>', methods=['POST'])
@formacion_permission_required
def eliminar_pregunta(pregunta_id):
    pregunta = Pregunta.query.get_or_404(pregunta_id)
    curso_id = pregunta.examen.curso_id
    db.session.delete(pregunta)
    db.session.commit()
    flash('Pregunta eliminada.', 'success')
    return redirect(url_for('admin.gestionar_examen', curso_id=curso_id))

# ============== GESTIÓN AVANZADA DE CURSOS ==============

@admin_bp.route('/formacion/curso/<int:id>/eliminar', methods=['POST'])
@formacion_permission_required
def eliminar_curso(id):
    curso = Curso.query.get_or_404(id)
    # Verificar si tiene historial importante (opcional, por ahora permitimos borrar)
    db.session.delete(curso)
    db.session.commit()
    flash('Curso eliminado correctamente.', 'success')
    return redirect(url_for('admin.listar_cursos'))

@admin_bp.route('/formacion/curso/<int:id>/toggle-estado', methods=['POST'])
@formacion_permission_required
def toggle_estado_curso(id):
    curso = Curso.query.get_or_404(id)
    if curso.estado == 'Activo':
        curso.estado = 'Inactivo'
    else:
        curso.estado = 'Activo'
    db.session.commit()
    return jsonify({'success': True, 'nuevo_estado': curso.estado})

@admin_bp.route('/formacion/curso/<int:id>/matriculas', methods=['GET'])
@formacion_permission_required
def gestionar_matriculas(id):
    curso = Curso.query.get_or_404(id)
    usuarios = Usuario.query.filter_by(activo=True).all()
    matriculados_ids = [u.id for u in curso.estudiantes]
    
    return render_template('admin/formacion/gestion_matriculas.html', 
                         curso=curso, 
                         usuarios=usuarios, 
                         matriculados_ids=matriculados_ids)

@admin_bp.route('/formacion/curso/<int:id>/matricular', methods=['POST'])
@formacion_permission_required
def matricular_usuario(id):
    curso = Curso.query.get_or_404(id)
    usuario_id = int(request.form.get('usuario_id'))
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if usuario not in curso.estudiantes:
        curso.estudiantes.append(usuario)
        db.session.commit()
        flash(f'Usuario {usuario.nombre_completo} matriculado.', 'success')
    
    return redirect(url_for('admin.gestionar_matriculas', id=curso.id))

@admin_bp.route('/formacion/curso/<int:id>/desmatricular', methods=['POST'])
@formacion_permission_required
def desmatricular_usuario(id):
    curso = Curso.query.get_or_404(id)
    usuario_id = int(request.form.get('usuario_id'))
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if usuario in curso.estudiantes:
        curso.estudiantes.remove(usuario)
        db.session.commit()
        flash(f'Usuario {usuario.nombre_completo} retirado.', 'warning')
        
    return redirect(url_for('admin.gestionar_matriculas', id=curso.id))

# ============== GESTIÓN DE USUARIOS (ADMIN) ==============

@admin_bp.route('/usuarios', methods=['GET'])
@admin_required
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('admin/usuarios/listar.html', usuarios=usuarios)

@admin_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
@admin_required
def crear_usuario():
    if request.method == 'POST':
        nombre_completo = request.form.get('nombre_completo')
        email = request.form.get('email')
        rol = request.form.get('rol')
        
        # Verificar email duplicado
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado.', 'error')
            return redirect(url_for('admin.crear_usuario'))
            
        # Generar Contraseña Aleatoria (8 chars)
        chars = string.ascii_letters + string.digits
        password = ''.join(random.choice(chars) for i in range(10))
        
        # Crear Usuario
        nuevo_usuario = Usuario(
            nombre_completo=nombre_completo,
            email=email,
            rol=rol,
            activo=True
        )
        nuevo_usuario.set_password(password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        # Enviar Credenciales por Email
        subject = "Bienvenido a SST Smart System - Tus Credenciales"
        html_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
            <h2 style="color: #2563eb;">Bienvenido, {nombre_completo}</h2>
            <p>Se ha creado tu cuenta en el sistema de Gestión SST.</p>
            <p><strong>Rol Asignado:</strong> {rol}</p>
            <div style="background: #f1f5f9; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p style="margin: 0; font-weight: bold;">Tus Credenciales:</p>
                <p style="margin: 5px 0;">Usuario: {email}</p>
                <p style="margin: 5px 0;">Contraseña: <span style="font-family: monospace; font-size: 1.2em; color: #dc2626;">{password}</span></p>
            </div>
            <p>Por favor, ingresa al sistema y cambia tu contraseña lo antes posible.</p>
            <a href="{url_for('auth.login', _external=True)}" style="background:#2563eb;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">Iniciar Sesión</a>
        </div>
        """
        
        email_enviado = NotificationService.enviar_email(email, subject, html_content)
        NotificationService.notificar_usuario(nuevo_usuario.id, "Bienvenido al sistema. Revisa tu correo para ver tus credenciales.", "success")
        
        if email_enviado:
            flash(f'Usuario creado. Contraseña enviada a {email}.', 'success')
        else:
            flash(f'Usuario creado, pero hubo un error enviando el correo a {email}.', 'warning')
        
        return redirect(url_for('admin.listar_usuarios'))
        
    roles = ROLES_TODOS
    return render_template('admin/usuarios/crear.html', roles=roles)

@admin_bp.route('/usuarios/<int:user_id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_usuario(user_id):
    usuario = Usuario.query.get_or_404(user_id)
    if request.method == 'POST':
        usuario.nombre_completo = request.form.get('nombre_completo')
        usuario.email = request.form.get('email')
        usuario.rol = request.form.get('rol')
        usuario.activo = 'activo' in request.form
        
        db.session.commit()
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('admin.listar_usuarios'))
        
    roles = ROLES_TODOS
    return render_template('admin/usuarios/editar.html', usuario=usuario, roles=roles)

# Fin del archivo admin.py