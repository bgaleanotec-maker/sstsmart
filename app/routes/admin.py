from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import (
    CategoriaArea, Dependencia, RolSST, TipoReporte, 
    TipoEvidencia, MetodologiaInvestigacion,
    NivelRiesgo, MatrizRiesgos, GestorResponsabilidades, 
    ReglasEscalonamiento, PasoEscalonamiento
)
from functools import wraps
from app.routes import admin_bp

# Decorator para verificar si es admin
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.rol != 'Admin':
            flash('No tienes permiso para acceder', 'error')
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
        'gestores_configurados': GestorResponsabilidades.query.count()
    }
    return render_template('admin/dashboard.html', stats=stats)

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