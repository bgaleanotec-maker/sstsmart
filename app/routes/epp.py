# -*- coding: utf-8 -*-
"""Kardex de EPP y dotación (art. 2.2.4.6.24 D. 1072/2015; Módulo 11).

La jurisprudencia (SL854-2023, SL4665-2018) fija cuatro deberes en EPP:
suministrar el elemento idóneo, capacitar en su uso, verificar el uso y
reponerlo a tiempo. Este kardex documenta los deberes 1, 2 y 4; las
inspecciones del módulo de controles cubren el 3.
"""
from datetime import date, timedelta
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.constants import ROL_ADMIN, ROL_RESPONSABLE_SST
from app.models import Usuario
from app.models.sgsst import EntregaEPP

epp_bp = Blueprint('epp', __name__, url_prefix='/epp')

ELEMENTOS_COMUNES = [
    'Casco de seguridad', 'Gafas de seguridad', 'Protección auditiva',
    'Respirador / mascarilla', 'Guantes de seguridad', 'Botas de seguridad',
    'Arnés de cuerpo completo', 'Eslinga con absorbedor', 'Overol / ropa de trabajo',
    'Careta de soldadura', 'Delantal', 'Otro',
]


def sst_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.tiene_rol(ROL_ADMIN, ROL_RESPONSABLE_SST):
            flash('Solo el responsable del SG-SST o un administrador puede registrar entregas', 'error')
            return redirect(url_for('epp.kardex'))
        return f(*args, **kwargs)
    return wrapper


@epp_bp.route('/')
@login_required
def kardex():
    q = EntregaEPP.query
    trabajador_id = request.args.get('trabajador_id', type=int)
    if trabajador_id:
        q = q.filter_by(trabajador_id=trabajador_id)
    # El empleado solo ve su propio kardex
    if not current_user.tiene_rol(ROL_ADMIN, ROL_RESPONSABLE_SST):
        q = q.filter_by(trabajador_id=current_user.id)
    entregas = q.order_by(EntregaEPP.fecha_entrega.desc()).limit(300).all()
    vencidas = [e for e in entregas if e.reposicion_vencida]
    sin_capacitacion = [e for e in entregas if not e.capacitado_en_uso]
    usuarios = Usuario.query.filter_by(activo=True).all()
    return render_template('epp/kardex.html', entregas=entregas,
                           vencidas=vencidas, sin_capacitacion=sin_capacitacion,
                           usuarios=usuarios, elementos=ELEMENTOS_COMUNES,
                           filtro_trabajador=trabajador_id)


@epp_bp.route('/nueva', methods=['POST'])
@sst_required
def nueva():
    vida = request.form.get('vida_util_meses', type=int)
    fecha_e = (date.fromisoformat(request.form['fecha_entrega'])
               if request.form.get('fecha_entrega') else date.today())
    entrega = EntregaEPP(
        trabajador_id=int(request.form['trabajador_id']),
        elemento=request.form.get('elemento') or 'Otro',
        referencia=request.form.get('referencia'),
        certificacion=request.form.get('certificacion'),
        cantidad=request.form.get('cantidad', type=int) or 1,
        fecha_entrega=fecha_e,
        vida_util_meses=vida,
        fecha_reposicion=(fecha_e + timedelta(days=30 * vida)) if vida else None,
        capacitado_en_uso=request.form.get('capacitado_en_uso') == 'on',
        constancia=request.form.get('constancia'),
        observaciones=request.form.get('observaciones'),
        entregado_por_id=current_user.id,
    )
    db.session.add(entrega)
    db.session.commit()
    flash('Entrega registrada en el kardex', 'success')
    return redirect(url_for('epp.kardex'))
