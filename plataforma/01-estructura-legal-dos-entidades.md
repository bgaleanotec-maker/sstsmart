# Estructura legal: S.A.S. de apps + abogado persona natural

> Concepto de trabajo (13-oct-2026). No reemplaza la validación de un especialista en régimen
> disciplinario y protección de datos antes del lanzamiento B2C. Complementa
> `docs/02-producto/04-especificacion-servicios-juridicos.md` (frontera software/bufete para SST).
> El texto de la Ley 1123/2007 se tomó de su transcripción en la Sentencia C-009/2023: **confirmar numerales contra SUIN-Juriscol** `[VERIFICAR]`.

---

## 1. Las dos entidades

| | **S.A.S. de apps** (nombre por decidir, D2) | **Brian Galeano, abogado** (marca "Galeano y Asociados") |
|---|---|---|
| Qué vende | Licencias SaaS B2B (SST, PESV) y herramientas B2C de autoservicio (peticiones, tutelas, calendario tributario, guías de accidente) | Servicios profesionales: conceptos firmados, representación, defensa DIAN, litigio, retainer jurídico |
| Código CIIU | 6201 + 6311, 7020, 6202 · **sin 6910** (decisión vigente en `empresa/`) | Persona natural con tarjeta profesional |
| Contrato con el cliente | Términos y condiciones de la plataforma | Contrato de prestación de servicios profesionales (poder cuando aplique) |
| Factura | La S.A.S. | El abogado (factura electrónica propia) |
| Responde por | El funcionamiento del software | El servicio profesional (régimen disciplinario y civil) |
| Datos | Responsable frente a usuarios B2C; encargado frente a empresas B2B | Responsable de los datos de sus clientes; secreto profesional |

**Regla:** cuentas, bases de datos, dominios y facturación separados. Si el abogado usa la plataforma, paga la misma tarifa SaaS que pagaría otro abogado, por escrito.

## 2. Qué puede hacer la S.A.S. sin "ejercer la abogacía"

| Norma | Regla | Efecto |
|---|---|---|
| Decreto 196/1971, art. 25 | Nadie litiga en causa propia o ajena sin ser abogado inscrito, salvo excepciones | La S.A.S. nunca actúa como apoderada ni radica en nombre del usuario |
| Decreto 196/1971, art. 28 | Excepciones: derecho de petición y acciones públicas; mínima cuantía (hasta 40 SMMLV, art. 25 CGP); conciliación administrativa y laboral de única instancia; oposición en secuestro y entrega | **Lista blanca** de trámites que la app puede generar |
| Decreto 2591/1991, arts. 10 y 14 | La tutela la presenta el afectado, sin apoderado | La tutela está en la lista blanca |
| CGP, art. 73 | Se comparece por abogado salvo que la ley permita actuar directamente | Demandas de menor/mayor cuantía, recursos en procesos con apoderado y demanda contencioso-tributaria: **fuera** de la app, se derivan |
| Ley 2452/2025 (nuevo CPTSS) | Habría eliminado la única instancia laboral `[VERIFICAR]` | Que la mínima cuantía laboral sea sin abogado está `[VERIFICAR]`. Hasta confirmarlo, lo laboral judicial **se deriva** |

**Productos de la S.A.S. que rozan el límite:** "informe de un acto DIAN", "calculadora de accidente" y "tutela premium" son legítimos solo como **cálculos y chequeos automáticos genéricos, sin recomendación sobre el caso concreto**. Si interviene criterio humano sobre el caso, es servicio del abogado y lo factura él.

**Dónde está el riesgo:** pasar de herramienta a asesoría personalizada (analizar el caso concreto y recomendar estrategia), presentar la IA como "abogado" o generar escritos para trámites que exigen abogado. Si la S.A.S. "ejerce" sin ser abogada, la exposición disciplinaria recae en Brian como socio y abogado (patrocinio del ejercicio ilegal, Ley 1123 art. 30, numeral `[VERIFICAR]`).

## 3. Ley 1123/2007 aplicada al modelo

| Regla | Artículo | Qué significa para el producto |
|---|---|---|
| No usar intermediarios para obtener poderes ni compartir honorarios con quien recomienda | Art. 30 num. 5 | La S.A.S. **no cobra por cliente derivado** ni recibe parte de honorarios |
| No captar clientes aprovechando una calamidad | Art. 30 num. 7 | **Accidentes:** cero contacto proactivo, cero notificaciones de venta jurídica, cero *retargeting* tras registrar un siniestro |
| Publicidad del abogado limitada a nombre, títulos, cargos, áreas y domicilio | Art. 31 num. 1 | El marketing de Galeano y Asociados va separado del de la app. Sin testimonios, sin montos ganados, sin "el mejor" |
| No garantizar resultados | Art. 34 | Ni la app ni el abogado prometen ganar |
| No representar intereses contrapuestos (también dentro de una firma) | Art. 34 lit. e | **Control de conflictos** antes de aceptar un caso (ver §6) |
| Secreto profesional | Art. 34 lit. f; art. 28 (num. `[VERIFICAR]`) | Muro de datos entre la S.A.S. y la práctica |
| Revelar relaciones que afecten la independencia | Art. 34 lit. h | Revelar que el abogado es socio de la S.A.S. |
| Honorarios no desproporcionados ni mayores que la participación del cliente | Art. 35 nums. 1 y 2 | Techo práctico de cuota litis: **50%**. La CNDJ absolvió un pacto del 50% (Rad. 17001110200020190033601, 31-ene-2024) |

**Recomendación de cuota litis** `[E]`: 20-30% más un fijo moderado en tránsito y laboral; dejar por escrito la base del porcentaje (bruto o neto de gastos); documentar la complejidad. Tarifas CONALBOS 2026 `[VERIFICAR]`.

No se encontró jurisprudencia de la Comisión Nacional de Disciplina Judicial sobre captación por plataformas `[VERIFICAR en su relatoría]`. Sí hay sanciones por conducta del abogado en redes (Rad. 540012502000202100976 01, 24-mar-2026): la CNDJ juzga lo digital con el mismo estándar.

## 4. Derivación lícita de la app al abogado

| Elemento | Diseño obligatorio |
|---|---|
| Iniciativa del usuario | Botón "Hablar con un abogado". Nunca un paso obligatorio del flujo |
| Alternativas | Mostrar siempre Defensoría del Pueblo, consultorios jurídicos y "cualquier abogado de su confianza" |
| Revelación | "Galeano y Asociados es la práctica de Brayan Galeano Tobón, socio de [S.A.S.]" |
| Datos | Se comparten con el abogado **solo** con una autorización separada, específica y revocable |
| Dinero | Sin comisión por referido. Contrato y factura del abogado aparte |
| Tránsito | Derivación solo a petición del usuario, con un periodo de reflexión `[E: 48 h]` desde el registro del siniestro |
| A futuro | Directorio con varios abogados (D8): reduce el riesgo del art. 30 num. 5 y libera capacidad |

## 5. IA, consumidor y datos personales

**IA**
- **Sentencia T-323/2024** (Corte Constitucional): principios de transparencia, responsabilidad, privacidad, no sustitución del razonamiento humano y verificación. Obliga a jueces; es estándar orientador para abogados.
- **Acuerdo PCSJA24-12243** (CSJ, vigente desde el 16-dic-2024): declarar el uso de IA en actos judiciales. Orientador para litigantes: buena práctica declararlo.
- **Circular Externa SIC 002 del 21-ago-2024**: **sí obliga a la S.A.S.** Test de idoneidad, necesidad y proporcionalidad; estudio de impacto de privacidad previo si hay alto riesgo; autorización expresa para datos sensibles; prohibido entrenar modelos con ellos sin autorización.
- Proyecto de ley de IA de Minciencias (ago-2026): sin aprobar `[VERIFICAR]`.

**Consumidor (Ley 1480/2011)**
- Retracto de 5 días hábiles en ventas a distancia (art. 47). Excepción si el servicio empezó con acuerdo del consumidor: pedir aceptación expresa ("Solicito iniciar ahora y entiendo que pierdo el retracto").
- Precio total con IVA, cancelación simple de suscripciones, reembolso en 30 días cuando proceda.
- No exonerar totalmente a la S.A.S. de responsabilidad: riesgo de cláusula abusiva `[VERIFICAR art. 43]`.

**Datos (Ley 1581/2012)**
- Salud (tutelas) y lesiones (accidentes) son **datos sensibles**: autorización explícita y facultativa, finalidad específica, cifrado, mínimo necesario.
- Datos de menores (tutelas de menores): régimen reforzado `[VERIFICAR art. 7]`.
- Proveedor de IA en el exterior = transmisión o transferencia internacional: contrato de transmisión.
- Registro de bases en el RNBD según umbral `[VERIFICAR]`.
- Historia clínica: reservada (Res. 1995/1999, Ley 2015/2020); solo con autorización del paciente.

## 6. Conflictos de interés (nuevo — no estaba en el dossier)

| Situación | Riesgo | Control |
|---|---|---|
| Empresa con retainer SST/PESV (cliente del abogado) y trabajador que llega por la app laboral contra esa empresa | Intereses contrapuestos (art. 34 lit. e) | Bloqueo automático: no se acepta. Se ofrece el directorio o la Defensoría |
| Empresa con PESV (cliente B2B) y víctima de un vehículo de esa empresa | Ídem si la empresa tiene retainer; reputacional si solo es cliente SaaS | Bloqueo con retainer; con solo SaaS, decisión caso a caso registrada |
| Usuario de tutela contra una EPS que es cliente B2B | Bajo hoy (no hay EPS clientes), alto si se vende B2B a IPS o EPS | No vender B2B a EPS mientras exista la vertical de tutelas de salud |
| Empleador de Brian (Vanti) | Conflicto con el contrato laboral `[VERIFICAR cláusulas]` | No aceptar casos contra Vanti ni su grupo; revisar exclusividad |

**Implementación:** tabla `contraparte` normalizada por NIT o cédula, con verificación al crear un caso en la consola del abogado. Ver épica E6 en `06-backlog-claude-code.md`.

## 7. Tributario básico

| Punto | Dato | Fuente |
|---|---|---|
| UVT 2026 | $52.374 | Res. DIAN 000238/2025 [V] |
| Abogado persona natural, no responsable de IVA | Hasta 3.500 UVT ($183.309.000 en 2026) y demás requisitos del art. 437 par. 3 ET. Los honorarios jurídicos están gravados | Actualícese [V] |
| Facturación electrónica del abogado | Profesionales liberales obligados, salvo exceptuados `[VERIFICAR alcance de la Res. DIAN 000227/2025]` | Gerencie |
| Régimen SIMPLE para profesiones liberales | La C-540/2023 revivió el régimen de la Ley 2155/2021 `[VERIFICAR tarifas 2026]` | Ámbito Jurídico |
| S.A.S. de software | Régimen ordinario, responsable de IVA, factura con 19% (decisión vigente en `empresa/`) | `empresa/02-dian-y-facturacion/` |

## 8. Cuándo pasar del abogado persona natural a una sociedad de abogados

Cualquiera de estas señales:
- ingresos jurídicos cerca de 3.500 UVT o necesidad de facturar con IVA de todas formas;
- contratar o asociar a otros abogados;
- clientes corporativos que exigen contratar con persona jurídica;
- volumen de casos derivados que justifique separar patrimonio y responsabilidad (en `empresa/`: retainer > $3M/mes sostenido).

Forma: S.A.S. con objeto exclusivamente jurídico prestado por abogados inscritos. **Nunca fusionarla con la S.A.S. de apps.** No se encontró registro especial obligatorio para sociedades de abogados en 2026 `[VERIFICAR]`.

## 9. Doce reglas de diseño de producto (obligatorias para Code)

1. **Nunca prometer resultados**: sin "gana tu tutela", sin tasas de éxito nacionales presentadas como propias, sin montos.
2. **Lista blanca de trámites** (§2). Fuera de ella, la app bloquea, explica por qué y ofrece derivar.
3. **Aviso permanente**: "Herramienta de autoservicio. No es asesoría ni representación jurídica. Usted revisa, firma y presenta el documento."
4. **El usuario es autor y firmante**: revisión obligatoria antes de descargar. La app no radica ni actúa por él.
5. **Botón "Hablar con un abogado"** opcional, con revelación del vínculo y alternativas gratuitas.
6. **Cero comisión** por cliente derivado.
7. **Tránsito: no captar en calamidad**: sin contacto proactivo ni *retargeting*; periodo de reflexión.
8. **Muro de datos**: transferencia al abogado solo con autorización separada y revocable; auditada.
9. **Etiqueta de IA** en cada documento: modelo, fecha, aviso de posibles errores y verificación de citas.
10. **Datos sensibles mínimos**: autorización explícita, cifrado, nunca para entrenar modelos, estudio de impacto antes de lanzar.
11. **Pago y retracto transparentes**: precio con IVA, aceptación expresa de inicio inmediato, cancelación en un clic.
12. **Control de conflictos** antes de aceptar cualquier caso en la consola del abogado.

Fuentes: `fuentes.md` §1.
