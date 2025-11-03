# app/routes/controles.py
"""
Rutas para gestionar Controles SST
Decreto 1072/2015 - Resolución 0312/2019
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Control, SeguimientoControl, RiesgoMatriz, Usuario
from app.models.control import TipoControl, NivelControl, EstadoControl
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

controles_bp = Blueprint('controles', __name__, url_prefix='/controles')

# ============== LISTAR CONTROLES ==============

@controles_bp.route('/', methods=['GET'])
@login_required
def listar_controles():
    """Lista todos los controles"""
    filtro_estado = request.args.get('estado', '')
    filtro_riesgo = request.args.get('riesgo_id', '')
    
    query = Control.query.filter_by(activo=True)
    
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
                         filtro_riesgo=filtro_riesgo)

# ============== CREAR CONTROL ==============

@controles_bp.route('/crear/<int:riesgo_id>', methods=['GET', 'POST'])
@login_required
def crear_control(riesgo_id):
    """Crea un nuevo control para un riesgo"""
    
    riesgo = RiesgoMatriz.query.get_or_404(riesgo_id)
    
    if request.method == 'POST':
        try:
            # Generar código único
            ultimo_control = Control.query.order_by(Control.id.desc()).first()
            numero = (ultimo_control.id + 1) if ultimo_control else 1
            codigo = f"CTL-{numero:03d}-{datetime.utcnow().year}"
            
            control = Control(
                codigo=codigo,
                nombre=request.form.get('nombre'),
                descripcion=request.form.get('descripcion'),
                tipo_control=request.form.get('tipo_control', TipoControl.PREVENTIVO.value),
                nivel_control=request.form.get('nivel_control', NivelControl.FUENTE.value),
                riesgo_id=riesgo_id,
                responsable_id=request.form.get('responsable_id') or current_user.id,
                fecha_planeada=datetime.fromisoformat(request.form.get('fecha_planeada')) if request.form.get('fecha_planeada') else None,
                presupuesto_estimado=float(request.form.get('presupuesto_estimado', 0)) if request.form.get('presupuesto_estimado') else None,
                requiere_seguimiento_periodico=request.form.get('requiere_seguimiento') == 'on',
                frecuencia_seguimiento_dias=int(request.form.get('frecuencia_seguimiento', 30)) if request.form.get('frecuencia_seguimiento') else 30,
                estado=EstadoControl.PLANIFICADO.value
            )
            
            db.session.add(control)
            db.session.commit()
            
            logger.info(f"✅ Control {codigo} creado para riesgo {riesgo_id}")
            flash(f'Control "{control.nombre}" creado exitosamente', 'success')
            return redirect(url_for('controles.listar_controles'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ Error creando control: {str(e)}", exc_info=True)
            flash(f'Error al crear control: {str(e)}', 'error')
            return redirect(request.referrer)
    
    usuarios = Usuario.query.filter_by(activo=True).all()
    tipos = [t.value for t in TipoControl]
    niveles = [n.value for n in NivelControl]
    
    return render_template('controles/crear.html',
                         riesgo=riesgo,
                         usuarios=usuarios,
                         tipos=tipos,
                         niveles=niveles)

# ============== EDITAR CONTROL ==============

@controles_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
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
            
            db.session.commit()
            logger.info(f"✅ Control {control.codigo} actualizado")
            flash('Control actualizado exitosamente', 'success')
            return redirect(url_for('controles.listar_controles'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ Error editando control: {str(e)}", exc_info=True)
            flash(f'Error al editar control: {str(e)}', 'error')
            return redirect(request.referrer)
    
    usuarios = Usuario.query.filter_by(activo=True).all()
    tipos = [t.value for t in TipoControl]
    niveles = [n.value for n in NivelControl]
    
    return render_template('controles/editar.html',
                         control=control,
                         usuarios=usuarios,
                         tipos=tipos,
                         niveles=niveles)

# ============== MARCAR IMPLEMENTADO ==============

@controles_bp.route('/<int:id>/implementado', methods=['POST'])
@login_required
def marcar_implementado(id):
    """Marca un control como implementado"""
    
    control = Control.query.get_or_404(id)
    
    try:
        evidencia = request.form.get('evidencia', '')
        control.marcar_implementado(evidencia)
        db.session.commit()
        
        logger.info(f"✅ Control {control.codigo} marcado como implementado")
        flash('Control marcado como implementado', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(request.referrer)

# ============== VERIFICAR CONTROL ==============

@controles_bp.route('/<int:id>/verificar', methods=['POST'])
@login_required
def verificar_control(id):
    """Verifica un control implementado"""
    
    control = Control.query.get_or_404(id)
    
    try:
        efectividad = int(request.form.get('efectividad', 100))
        control.marcar_verificado(efectividad)
        db.session.commit()
        
        logger.info(f"✅ Control {control.codigo} verificado con {efectividad}% efectividad")
        flash(f'Control verificado con {efectividad}% efectividad', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(request.referrer)

# ============== SEGUIMIENTO CONTROL ==============

@controles_bp.route('/<int:id>/seguimiento', methods=['POST'])
@login_required
def agregar_seguimiento(id):
    """Agrega un seguimiento a un control"""
    
    control = Control.query.get_or_404(id)
    
    try:
        seguimiento = SeguimientoControl(
            control_id=id,
            responsable_revision_id=current_user.id,
            sigue_vigente=request.form.get('sigue_vigente') == 'on',
            efectividad_actual=int(request.form.get('efectividad_actual', 100)),
            observaciones=request.form.get('observaciones'),
            requiere_ajustes=request.form.get('requiere_ajustes') == 'on',
            ajustes_recomendados=request.form.get('ajustes_recomendados')
        )
        
        db.session.add(seguimiento)
        control.ultima_revision = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"✅ Seguimiento agregado a control {control.codigo}")
        flash('Seguimiento registrado exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(request.referrer)

# ============== CERRAR CONTROL ==============

@controles_bp.route('/<int:id>/cerrar', methods=['POST'])
@login_required
def cerrar_control(id):
    """Cierra un control"""
    
    control = Control.query.get_or_404(id)
    
    try:
        control.cerrar()
        db.session.commit()
        
        logger.info(f"✅ Control {control.codigo} cerrado")
        flash('Control cerrado exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(request.referrer)

# ============== ELIMINAR CONTROL ==============

@controles_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_control(id):
    """Elimina (desactiva) un control"""
    
    control = Control.query.get_or_404(id)
    
    try:
        control.activo = False
        db.session.commit()
        
        logger.info(f"✅ Control {control.codigo} eliminado")
        flash('Control eliminado exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('controles.listar_controles'))

# ============== API ==============

@controles_bp.route('/api/riesgo/<int:riesgo_id>', methods=['GET'])
@login_required
def api_controles_riesgo(riesgo_id):
    """API: Obtiene controles de un riesgo"""
    
    controles = Control.query.filter_by(riesgo_id=riesgo_id, activo=True).all()
    
    return jsonify([{
        'id': c.id,
        'codigo': c.codigo,
        'nombre': c.nombre,
        'tipo': c.tipo_control,
        'nivel': c.nivel_control,
        'estado': c.estado,
        'efectividad': c.efectividad_porcentaje
    } for c in controles])