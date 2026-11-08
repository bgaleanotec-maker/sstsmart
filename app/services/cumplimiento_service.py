# -*- coding: utf-8 -*-
"""Lógica del módulo de cumplimiento: activar programas, medir avance,
generar reportes con fecha, diagnosticar qué programa aplica y valorar riesgos.

Ninguna fecha la calcula la IA (ADR-P4): salen del catálogo y de este archivo.
"""
from datetime import date, timedelta
from math import ceil

from app import db
from app.data.programas_cumplimiento import PROGRAMAS, PARAMETROS, requisitos_de, parametro
from app.models.cumplimiento import (ProgramaCumplimiento, RequisitoCumplimiento,
                                     ReporteCumplimiento, Contraparte)


# ---------- riesgo ----------

def nivel_riesgo(puntaje):
    """Probabilidad × impacto (1..25) → bajo ≤6, medio ≤12, alto >12 (propuesta)."""
    if puntaje is None:
        return 'bajo'
    if puntaje > 12:
        return 'alto'
    if puntaje > 6:
        return 'medio'
    return 'bajo'


# ---------- programas ----------

def _sumar_meses(fecha, meses):
    mes = fecha.month - 1 + meses
    anio = fecha.year + mes // 12
    mes = mes % 12 + 1
    dia = min(fecha.day, 28)
    return date(anio, mes, dia)


def proxima_ocurrencia(mes, dia, hoy):
    """Próxima fecha (incluye hoy) de un día/mes fijo."""
    candidata = date(hoy.year, mes, dia)
    if candidata < hoy:
        candidata = date(hoy.year + 1, mes, dia)
    return candidata


def generar_reportes(programa, hoy=None, meses=12):
    """Crea (idempotente) los reportes del catálogo que vencen en los próximos `meses`."""
    hoy = hoy or date.today()
    horizonte = _sumar_meses(hoy, meses)
    existentes = {(r.codigo, r.fecha_limite) for r in programa.reportes}
    nuevos = 0
    for rep in programa.info.get('reportes', []):
        for mes, dia in rep['fechas']:
            fecha = proxima_ocurrencia(mes, dia, hoy)
            while fecha <= horizonte:
                if (rep['codigo'], fecha) not in existentes:
                    db.session.add(ReporteCumplimiento(
                        programa=programa, codigo=rep['codigo'], nombre=rep['nombre'],
                        fecha_limite=fecha, verificado=rep.get('verificado', False),
                        notas=rep.get('norma')))
                    existentes.add((rep['codigo'], fecha))
                    nuevos += 1
                fecha = date(fecha.year + 1, mes, dia)
    return nuevos


def activar_programa(codigo, regimen, usuario_id=None, hoy=None):
    """Activa un programa del catálogo para la empresa del contexto y crea sus
    requisitos y reportes. Si ya existe, lo devuelve sin duplicar."""
    hoy = hoy or date.today()
    if codigo not in PROGRAMAS:
        raise ValueError(f'Programa desconocido: {codigo}')
    if regimen not in PROGRAMAS[codigo]['regimenes']:
        raise ValueError(f'Régimen desconocido para {codigo}: {regimen}')
    programa = ProgramaCumplimiento.query.filter_by(codigo=codigo).first()
    if programa:
        programa.estado = 'activo'
        if programa.regimen != regimen:
            programa.regimen = regimen
            sincronizar_requisitos(programa)
        db.session.commit()
        return programa
    programa = ProgramaCumplimiento(codigo=codigo, regimen=regimen, creado_por_id=usuario_id,
                                    fecha_activacion=hoy)
    db.session.add(programa)
    db.session.flush()
    sincronizar_requisitos(programa)
    generar_reportes(programa, hoy)
    db.session.commit()
    return programa


def sincronizar_requisitos(programa):
    """Asegura una fila por requisito del régimen; marca `no_aplica` los que
    dejaron de aplicar al cambiar de régimen (no borra evidencia)."""
    aplican = {r['codigo'] for r in requisitos_de(programa.codigo, programa.regimen)}
    actuales = {r.codigo: r for r in programa.requisitos}
    for cod in aplican:
        if cod not in actuales:
            db.session.add(RequisitoCumplimiento(programa=programa, codigo=cod))
        elif actuales[cod].estado == 'no_aplica':
            actuales[cod].estado = 'pendiente'
    for cod, fila in actuales.items():
        if cod not in aplican:
            fila.estado = 'no_aplica'
    db.session.flush()


def marcar_requisito(req, estado, evidencia=None, fecha=None, responsable_id=None):
    """Cambia el estado; si queda cumplido y es periódico, programa la próxima revisión."""
    if estado not in ('pendiente', 'en_curso', 'cumplido', 'no_aplica'):
        raise ValueError(estado)
    req.estado = estado
    if evidencia is not None:
        req.evidencia = evidencia
    if responsable_id is not None:
        req.responsable_id = responsable_id or None
    if estado == 'cumplido':
        req.fecha_cumplimiento = fecha or date.today()
        meses = req.info.get('periodicidad_meses')
        req.proxima_revision = _sumar_meses(req.fecha_cumplimiento, meses) if meses else None
    elif estado in ('pendiente', 'en_curso'):
        req.fecha_cumplimiento = None
    return req


def avance(programa, hoy=None):
    """Avance del programa: cumplidos / exigibles, con vencidos y pendientes."""
    hoy = hoy or date.today()
    exigibles = [r for r in programa.requisitos if r.estado != 'no_aplica']
    cumplidos = [r for r in exigibles if r.estado == 'cumplido' and not r.vencido(hoy)]
    vencidos = [r for r in exigibles if r.vencido(hoy)]
    pendientes = [r for r in exigibles if r.estado in ('pendiente', 'en_curso')]
    total = len(exigibles)
    pct = round(100 * len(cumplidos) / total) if total else 0
    return {
        'total': total, 'cumplidos': len(cumplidos), 'vencidos': len(vencidos),
        'pendientes': len(pendientes), 'porcentaje': pct,
        'nivel': 'verde' if pct >= 85 else ('amarillo' if pct >= 50 else 'rojo'),
    }


def reportes_pendientes(programa=None, hoy=None, dias=120):
    hoy = hoy or date.today()
    q = ReporteCumplimiento.query.filter(ReporteCumplimiento.estado == 'pendiente',
                                         ReporteCumplimiento.fecha_limite <= hoy + timedelta(days=dias))
    if programa is not None:
        q = q.filter_by(programa_id=programa.id)
    return q.order_by(ReporteCumplimiento.fecha_limite).all()


def resumen_empresa(hoy=None):
    """Cifras para el índice del módulo y el panel principal."""
    hoy = hoy or date.today()
    programas = ProgramaCumplimiento.query.filter_by(estado='activo').all()
    requisitos_pendientes = 0
    requisitos_vencidos = 0
    for p in programas:
        a = avance(p, hoy)
        requisitos_pendientes += a['pendientes']
        requisitos_vencidos += a['vencidos']
    contrapartes = Contraparte.query.filter(Contraparte.estado != 'retirada').all()
    sin_verificar = sum(1 for c in contrapartes if c.verificacion_vencida(hoy))
    coincidencias = sum(1 for c in contrapartes if c.resultado_verificacion == 'coincidencia'
                        and c.estado == 'activa')
    return {
        'programas': programas,
        'requisitos_pendientes': requisitos_pendientes,
        'requisitos_vencidos': requisitos_vencidos,
        'reportes': reportes_pendientes(None, hoy),
        'contrapartes': len(contrapartes),
        'contrapartes_sin_verificar': sin_verificar,
        'coincidencias_abiertas': coincidencias,
    }


# ---------- diagnóstico "¿me aplica?" ----------

def diagnostico(vigilada_supertransporte=False, supervisada_supersociedades=False,
                ingresos=None, activos=None):
    """Qué programa aplica según los datos de la empresa. Propuesta orientativa:
    cada umbral está marcado [VERIFICAR] hasta que Brian confirme la fuente."""
    uvb = parametro('uvb')
    uvt = parametro('uvt')
    smlmv = parametro('smlmv')
    umbral_sarlaft = parametro('umbral_sarlaft_uvb') * uvb
    umbral_rnbd = parametro('umbral_rnbd_uvt') * uvt
    umbral_sagrilaft = parametro('umbral_sagrilaft_smlmv') * smlmv
    salida = []

    if vigilada_supertransporte:
        if ingresos is None:
            salida.append(dict(codigo='sarlaft_transporte', aplica='probable', regimen=None,
                               razon='Vigilada por la Supertransporte: aplica SARLAFT completo o el Régimen de '
                                     'Medidas Simplificadas según los ingresos del año anterior. Indica los ingresos para saber cuál.'))
        elif ingresos >= umbral_sarlaft:
            salida.append(dict(codigo='sarlaft_transporte', aplica='obligatorio', regimen='completo',
                               razon=f'Ingresos iguales o superiores a 142.206,50 UVB (≈ ${umbral_sarlaft:,.0f}): SARLAFT completo.'.replace(',', '.')))
        else:
            salida.append(dict(codigo='sarlaft_transporte', aplica='obligatorio', regimen='simplificado',
                               razon=f'Ingresos inferiores a 142.206,50 UVB (≈ ${umbral_sarlaft:,.0f}): Régimen de Medidas Simplificadas.'.replace(',', '.')))
        reg_ptee = 'responsable' if (ingresos is not None and ingresos < umbral_sarlaft) else 'oficial'
        salida.append(dict(codigo='ptee_transporte', aplica='obligatorio', regimen=reg_ptee,
                           razon='Persona jurídica vigilada por la Supertransporte: PTEE obligatorio (plazo ampliado al 18-ago-2026). '
                                 + ('Por sus ingresos puede designar un responsable de cumplimiento interno.' if reg_ptee == 'responsable'
                                    else 'Requiere oficial de cumplimiento (puede ser el mismo del SARLAFT).')))

    if supervisada_supersociedades:
        base = max(ingresos or 0, activos or 0)
        if ingresos is None and activos is None:
            salida.append(dict(codigo='sagrilaft', aplica='probable', regimen=None,
                               razon='Supervisada por la Supersociedades: depende de ingresos o activos frente a 30.000 SMLMV (varía por sector).'))
        elif base >= umbral_sagrilaft:
            salida.append(dict(codigo='sagrilaft', aplica='obligatorio', regimen='completo',
                               razon=f'Ingresos o activos iguales o superiores a 30.000 SMLMV (≈ ${umbral_sagrilaft:,.0f}).'.replace(',', '.')))
        else:
            salida.append(dict(codigo='sagrilaft', aplica='recomendado', regimen='minimo',
                               razon='Por debajo del umbral general; algunos sectores tienen umbrales menores y el régimen de medidas mínimas sigue siendo buena práctica.'))

    if activos is not None and activos > umbral_rnbd:
        salida.append(dict(codigo='datos_personales', aplica='obligatorio', regimen='rnbd',
                           razon=f'Activos superiores a 100.000 UVT (≈ ${umbral_rnbd:,.0f}): inscripción y actualización anual en el RNBD, además del programa documental.'.replace(',', '.')))
    else:
        salida.append(dict(codigo='datos_personales', aplica='obligatorio', regimen='documental',
                           razon='Toda empresa que trata datos de empleados o clientes debe tener política, autorizaciones y aviso de privacidad. '
                                 + ('Con activos superiores a 100.000 UVT se suma el RNBD.' if activos is None else 'Por sus activos no debe inscribirse en el RNBD.')))

    for s in salida:
        s['nombre'] = PROGRAMAS[s['codigo']]['nombre']
        s['nombre_regimen'] = PROGRAMAS[s['codigo']]['regimenes'].get(s['regimen']) if s['regimen'] else None
    return salida


def parametros_vigentes():
    """Para mostrar en la interfaz de dónde salen los umbrales."""
    return [dict(nombre=k, **v) for k, v in PARAMETROS.items()]


def meses_restantes(fecha, hoy=None):
    hoy = hoy or date.today()
    return max(0, ceil((fecha - hoy).days / 30))
