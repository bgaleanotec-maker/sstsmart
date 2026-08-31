# -*- coding: utf-8 -*-
"""Núcleo documental SG-SST: Política, Plan anual de trabajo e Indicadores.

Módulos 2, 5 y 12 de la guía estratégica; obligaciones de los arts.
2.2.4.6.5-6 (política), 2.2.4.6.17 (plan anual) y 2.2.4.6.19-21 +
Res. 0312 art. 30 (indicadores mínimos).
"""
from datetime import datetime, date
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.constants import ROL_ADMIN, ROL_RESPONSABLE_SST
from app.models import Empresa, Usuario, Evento
from app.models.sgsst import PoliticaSST, PlanTrabajoActividad

sgsst_bp = Blueprint('sgsst', __name__, url_prefix='/sgsst')


def sst_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.tiene_rol(ROL_ADMIN, ROL_RESPONSABLE_SST):
            flash('Solo el responsable del SG-SST o un administrador puede gestionar esto', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return wrapper


def _empresa():
    if current_user.empresa_id:
        return db.session.get(Empresa, current_user.empresa_id)
    return Empresa.query.first()


PLANTILLA_POLITICA = """POLÍTICA DE SEGURIDAD Y SALUD EN EL TRABAJO

{razon_social} (NIT {nit}), dedicada a su actividad económica principal, se compromete con la protección y promoción de la salud de sus trabajadores, contratistas y visitantes, procurando su integridad física y mental mediante el control de los peligros y riesgos, el mejoramiento continuo del Sistema de Gestión de Seguridad y Salud en el Trabajo (SG-SST) y el cumplimiento de la normatividad legal vigente en riesgos laborales (Ley 1562 de 2012, Decreto 1072 de 2015, Resolución 0312 de 2019 y demás normas aplicables).

La alta dirección se compromete a:
1. Identificar los peligros, evaluar y valorar los riesgos de todas las actividades, y establecer los respectivos controles bajo la jerarquía de eliminación, sustitución, controles de ingeniería, administrativos y elementos de protección personal.
2. Proteger la seguridad y salud de todos los trabajadores mediante la mejora continua del SG-SST.
3. Destinar los recursos humanos, técnicos y financieros necesarios para la implementación y mantenimiento del SG-SST.
4. Promover la participación de los trabajadores y del COPASST (o Vigía de SST) en las actividades del sistema.
5. Cumplir la normatividad nacional vigente aplicable en materia de riesgos laborales.

Esta política será publicada, difundida a todos los niveles de la organización, y revisada como mínimo una vez al año o cuando cambien las condiciones de trabajo."""


# ============ PANEL ============

@sgsst_bp.route('/')
@login_required
def panel():
    anio = datetime.utcnow().year
    politica = PoliticaSST.query.filter_by(anio=anio).first()
    actividades = PlanTrabajoActividad.query.filter_by(anio=anio).all()
    ejecutadas = sum(1 for a in actividades if a.estado == 'Ejecutada')
    vencidas = sum(1 for a in actividades if a.vencida)
    return render_template('sgsst/panel.html', anio=anio, politica=politica,
                           total_act=len(actividades), ejecutadas=ejecutadas,
                           vencidas=vencidas,
                           indicadores=_indicadores_anio(anio))


# ============ POLÍTICA SST ============

@sgsst_bp.route('/politica', methods=['GET', 'POST'])
@login_required
def politica():
    anio = int(request.args.get('anio') or datetime.utcnow().year)
    empresa = _empresa()
    actual = PoliticaSST.query.filter_by(anio=anio).first()

    if request.method == 'POST':
        if not current_user.tiene_rol(ROL_ADMIN, ROL_RESPONSABLE_SST):
            flash('No tienes permiso para editar la política', 'error')
            return redirect(url_for('sgsst.politica', anio=anio))
        if not actual:
            actual = PoliticaSST(anio=anio, contenido='', creada_por_id=current_user.id)
            db.session.add(actual)
        else:
            actual.version = (actual.version or 1) + 1
        actual.contenido = request.form.get('contenido', '').strip()
        actual.firmada_por = request.form.get('firmada_por')
        actual.cargo_firmante = request.form.get('cargo_firmante')
        if request.form.get('fecha_firma'):
            actual.fecha_firma = date.fromisoformat(request.form['fecha_firma'])
        actual.divulgada = request.form.get('divulgada') == 'on'
        if actual.divulgada and request.form.get('fecha_divulgacion'):
            actual.fecha_divulgacion = date.fromisoformat(request.form['fecha_divulgacion'])
        db.session.commit()
        flash(f'Política SST {anio} guardada (versión {actual.version})', 'success')
        return redirect(url_for('sgsst.politica', anio=anio))

    plantilla = ''
    if not actual and empresa:
        plantilla = PLANTILLA_POLITICA.format(
            razon_social=empresa.razon_social, nit=empresa.nit)
    historicas = PoliticaSST.query.order_by(PoliticaSST.anio.desc()).all()
    return render_template('sgsst/politica.html', anio=anio, politica=actual,
                           plantilla=plantilla, historicas=historicas)


@sgsst_bp.route('/politica/<int:anio>/imprimir')
@login_required
def politica_imprimir(anio):
    pol = PoliticaSST.query.filter_by(anio=anio).first_or_404()
    return render_template('sgsst/politica_imprimir.html', politica=pol,
                           empresa=_empresa())


# ============ PLAN ANUAL DE TRABAJO ============

@sgsst_bp.route('/plan', methods=['GET', 'POST'])
@login_required
def plan():
    anio = int(request.args.get('anio') or request.form.get('anio')
               or datetime.utcnow().year)

    if request.method == 'POST':
        if not current_user.tiene_rol(ROL_ADMIN, ROL_RESPONSABLE_SST):
            flash('No tienes permiso para editar el plan', 'error')
            return redirect(url_for('sgsst.plan', anio=anio))
        act = PlanTrabajoActividad(
            anio=anio,
            objetivo=request.form.get('objetivo', ''),
            actividad=request.form.get('actividad', ''),
            responsable_id=int(request.form['responsable_id']) if request.form.get('responsable_id') else None,
            recursos=request.form.get('recursos'),
            fecha_programada=date.fromisoformat(request.form['fecha_programada']) if request.form.get('fecha_programada') else None,
        )
        db.session.add(act)
        db.session.commit()
        flash('Actividad agregada al plan', 'success')
        return redirect(url_for('sgsst.plan', anio=anio))

    actividades = (PlanTrabajoActividad.query.filter_by(anio=anio)
                   .order_by(PlanTrabajoActividad.fecha_programada).all())
    usuarios = Usuario.query.filter_by(activo=True).all()
    ejecutadas = sum(1 for a in actividades if a.estado == 'Ejecutada')
    return render_template('sgsst/plan.html', anio=anio, actividades=actividades,
                           usuarios=usuarios, ejecutadas=ejecutadas,
                           anio_actual=datetime.utcnow().year)


@sgsst_bp.route('/plan/<int:id>/estado', methods=['POST'])
@sst_required
def plan_estado(id):
    act = PlanTrabajoActividad.query.get_or_404(id)
    nuevo = request.form.get('estado')
    if nuevo in ('Programada', 'En_Ejecucion', 'Ejecutada'):
        act.estado = nuevo
        if nuevo == 'Ejecutada' and not act.fecha_ejecucion:
            act.fecha_ejecucion = date.today()
        if request.form.get('evidencia'):
            act.evidencia = request.form['evidencia']
        db.session.commit()
        flash('Actividad actualizada', 'success')
    return redirect(url_for('sgsst.plan', anio=act.anio))


# ============ INDICADORES (Res. 0312 art. 30) ============

def _indicadores_anio(anio):
    """Indicadores mínimos calculados desde los eventos registrados."""
    empresa = _empresa()
    n_trab = (empresa.num_trabajadores if empresa else 0) or 0
    eventos = Evento.query.filter(
        db.extract('year', Evento.fecha_apertura_real) == anio).all()

    def es_at(e):
        t = (e.tipo or '').lower()
        return 'accidente' in t or t.strip() in ('at', 'a.t.')

    def es_el(e):
        t = (e.tipo or '').lower()
        return 'enfermedad' in t or t.strip() in ('el', 'e.l.')

    ats = [e for e in eventos if es_at(e)]
    els = [e for e in eventos if es_el(e)]
    mortales = [e for e in eventos if 'mortal' in (e.tipo or '').lower()
                or 'muerte' in (e.descripcion or '').lower()]
    dias_incap = sum(e.dias_incapacidad or 0 for e in eventos)

    return {
        'anio': anio,
        'n_trabajadores': n_trab,
        'num_at': len(ats),
        'num_el': len(els),
        'num_mortales': len(mortales),
        'dias_incapacidad': dias_incap,
        # Fórmulas de la Res. 0312/2019 art. 30 (base anual)
        'frecuencia': round(len(ats) / n_trab * 100, 2) if n_trab else None,
        'severidad': round(dias_incap / n_trab * 100, 2) if n_trab else None,
        'mortalidad': round(len(mortales) / len(ats) * 100, 2) if ats else 0.0,
        'prevalencia_el': round(len(els) / n_trab * 100000, 1) if n_trab else None,
        'ausentismo': round(dias_incap / (n_trab * 300) * 100, 2) if n_trab else None,
    }


@sgsst_bp.route('/indicadores')
@login_required
def indicadores():
    anio = int(request.args.get('anio') or datetime.utcnow().year)
    return render_template('sgsst/indicadores.html',
                           ind=_indicadores_anio(anio), anio=anio,
                           anio_actual=datetime.utcnow().year)
