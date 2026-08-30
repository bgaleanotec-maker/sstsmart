# -*- coding: utf-8 -*-
"""Siembra/actualiza la Matriz Legal SG-SST con la normatividad colombiana
vigente a agosto de 2026 (verificada contra fuentes oficiales y especializadas).

Uso:  python scripts/seed_matriz_legal.py

Idempotente: hace upsert por (norma, articulo). No borra requisitos creados
manualmente. Las normas DEROGADAS de la versión anterior de la matriz se
marcan en la descripción de su reemplazo.

IMPORTANTE (cambios clave 2022-2026 que esta siembra ya incorpora):
- Res. 2404/2019 (psicosocial)  -> DEROGADA por Res. 2764/2022
- Res. 2346/2007 (ex. médicos)  -> DEROGADA por Res. 1843/2025
- Res. 652 y 1356/2012 (convivencia) -> DEROGADAS por Res. 3461/2025
- Reforma laboral: Ley 2466/2025 (jornada, teletrabajo, plataformas)
- Jornada máxima 42 h/semana desde 15-jul-2026 (Ley 2101/2021)
- Autoevaluación Res. 0312 se registra en la app SGRL del Fondo de
  Riesgos Laborales (Circulares 009/2025 y 027/2026 de Mintrabajo)
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.matriz_legal import RequisitoLegal

# (norma, articulo, descripcion, entidad, anio)
REQUISITOS = [
    # ---------- Marco núcleo ----------
    ("Ley 1562 de 2012", "Toda la norma",
     "Ley marco del Sistema General de Riesgos Laborales. Define AT/EL, obliga "
     "a implementar el SG-SST y a la afiliación de trabajadores a la ARL.",
     "Congreso de la República", 2012),

    ("Decreto 1072 de 2015", "Arts. 2.2.4.6.1 a 2.2.4.6.42",
     "Decreto Único Reglamentario del Sector Trabajo. Capítulo 6: obligación de "
     "implementar el SG-SST bajo ciclo PHVA: política SST firmada, plan anual de "
     "trabajo, matriz de peligros, objetivos e indicadores, gestión del cambio, "
     "adquisiciones, contratistas, auditoría anual, revisión por la alta "
     "dirección y conservación documental (20 años para registros clave).",
     "Ministerio del Trabajo", 2015),

    ("Decreto 1072 de 2015", "Cap. 2.2.4.11 (ex Decreto 472 de 2015)",
     "Criterios de graduación de multas por incumplimiento del SG-SST y normas "
     "de riesgos laborales. Rangos por tamaño de empresa en SMMLV (micro hasta "
     "~55, gran empresa hasta 1.000 SMMLV; clausuras Ley 1610 de 2013). "
     "SMMLV 2026: $1.750.905 (Decretos 1469/1470 de 2025 y 159 de 2026 — "
     "valor con contingencia jurídica, parametrizar).",
     "Ministerio del Trabajo", 2015),

    ("Resolución 0312 de 2019", "Arts. 3, 9, 16 (estándares por tamaño)",
     "Estándares mínimos del SG-SST: 7 estándares (≤10 trabajadores riesgo "
     "I-III), 21 estándares (11-50 trabajadores riesgo I-III), 60 estándares "
     "(>50 trabajadores o riesgo IV-V).",
     "Ministerio del Trabajo", 2019),

    ("Resolución 0312 de 2019", "Arts. 25-28 (fases anuales)",
     "Autoevaluación anual en diciembre, plan de mejoramiento, plan anual de "
     "trabajo del año siguiente y seguimiento en julio. Copia a la ARL. "
     "Registro anual obligatorio en la aplicación web SGRL del Fondo de Riesgos "
     "Laborales (Circular 009/2025 vigencia 2024; Circular 027/2026 vigencia "
     "2025 con plazo 31-jul-2026).",
     "Ministerio del Trabajo", 2019),

    ("Resolución 0312 de 2019", "Art. 30 (indicadores mínimos)",
     "Indicadores mínimos de SST: frecuencia y severidad de accidentalidad, "
     "mortalidad proporcional por AT, prevalencia e incidencia de enfermedad "
     "laboral y ausentismo por causa médica.",
     "Ministerio del Trabajo", 2019),

    # ---------- Psicosocial / convivencia / acoso ----------
    ("Resolución 2764 de 2022", "Toda la norma",
     "Batería de instrumentos de evaluación de factores de riesgo psicosocial "
     "(DEROGA la Res. 2404/2019). Periodicidad: anual si riesgo alto/muy alto, "
     "bienal si medio/bajo. Aplica psicólogo especialista; el empleador solo "
     "conserva resultados agregados, nunca los instrumentos individuales.",
     "Ministerio del Trabajo", 2022),

    ("Resolución 3461 de 2025", "Toda la norma",
     "Comités de Convivencia Laboral (DEROGA Res. 652 y 1356 de 2012). Comité "
     "por cada centro de trabajo, composición por rangos de personal, funciones "
     "preventivas reforzadas y armonización con el Convenio 190 OIT (violencia "
     "y acoso). Gestión confidencial de quejas y actas.",
     "Ministerio del Trabajo", 2025),

    ("Ley 1010 de 2006", "Toda la norma",
     "Acoso laboral: prevención, mecanismos internos de queja y protección al "
     "denunciante. Se articula con el Comité de Convivencia (Res. 3461/2025).",
     "Congreso de la República", 2006),

    ("Ley 2365 de 2024", "Toda la norma",
     "Prevención, protección y atención del acoso sexual en el ámbito laboral. "
     "Exige protocolo interno de prevención y atención de casos.",
     "Congreso de la República", 2024),

    # ---------- Medicina del trabajo ----------
    ("Resolución 1843 de 2025", "Toda la norma",
     "Evaluaciones médicas ocupacionales e historia clínica ocupacional "
     "(DEROGA Res. 2346/2007, 1918/2009, 1075/1992 y 4050/1994). Exámenes de "
     "ingreso, periódicos, de egreso y post-incapacidad; profesiograma; custodia "
     "de la historia clínica en la IPS/médico ocupacional, no en el empleador.",
     "Ministerio del Trabajo", 2025),

    # ---------- Comités y estructura ----------
    ("Resolución 2013 de 1986", "Toda la norma",
     "COPASST (Comité Paritario de SST): conformación, elecciones, reuniones "
     "mensuales y actas. Empresas de ≤10 trabajadores: Vigía de SST "
     "(D. 1072/2015).",
     "Ministerios de Trabajo y Salud", 1986),

    # ---------- Accidentes y enfermedades ----------
    ("Resolución 156 de 2005", "Toda la norma",
     "Formatos FURAT y FUREL para reporte de accidentes de trabajo y "
     "enfermedades laborales a ARL/EPS dentro de los 2 días hábiles. VIGENTE, "
     "modificada por Res. 2851/2015. (Verificar periódicamente si Mintrabajo "
     "habilita módulo de reporte AT/EL en la plataforma SGRL.)",
     "Ministerio de la Protección Social", 2005),

    ("Resolución 2851 de 2015", "Art. 1",
     "Amplía el reporte: AT graves y mortales y EL diagnosticadas deben "
     "informarse también a la Dirección Territorial del Ministerio del Trabajo "
     "dentro de los 2 días hábiles siguientes.",
     "Ministerio del Trabajo", 2015),

    ("Resolución 1401 de 2007", "Toda la norma",
     "Investigación de incidentes y accidentes de trabajo: equipo investigador, "
     "informe dentro de los 15 días, determinación de causas y medidas de "
     "intervención (metodología de causalidad).",
     "Ministerio de la Protección Social", 2007),

    ("Decreto 1530 de 1996", "Toda la norma",
     "Reglamenta AT mortal (investigación con participación de la ARL) y "
     "empresas de servicios temporales en riesgos laborales. Vigente en lo "
     "pertinente / compilado.",
     "Presidencia de la República", 1996),

    # ---------- Tareas de alto riesgo ----------
    ("Resolución 4272 de 2021", "Toda la norma",
     "Requisitos mínimos de seguridad para trabajo en alturas (derogó la Res. "
     "1409/2012; VIGENTE a 2026). Programa de prevención contra caídas, "
     "permisos de trabajo, coordinador de alturas, certificación y "
     "reentrenamiento del personal autorizado.",
     "Ministerio del Trabajo", 2021),

    ("Resolución 0491 de 2020", "Toda la norma",
     "Espacios confinados: requisitos de entrada segura, permisos, vigía, "
     "atmósferas peligrosas, entrenamiento y certificación.",
     "Ministerio del Trabajo", 2020),

    ("Resolución 1857 de 2024", "Toda la norma",
     "Requisitos de SST para trabajo seguro en calderas y equipos a presión "
     "(tarea de alto riesgo). [Verificación parcial: confirmar texto oficial.]",
     "Ministerio del Trabajo", 2024),

    # ---------- Modalidades de trabajo / jornada ----------
    ("Ley 2466 de 2025", "Reforma laboral",
     "Modifica +80 artículos del CST: consolidación de teletrabajo/trabajo "
     "remoto (auxilio de conectividad <2 SMMLV, control de jornada remota), "
     "riesgos laborales para trabajadores de plataformas digitales, recargos "
     "dominicales 100% y nocturno desde 7 p.m. (graduales). Impacto SST "
     "indirecto vía jornada, modalidades y cobertura.",
     "Congreso de la República", 2025),

    ("Ley 2101 de 2021", "Art. 3 (implementación gradual)",
     "Reducción de jornada máxima legal a 42 horas semanales desde el "
     "15-jul-2026 (última fase), sin reducción salarial. Afecta cálculo de "
     "horas-hombre para indicadores y programación de capacitaciones.",
     "Congreso de la República", 2021),

    ("Ley 2191 de 2022", "Toda la norma",
     "Desconexión laboral: política documentada y canal de quejas. Reforzada "
     "por la Ley 2466/2025 para modalidades remotas. Conecta con vigilancia de "
     "riesgo psicosocial.",
     "Congreso de la República", 2022),

    ("Ley 2088 de 2021", "Toda la norma",
     "Trabajo en casa (habilitación excepcional): auxilio de conectividad para "
     "quienes ganan <2 SMMLV y extensión de obligaciones SST al domicilio.",
     "Congreso de la República", 2021),

    # ---------- Higiene / base histórica ----------
    ("Ley 9 de 1979", "Título III",
     "Código Sanitario Nacional: disposiciones de salud ocupacional, "
     "condiciones ambientales, agentes químicos, físicos y biológicos.",
     "Congreso de la República", 1979),

    ("Resolución 2400 de 1979", "Toda la norma",
     "Estatuto de seguridad industrial: vivienda, higiene y seguridad en "
     "establecimientos de trabajo (orden y aseo, EPP, máquinas, incendios).",
     "Ministerio del Trabajo", 1979),

    ("GTC 45 (guía técnica)", "Guía voluntaria",
     "Metodología usual (no obligatoria por sí misma) para identificación de "
     "peligros y valoración de riesgos exigida por D. 1072/2015 art. "
     "2.2.4.6.15. La empresa puede adoptar otra metodología documentada.",
     "ICONTEC", 2012),

    ("Resolución 147 de 2024", "Toda la norma",
     "Formulario Único de Afiliación y Reporte de Novedades al Sistema General "
     "de Riesgos Laborales. [Verificación parcial: confirmar alcance.]",
     "Ministerio del Trabajo", 2024),
]


def seed():
    creados, actualizados = 0, 0
    for norma, articulo, descripcion, entidad, anio in REQUISITOS:
        req = RequisitoLegal.query.filter_by(norma=norma, articulo=articulo).first()
        if req:
            req.descripcion = descripcion
            req.entidad = entidad
            req.anio = anio
            actualizados += 1
        else:
            db.session.add(RequisitoLegal(
                norma=norma, articulo=articulo, descripcion=descripcion,
                entidad=entidad, anio=anio,
            ))
            creados += 1
    db.session.commit()
    print(f"Matriz legal: {creados} requisitos creados, {actualizados} actualizados.")
    print("Recuerda: la valoración jurídica (estado Cumple/No cumple) la hace el "
          "abogado/responsable SST en la app.")


if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG', 'development'))
    with app.app_context():
        seed()
