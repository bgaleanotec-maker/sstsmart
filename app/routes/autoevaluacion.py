"""Autoevaluación de Estándares Mínimos — Resolución 0312 de 2019.

El gancho comercial del producto (docs/02-producto §3.1): determina el régimen
(7/21/60), diligencia ítem por ítem, calcula puntaje y clasificación, deriva el
plan de mejoramiento y exporta el resultado para el registro anual en la
plataforma SGRL del Fondo de Riesgos Laborales.
"""
import csv
import io
from datetime import datetime
from functools import wraps

from flask import (Blueprint, render_template, request, redirect, url_for,
                   flash, Response)
from flask_login import login_required, current_user

from app import db
from app.constants import ROL_ADMIN, ROL_RESPONSABLE_SST
from app.models import Empresa, Usuario
from app.models.autoevaluacion import Autoevaluacion, AccionMejora
from app.services import autoevaluacion_service as svc
from app.data.estandares_0312 import ESTANDARES, items_para_regimen

autoevaluacion_bp = Blueprint('autoevaluacion', __name__, url_prefix='/autoevaluacion')


def sst_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.tiene_rol(ROL_ADMIN, ROL_RESPONSABLE_SST):
            flash('Solo el responsable del SG-SST o un administrador puede gestionar la autoevaluación', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return wrapper


def _empresa_actual():
    if current_user.empresa_id:
        return db.session.get(Empresa, current_user.empresa_id)
    return Empresa.query.first()  # fase de transición: instancia monoempresa


# ============ PERFIL DE EMPRESA (determina el régimen) ============

@autoevaluacion_bp.route('/empresa', methods=['GET', 'POST'])
@sst_required
def perfil_empresa():
    empresa = _empresa_actual()
    if request.method == 'POST':
        if not empresa:
            empresa = Empresa(nit=request.form.get('nit') or 'SIN-NIT')
            db.session.add(empresa)
        empresa.nit = request.form.get('nit') or empresa.nit
        empresa.razon_social = request.form.get('razon_social') or 'Mi empresa'
        empresa.ciiu = request.form.get('ciiu')
        empresa.num_trabajadores = int(request.form.get('num_trabajadores') or 1)
        empresa.clase_riesgo = int(request.form.get('clase_riesgo') or 1)
        empresa.calcular_regimen()
        db.session.flush()
        if not current_user.empresa_id:
            current_user.empresa_id = empresa.id
        db.session.commit()
        flash(f'Empresa actualizada. Régimen aplicable: {empresa.regimen_estandares} estándares '
              f'(Res. 0312/2019)', 'success')
        return redirect(url_for('autoevaluacion.lista'))
    return render_template('autoevaluacion/empresa.html', empresa=empresa)


# ============ HISTÓRICO Y CREACIÓN ============

@autoevaluacion_bp.route('/')
@login_required
def lista():
    empresa = _empresa_actual()
    autoevaluaciones = (Autoevaluacion.query
                        .order_by(Autoevaluacion.anio.desc()).all())
    return render_template('autoevaluacion/lista.html',
                           empresa=empresa,
                           autoevaluaciones=autoevaluaciones,
                           anio_actual=datetime.utcnow().year)


@autoevaluacion_bp.route('/nueva', methods=['POST'])
@sst_required
def nueva():
    empresa = _empresa_actual()
    if not empresa:
        flash('Primero configura los datos de la empresa (trabajadores y clase de riesgo)', 'warning')
        return redirect(url_for('autoevaluacion.perfil_empresa'))
    anio = int(request.form.get('anio') or datetime.utcnow().year)
    if Autoevaluacion.query.filter_by(anio=anio).first():
        flash(f'Ya existe una autoevaluación para la vigencia {anio}', 'warning')
        return redirect(url_for('autoevaluacion.lista'))
    autoeval = svc.crear_autoevaluacion(empresa, anio, current_user.id)
    flash(f'Autoevaluación {anio} creada — régimen de {autoeval.regimen} estándares', 'success')
    return redirect(url_for('autoevaluacion.diligenciar', id=autoeval.id))


# ============ DILIGENCIAMIENTO ============

@autoevaluacion_bp.route('/<int:id>', methods=['GET'])
@login_required
def diligenciar(id):
    autoeval = Autoevaluacion.query.get_or_404(id)
    respuestas = {r.item_codigo: r for r in autoeval.respuestas}
    # Ítems exigibles agrupados por ciclo → estándar
    grupos = []
    for item in items_para_regimen(autoeval.regimen):
        cod, ciclo, estandar, desc, peso, _e7, _e21 = item
        if not grupos or grupos[-1]['ciclo'] != ciclo or grupos[-1]['estandar'] != estandar:
            grupos.append({'ciclo': ciclo, 'estandar': estandar, 'items': []})
        grupos[-1]['items'].append({
            'codigo': cod, 'descripcion': desc, 'puntaje': peso,
            'respuesta': respuestas.get(cod),
        })
    svc.calcular_puntaje(autoeval)  # puntaje parcial en vivo
    db.session.commit()
    return render_template('autoevaluacion/diligenciar.html',
                           autoeval=autoeval, grupos=grupos,
                           desglose=svc.desglose_por_ciclo(autoeval))


@autoevaluacion_bp.route('/<int:id>/guardar', methods=['POST'])
@sst_required
def guardar(id):
    autoeval = Autoevaluacion.query.get_or_404(id)
    if autoeval.estado == 'CERRADA':
        flash('Esta autoevaluación ya está cerrada', 'warning')
        return redirect(url_for('autoevaluacion.resultado', id=id))
    for resp in autoeval.respuestas:
        valor = request.form.get(f'cal_{resp.item_codigo}')
        if valor in ('CUMPLE', 'NO_CUMPLE', 'NO_APLICA'):
            resp.calificacion = valor
            resp.justificacion = request.form.get(f'jus_{resp.item_codigo}') or resp.justificacion
    svc.calcular_puntaje(autoeval)
    db.session.commit()
    if request.form.get('accion') == 'cerrar':
        try:
            svc.cerrar_autoevaluacion(autoeval)
            flash('Autoevaluación cerrada y plan de mejoramiento generado', 'success')
            return redirect(url_for('autoevaluacion.resultado', id=id))
        except ValueError as e:
            flash(str(e), 'error')
    else:
        flash('Avance guardado', 'success')
    return redirect(url_for('autoevaluacion.diligenciar', id=id))


# ============ RESULTADO Y PLAN DE MEJORA ============

@autoevaluacion_bp.route('/<int:id>/resultado')
@login_required
def resultado(id):
    autoeval = Autoevaluacion.query.get_or_404(id)
    acciones = autoeval.acciones.order_by(AccionMejora.item_codigo).all()
    usuarios = Usuario.query.filter_by(activo=True).all()
    return render_template('autoevaluacion/resultado.html',
                           autoeval=autoeval,
                           desglose=svc.desglose_por_ciclo(autoeval),
                           texto_accion=svc.texto_accion(autoeval.clasificacion),
                           acciones=acciones,
                           usuarios=usuarios)


@autoevaluacion_bp.route('/accion/<int:accion_id>', methods=['POST'])
@sst_required
def actualizar_accion(accion_id):
    accion = AccionMejora.query.get_or_404(accion_id)
    if request.form.get('responsable_id'):
        accion.responsable_id = int(request.form['responsable_id'])
    if request.form.get('fecha_limite'):
        accion.fecha_limite = datetime.fromisoformat(request.form['fecha_limite']).date()
    if request.form.get('estado') in ('Abierta', 'En_Proceso', 'Cerrada'):
        accion.estado = request.form['estado']
    db.session.commit()
    flash('Acción de mejora actualizada', 'success')
    return redirect(url_for('autoevaluacion.resultado', id=accion.autoevaluacion_id))


# ============ EXPORTACIÓN (registro SGRL / ARL) ============

@autoevaluacion_bp.route('/<int:id>/export.csv')
@login_required
def exportar_csv(id):
    autoeval = Autoevaluacion.query.get_or_404(id)
    respuestas = {r.item_codigo: r for r in autoeval.respuestas}
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=';')
    w.writerow(['Autoevaluación de Estándares Mínimos SG-SST — Resolución 0312 de 2019'])
    w.writerow(['Vigencia', autoeval.anio, 'Régimen', f'{autoeval.regimen} estándares'])
    w.writerow(['Puntaje', autoeval.puntaje_total, 'Valoración', autoeval.clasificacion or ''])
    w.writerow([])
    w.writerow(['Ciclo', 'Estándar', 'Ítem', 'Descripción', 'Peso',
                'Calificación', 'Puntaje obtenido', 'Justificación'])
    for cod, ciclo, estandar, desc, peso, _e7, _e21 in ESTANDARES:
        r = respuestas.get(cod)
        if r:
            w.writerow([ciclo, estandar, cod, desc, peso,
                        r.calificacion, r.puntaje_obtenido, r.justificacion or ''])
        else:
            w.writerow([ciclo, estandar, cod, desc, peso,
                        'NO EXIGIBLE (se otorga)', peso, f'No exigible para régimen de {autoeval.regimen}'])
    out = buf.getvalue().encode('utf-8-sig')  # BOM para Excel
    return Response(out, mimetype='text/csv', headers={
        'Content-Disposition':
            f'attachment; filename=autoevaluacion_0312_{autoeval.anio}.csv'
    })
