# Vertical 2 — PESV (Plan Estratégico de Seguridad Vial)

**Estado:** especificado en `docs/02-producto/03-especificacion-modulo-pesv.md` y `docs/01-mercado/03-mercado-pesv-seguridad-vial.md` (ago-2026). Este archivo **actualiza y corrige** con la investigación del 13-oct-2026.

## 1. Lo que se confirma
| Punto | Estado oct-2026 | Fuente |
|---|---|---|
| Obligados | Más de 10 vehículos (propios, de trabajadores, contratistas o terceros) **o** que contraten o administren conductores (metodología: desde 2 conductores). Ley 1503/2011 art. 12 mod. Ley 2050/2020 | Ley 2050/2020 [V] |
| Metodología | Res. 20223040040595/2022: 24 pasos, fases PHVA, niveles básico (18 pasos), estándar (22), avanzado (24) | implementandosgi, mipesv [V secundaria] |
| **Circular 0034 del 30-mar-2026** | Es de **MinTrabajo** (Diario Oficial 53.457, 13-abr-2026). Misionalidad 2 reporta indicadores (Tabla 10, paso 20) con corte al 31-dic, por **Microsoft Forms** | detransito.net, safetyworkla [V secundaria] |
| Ventana de reporte | Último dígito del NIT: 0-1 → 6 ene · 2-3 → 11 ene · 4-5 → 17 ene · 6-7 → 23 ene · 8-9 → último día de enero. **`[VERIFICAR texto oficial]`**: en 2027 el 11-ene es festivo, el 17 y el 31 son domingo y el 23 es sábado; puede tratarse de días hábiles o de fechas de 2026. El recordatorio debe pasar por el motor de plazos | Ídem (secundarias) |
| Sanción por no reportar (M2) | Art. 13 Ley 1562/2012; la circular no fija montos | Ídem |
| Vigilados Supertransporte | Formulario 1 en SISI-PESV a más tardar el 10.º día hábil de agosto; Formulario 2 (indicadores) con acumulado anual en enero. Sanción: art. 46 Ley 336/1996, 1 a 2.000 SMMLV | Supertransporte [V] |
| Cumplimiento | 2024: 5.446 de ~10.328 vigilados reportaron (53%); 4.410 sin registro | Asuntos Legales [V] |

## 2. Correcciones y novedades frente al dossier
1. **Niveles en misionalidad 2** (rangos secundarios, `[VERIFICAR contra la tabla oficial]`): básico 11-49 vehículos o 2-49 conductores; estándar 50-100; avanzado más de 100. El límite "50" aparece en dos niveles en las fuentes.
2. **El reporte de vigilados migra**: el Anexo Técnico PESV se cita bajo la Res. 1455 del 26-feb-2025 y menciona un módulo en **SINST-VIGIA 2** `[VERIFICAR]`. El modelo `pesv_reporte` debe aceptar un destino nuevo sin migración (enum abierto o tabla de destinos).
3. **No hay multas PESV en firme publicadas**: solo aperturas de investigación (p. ej. Res. 14388 del 16-sep-2025). No usar "multas de hasta 2.000 SMMLV" como gancho sin esa precisión.
4. **Competidor con precio público: MiPESV** — Básico $149.000, Estándar $289.000, Avanzado $499.000/mes (30 días de prueba). El dossier fijó PESV Básico en $199.000: revisar contra este ancla.
5. **Datos externos**: RUNT 2.0 vende consulta masiva por web service con contrato y tarifa regulada; SIMIT no tiene API comercial conocida; intermediarios como Verifik venden consulta (precio no publicado). Raspar el portal ciudadano **no** es vía autorizada (misma lógica que Radar Judicial). Lanzar con carga manual y alertas.

## 3. Brechas de la competencia que el módulo debe cerrar
1. Nadie exporta directo al formulario de MinTrabajo (Tabla 10) ni al Formulario 2.
2. Los PESV puros no comparten matriz de peligros, investigación de accidentes ni indicadores con el SG-SST: el cliente trabaja dos veces. **Nuestro argumento: un solo sistema** (la propia Circular 0034 cita el art. 32 de la Res. 0312).
3. Precios sin límite de vehículos ni usuarios publicado.
4. Enfoque en flotas de transporte; casi nadie atiende misionalidad 2 con motos de vendedores o técnicos.

## 4. Precio sugerido (propuesta, no dato de mercado)
| Nivel | Complemento para clientes SST | PESV solo | Incluye |
|---|---|---|---|
| Básico | $99.000-129.000/mes | $149.000 | Hasta 49 vehículos, preoperacional, reporte MinTrabajo |
| Estándar | $219.000-259.000 | $289.000 | Hasta 100 vehículos, mantenimiento, comparendos, siniestros |
| Avanzado | $399.000 + $2.000-4.000 por vehículo adicional | $499.000 + | Contratistas, telemática, auditoría |

Implementación opcional $500.000-1.500.000. Servicio de diseño de PESV por el abogado/consultor: ver `docs/02-producto/04` ($4.900.000).

## 5. Canales (orden)
1. Clientes SST actuales: venta cruzada con campaña para **enero de 2027**.
2. Consultores SST/PESV con licencia multiempresa.
3. Venta directa a medianas de misionalidad 2 (logística, servicios técnicos, ventas de campo con motos).
4. ARL y corredores `[VERIFICAR viabilidad de que la ARL pague la licencia]`.

## 6. Sinergias con otras verticales
- **Accidentes de tránsito**: el siniestro vial laboral es a la vez AT (FURAT) y siniestro PESV. Ojo con el conflicto de interés al representar víctimas (ver `../01-estructura-legal-dos-entidades.md` §6).
- **GPS-Comercial** (idea en el cerebro): km recorridos y velocidad para indicadores.
- **Fotomultas**: comparendos de conductores como indicador PESV.

## 7. MVP para enero de 2027 (prioridad 1)
Autodiagnóstico de nivel · lista de 24 pasos con evidencias compartiendo plan anual del SG-SST · conductores (licencias, comparendos) · vehículos (SOAT, RTM, mantenimiento) · preoperacional PWA offline · siniestros (registro único AT + vial) · indicadores Tabla 10 · **exportación al formulario MinTrabajo** y recordatorio por último dígito del NIT. Detalle en épica E3 de `../06-backlog-claude-code.md`.

Fuentes: `../fuentes.md` §4.
