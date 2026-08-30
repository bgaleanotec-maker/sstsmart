# Especificación — Matriz legal viva y servicios jurídicos

**La tesis:** la formación jurídica es el único diferenciador de este producto que **ningún competidor de software puede copiar**. Isolución no va a contratar abogados; Verifty no va a firmar conceptos. Pero para monetizarla hay que respetar una frontera que la ley colombiana dibuja con claridad, y montar la operación en dos personas jurídicas distintas.

---

## 1. La frontera: qué vende el software y qué vende el bufete

| **SST Smart SAS** (software) | **Galeano y Asociados** (bufete) |
|---|---|
| Licencia de uso de la plataforma | Concepto jurídico firmado |
| Información normativa estructurada y versionada | Asesoría personalizada al caso concreto |
| Automatización documental y plantillas | Revisión y firma de un abogado con tarjeta profesional |
| Alertas de cambio normativo | Representación ante MinTrabajo o Supertransporte |
| Cálculo de puntajes y planes de mejora | Defensa en investigación administrativa |

**Por qué importa, en concreto:**

- El **Decreto 196 de 1971** (Estatuto del Ejercicio de la Abogacía) y la **Ley 1123 de 2007** (Código Disciplinario del Abogado) estructuran la abogacía como ejercicio de **personas naturales con tarjeta profesional**, sujetas a la jurisdicción de la Comisión Nacional de Disciplina Judicial, con faltas tipificadas por publicidad y captación indebida de clientela. **Una SAS de software no "ejerce la abogacía"**; el bufete sí presta el servicio jurídico.
- **Sí se puede vender asesoría jurídica por suscripción** — no hay prohibición de ese modelo de remuneración. Lo regulado es *cómo* se ejerce y se publicita: el servicio lo presta un abogado identificado, la publicidad no puede ser engañosa ni prometer resultados, y no se puede pagar comisión a terceros por referir clientes.
- Fiscalmente: en el Régimen Simple los servicios profesionales con predominio del factor intelectual pagan **7,3%–8,3% con tope de 12.000 UVT**. Mezclar la facturación de software con la jurídica arrastra todo al grupo más caro. Ver [`../04-empresa/01`](../04-empresa/01-constitucion-y-estructura-societaria.md).

**En el producto esto se traduce en tres reglas de interfaz, no negociables:**

1. Toda respuesta generada automáticamente lleva el sello: *"Información normativa. No constituye asesoría jurídica ni sustituye el concepto de un profesional."*
2. Todo concepto jurídico muestra el **nombre y la tarjeta profesional del abogado que lo firma**, y su fecha.
3. La plataforma nunca dice "le recomendamos que…" sobre una situación concreta sin abogado detrás. Dice "la norma exige X" y ofrece escalar a consulta.

---

## 2. Matriz legal viva — el hueco #1 del mercado

### 2.1 El problema que resuelve

ISOTools e Isolución tienen "matriz de requisitos legales": una **tabla estática que alguien debe actualizar a mano**. `scripts/seed_matriz_legal.py` hoy es lo mismo — un volcado, excelente y actualizado, pero estático.

Entre 2022 y 2025 se derogaron cinco normas estructurales del SG-SST. **Ninguna plataforma revisada declara gestionar ese ciclo de vida.** Y ese es precisamente el trabajo que un abogado sabe hacer y un ingeniero no.

### 2.2 Modelo de datos

```
norma            (id, tipo{ley|decreto|resolucion|circular}, numero, año, emisor,
                  titulo, fecha_expedicion, fecha_vigencia, url_oficial,
                  estado{vigente|derogada|modificada|suspendida},
                  fecha_ultima_verificacion, verificada_por_usuario_id)
norma_relacion   (norma_origen_id, norma_destino_id,
                  tipo{deroga|modifica|reglamenta|compila|sustituye}, articulos_afectados)
requisito_legal  (norma_id, articulo, texto_obligacion, aplicabilidad_json,
                  periodicidad, evidencia_esperada)
                  -- aplicabilidad_json: {clase_riesgo:[], min_trab:, max_trab:,
                  --                      ciiu:[], tiene_flota:bool, ...}
empresa_requisito (empresa_id, requisito_id, aplica_bool, estado_cumplimiento,
                  valoracion_probabilidad, valoracion_impacto, responsable_id,
                  fecha_limite)
requisito_evidencia (empresa_requisito_id, documento_id, version, vigente_hasta)
impacto_normativo (norma_relacion_id, empresa_id, entidad_afectada{documento|control|
                  evidencia|curso|plantilla}, entidad_id, estado{pendiente|resuelto},
                  tarea_id)
```

### 2.3 El flujo que nadie más tiene

```
1. El abogado registra un cambio normativo (norma nueva + relación "deroga")
        ↓
2. El sistema resuelve qué requisitos quedan sin vigencia y cuáles nacen
        ↓
3. Para CADA empresa, evalúa aplicabilidad_json contra su perfil
   (clase de riesgo, trabajadores, CIIU, flota, sedes)
        ↓
4. Genera registros en impacto_normativo: qué documentos, controles,
   evidencias y cursos de esa empresa quedan desactualizados
        ↓
5. Crea tareas con responsable y fecha límite
        ↓
6. Notifica: al responsable SST de la empresa y, si hay consultor,
   a su consola multiempresa agregada
        ↓
7. El tablero muestra "3 documentos afectados por la Res. 3461/2025"
   con enlace directo a cada uno
```

**Ese paso 4 es el producto.** Es la diferencia entre "aquí está la norma nueva" (lo que hacen todos) y "estos tres documentos suyos quedaron obsoletos y aquí están las tareas" (lo que no hace nadie).

### 2.4 Contenido inicial ya disponible

`scripts/seed_matriz_legal.py` ya tiene resueltas las derogatorias clave: Res. 2764/2022 (derogó la 2404/2019) · Res. 1843/2025 (derogó la 2346/2007) · Res. 3461/2025 (derogó 652 y 1356 de 2012) · Res. 908/2025 (licencias SST) · Ley 2466/2025 · Ley 2101/2021 (42 horas desde el 15-jul-2026) · Ley 2365/2024 · Ley 2191/2022 · Circular 027/2026.

Falta añadir el bloque de seguridad vial: Ley 1503/2011, Decreto 2851/2013, Res. 40595/2022, Res. 5178/2023 (Supertransporte), **Circular 0034/2026** y Ley 2251/2022 — esta última **como marco, no como fuente de obligación PESV**, que es un error común del sector.

### 2.5 Procedimiento de vigilancia normativa

Esto no es opcional: es lo que reduce la exposición por responsabilidad profesional (§5) y lo que se le muestra a un cliente que pregunta "¿y cómo sé que está al día?".

| Frecuencia | Fuente | Responsable |
|---|---|---|
| Diaria | Diario Oficial (imprenta.gov.co), alertas de MinTrabajo y MinTransporte | Automatizado + revisión del abogado |
| Semanal | Safetya, Consejo Colombiano de Seguridad, normogramas de Función Pública | Abogado |
| Mensual | Conceptos y circulares de MinTrabajo, MinSalud, Supertransporte | Abogado |
| Trimestral | Jurisprudencia de la Corte Constitucional y el Consejo de Estado sobre SST | Abogado |
| Anual | Revisión completa de la matriz, norma por norma | Abogado |

Cada norma guarda `fecha_ultima_verificacion` y `verificada_por_usuario_id`. **Ese campo se muestra en la interfaz** — es la prueba visible de diligencia, y es también la defensa si algún día hay una reclamación.

---

## 3. El retainer jurídico — planes

Ancla de precio del mercado: **Legis silvIA cobra $159.664/mes por IA jurídica con consultas ilimitadas**. Ese es el techo mental del comprador colombiano para *"inteligencia normativa"*. Lo que se cobre por encima tiene que ser **trabajo humano de abogado**, no software.

| Plan | Precio/mes | Qué incluye | Quién lo presta |
|---|---|---|---|
| **Legal Básico** | **$190.000** | Matriz legal viva con alertas · 2 consultas escritas/mes (respuesta ≤5 días hábiles) · revisión anual del SG-SST con informe | Bufete |
| **Legal Plus** | **$490.000** | Todo lo anterior · 6 consultas/mes (≤3 días hábiles) · **conceptos escritos firmados** · revisión de contratos laborales y de contratistas · reglamento interno de trabajo | Bufete |
| **Legal Defensa** | **$1.290.000** | Todo lo anterior · consultas ilimitadas · **acompañamiento en visita de inspección** del MinTrabajo · 1 requerimiento o investigación administrativa/año incluido · respuesta a requerimientos en 24 h | Bufete |

**Servicios por proyecto (facturación aparte, no MRR):**

| Servicio | Precio | Referencia de mercado |
|---|---|---|
| Implementación completa del SG-SST | $2.900.000 – $6.900.000 | Mentora: $1,49M–$7,89M · Proestrategia: desde $2,5M |
| **Diseño e implementación del PESV** | **$4.900.000** | Mercado: $8M–$20M |
| Defensa en investigación administrativa | Cuota fija + éxito | — |
| Auditoría interna del SG-SST o del PESV | $1.900.000 | — |
| Batería de riesgo psicosocial (Res. 2764/2022) | Aliado con psicólogo licenciado | Mercado: desde $1,1M |

> **Regla de oro del retainer:** el cupo de consultas debe ser **suficientemente generoso para que el cliente lo perciba como incluido, y suficientemente acotado para que no consuma el margen**. Con Legal Básico a $190.000 y 2 consultas, cada consulta cuesta $95.000 de ingreso — sostenible solo si la mayoría se resuelve con plantillas ya construidas. **Mide el consumo real desde el primer mes** y ajusta antes de escalar el plan.

---

## 4. Cómo se opera dentro de la plataforma

El módulo `juridico` ya existe (consultas con SLA por prioridad, asignación a abogado, conceptos y PDF). Lo que falta para convertirlo en retainer:

| Funcionalidad | Descripción |
|---|---|
| **Cupo por plan** | Contador de consultas del mes, visible para el cliente. Consulta N+1 se ofrece como excedente pagado, no se rechaza en silencio |
| **SLA diferenciado** | 5 / 3 / 1 días hábiles según plan, con reloj visible y alerta al abogado |
| **Biblioteca de respuestas** | Las 50 consultas más frecuentes, con respuesta base que el abogado adapta y firma. **Es lo que hace rentable el retainer** |
| **Expediente por empresa** | Todas las consultas, conceptos y documentos en un solo lugar, exportable |
| **Firma y tarjeta profesional** | Cada concepto sale con nombre, tarjeta y fecha del abogado |
| **Escalamiento desde cualquier módulo** | Botón "consultar al abogado" en la matriz legal, la autoevaluación y el PESV, que arrastra el contexto del ítem |
| **Facturación separada** | El retainer lo factura el bufete, no la SAS de software. Dos facturas, dos NIT |

---

## 5. Gestión del riesgo profesional

**El escenario que hay que prevenir:** un cliente es sancionado por el Ministerio del Trabajo porque la matriz legal seguía citando la Res. 2404/2019, derogada en 2022. La exposición es contractual y potencialmente extracontractual.

**Seis controles, en orden de efectividad:**

1. **Procedimiento documentado de vigilancia normativa** (§2.5), con `fecha_ultima_verificacion` visible por norma en la interfaz. Es la prueba de diligencia.
2. **Disclaimers en producto:**
   - *"El contenido normativo de esta plataforma es informativo y no constituye asesoría jurídica ni sustituye el concepto de un profesional."*
   - *"La responsabilidad del cumplimiento del SG-SST recae en el empleador conforme al Decreto 1072 de 2015."*
3. **Limitación contractual de responsabilidad** al valor pagado en los últimos 12 meses. Válida entre comerciantes, **pero no oponible frente a dolo o culpa grave** — no es un escudo absoluto.
4. **Póliza de responsabilidad civil profesional (E&O).** Disponible en Colombia (SBS Seguros y otros corredores). **[NE]** La prima real para E&O tecnológico-jurídico no está publicada; el rango de $500.000–$2.000.000 anuales que circula corresponde a RC general de pequeñas empresas, no a E&O. **Cotizar con corredor, no presupuestar el rango.**
5. **Separación societaria** (§1): el error de un concepto no debe poder ejecutarse contra el código, la marca ni los contratos de suscripción.
6. **Revisión humana obligatoria de toda salida de IA** que llegue al cliente como recomendación. Hay presión regulatoria creciente sobre decisiones automatizadas: si el módulo de IA sugiere clasificaciones de riesgo que afecten a un trabajador, **documenta que hay revisión humana y que la IA no decide sola**.

---

## 6. Por qué esto gana

Safetya tiene la autoridad normativa del país y no tiene software transaccional. ISOTools tiene el software y no tiene abogados. Las ARL regalan un archivador que no se actualiza. Los cinco chatbots del mercado conversan sobre la norma pero ninguno propaga el impacto de una derogatoria a los documentos concretos de una empresa concreta.

**La combinación de matriz legal viva + retainer firmado por abogado es un foso que un competidor de software no cruza contratando a un desarrollador más.** Tiene que montar un bufete.
