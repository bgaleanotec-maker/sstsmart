# -*- coding: utf-8 -*-
"""Tabla de valores de los Estándares Mínimos del SG-SST — Resolución 0312 de 2019.

60 ítems agrupados por ciclo PHVA; los puntajes suman 100 (art. 27).
`en7` / `en21` marcan los subconjuntos exigibles a empresas de ≤10 trabajadores
riesgo I-III (art. 3) y de 11-50 trabajadores riesgo I-III (art. 9). Todos los
ítems aplican al régimen de 60 (art. 16).

Regla de cálculo (arts. 27-28): ítem que CUMPLE → puntaje pleno; NO CUMPLE → 0;
NO APLICA justificado → puntaje pleno. Los ítems que no son exigibles para el
régimen de la empresa (7 o 21) se califican con el puntaje pleno.
Clasificación del resultado: CRÍTICO < 60 · MODERADAMENTE ACEPTABLE 60-85 ·
ACEPTABLE > 85.

Los textos son resúmenes operativos del ítem, no transcripción literal de la
norma; para efectos legales consulte el texto oficial de la Resolución 0312.
"""

# (codigo, ciclo, estandar, descripcion, puntaje, en7, en21)
ESTANDARES = [
    # ================= I. PLANEAR — RECURSOS (10%) =================
    ("1.1.1", "PLANEAR", "Recursos financieros, técnicos y humanos",
     "Responsable del SG-SST designado, con licencia SST vigente (o curso de 50 horas según el caso)", 0.5, True, True),
    ("1.1.2", "PLANEAR", "Recursos financieros, técnicos y humanos",
     "Responsabilidades en SST asignadas y documentadas en todos los niveles", 0.5, False, False),
    ("1.1.3", "PLANEAR", "Recursos financieros, técnicos y humanos",
     "Asignación de recursos financieros, técnicos y humanos para el SG-SST", 0.5, False, True),
    ("1.1.4", "PLANEAR", "Recursos financieros, técnicos y humanos",
     "Afiliación de todos los trabajadores al Sistema General de Riesgos Laborales", 0.5, True, True),
    ("1.1.5", "PLANEAR", "Recursos financieros, técnicos y humanos",
     "Pago de pensión de alto riesgo para trabajadores expuestos (Decreto 2090/2003)", 0.5, False, False),
    ("1.1.6", "PLANEAR", "Recursos financieros, técnicos y humanos",
     "COPASST o Vigía de SST conformado y en funcionamiento", 0.5, False, True),
    ("1.1.7", "PLANEAR", "Recursos financieros, técnicos y humanos",
     "Capacitación de los integrantes del COPASST / Vigía", 0.5, False, False),
    ("1.1.8", "PLANEAR", "Recursos financieros, técnicos y humanos",
     "Comité de Convivencia Laboral conformado y en funcionamiento (Res. 3461/2025)", 0.5, False, True),
    ("1.2.1", "PLANEAR", "Capacitación en el SG-SST",
     "Programa de capacitación anual en promoción y prevención, con cobertura a todos los trabajadores", 2.0, True, True),
    ("1.2.2", "PLANEAR", "Capacitación en el SG-SST",
     "Inducción y reinducción en SST a todos los trabajadores", 2.0, False, False),
    ("1.2.3", "PLANEAR", "Capacitación en el SG-SST",
     "Curso virtual de 50 horas del responsable del SG-SST (y actualización de 20 horas)", 2.0, False, False),

    # ============ I. PLANEAR — GESTIÓN INTEGRAL DEL SG-SST (15%) ============
    ("2.1.1", "PLANEAR", "Política de SST",
     "Política de SST escrita, firmada, fechada, divulgada y actualizada", 1.0, False, True),
    ("2.2.1", "PLANEAR", "Objetivos del SG-SST",
     "Objetivos del SG-SST definidos, medibles, con metas, documentados y revisados", 1.0, False, False),
    ("2.3.1", "PLANEAR", "Evaluación inicial",
     "Evaluación inicial (autoevaluación) del SG-SST realizada", 1.0, False, False),
    ("2.4.1", "PLANEAR", "Plan anual de trabajo",
     "Plan anual de trabajo con objetivos, metas, responsables, recursos y cronograma, firmado", 2.0, True, True),
    ("2.5.1", "PLANEAR", "Conservación documental",
     "Archivo y retención documental del SG-SST (20 años para los registros del art. 2.2.4.6.13)", 2.0, False, True),
    ("2.6.1", "PLANEAR", "Rendición de cuentas",
     "Rendición anual de cuentas sobre el desempeño en SST de quienes tienen responsabilidades", 1.0, False, False),
    ("2.7.1", "PLANEAR", "Normatividad",
     "Matriz legal actualizada con la normatividad vigente en riesgos laborales aplicable", 2.0, False, False),
    ("2.8.1", "PLANEAR", "Comunicación",
     "Mecanismos de comunicación interna y externa del SG-SST y canal para inquietudes de trabajadores", 1.0, False, False),
    ("2.9.1", "PLANEAR", "Adquisiciones",
     "Procedimiento para identificar especificaciones de SST en compras y adquisiciones", 1.0, False, False),
    ("2.10.1", "PLANEAR", "Contratación",
     "Criterios de SST para evaluación y selección de proveedores y contratistas", 2.0, False, False),
    ("2.11.1", "PLANEAR", "Gestión del cambio",
     "Procedimiento de gestión del cambio: evaluación del impacto en SST de cambios internos y externos", 1.0, False, False),

    # ============ II. HACER — GESTIÓN DE LA SALUD (20%) ============
    ("3.1.1", "HACER", "Condiciones de salud en el trabajo",
     "Descripción sociodemográfica y diagnóstico de condiciones de salud de los trabajadores", 1.0, False, True),
    ("3.1.2", "HACER", "Condiciones de salud en el trabajo",
     "Actividades de medicina del trabajo y de promoción y prevención según prioridades", 1.0, False, True),
    ("3.1.3", "HACER", "Condiciones de salud en el trabajo",
     "Perfiles de cargo (profesiograma) informados al médico evaluador para los exámenes", 1.0, False, False),
    ("3.1.4", "HACER", "Condiciones de salud en el trabajo",
     "Evaluaciones médicas ocupacionales de ingreso, periódicas y de egreso (Res. 1843/2025)", 1.0, True, True),
    ("3.1.5", "HACER", "Condiciones de salud en el trabajo",
     "Custodia de las historias clínicas ocupacionales por la IPS o médico evaluador", 1.0, False, False),
    ("3.1.6", "HACER", "Condiciones de salud en el trabajo",
     "Cumplimiento de restricciones y recomendaciones médico-laborales", 1.0, False, True),
    ("3.1.7", "HACER", "Condiciones de salud en el trabajo",
     "Estilos de vida y entornos saludables (tabaquismo, alcoholismo, farmacodependencia)", 1.0, False, False),
    ("3.1.8", "HACER", "Condiciones de salud en el trabajo",
     "Agua potable, servicios sanitarios y disposición de basuras", 1.0, False, False),
    ("3.1.9", "HACER", "Condiciones de salud en el trabajo",
     "Eliminación adecuada de residuos sólidos, líquidos y gaseosos", 1.0, False, False),
    ("3.2.1", "HACER", "Registro y reporte de AT/EL",
     "Reporte de accidentes de trabajo y enfermedades laborales a ARL, EPS y Dirección Territorial (2 días hábiles)", 2.0, False, True),
    ("3.2.2", "HACER", "Registro y reporte de AT/EL",
     "Investigación de incidentes, accidentes de trabajo y enfermedades laborales (Res. 1401/2007)", 2.0, False, True),
    ("3.2.3", "HACER", "Registro y reporte de AT/EL",
     "Registro y análisis estadístico de accidentes e incidentes de trabajo y enfermedad laboral", 1.0, False, False),
    ("3.3.1", "HACER", "Vigilancia de condiciones de salud",
     "Medición de la frecuencia de la accidentalidad (mínimo mensual)", 1.0, False, False),
    ("3.3.2", "HACER", "Vigilancia de condiciones de salud",
     "Medición de la severidad de la accidentalidad (mínimo mensual)", 1.0, False, False),
    ("3.3.3", "HACER", "Vigilancia de condiciones de salud",
     "Medición de la mortalidad por accidentes de trabajo (mínimo anual)", 1.0, False, False),
    ("3.3.4", "HACER", "Vigilancia de condiciones de salud",
     "Medición de la prevalencia de enfermedad laboral (mínimo anual)", 1.0, False, False),
    ("3.3.5", "HACER", "Vigilancia de condiciones de salud",
     "Medición de la incidencia de enfermedad laboral (mínimo anual)", 1.0, False, False),
    ("3.3.6", "HACER", "Vigilancia de condiciones de salud",
     "Medición del ausentismo por causa médica (mínimo mensual)", 1.0, False, False),

    # ======== II. HACER — GESTIÓN DE PELIGROS Y RIESGOS (30%) ========
    ("4.1.1", "HACER", "Identificación de peligros y valoración de riesgos",
     "Metodología documentada para identificación de peligros y valoración de riesgos (p. ej. GTC 45)", 4.0, False, False),
    ("4.1.2", "HACER", "Identificación de peligros y valoración de riesgos",
     "Identificación de peligros y valoración de riesgos anual, con participación de los trabajadores", 4.0, True, True),
    ("4.1.3", "HACER", "Identificación de peligros y valoración de riesgos",
     "Identificación y priorización de sustancias catalogadas como carcinógenas o de toxicidad aguda", 3.0, False, False),
    ("4.1.4", "HACER", "Identificación de peligros y valoración de riesgos",
     "Mediciones ambientales físicas, químicas y biológicas cuando aplique", 4.0, False, False),
    ("4.2.1", "HACER", "Medidas de prevención y control",
     "Medidas de prevención y control con base en la jerarquía de controles, ejecutadas", 2.5, True, False),
    ("4.2.2", "HACER", "Medidas de prevención y control",
     "Verificación de la aplicación de las medidas por parte de los trabajadores", 2.5, False, False),
    ("4.2.3", "HACER", "Medidas de prevención y control",
     "Procedimientos e instructivos internos de SST elaborados y divulgados", 2.5, False, False),
    ("4.2.4", "HACER", "Medidas de prevención y control",
     "Inspecciones sistemáticas a instalaciones, maquinaria y equipos con participación del COPASST", 2.5, False, False),
    ("4.2.5", "HACER", "Medidas de prevención y control",
     "Mantenimiento periódico de instalaciones, equipos, máquinas y herramientas", 2.5, False, True),
    ("4.2.6", "HACER", "Medidas de prevención y control",
     "Entrega y reposición de EPP verificada, con capacitación en su uso", 2.5, False, True),

    # ======== II. HACER — GESTIÓN DE AMENAZAS (10%) ========
    ("5.1.1", "HACER", "Plan de prevención y respuesta ante emergencias",
     "Plan de prevención, preparación y respuesta ante emergencias, con análisis de amenazas y simulacros", 5.0, False, True),
    ("5.1.2", "HACER", "Plan de prevención y respuesta ante emergencias",
     "Brigada de prevención, preparación y respuesta conformada, capacitada y dotada", 5.0, False, True),

    # ======== III. VERIFICAR (5%) ========
    ("6.1.1", "VERIFICAR", "Gestión y resultados del SG-SST",
     "Definición y seguimiento de indicadores de estructura, proceso y resultado del SG-SST", 1.25, False, False),
    ("6.1.2", "VERIFICAR", "Gestión y resultados del SG-SST",
     "Auditoría anual del SG-SST", 1.25, False, False),
    ("6.1.3", "VERIFICAR", "Gestión y resultados del SG-SST",
     "Revisión anual por la alta dirección con alcance sobre todo el SG-SST", 1.25, False, True),
    ("6.1.4", "VERIFICAR", "Gestión y resultados del SG-SST",
     "Planificación de la auditoría con participación del COPASST", 1.25, False, False),

    # ======== IV. ACTUAR — MEJORAMIENTO (10%) ========
    ("7.1.1", "ACTUAR", "Acciones preventivas y correctivas",
     "Acciones preventivas y correctivas con base en los resultados del SG-SST", 2.5, False, False),
    ("7.1.2", "ACTUAR", "Acciones preventivas y correctivas",
     "Acciones de mejora conforme a la revisión de la alta dirección", 2.5, False, False),
    ("7.1.3", "ACTUAR", "Acciones preventivas y correctivas",
     "Acciones de mejora con base en investigaciones de AT/EL y de incidentes", 2.5, False, False),
    ("7.1.4", "ACTUAR", "Acciones preventivas y correctivas",
     "Implementación de planes de mejoramiento solicitados por la ARL o el Ministerio del Trabajo", 2.5, False, False),
]

assert abs(sum(e[4] for e in ESTANDARES) - 100.0) < 1e-6, "los puntajes deben sumar 100"
assert len(ESTANDARES) == 60, "deben ser 60 ítems"
assert sum(1 for e in ESTANDARES if e[5]) == 7, "el régimen mínimo son 7 estándares"
assert sum(1 for e in ESTANDARES if e[6]) == 21, "el régimen básico son 21 estándares"


def items_para_regimen(regimen):
    """Ítems exigibles para un régimen (7, 21 o 60)."""
    if regimen == 7:
        return [e for e in ESTANDARES if e[5]]
    if regimen == 21:
        return [e for e in ESTANDARES if e[6]]
    return list(ESTANDARES)


def clasificar(puntaje):
    """Art. 28: CRÍTICO <60 · MODERADAMENTE ACEPTABLE 60-85 · ACEPTABLE >85."""
    if puntaje < 60:
        return 'CRITICO'
    if puntaje <= 85:
        return 'MODERADO'
    return 'ACEPTABLE'


ACCIONES_POR_CLASIFICACION = {
    'CRITICO': ("Realizar y tener a disposición del Ministerio del Trabajo un plan de "
                "mejoramiento de inmediato, enviar reporte a la ARL y someterse a visita "
                "de verificación."),
    'MODERADO': ("Realizar y tener a disposición del Ministerio del Trabajo un plan de "
                 "mejoramiento y enviar reporte de avances a la ARL dentro de los seis (6) "
                 "meses siguientes."),
    'ACEPTABLE': ("Mantener la calificación y las evidencias, y continuar el plan anual "
                  "de trabajo del SG-SST."),
}
