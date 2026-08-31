# Las dos decisiones tributarias que no se deshacen barato

Se toman **antes de emitir la primera factura**. Cambiarlas después significa notas
crédito, refacturación y una conversación incómoda con cada cliente.

---

## 1. Contexto 2026

- **[NE]** La reforma tributaria estructural habría sido **rechazada por el Congreso el 9 de diciembre de 2025**; el marco seguiría siendo la **Ley 2277 de 2022**. El dato viene del dossier del repositorio, no de fuente primaria: **confírmalo con tu contador antes de basar una decisión en él**.
- **UVT 2026 = $52.374** · **SMMLV = $1.750.905**
- Tarifa general de renta para personas jurídicas: **35%**
- Tarifa general de IVA: **19%**

---

## 2. Decisión 1 — ¿IVA al 19% o exclusión por computación en la nube?

### 2.1 La norma

El **art. 476 num. 21 del Estatuto Tributario** excluye de IVA *"el suministro de páginas
web, servidores (hosting), computación en la nube y mantenimiento a distancia de programas
y equipos"*, reglamentado por el **Decreto 1412 de 2017**.

Suena hecho a la medida de un SaaS. Pero:

### 2.2 Cómo lo interpreta la DIAN — restrictivamente

| Doctrina | Qué exige |
|---|---|
| **Concepto 1444 del 22-dic-2017** | Un **autodiagnóstico conforme a la guía técnica de MinTIC, firmado por el responsable técnico**, para acreditar que el servicio es genuinamente computación en la nube |
| **Oficio 900930 de 2022** | La exclusión aplica **exclusivamente al proveedor de nube** —quien adquiere y gestiona la infraestructura y ejecuta el software en la nube—. **No aplica a corredores, agentes ni revendedores.** Los beneficios tributarios son de interpretación restrictiva |
| **Concepto 190 del 18-mar-2024** | Un intermediario solo accede *"si actúa como proveedor y cumple los modelos de servicio de cloud computing"* |

### 2.3 Las dos opciones, honestamente

| | **Opción A — facturar sin IVA** | **Opción B — facturar con 19%** |
|---|---|---|
| Requisito | Autodiagnóstico MinTIC firmado, documentación de arquitectura multi-tenant y de medición de consumo, **mantenidos vivos** | Ninguno |
| Efecto en tu precio | Precio final 19% menor | Precio final 19% mayor |
| Efecto real en el cliente | **Ninguno.** Tus clientes son empresas responsables de IVA: el 19% es **descontable para ellos** | **Ninguno**, por lo mismo |
| Efecto en tu caja | Positivo | Neutro — el IVA no es tuyo, lo recaudas y lo giras |
| Riesgo | Glosa de la DIAN por IVA no facturado, sobre **todas** las facturas del período no prescrito, más sanción e intereses | Cero |
| Trabajo que exige | Real y continuo | Cero |

### 2.4 Recomendación: **Opción B — inscríbete como responsable de IVA (código 48) y factura con 19%**

Tres razones, en orden de peso:

1. **La exclusión no te compra nada comercialmente.** El argumento "somos más baratos porque no cobramos IVA" no existe frente a un cliente que descuenta ese IVA. Estás asumiendo un riesgo fiscal a cambio de un beneficio que el cliente no percibe.
2. **El costo de mantener la posición es tiempo que no tienes.** El autodiagnóstico MinTIC no es un PDF que se firma una vez: es documentación técnica que debe reflejar la arquitectura real y actualizarse cuando cambia.
3. **La asimetría de consecuencias es brutal.** Si aciertas, ganas flujo de caja. Si fallas, una glosa sobre tres o cuatro años de suscripciones es existencial para una empresa de una persona.

**Cuándo revisar esta decisión:** cuando la plataforma tenga arquitectura multi-tenant
documentada, medición de consumo por tenant, y presupuesto para que un asesor tributario
monte y sostenga el expediente. Migrar de B a A es viable y prospectivo. Migrar de A a B
retroactivamente es el escenario que queremos evitar.

### 2.5 Si algún día eliges la Opción A — la regla que hay que recordar

**Desagrega precios.** Si vendes suscripción + consultoría en un paquete, **la consultoría
sí lleva 19%** y debe ir en factura separada. Un paquete indivisible facturado sin IVA es
la forma más fácil de perder la discusión.

**Lo que la exclusión nunca cubre:** dominios, certificados SSL, correo premium, email
marketing, ni el producto digital terminado.

### 2.6 Exportación de servicios

Si vendes a un cliente sin negocios en Colombia y el servicio se usa exclusivamente en el
exterior, la operación es **exenta (0%) con derecho a devolución del IVA descontable** —
siempre que inscribas la **responsabilidad 19** y cumplas los requisitos formales de la reglamentación vigente (compilada en el **Decreto 1625 de 2016**, el DUR tributario — **[NE]** no verifiqué el artículo exacto). La DIAN reconsideró varios de esos requisitos formales en 2025:
**verifica el estado con tu contador antes de la primera exportación.**

---

## 3. Decisión 2 — ¿Régimen ordinario o Régimen Simple (RST)?

### 3.1 Los números

| Elemento | Valor 2026 |
|---|---|
| Tope general de ingresos brutos del año anterior para el RST | < 100.000 UVT |
| **Tope para servicios profesionales / consultoría** | **12.000 UVT** |
| Tarifa RST — comercio, servicios técnicos | 1,6% – 4,5% sobre ingresos brutos |
| **Tarifa RST — servicios profesionales y consultoría (predominio del factor intelectual)** | **7,3% – 8,3% sobre ingresos brutos** |
| Descuento por pagos electrónicos | 0,5% |
| Plazo de inscripción para el año gravable | 27 de febrero. **Empresas nuevas: al inscribir el RUT, en cualquier momento del año** |

### 3.2 Recomendación: **régimen ordinario**

| A favor del RST | En contra |
|---|---|
| Unifica renta + ICA + avisos y tableros + sobretasa bomberil en una sola declaración | **No puedes compensar pérdidas fiscales** — y una plataforma en años 1–3 casi siempre las tiene |
| Elimina la retención en la fuente sobre tus ingresos, lo que mejora la caja | **No puedes aplicar el descuento del art. 256 ET por I+D+i** (30% del valor invertido) |
| Menos declaraciones y menos contador | **Riesgo de clasificación** en el grupo de 7,3–8,3% |

**El riesgo de clasificación es el argumento decisivo.** Que "desarrollo de software" sea
un servicio técnico (predominio material, 1,6–4,5%) o consultoría (predominio intelectual,
7,3–8,3%) **no es evidente, y la DIAN ha sido inconsistente**. Si cae en consultoría, una
plataforma con margen bruto de 40% pagaría el equivalente a más del 20% de su utilidad —
y además quedaría atrapada en el tope de 12.000 UVT, que con un ticket de $349.000/mes se
alcanza con relativamente pocos clientes.

**El RST es para operaciones rentables desde el día uno, con poca estructura de costos.**
Esta no lo es.

---

## 4. Beneficios tributarios de tecnología — qué sirve y qué es mito

| Beneficio | Estado 2026 |
|---|---|
| **Renta exenta de economía naranja** (art. 235-2 num. 1 ET) | **DEROGADA** por el art. 96 de la Ley 2277 de 2022. Solo la conservan quienes ya habían accedido con acto de conformidad emitido. **No es una vía disponible para una empresa nueva** — a pesar de que sigue apareciendo en material comercial desactualizado y en asesorías que no se han actualizado |
| **Descuento por inversión en I+D+i** (art. 256 ET) | **VIGENTE — 30%** del valor invertido, descontable del impuesto a cargo. Requiere **calificación previa del proyecto** por el Consejo Nacional de Beneficios Tributarios en CTeI (convocatoria anual de Minciencias) |
| Deducción por inversión en I+D+i (art. 158-1 ET) | Vigente, complementaria |
| Crédito fiscal I+D+i (art. 256-1 ET) | Vigente, dirigido a MiPymes; es un título negociable con la DIAN |

> **El descuento del art. 256 es el único beneficio realmente accesible y significativo.**
> Y tiene un detalle que lo arruina si se pasa por alto: **el proyecto se califica ex ante,
> no ex post**. Si vas a construir el módulo de SAGRILAFT o la matriz legal automatizada,
> preséntalo a la convocatoria de Minciencias **antes** de ejecutarlo. Presentado después,
> no sirve.

---

## 5. Retención en la fuente — cambios vigentes desde julio de 2026

**[NE]** Según el dossier del repositorio, el **Decreto 572 de 2025** fue suspendido
provisionalmente por el Consejo de Estado el 8 de mayo de 2026 y **reactivado el 1 de julio
de 2026**. No verifiqué esos dos hechos procesales en fuente primaria, y de ellos depende
toda la liquidación de retenciones a aliados. **Confírmalos con tu contador antes de la
primera liquidación.** Te aplica como agente retenedor cuando pagues comisiones a afiliados
y honorarios a contratistas:

| Concepto | Tarifa | Base mínima desde 1-jul-2026 |
|---|---|---|
| Honorarios y consultoría — persona jurídica | 11% | sin base |
| Honorarios y comisiones — persona natural **declarante** | 11% | sin base |
| Honorarios y comisiones — persona natural **no declarante** | 10% | sin base |
| Servicios generales — declarantes | 4% | 2 UVT = $104.748 |
| Compras generales — declarantes | 2,5% | 10 UVT = $523.740 |

> **[NE]** Las tarifas de honorarios y comisiones a personas naturales (10%/11%) son las
> tarifas históricamente aplicables del art. 392 ET; **no verifiqué que el Decreto 572 no
> las haya modificado**. Confírmalas con tu contador antes de la primera liquidación de
> comisiones de afiliados. Es directamente relevante para
> [`../04-programa-afiliados/`](../04-programa-afiliados/).

**[NE]** Tampoco pude verificar en fuente pública el porcentaje exacto de **autorretención
especial de renta** para los CIIU 62xx/63xx. El rango publicado es 0,55%–4,5% y las tarifas
altas corresponden a café, hidrocarburos y generación eléctrica. Consulta la tabla del art.
1.2.6.8 del DUT (anexo del Decreto 572) con tu contador — **no uses un valor supuesto**.

---

## 6. Resumen ejecutable

| Decisión | Respuesta | Se ejecuta en |
|---|---|---|
| IVA | **Responsable, código 48, facturar con 19%** | RUT casilla 53 |
| Régimen | **Ordinario, código 05** | RUT casilla 53 |
| ICA | Actividad 6201, agrupación 304, tarifa a confirmar en el RIT | RIT Bogotá |
| Beneficio de I+D | Presentar el proyecto a Minciencias **antes** de ejecutarlo | Convocatoria anual |

---

## Fuentes

[UVT 2026](https://incp.org.co/publicaciones/infoincp-publicaciones/impuestos/2025/11/dian-fijaria-en-52-374-el-valor-de-la-uvt-para-2026/) ·
[DIAN Oficio 900930 de 2022 — IVA cloud computing](https://normograma.dian.gov.co/dian/compilacion/docs/oficio_dian_900930_2022.htm) ·
[MinTIC — Decreto 1412 de 2017](https://www.mintic.gov.co/portal/715/w3-article-63377.html) ·
[Régimen Simple 2026](https://siemprealdia.co/colombia/impuestos/regimen-simple-de-tributacion/) ·
[Grupos del Régimen Simple](https://www.gerencie.com/grupos-del-regimen-simple-de-tributacion.html) ·
[Economía naranja derogada](https://actualicese.com/tratamiento-de-rentas-exentas-en-economia-naranja-y-agropecuaria-luego-de-la-reforma-tributaria/) ·
[Art. 256 ET](https://estatuto.co/256) ·
[Retención en la fuente 2026 y Decreto 572](https://siemprealdia.co/colombia/impuestos/tabla-de-retencion-en-la-fuente-2026/) ·
[Decreto 572 de 2025](https://normograma.dian.gov.co/dian/compilacion/docs/decreto_0572_2025.htm) ·
[Tarifa general de renta 2026](https://actualicese.com/tarifa-general-del-impuesto-de-renta-2026-para-personas-juridicas/)
