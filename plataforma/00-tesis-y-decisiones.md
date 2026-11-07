# Tesis y decisiones — plataforma de apps legales de nicho + práctica jurídica

**Fecha:** 13-oct-2026 · **Meta del dueño:** que el negocio jurídico-tecnológico sea rentable; referencia previa: ingreso medio ≥ $30M COP/mes en 18-24 meses.

---

## 1. La tesis en seis frases

1. Hay **dos motores con economía opuesta**. La **S.A.S. de apps** escala sin el tiempo de Brian (software por suscripción o por documento). La **práctica jurídica** tiene margen alto pero está **limitada por las horas de un abogado que trabaja tiempo completo en otra empresa**.
2. La S.A.S. vende **herramientas de autoservicio** en trámites que la ley permite hacer sin abogado (tutela, derecho de petición, reclamaciones directas, cumplimiento SST/PESV) y **software B2B**. No representa a nadie ni da asesoría personalizada (Decreto 196/1971 arts. 25 y 28; Decreto 2591/1991 arts. 10 y 14) [V].
3. Brian, como abogado persona natural, toma lo que **sí exige criterio o representación**: impugnaciones, desacatos difíciles, defensa ante la DIAN, demandas laborales y de responsabilidad civil, defensa administrativa SST/PESV y retainer jurídico B2B.
4. La conexión entre los dos es **lícita solo si es opcional, revelada y sin comisión**: la Ley 1123/2007 sanciona usar intermediarios para obtener poderes o compartir honorarios con quien recomienda (art. 30 num. 5) y captar clientes en situación de calamidad (art. 30 num. 7) [texto tomado de la C-009/2023; confirmar numerales en SUIN-Juriscol `[VERIFICAR]`].
5. Todo se construye sobre **un núcleo común** que ya existe a medias en `sst-project-v2` (multiempresa, módulos con precio, IA, notificaciones). Las verticales nuevas reutilizan tres piezas: **motor de plazos en días hábiles, generador de documentos y expediente con derivación consentida**.
6. El orden importa más que la lista: primero lo que **ya está construido y tiene fecha de compra** (SST + PESV con la ventana de enero de 2027), luego **lo que más tráfico trae con el mismo motor** (peticiones y tutelas), y luego **lo que mejor paga la hora de abogado** (defensa DIAN).

## 1bis. Portafolio confirmado por Brian (15-oct-2026)
| Pieza | Qué es | Dónde |
|---|---|---|
| **SST (Justrabajo) + PESV** | SaaS B2B ancla | `02-verticales/01-sst.md`, `02-pesv.md` |
| **Tutelas y peticiones** | Motor B2C de alto volumen | `02-verticales/03-tutelas-y-peticiones.md` |
| **Penal** | Víctimas en querellables, reparación y penal-SST para empleadores | `02-verticales/07-penal.md` |
| **Firma App** | Consola del abogado y producto para otros abogados | `02-verticales/08-firma-app.md` |
| **Cerebro Legal** | Motor jurídico con jurisprudencia real verificada, líneas, estrategias con Radar Judicial y **Radar de Oportunidades** (cada fallo de cortes, SIC, Superfinanciera, Supersolidaria se evalúa como negocio) | `empresa/Apis/cerebro_legal/` |
| **Radar Judicial** | Vigilancia de procesos (consulta a demanda / buzón Ley 2213) | `empresa/Apis/radar_judicial/` |
| Verticales adicionales de nicho | Impuestos (defensa DIAN), centrales de riesgo, laboral, insolvencia, tránsito, PH | `02-verticales/` |

## 2. Cifras que sostienen la tesis

| Dato | Valor | Fuente |
|---|---|---|
| Tutelas radicadas en despachos, 2025 | **1.202.436** (+162% vs. 2020) | CSJ, mar-2026 [V] |
| Tutelas en salud 2025 / % concedidas | 378.895 / **78,4%** concedidas | CSJ [V] |
| Tutelas por derecho de petición 2025 | 432.658 (el derecho más tramitado) | CSJ [V] |
| Incidentes de desacato 2024 | 187.901 (+112% vs. 2020) | CSJ vía El Tiempo [V] |
| Muertes viales 2024 / Q1-2026 | 8.271 / +20,1% interanual | ONSV, ANSV [V] |
| Víctimas atendidas por accidentes de tránsito, 2023 | ~1,1 millones | ADRES–Fasecolda [V] |
| Declarantes de renta esperados, 2026 | > 7 millones | DIAN vía Portafolio [V] |
| Gestión de fiscalización DIAN 2025 | $12,84 billones; 15.743 casos por factura electrónica | Informe de Gestión DIAN 2025 [V] |
| Vigilados Supertransporte obligados a PESV sin registro | 4.410 de ~10.328 (43%); 5.446 reportaron, 472 en trámite | Supertransporte vía Asuntos Legales, 2024 [V] |
| Solicitudes de insolvencia persona natural | 10.441 (2024) → 18.726 (2025) → ~26.640 proyectadas (2026) | SICAAC vía Infobae [V] |
| Empresas afiliadas a riesgos laborales | 1.227.399 | CCS/Fasecolda 2025 [V] |

Detalle y fuentes en `02-verticales/` y `fuentes.md`.

## 3. Hallazgos que cambian el plan

1. **El cuello de botella es la hora de abogado, no la demanda.** Con 60 h/mes, la práctica de Brian se estanca en **~$8-9M/mes en caja**, aunque la demanda supuesta pida 83 h en el mes 12 y 228 h en el mes 24 [E, `modelo/salida_60h.md`]. Cada retainer nuevo desplaza casos DIAN que pagan más por hora. La cuota litis no cabe sin un abogado adicional. Con uno (~160 h en total), la práctica llega a ~$23M/mes en el mes 24, antes de su costo (~$5,1M), y supera el tope de no responsable de IVA.
2. **Conflicto de interés estructural.** Los clientes del retainer SST/PESV son **empleadores** y empresas con flota. Representar a **trabajadores** (laboral) o **víctimas de tránsito** contra esos mismos clientes es representar intereses contrapuestos (Ley 1123 art. 34 lit. e). Hace falta un **control de conflictos** en la consola del abogado y una decisión de posicionamiento (ver D3).
3. **La derivación desde la app tiene reglas duras.** Opcional, con revelación del vínculo ("el abogado es socio de la S.A.S."), con alternativas gratuitas (Defensoría, consultorios jurídicos), **sin pago por cliente referido** y, en accidentes, **sin contacto proactivo** a la víctima.
4. **El documento ya no se puede cobrar caro.** Las tutelas y peticiones tienen piso gratis (Defensoría, consultorios, plantillas, IA genérica), y desde abril de 2026 la **ADRES** tiene una plataforma gratuita para reclamar sin intermediarios. El valor está en **el seguimiento de plazos, el desacato, la prueba y la radicación sin errores**.
5. **Dos precedentes que no hay que repetir.** **DoNotPay** pagó US$193.000 a la FTC (orden de enero de 2025) por venderse como "abogado robot" sin probarlo. **Juzto** (fotomultas, Bogotá) cerró en dic-2023 tras ganar ~14% de 6.211 tutelas y recibir denuncias de usuarios. Regla: **nunca prometer resultados ni masificar escritos de baja calidad**.
6. **Hay fechas que venden solas:** omisos y requerimientos DIAN desde **nov-2026**; reporte PESV a MinTrabajo en **enero de 2027** escalonado por NIT (Circular 0034/2026 de **MinTrabajo**; fechas exactas y si son días hábiles `[VERIFICAR texto oficial]`); autoevaluación SG-SST **may-jul**; reforma pensional vigente desde **1-abr-2027**.

## 4. Las decisiones que solo Brian puede tomar

| # | Decisión | Recomendación de Claude | Bloquea |
|---|---|---|---|
| D1 | **¿Una sola S.A.S. para todas las apps?** | Sí. Una S.A.S. de software (CIIU 6201, sin 6910) con **marcas por vertical** para SEO y confianza. La práctica jurídica, separada | Constitución, T&C, facturación |
| D2 | **Nombre de la S.A.S. y marca paraguas** (Justrabajo, Cumplia u otro) | Razón social neutra y amplia. Justrabajo queda como marca de SST; cada vertical B2C lleva marca propia bajo el paraguas | Constitución, dominios |
| D3 | **Lado en laboral y tránsito:** ¿empleadores/empresas, trabajadores/víctimas o ambos? | Empleador en lo B2B (retainer y defensa administrativa). Trabajadores y víctimas **solo contra no-clientes**, con control automático de conflictos. Alternativa: directorio de abogados aliados para el lado trabajador | Verticales laboral y accidentes |
| D4 | **Horas/mes reales para la práctica** y revisión del contrato laboral con Vanti (exclusividad, conflictos) `[VERIFICAR]` | Fijar un número (p. ej. 40-60 h) y diseñar la oferta para esa capacidad | Todo lo que vende la práctica |
| D5 | **Secuencia de verticales** | La de `03-priorizacion-y-secuencia.md` §4: SST+PESV → peticiones/tutelas + calendario tributario → defensa DIAN en app + centrales de riesgo → laboral + insolvencia → accidentes + fotomultas (con abogado asociado) | Backlog de Code |
| D6 | **Pricing público SST** (por módulo en código vs. planes en el dossier) | Planes públicos + módulos como complemento. Decisión pendiente desde ago-2026 | Página de precios y cobro |
| D7 | **Repositorio:** seguir en `sst-project-v2` o separar | Monorepo en `sst-project-v2`: un núcleo y una app Flask con blueprints por vertical. Ver ADR-P1 en `04-arquitectura-plataforma.md` | Arranque de Code |
| D8 | **¿Solo Galeano y Asociados o directorio abierto de abogados?** | Arrancar con Galeano y Asociados, revelando el vínculo, y diseñar desde el día 1 para varios abogados (reduce el riesgo del art. 30 num. 5 y libera capacidad) | Diseño de la derivación |

| D9 | **Penal: ¿qué lado?** | Penal-SST solo del lado del empleador (con retainer); víctimas en tránsito y estafas. Nada de defensa con captura sin penalista aliado | Vertical penal |
| D10 | **Firma App: ¿portar al monorepo o mantener aparte?** | Portar por módulos a `sst-project-v2` como consola del abogado (ADR-P8) y archivar el repo viejo al terminar | Épica E13 |
| D11 | **Rama inicial del Cerebro Legal** (índice verificable, fase C1) | SST-laboral + tutela en salud: son las que más usan las verticales y la práctica | Épica C1 |

## 5. Foco recomendado — próximos 90 días (propuesta)

| Semana | Qué | Por qué ahora |
|---|---|---|
| 1-2 | Tomar D1, D2, D3 y D4. Constituir la S.A.S. con la ruta de `empresa/` | Sin S.A.S. no hay cobro ni T&C |
| 1-6 | Code: cobro (Wompi + factura electrónica), Postgres + RLS y **cuentas personales** en el núcleo (épicas **E0 y E1** del backlog) | Precondición de todo lo B2C y del cobro B2B |
| 3-10 | Code: módulo PESV con reporte para MinTrabajo (épica **E3**) y 3 pilotos SST/PESV | Ventana de enero de 2027 |
| 4-8 | Brian: abrir la línea **defensa DIAN** como abogado, con una landing y un diagnóstico manual (lo factura el abogado) | Temporada de requerimientos desde nov-2026; no requiere código para empezar |
| 1-8 | Brian: verificar las reglas de plazo y las citas iniciales (historia E2.0) | Sin eso, el motor no puede activar reglas |
| Desde ene-2027 | Code: motor de plazos y documentos (**E2**) + **derecho de petición** y **tutela de salud** con seguimiento (**E4**) | Volumen y tráfico orgánico; base de todas las verticales B2C (Fase 1 de `03-priorizacion`) |

## 6. Lo que este paquete no resuelve
- Cifras que no se encontraron en fuente pública (marcadas `[VERIFICAR]`; lista en `07-riesgos-y-pendientes.md`).
- Validación con clientes reales: todo precio B2C es hipótesis hasta medir conversión.
- Concepto de un especialista en protección de datos y en régimen disciplinario antes del lanzamiento B2C.
