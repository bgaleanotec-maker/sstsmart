# Modelo financiero — la ruta a $30 millones/mes

**Meta:** ingreso medio mensual ≥ **$30.000.000 COP** en 18–24 meses.
Modelo reproducible en `scripts/modelo_financiero.py` (incluido en este repo).

---

## 0. Antes de las tablas: ingreso no es utilidad

Hay que decirlo con claridad porque cambia toda la lectura de este documento.

| Escenario | Ingreso mensual | Utilidad operativa | Cuándo |
|---|---|---|---|
| **La meta como fue planteada** (ingreso $30M) | **$30,6M** | ~$7,8M | **Mes 20** |
| MRR puro de $30M (sin contar servicios) | $36,2M | ~$9,2M | Mes 24–25 |
| **Utilidad de $30M/mes** | ~$65–70M | $30M | **Mes 36+**, o con precio medio mayor |

En el escenario base, el mes 24 deja **~$9,2M de utilidad operativa** después de una nómina de $18,8M. Si lo que buscas es **$30M de ingreso disponible para ti**, el horizonte es de 36 meses o exige subir el ARPA sustancialmente.

Este documento modela la meta como la planteaste: **$30M de ingreso**. Pero la distinción hay que tenerla presente al tomar decisiones de contratación.

---

## 1. Supuestos del modelo

| Variable | Valor base | Fundamento |
|---|---|---|
| Precios | Esencial $149.000 · Profesional $349.000 · Corporativo $749.000 · Canal $590.000 + $49.000 por empresa adicional | [`01-pricing-y-empaquetado.md`](01-pricing-y-empaquetado.md) |
| Add-on PESV, precio medio ponderado | $299.000 | Mix básico/estándar/avanzado |
| Retainer jurídico, precio medio ponderado | $400.000 | Mix Básico/Plus/Defensa |
| **Churn mensual de logos** | **2,0%** (24% anual) | Conservador para SaaS B2B pyme en Colombia |
| Empresas por consultor en el canal | 4 → 8, creciendo semestralmente | El consultor migra su cartera progresivamente |
| **Attach rate PESV** | 10% → **23%** (mes 20) | Empieza bajo, sube con el módulo maduro y las campañas de enero |
| **Attach rate jurídico** | 8% → **23%** (mes 20) | Idem, con las campañas de mayo–julio |
| Servicios por proyecto | $2M/mes → tope $6,5M/mes | Implementaciones, diseños PESV, auditorías. **El puente de caja de los meses 1–12** |
| Comisión de pasarela | 3,15% efectivo | Wompi 2,65% + $700 + IVA |
| Tipo de cambio | $4.100/USD | Para costos de infraestructura |

**Nómina escalonada:**

| Mes | Contratación | Costo mensual |
|---|---|---|
| 6 | Desarrollador semi-senior | $4.900.000 |
| 12 | Comercial (fijo + comisión base) | $4.600.000 |
| 17 | Soporte / Customer Success | $4.200.000 |
| 19 | Abogado junior (opera el retainer) | $5.100.000 |
| **Total mes 24** | | **$18.800.000** |

*Factor prestacional 1,64 sobre el salario, según [`../04-empresa/02-tributario-y-facturacion.md`](../04-empresa/02-tributario-y-facturacion.md).*

**Otros costos fijos:** contador $700.000 → $1.300.000 (2 sociedades desde el mes 6) · infraestructura $164.000 → $2.870.000 según escala · herramientas $350.000 → $900.000 · marketing $800.000 → $2.000.000.

---

## 2. Escenario base — mes a mes

| Mes | Cuentas | MRR SaaS | MRR PESV | MRR Legal | **MRR total** | Servicios | **Ingreso del mes** | Costos | Utilidad |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 149.000 | 29.900 | 32.000 | **210.900** | 2.000.000 | **2.210.900** | 2.083.643 | 127.257 |
| 2 | 2 | 295.020 | 63.050 | 69.300 | **427.370** | 2.220.000 | **2.647.370** | 2.097.392 | 549.978 |
| 3 | 4 | 787.120 | 133.134 | 149.735 | **1.069.989** | 2.440.000 | **3.509.989** | 2.124.565 | 1.385.424 |
| 4 | 7 | 1.418.377 | 245.168 | 281.325 | **1.944.871** | 2.660.000 | **4.604.871** | 2.159.053 | 2.445.817 |
| 5 | 11 | 2.823.010 | 366.356 | 427.872 | **3.617.237** | 2.880.000 | **6.497.237** | 2.218.663 | 4.278.574 |
| **6** | **14** | 3.413.549 | 496.402 | 588.904 | **4.498.856** | 3.100.000 | **7.598.856** | 2.253.364 | 5.345.492 |
| 7 | 16 | 4.039.338 | 635.022 | 763.964 | **5.438.324** | 3.320.000 | **8.758.324** | 8.281.887 | 476.437 |
| 8 | 20 | 5.440.551 | 781.936 | 952.606 | **7.175.093** | 3.540.000 | **10.715.093** | 8.343.525 | 2.371.568 |
| 9 | 23 | 5.978.740 | 936.875 | 1.154.396 | **8.070.011** | 3.760.000 | **11.830.011** | 8.378.645 | 3.451.366 |
| 10 | 25 | 6.506.165 | 1.099.574 | 1.368.914 | **8.974.654** | 3.980.000 | **12.954.654** | 8.414.072 | 4.540.582 |
| 11 | 29 | 7.858.042 | 1.269.779 | 1.595.749 | **10.723.571** | 4.200.000 | **14.923.571** | 8.476.092 | 6.447.478 |
| **12** | **32** | 9.096.881 | 1.498.519 | 1.899.504 | **12.494.904** | 4.420.000 | **16.914.904** | 9.738.819 | 7.176.084 |
| 13 | 34 | 9.694.983 | 1.683.873 | 2.151.430 | **13.530.286** | 4.640.000 | **18.170.286** | 14.928.364 | 3.241.922 |
| 14 | 38 | 11.032.083 | 1.875.952 | 2.414.419 | **15.322.454** | 4.860.000 | **20.182.454** | 14.991.747 | 5.190.707 |
| 15 | 41 | 12.207.441 | 2.131.638 | 2.762.108 | **17.101.187** | 5.080.000 | **22.181.187** | 15.054.707 | 7.126.480 |
| 16 | 44 | 12.959.293 | 2.396.307 | 3.124.603 | **18.480.203** | 5.300.000 | **23.780.203** | 15.105.076 | 8.675.127 |
| 17 | 48 | 14.580.107 | 2.669.653 | 3.501.414 | **20.751.175** | 5.520.000 | **26.271.175** | 15.183.542 | 11.087.633 |
| **18** | **51** | 15.284.505 | 2.951.380 | 3.892.063 | **22.127.947** | 5.740.000 | **27.867.947** | 19.433.840 | 8.434.107 |
| 19 | 53 | 16.035.018 | 3.176.314 | 4.210.085 | **23.421.417** | 5.960.000 | **29.381.417** | 19.481.515 | 9.899.902 |
| **20** | **57** | 18.243.318 | 3.473.333 | 4.625.810 | **26.342.461** | 6.180.000 | **🎯 32.522.461** | 24.680.458 | 7.842.003 |
| 21 | 59 | 18.725.451 | 3.709.171 | 4.962.101 | **27.396.723** | 6.400.000 | **33.796.723** | 24.720.597 | 9.076.126 |
| 22 | 61 | 19.197.942 | 3.841.297 | 5.138.859 | **28.178.099** | 6.500.000 | **34.678.099** | 26.962.360 | 7.715.739 |
| 23 | 63 | 19.660.983 | 3.970.781 | 5.312.082 | **28.943.847** | 6.500.000 | **35.443.847** | 26.986.481 | 8.457.366 |
| **24** | **64** | 20.114.764 | 4.097.676 | 5.481.840 | **🎯 29.694.280** | 6.500.000 | **36.194.280** | 27.010.120 | 9.184.160 |

**Mes 24:** ARR **$356.331.357** · ARPA **$461.329/mes** · 64 cuentas · utilidad operativa **$9,18M** (25% del ingreso).

> **Nota sobre los meses 7, 13 y 20:** la utilidad cae en esos meses porque entra una contratación nueva. Es normal y esperado, pero **exige tener colchón de caja antes de cada una**. No contrates el mes en que apenas alcanzas el punto de equilibrio.

---

## 3. Los tres escenarios

| Escenario | Supuestos | MRR m12 | MRR m18 | MRR m24 | Cuentas m24 | Ingreso m24 | ARR m24 |
|---|---|---:|---:|---:|---:|---:|---:|
| **Conservador** | Altas −30%, churn 3,0% | $8,39M | $14,51M | **$18,90M** | 41 | $23,45M | $226,8M |
| **Base** | — | $12,49M | $22,13M | **$29,69M** | 64 | $36,19M | $356,3M |
| **Agresivo** | Altas +35%, churn 1,5% | $17,22M | $30,89M | **$42,08M** | 91 | $50,86M | $505,0M |

**Cuándo se cruza la meta de $30M:**

| Escenario | Ingreso total ≥ $30M | MRR ≥ $30M |
|---|---|---|
| Conservador | Mes ~33 | Mes ~40 |
| **Base** | **Mes 20** | Mes 24–25 |
| Agresivo | **Mes 15** | **Mes 18** |

> **Lectura:** la meta de 18–24 meses **se cumple en el escenario base**, contando el ingreso total (MRR + servicios). Y el escenario conservador **no llega** — lo que hace que las dos variables de abajo sean las que realmente importan.

---

## 4. Las dos variables que deciden todo

### 4.1 El churn, en primer lugar

Es la diferencia entre los tres escenarios más que cualquier otra cosa. Con **3% mensual**, el negocio pierde 30% de su base al año y cada venta nueva solo repone lo perdido. Con **1,5%**, el mismo esfuerzo comercial produce el doble de MRR al mes 24.

**Palancas de retención, en orden de efectividad:**

1. **El calendario de cumplimiento con alertas.** Un cliente que recibe la alerta correcta el día correcto no cancela. Es la funcionalidad de retención más barata que puedes construir → [`../04-empresa/05-calendario-de-obligaciones.md`](../04-empresa/05-calendario-de-obligaciones.md)
2. **Add-ons.** Un cliente con tres módulos activos tiene un costo de cambio mucho mayor que uno con uno solo.
3. **Pago anual.** Elimina 11 oportunidades de cancelar al año.
4. **El canal.** Un consultor con 20 empresas migradas no se va: migrar de vuelta le cuesta semanas.

### 4.2 El attach rate de add-ons

El modelo asume que PESV y jurídico llegan a **23% cada uno** al mes 24. Si se quedan en 10%:

| | Con attach 23% | Con attach 10% | Diferencia |
|---|---:|---:|---:|
| MRR mes 24 | $29,69M | ~$25,5M | **−$4,2M/mes** |

Para conseguir el mismo MRR con attach de 10% harían falta **~14 cuentas más**, con todo el CAC que eso implica. **Vender un add-on a un cliente existente es varias veces más barato que conseguir un cliente nuevo.**

**Cuándo ofrecer el add-on:** en el **mes 2 o 3 de uso**, no en el checkout inicial. En el checkout el cliente está evaluando si el producto sirve; en el mes 3 ya lo sabe y el add-on resuelve un problema que él mismo detectó.

---

## 5. Composición del ingreso al mes 24

| Fuente | Monto | % |
|---|---:|---:|
| Suscripciones SaaS | $20.114.764 | 55,6% |
| Add-on PESV | $4.097.676 | 11,3% |
| Retainer jurídico | $5.481.840 | 15,1% |
| **Subtotal recurrente (MRR)** | **$29.694.280** | **82,0%** |
| Servicios por proyecto | $6.500.000 | 18,0% |
| **Total** | **$36.194.280** | **100%** |

> **82% de ingreso recurrente es una estructura sana.** Si al mes 24 los servicios pesaran más del 35%, no tendrías un SaaS: tendrías una consultora con software, con la valoración y la escalabilidad de una consultora.

**Pero en los meses 1–12 los servicios son el 40–60% del ingreso, y eso está bien.** Son el puente de caja mientras el MRR madura. La trampa es quedarse ahí: **cada proyecto de consultoría consume tiempo que no construye producto.** La regla práctica: no aceptar proyectos que no dejen algo reutilizable en la plataforma.

---

## 6. Estructura de costos al mes 24

| Concepto | Mensual | % del ingreso |
|---|---:|---:|
| Nómina (4 personas) | $18.800.000 | 51,9% |
| Marketing | $2.000.000 | 5,5% |
| Infraestructura (Render, R2, herramientas) | $2.870.000 | 7,9% |
| Contabilidad (2 sociedades) | $1.300.000 | 3,6% |
| Comisión de pasarela (3,15%) | $1.140.120 | 3,1% |
| Herramientas y software | $900.000 | 2,5% |
| **Total** | **$27.010.120** | **74,6%** |
| **Utilidad operativa** | **$9.184.160** | **25,4%** |

*Antes de impuestos. Renta 35% en régimen ordinario, más ICA.*

---

## 7. Necesidad de caja

| Mes | Utilidad acumulada |
|---|---:|
| 6 | ~$14,1M |
| 12 | ~$42,1M |
| 18 | ~$97,7M |
| 24 | ~$149,6M |

**El modelo nunca entra en caja negativa acumulada**, porque los servicios por proyecto sostienen los primeros meses y las contrataciones están escalonadas contra el ingreso.

**Capital de arranque necesario: ~$7 millones** (constitución, marca, infraestructura y contabilidad de los primeros tres meses) → [`../04-empresa/00-checklist-maestro.md`](../04-empresa/00-checklist-maestro.md).

> **La condición que sostiene esto:** que los servicios por proyecto realmente lleguen a **$2M el primer mes**. Si el bufete no puede vender una implementación de SG-SST o un diseño de PESV en el mes 1, el modelo necesita ~$25M de capital para llegar al mes 6. **Vende un proyecto antes de escribir la primera línea del módulo de facturación.**

---

## 8. Alternativa: llegar a $30M con menos cuentas

Si la adquisición resulta más lenta de lo previsto, la misma meta se alcanza subiendo el ARPA:

| Estrategia | Cuentas necesarias | ARPA | Viabilidad |
|---|---:|---:|---|
| Mix del modelo base | 64 | $461.329 | La del plan |
| **Foco en Corporativo y Canal** | **~40** | ~$740.000 | Ciclo de venta más largo; exige SSO, multi-sede y due diligence. **Adelanta el R6 del roadmap** |
| Foco en Esencial | ~130 | ~$230.000 | Requiere marketing masivo y soporte escalado. **No recomendado**: el margen no aguanta el costo de soporte |
| **Peso alto de servicios** | ~40 + $15M/mes en proyectos | — | **Riesgo estructural**: te conviertes en consultora |

> **La opción de menos riesgo es la segunda:** priorizar el canal de consultores y el plan Corporativo. Menos cuentas, más ARPA, menos costo de soporte por peso de ingreso. Y el canal tiene el CAC más bajo del plan.

---

## 9. Tablero mensual

Revisa estas ocho cifras el primer lunes de cada mes:

| Métrica | Objetivo mes 12 | Objetivo mes 24 |
|---|---|---|
| MRR | $12,5M | **$29,7M** |
| Cuentas activas | 32 | **64** |
| ARPA | $390.000 | **$461.329** |
| Churn mensual de logos | <2,0% | **<1,5%** |
| Attach rate PESV | 15% | **23%** |
| Attach rate jurídico | 15% | **23%** |
| Ingreso de servicios | $4,4M | $6,5M |
| Utilidad operativa | $7,2M | **$9,2M** |

**Si una métrica se desvía más del 20% durante dos meses seguidos, revisa el supuesto — no el esfuerzo.**

Detalle de CAC, LTV y payback en [`03-unit-economics-y-metricas.md`](03-unit-economics-y-metricas.md).
