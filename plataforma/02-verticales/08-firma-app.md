# Vertical 8 — Firma App: la consola del abogado (y un producto para abogados)

**Decisión de Brian (15-oct-2026):** Firma App entra a la plataforma.

## 1. Qué es ahora
Firma App deja de ser un proyecto aparte y pasa a ser **la consola del abogado** de toda la plataforma:
- Para **Brian**: CRM de prospectos y clientes, expedientes, agenda, honorarios, WhatsApp, firma de documentos, derivaciones que llegan de las verticales (con consentimiento y control de conflictos), sugerencias de estrategia del Cerebro Legal y alertas de Radar Judicial.
- Para **otros abogados y firmas pequeñas**: el mismo producto vendido como SaaS por la S.A.S. (tenant `practica_juridica`). Eso abre el **directorio de abogados** (decisión D8), reduce el riesgo de que la plataforma sea un canal exclusivo hacia Brian y libera capacidad cuando él no da abasto.

## 2. Qué se reutiliza de `firma_app/` (código de feb-2026)
| Pieza de Firma App | Destino en la plataforma |
|---|---|
| Modelos `cliente`, `prospecto`, `caso`, `actividad`, `cita`, `documento`, `factura`, `area_practica`, `proceso_dinamico` | Consola del abogado (épica E6) sobre el núcleo: `caso`, `expediente`, `derivacion`, `contraparte` |
| `whatsapp_service.py`, simulador | Canal WhatsApp del núcleo de notificaciones |
| `ai_service.py` (Gemini), chatbot | Detrás de los guardrails de IA del núcleo (ADR-P4) |
| Facturación de honorarios | Facturación **del abogado**, separada de la de la S.A.S. |
| Landing builder, portal del cliente | Fase posterior |
| `siguiente.md` (cockpit de 3 columnas, Twilio, agenda) | Diseño de la consola, fase posterior |
| **`judicial_scraper.py` (Selenium "para saltar WAF/CAPTCHA")** | **No se porta.** Se reemplaza por el cliente de Radar Judicial (consulta a demanda / buzón Ley 2213) |
| `.env`, bases SQLite, `error.log` | No se portan; rotar las llaves si alguna vez se compartieron |

**Recomendación (ADR-P8):** portar por módulos al monorepo `sst-project-v2` en vez de mantener dos apps Flask. Firma App queda como referencia de código hasta terminar la migración y luego se archiva.

## 3. Lo que la hace diferente para otros abogados
Lo que los competidores no unen (según lo publicado; vLex, Legis, Juztina, Lemontech venden búsqueda o gestión por separado `[VERIFICAR con demos]`):
1. Vigilancia de procesos (Radar) **+** estrategia sugerida (Cerebro) **+** expediente en la misma pantalla.
2. Plazos calculados por un motor con fuentes verificadas.
3. Citas validadas (cero citas inexistentes).
4. Control de conflictos de interés incorporado.

## 4. Precio (propuesta, a validar)
Referencias: Lemontech (gestión de firmas, en expansión en Colombia 2026), Juztina (US$10/mes según Forbes Perú, solo búsqueda) `[VERIFICAR]`. Hipótesis de arranque: plan abogado independiente y plan firma pequeña por usuario/mes, con Radar y Cerebro como complementos. Definir tras 5 entrevistas con abogados.

## 5. MVP de la consola (para Brian primero)
1. Bandeja de derivaciones con consentimiento y control de conflictos.
2. Expediente por caso con plazos, documentos y eventos de Radar.
3. Sugerencias del Cerebro por actuación (borrador, nunca automático).
4. Agenda y recordatorios (WhatsApp/correo).
5. Honorarios y factura del abogado.
6. Tablero de horas y valor por hora por línea (para la decisión de capacidad).

Épica E13 en `../06-backlog-claude-code.md`.
