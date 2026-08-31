# -*- coding: utf-8 -*-
"""Catálogo de módulos comerciales de Justrabajo.

Único punto de verdad para: qué módulos existen, su precio de lista mensual
(COP), qué blueprint protegen y cómo se muestran. La contratación por empresa
vive en EmpresaModulo (app/models/suscripcion.py); si una empresa tiene un
precio pactado distinto, ese manda.

Descuento por volumen (sobre el subtotal de lista):
  3-4 módulos → 10% · 5-6 módulos → 15% · 7 (todos) → 20%
Ejemplo: 4 módulos núcleo (reportes + autoevaluación + matriz legal +
controles) = $540.000 − 10% = $486.000/mes ≈ el "4 módulos ~ $500 mil".
"""

# codigo: (nombre, precio_lista_mensual, blueprint, icono FontAwesome, descripcion corta)
MODULOS = {
    'sgsst': {
        'nombre': 'Política y plan de trabajo',
        'precio': 130_000,
        'blueprint': 'sgsst',
        'icono': 'fa-file-signature',
        'descripcion': 'Política SST versionada y firmada, plan anual con semáforo e indicadores del art. 30.',
    },
    'epp': {
        'nombre': 'EPP y dotación',
        'precio': 100_000,
        'blueprint': 'epp',
        'icono': 'fa-helmet-safety',
        'descripcion': 'Kardex de entregas con constancia, certificaciones y alertas de reposición: tu prueba de defensa.',
    },
    'autoevaluacion': {
        'nombre': 'Autoevaluación 0312',
        'precio': 150_000,
        'blueprint': 'autoevaluacion',
        'icono': 'fa-clipboard-check',
        'descripcion': 'Estándares mínimos 7/21/60, puntaje, plan de mejoramiento y export para SGRL.',
    },
    'reportes': {
        'nombre': 'Reportes e incidentes',
        'precio': 120_000,
        'blueprint': 'reportes',
        'icono': 'fa-triangle-exclamation',
        'descripcion': 'Condiciones inseguras con foto, asignación automática, SLA y escalamiento.',
    },
    'matriz_legal': {
        'nombre': 'Matriz legal viva',
        'precio': 150_000,
        'blueprint': 'matriz_legal',
        'icono': 'fa-scale-balanced',
        'descripcion': 'Normatividad SST vigente, valoración jurídica y evidencias versionadas.',
    },
    'controles': {
        'nombre': 'Controles y riesgos',
        'precio': 120_000,
        'blueprint': 'controles',
        'icono': 'fa-shield-halved',
        'descripcion': 'Ciclo de vida de controles, jerarquía, seguimientos y efectividad.',
    },
    'formacion': {
        'nombre': 'Formación',
        'precio': 100_000,
        'blueprint': 'formacion',
        'icono': 'fa-graduation-cap',
        'descripcion': 'Cursos, exámenes, certificados y ranking de tu equipo.',
    },
    'juridico': {
        'nombre': 'Jurídico',
        'precio': 200_000,
        'blueprint': 'juridico',
        'icono': 'fa-gavel',
        'descripcion': 'Consultas con abogado, SLA por prioridad, conceptos y expediente PDF.',
    },
    'ia': {
        'nombre': 'Asistente IA',
        'precio': 80_000,
        'blueprint': 'ia',
        'icono': 'fa-wand-magic-sparkles',
        'descripcion': 'Análisis de fotos de condiciones inseguras y experto SST que cita la norma.',
    },
}

# blueprint -> codigo de módulo (para el gating por request)
BLUEPRINT_A_MODULO = {v['blueprint']: k for k, v in MODULOS.items()}


def descuento_por_volumen(n_modulos):
    if n_modulos >= 8:
        return 0.20
    if n_modulos >= 5:
        return 0.15
    if n_modulos >= 3:
        return 0.10
    return 0.0


def cotizar(codigos):
    """[(codigo, precio_lista)], subtotal, descuento, total para una selección."""
    lineas = [(c, MODULOS[c]['precio']) for c in codigos if c in MODULOS]
    subtotal = sum(p for _, p in lineas)
    desc = descuento_por_volumen(len(lineas))
    total = round(subtotal * (1 - desc))
    return lineas, subtotal, desc, total
