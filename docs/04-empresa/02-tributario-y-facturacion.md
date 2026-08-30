# Tributario y facturación electrónica

> Verificado a agosto de 2026. **UVT 2026 = $52.374** (UVT 2025 = $49.799) · SMMLV = $1.750.905 + auxilio de transporte $249.095.

**Contexto:** la reforma tributaria estructural fue **rechazada por el Congreso el 9 de diciembre de 2025**. El marco sigue siendo la **Ley 2277 de 2022**. Por decretos de conmoción quedaron vigentes en 2026 un impuesto al patrimonio de personas jurídicas (desde 200.000 UVT de patrimonio líquido ≈ $10.474 millones — no te toca) y un impuesto al juego en línea; ambos bajo revisión de la Corte Constitucional.

---

## 1. RUT — responsabilidades a inscribir

| Código | Responsabilidad | ¿Aplica? |
|---|---|---|
| **05** | Renta y complementario, régimen ordinario | Sí (o 47 si eliges Simple) |
| **07** | Retención en la fuente a título de renta | Sí |
| **42** | Obligado a llevar contabilidad | Sí |
| **52** | Facturador electrónico | Sí |
| **48** | Responsable de IVA | **Depende — ver §2** |
| **49** | No responsable de IVA | Alternativa a 48 |
| **59** | Autorretenedor especial de renta | Si aplicas la exoneración del art. 114-1 |
| **19** | Productor de bienes/servicios exentos | **Imprescindible si exportas servicios** |
| **47** | Régimen Simple | Alternativa a 05/07 |

**El ICA no se inscribe en el RUT.** Se hace en el **RIT** ante la Secretaría Distrital de Hacienda de Bogotá.

---

## 2. IVA sobre SaaS — la decisión más delicada

**Tarifa general: 19%.** Pero el **art. 476 num. 21 del ET** excluye de IVA *"el suministro de páginas web, servidores (hosting), computación en la nube y mantenimiento a distancia de programas y equipos"*, reglamentado por el **Decreto 1412 de 2017**.

### 2.1 Cómo lo interpreta la DIAN — restrictivamente

| Doctrina | Qué dice |
|---|---|
| **Concepto 1444 del 22-dic-2017** | Exige un **autodiagnóstico conforme a la guía técnica de MinTIC, firmado por el responsable técnico**, para acreditar que el servicio es genuinamente cloud computing |
| **Oficio 900930 de 2022** | La exclusión aplica **exclusivamente al proveedor de nube** — quien adquiere y gestiona la infraestructura y ejecuta el software en la nube. **No aplica a corredores, agentes ni revendedores.** Los beneficios tributarios son de interpretación restrictiva |
| **Concepto 190 del 18-mar-2024** | Un intermediario solo accede *"si actúa como proveedor y cumple los modelos de servicio de cloud computing"* |

### 2.2 Qué significa para SST Smart

Un SaaS multi-tenant que cumple las cinco características NIST (autoservicio bajo demanda, acceso amplio por red, recursos compartidos, elasticidad rápida, servicio medible) **tiene argumento sólido** para facturar sin IVA bajo el num. 21.

**Pero hay que documentarlo antes de la primera factura:**

- Autodiagnóstico MinTIC firmado por el responsable técnico
- Documentación de arquitectura, con evidencia de multi-tenancy y de medición de consumo
- **Desagregación de precios**: si vendes SaaS + consultoría en un paquete, **la consultoría sí lleva 19%** y debe facturarse por separado

**No cubre:** dominios, certificados SSL, correo premium, email marketing, ni el producto digital terminado.

### 2.3 La recomendación honesta

| Opción | Cuándo elegirla |
|---|---|
| **Facturar sin IVA** (exclusión num. 21) | Solo si montas el autodiagnóstico MinTIC **el mismo mes** y mantienes la documentación viva |
| **Facturar con 19%** | **Si no vas a montar esa documentación, elige esta y duerme tranquilo.** Una glosa por IVA no facturado sobre tres o cuatro años de suscripciones es existencial para una empresa temprana |

Y considera el efecto comercial: tus clientes son empresas responsables de IVA, así que el 19% es **descontable para ellos** — no encarece realmente su compra. La exclusión te ayuda a ti en flujo de caja, no a ellos en precio.

### 2.4 Exportación de servicios

Si vendes a un cliente sin negocios en Colombia y el servicio se usa exclusivamente en el exterior, es **exento (0%) con derecho a devolución del IVA descontable** — siempre que inscribas la **responsabilidad 19** y cumplas los requisitos formales del Decreto 1080/2015.

La DIAN reconsideró varios requisitos formales de esta exención en 2025; **verifica el estado con tu contador antes de exportar**.

---

## 3. Renta y Régimen Simple

### 3.1 Régimen ordinario

Tarifa general 2026: **35%**. Sin sobretasa para software. Aplica la tasa mínima de tributación (TTD 15%) del art. 240 par. 6 ET.

### 3.2 Régimen Simple (RST)

| Elemento | Valor 2026 |
|---|---|
| Tope general de ingresos brutos del año anterior | < 100.000 UVT = **$4.979.900.000** (UVT 2025) |
| **Tope para servicios profesionales / consultoría** | **12.000 UVT** |
| Plazo de inscripción para el año gravable 2026 | **27 de febrero de 2026** (empresas nuevas: al inscribir el RUT, en cualquier momento) |
| Tarifa — comercio, servicios técnicos | 1,6% – 4,5% |
| **Tarifa — servicios profesionales y consultoría (factor intelectual)** | **7,3% – 8,3%** |
| Descuento por pagos electrónicos | 0,5% |

### 3.3 ¿Conviene el RST a una SaaS? — probablemente no, y aquí está por qué

**Es una decisión de alto impacto y baja certeza.** La calificación de "desarrollo de software" como servicio técnico (predominio material) frente a consultoría (predominio intelectual) **no es evidente y la DIAN ha sido inconsistente**. Si cae en el grupo de consultoría, a 8,3% sobre ingresos brutos, una SaaS con márgenes de 40% pagaría el equivalente a más del 20% de la utilidad — y además quedaría atrapada en el tope de 12.000 UVT.

| A favor del RST | En contra |
|---|---|
| Unifica renta + ICA + avisos y tableros + sobretasa bomberil | **No puedes compensar pérdidas fiscales** — y una SaaS en años 1–3 casi siempre las tiene |
| Elimina la retención en la fuente sobre tus ingresos (mejora la caja) | **No puedes aplicar el descuento del art. 256 ET por I+D+i** (30%) |
| Menos declaraciones | Riesgo de clasificación en el grupo de 7,3–8,3% |

> **Recomendación: régimen ordinario**, si esperas pérdidas fiscales o inversión en I+D en los primeros años. El RST es para operaciones rentables desde el día uno, con poca estructura de costos.

---

## 4. ICA en Bogotá

| Actividad | Agrupación | Tarifa por mil |
|---|---|---|
| 6201 desarrollo de sistemas informáticos | 304 | **9,66 ‰** |
| 6209 otras actividades de TI | 304 | 9,66 ‰ |
| 6311 procesamiento de datos y hosting | 304 | 9,66 ‰ |
| 6202 consultoría informática | 302 | **8,66 ‰** (subió de 6,9 ‰ en 2022) |
| 6910 profesiones liberales (abogacía) | 306 | **7,66 ‰** (bajó de 9,66 ‰ en 2022) |

Base normativa: Acuerdo Distrital 780 de 2020 y Resolución SDH-000265 de 2021 (adoptó la CIIU Rev. 4 A.C.).

> **[NE] Advertencia:** el cambio de tarifas 6,9→8,66 y 9,66→7,66 se verificó en fuente secundaria, y las tarifas por actividad en tablas de terceros. **No logré confirmar la fila exacta del 6201 en la Cartilla ICA oficial.** Confírmalo en el RIT antes de la primera declaración.

**Otros datos:** sobretasa bomberil del 1% del ICA si los ingresos netos superan 43.498 UVT · base mínima de retención de ICA por servicios: **4 UVT = $209.496**.

Bogotá aprobó incentivos de exención de ICA para nuevas inversiones grandes (88.073–880.728 UVT), pero **con vigencia desde el 1 de enero de 2027** y sujetos a modificación del Concejo. **No cuentes con ellos hoy.**

---

## 5. Retención en la fuente — cambio vigente desde julio de 2026

El **Decreto 572 de 2025** fue suspendido provisionalmente por el Consejo de Estado el 8 de mayo de 2026 y **reactivado el 1 de julio de 2026**. Bases y tarifas cambiaron a mitad de año:

| Concepto | Tarifa | Base mínima (desde 1-jul-2026) |
|---|---|---|
| Honorarios y consultoría (persona jurídica) | **11%** | sin base |
| Servicios generales (declarantes) | **4%** | **2 UVT = $104.748** (antes 4 UVT) |
| Compras generales (declarantes) | 2,5% | **10 UVT = $523.740** (antes 27 UVT) |
| Autorretención especial de renta | 0,55% – 4,5% según CIIU | sobre valor bruto sin IVA |

> **[NE]** No pude verificar en fuente pública el porcentaje exacto de autorretención especial para los CIIU 62xx/63xx. El rango publicado es 0,55%–4,5%, y las tarifas altas (4,5%) corresponden a café, hidrocarburos y generación eléctrica. **Consulta la tabla del art. 1.2.6.8 del DUT (anexo del Decreto 572) con tu contador — no uses un valor supuesto.**

---

## 6. Beneficios tributarios para tecnología — qué sobrevive

| Beneficio | Estado 2026 |
|---|---|
| **Renta exenta de economía naranja** (art. 235-2 num. 1 ET) | **DEROGADA** por el art. 96 de la Ley 2277 de 2022. Solo la conservan quienes **ya habían accedido** (con acto de conformidad emitido). **No es una vía disponible para una empresa nueva en 2026** — a pesar de que sigue apareciendo en material comercial desactualizado |
| **Descuento por inversión en I+D+i** (art. 256 ET) | **VIGENTE — 30%** del valor invertido, descontable del impuesto a cargo. Requiere **calificación previa del proyecto** por el Consejo Nacional de Beneficios Tributarios en CTeI (convocatoria anual de Minciencias) |
| Deducción por inversión en I+D+i (art. 158-1 ET) | Vigente, complementaria |
| Crédito fiscal I+D+i / capital humano de alto nivel (art. 256-1 ET) | Vigente, dirigido a MiPymes; es un título negociable con la DIAN |

> **El descuento del 30% del art. 256 es el único beneficio realmente accesible y significativo** para una SaaS nueva. Requiere planeación: **el proyecto se califica ex ante, no ex post**. Si vas a construir el módulo de IA o la matriz legal viva, preséntalo a la convocatoria antes de ejecutarlo.

---

## 7. Nómina y contratación

### 7.1 Exoneración de parafiscales (art. 114-1 ET, vigente 2026)

Las personas jurídicas contribuyentes de renta están exoneradas de **SENA (2%), ICBF (3%) y salud del empleador (8,5%)** por trabajadores que devenguen **menos de 10 SMMLV (< $17.509.050)**. **La caja de compensación (4%) se paga siempre.**

### 7.2 Costo real de un empleado

Para un trabajador de salario mínimo, el costo total mensual para el empleador es **$2.864.324** — un **factor prestacional de ~1,64** sobre el salario. Presupuesta ese multiplicador para toda proyección de nómina.

### 7.3 Reforma laboral (Ley 2466 de 2025) — lo que ya te aplica

- **42 horas/semana desde el 1 de julio de 2026** (Ley 2101/2021).
- **Recargo nocturno desde las 7:00 p.m.** (antes 9:00 p.m.), 35%.
- Recargo dominical y festivo: 80% hasta junio 2026 → **90% de julio a diciembre 2026** → **100% en 2027**.
- **Auxilio de conectividad** ($249.095/mes) para trabajadores remotos que devenguen hasta 2 SMMLV.
- Proceso disciplinario formal obligatorio (descargos escritos, mínimo 5 días hábiles).

### 7.4 Prestación de servicios vs. laboral — no te engañes

Un contrato de prestación de servicios con un desarrollador que **trabaja horario fijo, con tus herramientas y bajo tus instrucciones** es un **contrato realidad**. La contingencia: prestaciones, aportes e indemnizaciones **retroactivas hasta por 3 años**, más la sanción moratoria del art. 65 del CST.

> **Para desarrolladores de núcleo, contrata laboralmente.** Reserva la prestación de servicios para trabajo genuinamente autónomo, por entregables, con contratistas que facturen a varios clientes. Y en ambos casos, **firma la cesión de derechos patrimoniales** → [`03-datos-personales-y-propiedad-intelectual.md`](03-datos-personales-y-propiedad-intelectual.md).

---

## 8. Facturación electrónica

### 8.1 Marco

**Resolución 000165 de 2023** (anexo técnico v1.9), **consolidada por la Resolución 000227 del 23 de septiembre de 2025**, que unificó ~70 normas dispersas.

**Habilitación:** portal DIAN → Habilitación → registro como facturador → set de pruebas con el software elegido → habilitación en producción.

**Documentos del sistema:** factura electrónica de venta · notas crédito y débito · **documento soporte** (para compras a no obligados a facturar — tus contratistas) · **nómina electrónica** (obligatoria si tienes empleados) · documento equivalente electrónico · **RADIAN** (registro de la factura como título valor, para factoring).

**Novedad útil de la Res. 000227:** máximo tres datos exigibles al comprador en el checkout (tipo y número de identificación, nombre o razón social, correo) y **servicio de la DIAN para autocompletar nombre y correo desde el NIT**. Aprovéchalo para reducir fricción en tu formulario de suscripción.

### 8.2 Proveedores tecnológicos

**Alegra (planes anuales, 2026):**

| Plan | Facturación electrónica | Contabilidad | Nómina |
|---|---|---|---|
| Emprendedor | **$13.425/mes** | $56.175/mes | $22.425/mes (1–10 empleados) |
| Pyme | $37.425 | $122.925 | $51.750 (11–20) |
| Pro | $74.925 | $188.175 | $104.250 (21–45) |
| Plus | $134.925 | $239.925 | $194.250 (45–90) |

Facturas de venta ilimitadas, certificado digital gratuito y usuario contador incluidos.

**[NE]** Siigo, Factus, Dataico, Facture y Carvajal **no publican tarifas comparables de forma abierta**; requieren cotización.

> **La solución gratuita de la DIAN es válida pero no tiene API** — inviable para automatizar cobro recurrente. No la consideres.

### 8.3 Integración con el cobro recurrente

```
pago exitoso en la pasarela → webhook → tu backend → API de facturación
  → emisión → validación DIAN → envío al cliente con el CUFE
```

> **Nunca emitas la factura antes de confirmar el pago.** Una factura emitida y no pagada genera **IVA e ingreso fiscal devengado** que tendrás que anular con nota crédito — y si eso pasa a escala, tu contabilidad se vuelve un problema.

Alegra expone API de facturación electrónica, y Treli integra nativamente con Alegra. Detalle en [`04-pagos-y-cobranza-recurrente.md`](04-pagos-y-cobranza-recurrente.md).

---

## Costos no publicados — declaración explícita

1. **Autorretención especial de renta para CIIU 62xx/63xx** — rango 0,55%–4,5%; la fila exacta no está en fuente accesible.
2. **Tarifa ICA exacta para 6201** — las tablas de terceros la ubican en la agrupación 304; no confirmé la Cartilla ICA oficial.
3. **Precios de Siigo, Factus, Dataico, Facture y Carvajal.**
4. **Honorarios contables mensuales** — no hay tarifa regulada; $300.000–$800.000/mes por entidad es referencia de mercado.

## Fuentes

[UVT 2026](https://incp.org.co/publicaciones/infoincp-publicaciones/impuestos/2025/11/dian-fijaria-en-52-374-el-valor-de-la-uvt-para-2026/) · [Reforma rechazada; renta 35%, IVA 19%](https://www.ofima.com/blog/reforma-tributaria-colombia/) · [Tarifa general de renta 2026](https://actualicese.com/tarifa-general-del-impuesto-de-renta-2026-para-personas-juridicas/) · [DIAN Oficio 900930 de 2022 — IVA cloud computing](https://normograma.dian.gov.co/dian/compilacion/docs/oficio_dian_900930_2022.htm) · [IVA para SaaS — Phylo Legal](https://phylo.co/blog/iva-para-saas-en-colombia-lo-que-nadie-te-explica/) · [MinTIC — Decreto 1412/2017](https://www.mintic.gov.co/portal/715/w3-article-63377.html) · [DIAN reconsidera exención de exportación de servicios](https://incp.org.co/publicaciones/infoincp-publicaciones/impuestos/2025/02/dian-reconsidera-requisitos-para-la-exencion-del-iva-en-la-exportacion-de-servicios/) · [Régimen Simple 2026](https://siemprealdia.co/colombia/impuestos/regimen-simple-de-tributacion/) · [Grupos del RST](https://www.gerencie.com/grupos-del-regimen-simple-de-tributacion.html) · [ICA Bogotá — Res. SDH-000265/2021](https://bogota.gov.co/mi-ciudad/hacienda/se-actualizan-actividades-y-tarifas-de-ica) · [Secretaría de Hacienda — ICA](https://www.haciendabogota.gov.co/es/impuestos/impuesto-de-industria-y-comercio-ica) · [Retención en la fuente 2026 y Decreto 572](https://siemprealdia.co/colombia/impuestos/tabla-de-retencion-en-la-fuente-2026/) · [Decreto 572 de 2025](https://normograma.dian.gov.co/dian/compilacion/docs/decreto_0572_2025.htm) · [Economía naranja derogada](https://actualicese.com/tratamiento-de-rentas-exentas-en-economia-naranja-y-agropecuaria-luego-de-la-reforma-tributaria/) · [Art. 256 ET](https://estatuto.co/256) · [Exoneración de parafiscales 2026](https://actualicese.com/exonerados-de-aportes-parafiscales-en-2026/) · [Reforma laboral 2026](https://calculadoranomina.co/articulos/reforma-laboral-2026-colombia/) · [Facturación electrónica DIAN 2026](https://siemprealdia.co/colombia/impuestos/sistema-de-facturacion-electronica-en-colombia/) · [Resolución 000227 de 2025](https://www.sai-open.com/nueva/facturacion-electronica-colombia-2026-resolucion-000227/) · [Alegra — precios](https://www.alegra.com/colombia/precios/)
