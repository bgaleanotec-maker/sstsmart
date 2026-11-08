# -*- coding: utf-8 -*-
"""Módulo de cumplimiento: SARLAFT transporte, PTEE, SAGRILAFT y datos personales.

Rutas:
  /cumplimiento/                       programas disponibles y activados + diagnóstico
  /cumplimiento/activar/<codigo>       POST activa un programa con su régimen
  /cumplimiento/p/<id>                 panel del programa: avance, oficial, requisitos, reportes
  /cumplimiento/p/<id>/riesgos         matriz de riesgos del programa
  /cumplimiento/contrapartes           debida diligencia (compartida por los programas)
"""
from datetime import date
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user

from app import db
from app.constants import ROLES_CUMPLIMIENTO_GESTION
from app.data.programas_cumplimiento import (PROGRAMAS, TIPOS_CONTRAPARTE, FACTORES_RIESGO,
                                             ETAPAS, normas_pendientes)
from app.models import Usuario
from app.models.cumplimiento import (ProgramaCumplimiento, RequisitoCumplimiento, Contraparte,
                                     RiesgoCumplimiento, ReporteCumplimiento,
                                     ESTADOS_REQUISITO, NIVELES_RIESGO)
from app.services import cumplimiento_service as svc
from app.services import listas_restrictivas as listas

cumplimiento_bp = Blueprint('cumplimiento', __name__, url_prefix='/cumplimiento')


def gestion_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.tiene_rol(*ROLES_CUMPLIMIENTO_GESTION):
            flash('Solo el oficial de cumplimiento, la gerencia o un administrador puede modificar esto', 'error')
            return redirect(url_for('cumplimiento.index'))
        return f(*args, **kwargs)
    return wrapper


def _fecha(valor):
    return date.fromisoformat(valor) if valor else None


def _programa_o_404(id):
    return ProgramaCumplimiento.query.filter_by(id=id).first_or_404()


# ---------- índice y diagnóstico ----------

@cumplimiento_bp.route('/')
@login_required
def index():
    resumen = svc.resumen_empresa()
    activos = {p.codigo: p for p in resumen['programas']}
    avances = {p.id: svc.avance(p) for p in resumen['programas']}

    diag = None
    datos = {}
    if request.args.get('diag'):
        datos = {
            'vigilada_supertransporte': request.args.get('supertransporte') == 'on',
            'supervisada_supersociedades': request.args.get('supersociedades') == 'on',
            'ingresos': request.args.get('ingresos', type=int),
            'activos': request.args.get('activos', type=int),
        }
        diag = svc.diagnostico(**datos)
    return render_template('cumplimiento/index.html', catalogo=PROGRAMAS, activos=activos,
                           avances=avances, resumen=resumen, diag=diag, datos=datos,
                           parametros=svc.parametros_vigentes(),
                           normas_pendientes=normas_pendientes,
                           puede_gestionar=current_user.tiene_rol(*ROLES_CUMPLIMIENTO_GESTION))


@cumplimiento_bp.route('/activar/<codigo>', methods=['POST'])
@gestion_required
def activar(codigo):
    if codigo not in PROGRAMAS:
        abort(404)
    regimen = request.form.get('regimen') or next(iter(PROGRAMAS[codigo]['regimenes']))
    try:
        programa = svc.activar_programa(codigo, regimen, current_user.id)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('cumplimiento.index'))
    flash(f'{programa.nombre} activado ({programa.nombre_regimen}). Empieza por la política y el oficial.', 'success')
    return redirect(url_for('cumplimiento.programa', id=programa.id))


# ---------- panel del programa ----------

@cumplimiento_bp.route('/p/<int:id>')
@login_required
def programa(id):
    p = _programa_o_404(id)
    hoy = date.today()
    por_etapa = []
    for etapa in ETAPAS:
        filas = [r for r in p.requisitos if r.info.get('etapa') == etapa and r.estado != 'no_aplica']
        if filas:
            por_etapa.append((etapa, filas))
    no_aplican = [r for r in p.requisitos if r.estado == 'no_aplica']
    reportes = sorted(p.reportes, key=lambda r: (r.estado != 'pendiente', r.fecha_limite))
    return render_template('cumplimiento/programa.html', p=p, avance=svc.avance(p, hoy),
                           por_etapa=por_etapa, no_aplican=no_aplican, reportes=reportes,
                           usuarios=Usuario.query.filter_by(activo=True).all(),
                           estados=ESTADOS_REQUISITO, hoy=hoy,
                           n_riesgos=len(p.riesgos),
                           riesgos_altos=sum(1 for r in p.riesgos if r.nivel == 'alto'),
                           puede_gestionar=current_user.tiene_rol(*ROLES_CUMPLIMIENTO_GESTION))


@cumplimiento_bp.route('/p/<int:id>/oficial', methods=['POST'])
@gestion_required
def oficial(id):
    p = _programa_o_404(id)
    p.oficial_nombre = request.form.get('oficial_nombre') or None
    p.oficial_documento = request.form.get('oficial_documento') or None
    p.oficial_correo = request.form.get('oficial_correo') or None
    p.oficial_tipo = request.form.get('oficial_tipo') or None
    p.suplente_nombre = request.form.get('suplente_nombre') or None
    p.acta_designacion = request.form.get('acta_designacion') or None
    p.fecha_designacion = _fecha(request.form.get('fecha_designacion'))
    p.registro_sirel = request.form.get('registro_sirel') == 'on'
    p.fecha_aprobacion_politica = _fecha(request.form.get('fecha_aprobacion_politica'))
    p.notas = request.form.get('notas') or None
    db.session.commit()
    flash('Datos del oficial guardados', 'success')
    return redirect(url_for('cumplimiento.programa', id=p.id))


@cumplimiento_bp.route('/p/<int:id>/regimen', methods=['POST'])
@gestion_required
def cambiar_regimen(id):
    p = _programa_o_404(id)
    regimen = request.form.get('regimen')
    if regimen not in p.info.get('regimenes', {}):
        abort(400)
    p.regimen = regimen
    svc.sincronizar_requisitos(p)
    db.session.commit()
    flash(f'Régimen cambiado a {p.nombre_regimen}', 'success')
    return redirect(url_for('cumplimiento.programa', id=p.id))


@cumplimiento_bp.route('/p/<int:id>/requisito/<int:rid>', methods=['POST'])
@gestion_required
def requisito(id, rid):
    p = _programa_o_404(id)
    req = RequisitoCumplimiento.query.filter_by(id=rid, programa_id=p.id).first_or_404()
    estado = request.form.get('estado', req.estado)
    try:
        svc.marcar_requisito(req, estado, evidencia=request.form.get('evidencia'),
                             fecha=_fecha(request.form.get('fecha_cumplimiento')),
                             responsable_id=request.form.get('responsable_id', type=int) or 0)
    except ValueError:
        abort(400)
    db.session.commit()
    flash(f'"{req.nombre}" actualizado', 'success')
    return redirect(url_for('cumplimiento.programa', id=p.id) + f'#req-{req.id}')


@cumplimiento_bp.route('/p/<int:id>/reporte/<int:rid>', methods=['POST'])
@gestion_required
def reporte(id, rid):
    p = _programa_o_404(id)
    rep = ReporteCumplimiento.query.filter_by(id=rid, programa_id=p.id).first_or_404()
    estado = request.form.get('estado', 'presentado')
    if estado not in ('pendiente', 'presentado', 'no_aplica'):
        abort(400)
    rep.estado = estado
    rep.fecha_presentacion = _fecha(request.form.get('fecha_presentacion')) or (date.today() if estado == 'presentado' else None)
    rep.radicado = request.form.get('radicado') or rep.radicado
    db.session.commit()
    flash('Reporte actualizado', 'success')
    return redirect(url_for('cumplimiento.programa', id=p.id) + '#reportes')


@cumplimiento_bp.route('/p/<int:id>/reporte/nuevo', methods=['POST'])
@gestion_required
def reporte_nuevo(id):
    p = _programa_o_404(id)
    nombre = (request.form.get('nombre') or '').strip()
    fecha = _fecha(request.form.get('fecha_limite'))
    if not nombre or not fecha:
        flash('El reporte necesita nombre y fecha límite', 'error')
        return redirect(url_for('cumplimiento.programa', id=p.id) + '#reportes')
    db.session.add(ReporteCumplimiento(programa=p, codigo='manual', nombre=nombre, fecha_limite=fecha,
                                       verificado=True, notas=request.form.get('notas')))
    db.session.commit()
    flash('Reporte agregado', 'success')
    return redirect(url_for('cumplimiento.programa', id=p.id) + '#reportes')


# ---------- riesgos ----------

@cumplimiento_bp.route('/p/<int:id>/riesgos', methods=['GET', 'POST'])
@login_required
def riesgos(id):
    p = _programa_o_404(id)
    if request.method == 'POST':
        if not current_user.tiene_rol(*ROLES_CUMPLIMIENTO_GESTION):
            abort(403)
        descripcion = (request.form.get('descripcion') or '').strip()
        if not descripcion:
            flash('Describe el riesgo', 'error')
            return redirect(url_for('cumplimiento.riesgos', id=p.id))
        r = RiesgoCumplimiento(
            programa=p, factor=request.form.get('factor') if request.form.get('factor') in FACTORES_RIESGO else 'contraparte',
            descripcion=descripcion,
            probabilidad=min(5, max(1, request.form.get('probabilidad', type=int) or 3)),
            impacto=min(5, max(1, request.form.get('impacto', type=int) or 3)),
            controles=request.form.get('controles') or None,
            probabilidad_residual=request.form.get('probabilidad_residual', type=int) or None,
            impacto_residual=request.form.get('impacto_residual', type=int) or None,
            responsable_id=request.form.get('responsable_id', type=int) or None,
        )
        db.session.add(r)
        db.session.commit()
        flash('Riesgo agregado a la matriz', 'success')
        return redirect(url_for('cumplimiento.riesgos', id=p.id))
    filas = sorted(p.riesgos, key=lambda r: -r.residual)
    conteo = {n: sum(1 for r in filas if r.nivel == n) for n in NIVELES_RIESGO}
    return render_template('cumplimiento/riesgos.html', p=p, riesgos=filas, conteo=conteo,
                           factores=FACTORES_RIESGO, usuarios=Usuario.query.filter_by(activo=True).all(),
                           puede_gestionar=current_user.tiene_rol(*ROLES_CUMPLIMIENTO_GESTION))


@cumplimiento_bp.route('/riesgo/<int:rid>/eliminar', methods=['POST'])
@gestion_required
def riesgo_eliminar(rid):
    r = RiesgoCumplimiento.query.filter_by(id=rid).first_or_404()
    pid = r.programa_id
    db.session.delete(r)
    db.session.commit()
    flash('Riesgo eliminado', 'success')
    return redirect(url_for('cumplimiento.riesgos', id=pid))


# ---------- contrapartes ----------

@cumplimiento_bp.route('/contrapartes')
@login_required
def contrapartes():
    hoy = date.today()
    q = Contraparte.query.filter(Contraparte.estado != 'retirada')
    tipo = request.args.get('tipo')
    if tipo in TIPOS_CONTRAPARTE:
        q = q.filter_by(tipo=tipo)
    filas = q.order_by(Contraparte.nombre).limit(500).all()
    sin_verificar = [c for c in filas if c.verificacion_vencida(hoy)]
    coincidencias = [c for c in filas if c.resultado_verificacion == 'coincidencia' and c.estado == 'activa']
    return render_template('cumplimiento/contrapartes.html', contrapartes=filas, tipos=TIPOS_CONTRAPARTE,
                           sin_verificar=sin_verificar, coincidencias=coincidencias, filtro_tipo=tipo,
                           enlaces=listas.ENLACES_MANUALES, hoy=hoy,
                           lista_onu_configurada=bool(current_app.config.get('LISTA_ONU_URL')),
                           puede_gestionar=current_user.tiene_rol(*ROLES_CUMPLIMIENTO_GESTION))


@cumplimiento_bp.route('/contrapartes/nueva', methods=['POST'])
@gestion_required
def contraparte_nueva():
    nombre = (request.form.get('nombre') or '').strip()
    if not nombre:
        flash('La contraparte necesita un nombre', 'error')
        return redirect(url_for('cumplimiento.contrapartes'))
    c = Contraparte(
        tipo=request.form.get('tipo') if request.form.get('tipo') in TIPOS_CONTRAPARTE else 'cliente',
        nombre=nombre, tipo_documento=request.form.get('tipo_documento') or 'NIT',
        documento=(request.form.get('documento') or '').strip() or None,
        pais=request.form.get('pais') or 'Colombia', actividad=request.form.get('actividad') or None,
        pep=request.form.get('pep') == 'on',
        nivel_riesgo=request.form.get('nivel_riesgo') if request.form.get('nivel_riesgo') in NIVELES_RIESGO else 'bajo',
        fecha_vinculacion=_fecha(request.form.get('fecha_vinculacion')) or date.today(),
        creado_por_id=current_user.id,
    )
    if c.pep and c.nivel_riesgo == 'bajo':
        c.nivel_riesgo = 'alto'   # PEP exige debida diligencia intensificada
    db.session.add(c)
    db.session.commit()
    flash(f'{c.nombre} registrada. Verifícala en listas antes de vincularla.', 'success')
    return redirect(url_for('cumplimiento.contrapartes') + f'#c-{c.id}')


@cumplimiento_bp.route('/contrapartes/<int:cid>/verificar', methods=['POST'])
@gestion_required
def contraparte_verificar(cid):
    c = Contraparte.query.filter_by(id=cid).first_or_404()
    hoy = date.today()
    modo = request.form.get('modo', 'manual')
    if modo == 'automatico':
        disponible, coincidencias, fuente = listas.consultar(c.nombre, current_app.config.get('LISTA_ONU_URL'))
        if not disponible:
            flash('La lista ONU no está disponible ahora (configura LISTA_ONU_URL o inténtalo luego). '
                  'Puedes registrar una consulta manual.', 'warning')
            return redirect(url_for('cumplimiento.contrapartes') + f'#c-{c.id}')
        c.resultado_verificacion = 'coincidencia' if coincidencias else 'sin_coincidencia'
        c.fuente_verificacion = fuente
        c.detalle_verificacion = ('\n'.join(f"{m['nombre']} ({m['tipo']}, ref. {m['referencia']}, similitud {m['similitud']})"
                                            for m in coincidencias) or 'Sin coincidencias')
    else:
        resultado = request.form.get('resultado')
        if resultado not in ('sin_coincidencia', 'coincidencia'):
            abort(400)
        c.resultado_verificacion = resultado
        c.fuente_verificacion = (request.form.get('fuente') or 'Consulta manual').strip()
        c.detalle_verificacion = request.form.get('detalle') or None
    c.ultima_verificacion = hoy
    meses = {'alto': 6, 'medio': 12, 'bajo': 12}[c.nivel_riesgo or 'bajo']
    c.proxima_verificacion = svc._sumar_meses(hoy, meses)
    if c.resultado_verificacion == 'coincidencia':
        c.estado = 'bloqueada'
        flash(f'Posible coincidencia para {c.nombre}: queda bloqueada hasta que el oficial la revise. '
              'Una coincidencia de nombre no prueba nada por sí sola.', 'warning')
    else:
        if c.estado == 'bloqueada':
            c.estado = 'activa'
        flash(f'{c.nombre} verificada sin coincidencias. Próxima verificación: {c.proxima_verificacion:%d/%m/%Y}.', 'success')
    db.session.commit()
    return redirect(url_for('cumplimiento.contrapartes') + f'#c-{c.id}')


@cumplimiento_bp.route('/contrapartes/<int:cid>/estado', methods=['POST'])
@gestion_required
def contraparte_estado(cid):
    c = Contraparte.query.filter_by(id=cid).first_or_404()
    estado = request.form.get('estado')
    if estado not in ('activa', 'bloqueada', 'retirada'):
        abort(400)
    c.estado = estado
    if request.form.get('notas') is not None:
        c.notas = request.form.get('notas') or None
    if request.form.get('senales_alerta') is not None:
        c.senales_alerta = request.form.get('senales_alerta') or None
    db.session.commit()
    flash('Contraparte actualizada', 'success')
    return redirect(url_for('cumplimiento.contrapartes'))
