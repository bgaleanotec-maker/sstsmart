# Vertical 9 — Cumplimiento más allá de SST (SARLAFT, PTEE, SAGRILAFT, datos personales)

**Estado:** MVP construido el 8-nov-2026 como módulo `cumplimiento` del catálogo (rama `feat/E15-cumplimiento`).
Origen: Brian vio la pauta de Doctux S.A.S. en Facebook ("Kit SARLAFT para el sector transporte, $499.000 + IVA,
autogestionable") y pidió el mismo enfoque dentro de Justrabajo, habilitable por empresa, más los procesos afines
que una pyme pueda comprarle a una plataforma hecha por un abogado.

Revierte la nota de `06-verticales-candidatas.md` §3 ("descartado SAGRILAFT como producto propio"): no es un
producto aparte, es **un módulo más del mismo comprador** (la pyme que ya paga SST), como propuso la bandeja de
ideas el 23-oct-2026. El transporte es el gancho: las mismas transportadoras que necesitan PESV quedaron obligadas
al SARLAFT y al PTEE en 2025-2026.

## 1. Lo que dice la investigación (8-nov-2026)

Todo con fuente secundaria salvo donde se indica; **cada cita entra al producto con `[VERIFICAR]`** hasta que
Brian la confirme en el texto oficial (regla dura de `empresa/CLAUDE.md`).

| Programa | Autoridad y norma | A quién aplica | Fechas y datos clave |
|---|---|---|---|
| **SARLAFT transporte** (reemplaza al SIPLAFT) | Supertransporte, Res. 2328 del 6-mar-2025 (cap. 6, título V de la Circular Única), modificada por Res. 16615/2025 y Res. 4607/2026; Circular Externa 20265330000054 del 6-may-2026 fija la supervisión | Vigilados del art. 4.1.1 de la Circular Única (carga, pasajeros, especial, mixto, por cable, multimodal, desintegradoras). Ingresos del año anterior ≥ **142.206,50 UVB** → SARLAFT completo; por debajo → **Régimen de Medidas Simplificadas (RMS)** | UVB ≈ $12.110 (jun-2026) → umbral ≈ $1.722 millones. Primer reporte obligatorio: **10-ago-2026** (Acoltés). Oficial principal y suplente con acta, hoja de vida, formación en riesgos y registro en **SIREL**; un oficial externo atiende hasta **10 vigiladas**. Sanciones: art. 46 Ley 336/1996 (monto no confirmado). Fechas periódicas citadas por Acoltés son incoherentes: verificar la circular |
| **PTEE transporte** | Supertransporte, Res. 14673 del 18-sep-2025 (cap. 10, título V); Res. 7038 del 15-may-2026 amplía el plazo | Personas jurídicas vigiladas. Ingresos ≤ 142.206,50 UVB → pueden designar **responsable de cumplimiento** interno en vez de oficial | Plazo ampliado al **18-ago-2026** (ya venció: lo que sigue es supervisión). Publicación web obligatoria (art. 5.10.23) y reporte de soborno transnacional a Supersociedades (art. 5.10.27, Ley 1778/2016) |
| **SAGRILAFT / PTEE Supersociedades** | Circular 100-000016/2020 (mod. 100-000004/2021, 100-300000/2024), Circular Básica Jurídica 100-000002/2025; PTEE Circular 100-000011/2021 | Ingresos o activos ≥ 30.000 SMLMV (varios sectores; otros tienen umbral propio) o criptoactivos ≥ 100 SMLMV | Actualización **cada dos años** (quien implementó en 2024 actualiza en 2026). Proyecto de circular que unifica SAGRILAFT y PTEE: no expedido. Sanción real: Impoamericana Roger S.A.S., 19-feb-2026 (Ley 2195) |
| **Datos personales / RNBD** | SIC; Ley 1581/2012, Decreto 1377/2013 (compilado en el 1074/2015), Decreto 090/2018 | Programa documental: todas. RNBD: sociedades y ESAL con activos > **100.000 UVT** y entidades públicas | Actualización anual **2-ene a 31-mar**; reclamos semestrales (2026: 20-feb y 25-ago, fijadas por la SIC); cambios sustanciales en los 10 días hábiles del mes siguiente; base nueva en 2 meses. Proyecto de la SIC que cambia plazos desde 2027 (informe anual al 15-mar) |

Otros procesos afines detectados (no construidos; ver §5): canal de denuncias y beneficiario final (Ley 2195/2022,
RUB), cobro de cartera con factura electrónica como título valor (Ley 1231/2008, Decreto 1074/2015, RADIAN,
proyecto de decreto de ene-2026 con "juramento del emisor"), comité de convivencia y acoso (ya en SST), reforma
laboral Ley 2466/2025 (contratos y jornadas).

## 2. Competencia y precio

| Actor | Oferta | Precio |
|---|---|---|
| Doctux S.A.S. (pauta en Facebook, nov-2026) | Kit SARLAFT transporte autogestionable: documentos para "cumplir antes de que te sancionen" | **$499.000 + IVA**, una vez |
| Odoo `l10n_co_sagrilaft` (v19) | Módulo con listas ONU/OFAC y reportes UIAF | 1.985 (moneda no indicada) |
| Consultoras (Pirani, GAC, Risk Global, Affirma) | Implementación asistida y software de riesgos | No publican precio; Big Four para grandes |
| Oficiales de cumplimiento externos | Honorario mensual por empresa | Mercado fragmentado |

**Propuesta de precio (no decisión; D6 pendiente):** módulo `cumplimiento` a **$180.000/mes** de lista, con los
cuatro programas incluidos. Argumento frente al kit de $499.000: el kit son documentos; esto es la operación
(contrapartes verificadas con fecha y fuente, matriz viva, reportes con alarma, evidencia ordenada para la visita
de la Supertransporte). Un transportador con SST + PESV + cumplimiento se queda por tres obligaciones distintas.

## 3. Lo construido (MVP)

- **Catálogo** `app/data/programas_cumplimiento.py`: 4 programas, 43 requisitos por etapas (diseño, identificación,
  control, operación, reporte, monitoreo), regímenes por programa (completo/simplificado, oficial/responsable,
  rnbd/documental), reportes con fecha fija y `PARAMETROS` (UVB, UVT, SMMLV, umbrales) en un solo lugar con fuente
  y `verificado=False`.
- **Modelos tenant** (`app/models/cumplimiento.py`, tablas `cumpl_*`): `ProgramaCumplimiento` (régimen, oficial,
  SIREL, acta), `RequisitoCumplimiento` (estado, evidencia, revisión periódica), `Contraparte` (debida diligencia
  compartida por los programas: tipo, PEP, riesgo, verificación con fecha y fuente, bloqueo ante coincidencia),
  `RiesgoCumplimiento` (probabilidad × impacto, inherente y residual), `ReporteCumplimiento` (fecha límite,
  radicado, `verificado`).
- **Servicio** `app/services/cumplimiento_service.py`: activar programa (crea requisitos y reportes a 12 meses,
  idempotente), cambio de régimen sin perder evidencia, avance (%), diagnóstico "¿me aplica?" con los umbrales del
  catálogo, niveles de riesgo.
- **Listas vinculantes** `app/services/listas_restrictivas.py`: lector del XML público de la lista consolidada de la
  ONU (`LISTA_ONU_URL`, caché por proceso), búsqueda por nombre normalizado (tokens o similitud ≥ 0,88) y enlaces a
  OFAC y UE para consulta manual. Sin URL, solo consulta manual registrada. Nunca scraping ni evasión de controles.
- **Rutas** `/cumplimiento` (índice + diagnóstico, programa con oficial/requisitos/reportes, matriz de riesgos,
  contrapartes). Rol nuevo `Oficial_Cumplimiento`; escriben Admin, Gerente, Abogado y el oficial; leen todos.
- **Integración**: módulo `cumplimiento` en el catálogo ($180.000 propuesto), KPI "Otras obligaciones pendientes"
  en el panel, reportes/revisiones/reverificaciones en "Lo que vence pronto", grupo "Otras obligaciones" en la
  barra lateral, `seed_demo.py` con SARLAFT simplificado y 3 contrapartes.
- **Pruebas**: `tests/test_cumplimiento.py` (10) + 5 modelos en el test de aislamiento; 128 en total en verde.
  QA de rutas: 90 GET, 0 fallos. Capturas 15-17 en `rediseno-ui/capturas-qa/`.

## 4. Lo que falta (backlog E15, en orden)

| Historia | Criterio |
|---|---|
| E15.1 Brian verifica las normas del catálogo y las fechas de reporte (`verificado=True`) | La interfaz deja de mostrar `[VERIFICAR]`; texto de la Circular 20265330000054 y Res. 4607/2026 en `biblioteca_juridica` |
| E15.2 Generador de documentos base (política LA/FT, política anticorrupción, política de tratamiento de datos, acta de designación) con el motor de documentos de E2.4 | DOCX/PDF con etiqueta de IA y aviso de autoservicio; el usuario firma |
| E15.3 Recordatorios de reportes y reverificaciones por correo/WhatsApp (job en `scheduler.py`, 7/3/1 días) | Reutiliza `avisos` del CRM Legal; idempotente |
| E15.4 Señales de alerta por contraparte y registro de operaciones inusuales → borrador de ROS (sin enviarlo) | El ROS lo presenta el oficial en SIREL; la app solo documenta |
| E15.5 Red de oficiales de cumplimiento externos (perfil, cupo de 10 vigiladas, pago por empresa atendida) | Sin cobrar comisión al profesional por cliente (Ley 1123 art. 30 num. 5 si es abogado) |
| E15.6 Lista OFAC SDN descargable (CSV público) además de la ONU | Misma búsqueda; fuente registrada |
| E15.7 Landing `/cumplimiento` para transportadores (SST + PESV + SARLAFT en una sola plataforma) | Sin promesas de resultado; precio con IVA |

## 5. Procesos afines que una pyme compraría (propuesta, por evaluar)

1. **Cobro de cartera y procesos ejecutivos** (lo que Brian llamó "gestión de procesos ejecutivos"): la pyme
   registra facturas vencidas, la app calcula prescripción de la acción cambiaria (3 años, art. 789 C. de Co.
   `[VERIFICAR]`), intereses de mora a la tasa de usura y prepara el expediente (XML, representación gráfica,
   constancia de recibo, trazabilidad RADIAN) para que **un abogado** radique el ejecutivo. Encaja con el CRM
   Legal (`Proceso`) y con Radar Judicial para seguir el proceso. Riesgo: la S.A.S. no litiga; deriva sin comisión.
2. **Canal de denuncias y beneficiario final** (Ley 2195/2022 y RUB de la DIAN): formulario confidencial, registro
   de denuncias con protección al denunciante, recordatorio anual de actualización del RUB. Es un requisito del
   PTEE y lo piden también a quienes no están vigilados.
3. **Propiedad horizontal: cobro de cuotas** (ya en `06-verticales-candidatas.md`): el certificado del
   administrador es título ejecutivo; mismo motor que el punto 1.
4. **Contratos y reforma laboral (Ley 2466/2025)**: generador de contratos, otrosíes y reglamento interno
   actualizado, con alertas de jornada y recargos. Cruza con el conflicto de interés de D3.
5. **SG-SST de contratistas**: verificación documental de contratistas (planilla, afiliación, SST) con la misma
   tabla de contrapartes.

## 6. Decisiones que necesita Brian

- **D-C1** Precio del módulo ($180.000/mes propuesto) y si se vende solo o como complemento de SST/PESV.
- **D-C2** Verificar las citas de §1 (en especial las fechas periódicas de reporte a la Supertransporte).
- **D-C3** ¿Red de oficiales de cumplimiento externos como parte del producto (E15.5) o solo software?
- **D-C4** ¿Cobro de cartera como vertical propia (sección 5.1) o dentro del CRM Legal?

## Fuentes (8-nov-2026)

- Supertransporte, página SARLAFT-PTEE: https://www.supertransporte.gov.co/index.php/sarlaft/
- Acoltés, lineamientos SARLAFT y RMS (Circular 20265330000054/2026): https://acoltes.org/supertransporte-fijo-nuevos-lineamientos-para-sarlaft-y-regimen-de-medidas-simplificadas/
- Garrigues, Res. 7038/2026 (PTEE, UVB, responsable de cumplimiento): https://www.garrigues.com/es_ES/noticia/colombia-sector-transporte-introduce-nuevas-definiciones-flexibilizacion-designacion.md
- Compliance.com.co, Res. 2328/2025: https://www.compliance.com.co/el-sarlaft-sera-obligatorio-en-el-sector-transporte-por-la-resolucion-2328-de-2025/
- Deloitte, SARLAFT sector transporte: https://www.deloitte.com/latam/es/services/legal/perspectives/sarlaft-sector-transporte.html
- Pérez-Llorca, RNBD 2026: https://www.perezllorca.com/es-co/actualidad/boletin/nuevas-obligaciones-del-rnbd/
- Gómez-Pinzón en Asuntos Legales, RNBD (2021): https://www.asuntoslegales.com.co/consultorio/la-actualizacion-del-registro-nacional-de-bases-de-datos-3139521
- Supersociedades, SAGRILAFT: https://www.supersociedades.gov.co/web/asuntos-economicos-societarios/sagrilaft
- Siempre al Día, factura electrónica como título valor (proyecto de decreto 2026): https://siemprealdia.co/colombia/impuestos/factura-electronica-como-titulo-valor/
- PPU Legal, caso Impoamericana (Ley 2195): https://ppulegal.com/actualidad-legal/la-ley-2195-muestra-los-dientes-caso-impoamericana/
- Odoo, módulo SAGRILAFT: https://apps.odoo.com/apps/modules/19.0/l10n_co_sagrilaft
- Pauta de Doctux S.A.S. (captura de Brian, 8-nov-2026): kit SARLAFT $499.000 + IVA.
