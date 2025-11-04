"""
Rutas para gestionar Controles SST
Decreto 1072/2015 - Resolución 0312/2019

Sistema de permisos por rol:
- Admin, Responsable SST, Abogado, Gerente Area: Crear/Editar/Asignar
- Responsable de Control: Implementar/Carga evidencia
- Auditor: Ver/Verificar
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Control, SeguimientoControl, RiesgoMatriz, Usuario
from app.models.control import TipoControl, NivelControl, EstadoControl
from datetime import datetime
from functools import wraps
import logging

logger = logging.getLogger(__name__)

controles_bp = Blueprint('controles', __name__, url_prefix='/controles')

# ============== DECORADOR DE PERMISOS ==============

def require_role(*roles):
    """Decorador que verifica si el usuario tiene uno de los roles requeridos"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Obtener el rol del usuario actual (es string, no objeto)
            user_role = current_user.rol if hasattr(current_user, 'rol') and current_user.rol else None
            
            if user_role not in roles:
                flash(f'❌ No tienes permiso para esta acción. Roles requeridos: {", ".join(roles)}', 'error')
                logger.warning(f"⚠️ Acceso denegado a {current_user.nombre_completo} ({user_role}). Se requería: {roles}")
                return redirect(url_for('dashboard.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ============== LISTAR CONTROLES ==============

@controles_bp.route('/', methods=['GET'])
@login_required
def listar_controles():
    """Lista controles según rol del usuario"""
    
    user_role = current_user.rol if hasattr(current_user, 'rol') and current_user.rol else None
    filtro_estado = request.args.get('estado', '')
    filtro_riesgo = request.args.get('riesgo_id', '')
    
    query = Control.query.filter_by(activo=True)
    
    # Filtrar según rol
    if user_role not in ['Admin', 'Responsable SST', 'Abogado']:
        # Responsable de Control solo ve los asignados a él
        query = query.filter_by(responsable_id=current_user.id)
    
    # Aplicar filtros adicionales
    if filtro_estado:
        query = query.filter_by(estado=filtro_estado)
    if filtro_riesgo:
        query = query.filter_by(riesgo_id=filtro_riesgo)
    
    controles = query.all()
    estados = [e.value for e in EstadoControl]
    riesgos = RiesgoMatriz.query.all()
    
    return render_template('controles/listar.html', 
                         controles=controles, 
                         estados=estados,
                         riesgos=riesgos,
                         filtro_estado=filtro_estado,
                         filtro_riesgo=filtro_riesgo,
                         user_role=user_role)


# ============== MIS CONTROLES - Dashboard Personal ==============

@controles_bp.route('/mis-controles', methods=['GET'])
@login_required
def mis_controles():
    """Muestra controles según el rol del usuario"""
    
    user_role = current_user.rol if hasattr(current_user, 'rol') and current_user.rol else None
    
    if user_role in ['Admin', 'Responsable SST', 'Abogado']:
        # Estos roles ven TODOS los controles (para gestión)
        controles_asignados = Control.query.filter_by(activo=True).all()
        controles_creados = Control.query.filter(
            Control.creado_por == current_user.id,
            Control.activo == True
        ).all()
    else:
        # Responsable de Control ve SOLO los asignados a él
        controles_asignados = Control.query.filter_by(
            responsable_id=current_user.id,
            activo=True
        ).all()
        controles_creados = []
    
    # Agrupar por estado
    por_estado = {}
    for control in controles_asignados:
        estado = control.estado
        if estado not in por_estado:
            por_estado[estado] = []
        por_estado[estado].append(control)
    
    return render_template('controles/mis_controles.html',
                         controles_asignados=controles_asignados,
                         controles_creados=controles_creados,
                         por_estado=por_estado,
                         user_role=user_role)


# ============== CREAR CONTROL ==============

@controles_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@require_role('Admin', 'Responsable SST', 'Abogado', 'Gerente Area')
def crear_control():
    """Crea un nuevo control - Múltiples roles autorizados"""
    
    riesgo_id = request.args.get('riesgo_id')
    
    if request.method == 'POST':
        try:
            # Generar código único
            ultimo_control = Control.query.order_by(Control.id.desc()).first()
            numero = (ultimo_control.id + 1) if ultimo_control else 1
            codigo = f"CTL-{numero:03d}-{datetime.utcnow().year}"
            
            riesgo_id_form = request.form.get('riesgo_id')
            responsable_id = request.form.get('responsable_id')
            
            control = Control(
                codigo=codigo,
                nombre=request.form.get('nombre'),
                descripcion=request.form.get('descripcion'),
                tipo_control=request.form.get('tipo_control', TipoControl.PREVENTIVO.value),
                nivel_control=request.form.get('nivel_control', NivelControl.FUENTE.value),
                riesgo_id=int(riesgo_id_form) if riesgo_id_form else None,
                responsable_id=int(responsable_id) if responsable_id else current_user.id,
                creado_por=current_user.id,
                creado_por_rol=current_user.rol if hasattr(current_user, 'rol') else 'Desconocido',
                fecha_planeada=datetime.fromisoformat(request.form.get('fecha_planeada')) if request.form.get('fecha_planeada') else None,
                presupuesto_estimado=float(request.form.get('presupuesto_estimado', 0)) if request.form.get('presupuesto_estimado') else None,
                requiere_seguimiento_periodico=request.form.get('requiere_seguimiento') == 'on',
                frecuencia_seguimiento_dias=int(request.form.get('frecuencia_seguimiento', 30)) if request.form.get('frecuencia_seguimiento') else 30,
                estado=EstadoControl.PLANIFICADO.value
            )
            
            db.session.add(control)
            db.session.commit()
            
            logger.info(f"✅ Control {codigo} creado por {current_user.nombre_completo} ({current_user.rol})")
            flash(f'✅ Control "{control.nombre}" creado exitosamente', 'success')
            return redirect(url_for('controles.listar_controles'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ Error creando control: {str(e)}", exc_info=True)
            flash(f'❌ Error al crear control: {str(e)}', 'error')
            return redirect(request.referrer or url_for('controles.listar_controles'))
    
    usuarios = Usuario.query.filter_by(activo=True).all()
    tipos = [t.value for t in TipoControl]
    niveles = [n.value for n in NivelControl]
    riesgos = RiesgoMatriz.query.filter_by(activo=True).all()
    
    return render_template('controles/crear.html',
                         usuarios=usuarios,
                         tipos=tipos,
                         niveles=niveles,
                         riesgos=riesgos,
                         riesgo_id_param=riesgo_id)


# ============== EDITAR CONTROL ==============

@controles_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@require_role('Admin', 'Responsable SST', 'Abogado', 'Gerente Area')
def editar_control(id):
    """Edita un control existente"""
    
    control = Control.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            control.nombre = request.form.get('nombre')
            control.descripcion = request.form.get('descripcion')
            control.tipo_control = request.form.get('tipo_control')
            control.nivel_control = request.form.get('nivel_control')
            control.responsable_id = request.form.get('responsable_id')
            control.fecha_planeada = datetime.fromisoformat(request.form.get('fecha_planeada')) if request.form.get('fecha_planeada') else None
            control.presupuesto_estimado = float(request.form.get('presupuesto_estimado')) if request.form.get('presupuesto_estimado') else None
            control.requiere_seguimiento_periodico = request.form.get('requiere_seguimiento') == 'on'
            control.frecuencia_seguimiento_dias = int(request.form.get('frecuencia_seguimiento', 30))
            control.actualizado_en = datetime.utcnow()
            
            db.session.commit()
            logger.info(f"✅ Control {control.codigo} actualizado por {current_user.nombre_completo}")
            flash('✅ Control actualizado exitosamente', 'success')
            return redirect(url_for('controles.listar_controles'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ Error editando control: {str(e)}", exc_info=True)
            flash(f'❌ Error al editar control: {str(e)}', 'error')
            return redirect(request.referrer or url_for('controles.listar_controles'))
    
    usuarios = Usuario.query.filter_by(activo=True).all()
    tipos = [t.value for t in TipoControl]
    niveles = [n.value for n in NivelControl]
    
    return render_template('controles/editar.html',
                         control=control,
                         usuarios=usuarios,
                         tipos=tipos,
                         niveles=niveles)


# ============== ASIGNAR RESPONSABLE ==============

@controles_bp.route('/<int:id>/asignar-responsable', methods=['POST'])
@login_required
@require_role('Admin', 'Responsable SST', 'Abogado', 'Gerente Area')
def asignar_responsable(id):
    """Asigna responsable a un control"""
    
    control = Control.query.get_or_404(id)
    
    try:
        nuevo_responsable_id = request.form.get('responsable_id')
        fecha_planeada = request.form.get('fecha_planeada')
        
        control.responsable_id = int(nuevo_responsable_id)
        if fecha_planeada:
            control.fecha_planeada = datetime.fromisoformat(fecha_planeada)
        
        control.estado = EstadoControl.ASIGNADO.value
        db.session.commit()
        
        logger.info(f"✅ Control {control.codigo} asignado a responsable_id {control.responsable_id} por {current_user.nombre_completo}")
        flash('✅ Responsable asignado exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error asignando responsable: {str(e)}", exc_info=True)
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(request.referrer or url_for('controles.listar_controles'))


# ============== MARCAR IMPLEMENTADO ==============

@controles_bp.route('/<int:id>/implementado', methods=['POST'])
@login_required
def marcar_implementado(id):
    """Marca un control como implementado - Solo responsable asignado o gestores"""
    
    control = Control.query.get_or_404(id)
    user_role = current_user.rol if hasattr(current_user, 'rol') and current_user.rol else None
    
    # Verificar permisos
    if control.responsable_id != current_user.id and user_role not in ['Admin', 'Responsable SST', 'Abogado']:
        flash('❌ No tienes permiso para marcar este control como implementado', 'error')
        return redirect(request.referrer or url_for('controles.listar_controles'))
    
    try:
        evidencia = request.form.get('evidencia', '')
        control.evidencia_implementacion = evidencia
        control.estado = EstadoControl.IMPLEMENTADO.value
        control.fecha_verificacion = None
        
        db.session.commit()
        
        logger.info(f"✅ Control {control.codigo} marcado como implementado por {current_user.nombre_completo}")
        flash('✅ Control marcado como implementado', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(request.referrer or url_for('controles.listar_controles'))


# ============== VERIFICAR CONTROL ==============

@controles_bp.route('/<int:id>/verificar', methods=['POST'])
@login_required
@require_role('Admin', 'Responsable SST', 'Abogado', 'Auditor')
def verificar_control(id):
    """Verifica un control implementado - Gestores y auditores"""
    
    control = Control.query.get_or_404(id)
    
    try:
        efectividad = int(request.form.get('efectividad', 100))
        observaciones = request.form.get('observaciones', '')
        
        control.efectividad_porcentaje = efectividad
        control.estado = EstadoControl.VERIFICADO.value
        control.fecha_verificacion = datetime.utcnow()
        control.ultima_revision = datetime.utcnow()
        
        db.session.commit()
        
        logger.info(f"✅ Control {control.codigo} verificado con {efectividad}% efectividad por {current_user.nombre_completo}")
        flash(f'✅ Control verificado con {efectividad}% efectividad', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(request.referrer or url_for('controles.listar_controles'))


# ============== AGREGAR SEGUIMIENTO ==============

@controles_bp.route('/<int:id>/seguimiento', methods=['POST'])
@login_required
@require_role('Admin', 'Responsable SST', 'Abogado', 'Auditor')
def agregar_seguimiento(id):
    """Agrega un seguimiento periódico a un control"""
    
    control = Control.query.get_or_404(id)
    
    try:
        seguimiento = SeguimientoControl(
            control_id=id,
            responsable_revision_id=current_user.id,
            sigue_vigente=request.form.get('sigue_vigente') == 'on',
            efectividad_actual=int(request.form.get('efectividad_actual', control.efectividad_porcentaje or 100)),
            observaciones=request.form.get('observaciones'),
            requiere_ajustes=request.form.get('requiere_ajustes') == 'on',
            ajustes_recomendados=request.form.get('ajustes_recomendados')
        )
        
        db.session.add(seguimiento)
        control.ultima_revision = datetime.utcnow()
        
        if seguimiento.requiere_ajustes:
            control.estado = EstadoControl.REQUIERE_AJUSTE.value
        
        db.session.commit()
        
        logger.info(f"✅ Seguimiento agregado a control {control.codigo} por {current_user.nombre_completo}")
        flash('✅ Seguimiento registrado exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(request.referrer or url_for('controles.listar_controles'))


# ============== CERRAR CONTROL ==============

@controles_bp.route('/<int:id>/cerrar', methods=['POST'])
@login_required
@require_role('Admin', 'Responsable SST', 'Abogado')
def cerrar_control(id):
    """Cierra un control"""
    
    control = Control.query.get_or_404(id)
    
    try:
        control.estado = EstadoControl.CERRADO.value
        control.fecha_cierre = datetime.utcnow()
        control.activo = False
        
        db.session.commit()
        
        logger.info(f"✅ Control {control.codigo} cerrado por {current_user.nombre_completo}")
        flash('✅ Control cerrado exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(request.referrer or url_for('controles.listar_controles'))


# ============== ELIMINAR (DESACTIVAR) CONTROL ==============

@controles_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@require_role('Admin', 'Responsable SST', 'Abogado')
def eliminar_control(id):
    """Desactiva un control (eliminación lógica)"""
    
    control = Control.query.get_or_404(id)
    
    try:
        control.activo = False
        db.session.commit()
        
        logger.info(f"✅ Control {control.codigo} desactivado por {current_user.nombre_completo}")
        flash('✅ Control eliminado exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(url_for('controles.listar_controles'))


# ============== APIS ==============

@controles_bp.route('/api/riesgo/<int:riesgo_id>', methods=['GET'])
@login_required
def api_controles_riesgo(riesgo_id):
    """API: Obtiene controles de un riesgo específico"""
    
    controles = Control.query.filter_by(riesgo_id=riesgo_id, activo=True).all()
    
    return jsonify([{
        'id': c.id,
        'codigo': c.codigo,
        'nombre': c.nombre,
        'tipo': c.tipo_control,
        'nivel': c.nivel_control,
        'estado': c.estado,
        'efectividad': c.efectividad_porcentaje or 0
    } for c in controles])


@controles_bp.route('/api/usuario/<int:usuario_id>', methods=['GET'])
@login_required
def api_controles_usuario(usuario_id):
    """API: Obtiene controles asignados a un usuario"""
    
    controles = Control.query.filter_by(responsable_id=usuario_id, activo=True).all()
    
    return jsonify([{
        'id': c.id,
        'codigo': c.codigo,
        'nombre': c.nombre,
        'riesgo': c.riesgo.nombre_riesgo if c.riesgo else 'N/A',
        'estado': c.estado,
        'fecha_planeada': c.fecha_planeada.isoformat() if c.fecha_planeada else None
    } for c in controles])


@controles_bp.route('/api/estadisticas', methods=['GET'])
@login_required
def api_estadisticas():
    """API: Estadísticas de controles"""
    
    total = Control.query.filter_by(activo=True).count()
    por_estado = {}
    
    for estado in EstadoControl:
        cantidad = Control.query.filter_by(estado=estado.value, activo=True).count()
        por_estado[estado.value] = cantidad
    
    efectividad_promedio = db.session.query(
        db.func.avg(Control.efectividad_porcentaje)
    ).filter(Control.activo == True).scalar() or 0
    
    return jsonify({
        'total': total,
        'por_estado': por_estado,
        'efectividad_promedio': round(float(efectividad_promedio), 2)
    })