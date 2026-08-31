# Programa de Aliados — diseño económico y reglas

**El canal de consultores SST es el mejor CAC y el mejor LTV del plan de negocio.** Un
consultor independiente atiende entre 5 y 30 empresas, ya tiene la confianza del cliente, y
ya está resolviendo el problema a mano. No hay que convencerlo del problema: hay que darle
la herramienta y una razón económica para llevarla.

---

## 1. Qué modelo elegimos y por qué

Hay tres formas de remunerar a un aliado. Se eligió la primera como programa principal.

| Modelo | Cómo funciona | Por qué sí / por qué no |
|---|---|---|
| **Comisión por venta referida** ← **elegido** | El aliado refiere una empresa; gana un porcentaje de lo que esa empresa pague, mientras siga pagando | **Alineación perfecta**: el aliado gana solo si el cliente permanece, así que le importa que use la plataforma. Cero riesgo de caja: la comisión sale de un ingreso ya recibido. Simple de explicar en una llamada de tres minutos |
| Descuento por uso (plan Canal) | El consultor compra un paquete de N empresas a precio de canal y le factura a su cliente lo que quiera | Se mantiene **como opción secundaria** para el consultor que quiere marca propia y controlar el precio final. Requiere que el consultor asuma el riesgo de cartera |
| Comisión única por activación | Pago fijo por cada empresa que active y pague el primer mes | Descartado como modelo principal: incentiva vender y desaparecer. El churn del mes 2 es problema tuyo, no suyo |

---

## 2. La tabla de comisiones

| Concepto | Valor |
|---|---|
| **Comisión de lanzamiento** | **20%** del valor facturado sin IVA, durante los **primeros 12 meses** de cada cliente referido |
| **Comisión de permanencia** | **10%** del valor facturado sin IVA, **del mes 13 en adelante**, mientras el cliente siga activo y al día |
| **Nivel Aliado Senior** | Al alcanzar **10 clientes activos**, la comisión de lanzamiento sube a **25%** para los referidos nuevos |
| Add-ons (PESV, retainer jurídico) | Mismo porcentaje que el plan base |
| Consultoría e implementación facturada aparte | **Sin comisión** (margen bajo, trabajo tuyo) |

### Lo que gana un aliado, en pesos

Sobre los precios de lista del plan de monetización:

| Plan | Precio mes | Comisión mes 1–12 (20%) | **Año 1** | Comisión desde mes 13 (10%) | Año 2 en adelante |
|---|---|---|---|---|---|
| Esencial | $149.000 | $29.800 | **$357.600** | $14.900 | $178.800 |
| Profesional | $349.000 | $69.800 | **$837.600** | $34.900 | $418.800 |
| Corporativo | $749.000 | $149.800 | **$1.797.600** | $74.900 | $898.800 |

**El número que hay que decirle a un consultor:**

> *Cinco clientes en plan Profesional te dan **$349.000 al mes** el primer año, y
> **$174.500 al mes** de ahí en adelante sin volver a vender. Diez clientes son
> **$698.000 mensuales** el primer año.*

Ese es un ingreso pasivo real para un consultor independiente, y es lo que hace que valga la
pena la conversación.

### Lo que te cuesta a ti

| Concepto | Plan Profesional |
|---|---|
| Ingreso mensual | $349.000 |
| Comisión año 1 (20%) | −$69.800 |
| Costo de infraestructura por tenant (estimado) | −$25.000 **[NE]** |
| **Margen bruto mes, año 1** | **~$254.200 (73%)** |
| Margen bruto mes, año 2 en adelante | ~$289.100 (83%) |

Un cliente adquirido por canal deja **73% de margen bruto desde el primer mes**, sin gasto
de publicidad y sin ciclo de venta tuyo. Compáralo con el costo y el tiempo de conseguir ese
mismo cliente por contenido o por venta directa.

**[NE]** El costo de infraestructura por tenant es una estimación, no una medición. Ajústalo
cuando tengas datos reales de consumo.

---

## 3. Reglas del programa

### 3.1 Quién puede ser aliado

- Consultores y asesores en SG-SST, seguridad vial o cumplimiento
- Contadores, revisores fiscales y abogados con cartera de pymes
- Profesionales con licencia SST vigente
- Empresas de servicios de gestión y outsourcing

**No pueden serlo:** empleados de la sociedad · personas que representen legalmente a la
empresa referida, salvo declaración expresa y aprobación previa · quien esté vinculado a un
competidor directo.

### 3.2 Atribución — cómo se decide de quién es un referido

Dos vías, en este orden de prelación:

1. **Registro previo del prospecto** (gana siempre). El aliado registra el NIT en su panel. Queda reservado **90 días**. Si esa empresa contrata en ese plazo, el referido es suyo aunque haya llegado por otro canal.
2. **Enlace de referido.** `https://[dominio]/?ref=CODIGO` deja una cookie de **90 días**. Si la empresa se registra dentro de ese plazo y el NIT no estaba reservado por otro, el referido se atribuye a ese código.

**Conflictos:** el registro previo vence al enlace. Entre dos registros previos del mismo
NIT, gana el primero en el tiempo. Un NIT que ya es cliente activo **no puede ser referido**.

### 3.3 Cuándo se causa la comisión

La comisión se causa cuando **la factura del cliente referido está efectivamente pagada**.
No al firmar, no al emitir la factura: **al recibir el dinero**.

### 3.4 Cuándo se pierde

| Situación | Efecto |
|---|---|
| Devolución o *chargeback* del pago | Se reversa la comisión de esa factura |
| Cliente en mora > 60 días | Se suspende la comisión hasta que se normalice |
| Cliente cancela | Cesan las comisiones futuras; las causadas se pagan |
| Fraude comprobado | Terminación inmediata y pérdida de las comisiones **no causadas**; se reversan las causadas sobre los referidos obtenidos con la conducta fraudulenta. Las demás causadas se pagan |
| Aliado inactivo > 12 meses sin referidos nuevos | Conserva las comisiones de permanencia de sus clientes activos. **No se le quitan**: sería una traición al trato |

### 3.5 Liquidación y pago

| Elemento | Regla |
|---|---|
| Corte | Último día de cada mes |
| Liquidación disponible en el panel | Día **10** del mes siguiente |
| Pago | Antes del día **20** del mes siguiente |
| Mínimo acumulado para pagar | **$100.000**. Por debajo, se acumula al mes siguiente |
| Soporte | El aliado emite **factura electrónica**; si no está obligado a facturar, se emite **documento soporte en adquisiciones a no obligados a facturar** |
| Retención en la fuente | Se practica la que corresponda por comisiones. **[NE]** Confirma la tarifa vigente con el contador antes de la primera liquidación — ver [`../02-dian-y-facturacion/02-decision-iva-y-regimen.md`](../02-dian-y-facturacion/02-decision-iva-y-regimen.md) §5 |
| IVA | Si el aliado es responsable de IVA, lo liquida sobre su comisión y va en su factura |

### 3.6 Prohibiciones — las que evitan problemas reales

- **Auto-referido.** Referir la empresa propia o una en la que se tenga participación o representación, sin declararlo y obtener aprobación.
- **Publicidad pagada sobre la marca.** Comprar anuncios con el nombre de la marca o variaciones cercanas. Ese tráfico ya era tuyo; pagar comisión por él es pagar dos veces.
- **Suplantación.** Presentarse como empleado, representante o distribuidor autorizado. **El aliado no representa a la sociedad ni puede obligarla.**
- **Promesas propias.** Ofrecer descuentos, plazos, funcionalidades o niveles de servicio no publicados. Lo que el aliado prometa y tú no puedas cumplir, lo pagas tú en churn.
- **Spam.** Correo masivo no solicitado, mensajes automatizados en WhatsApp, publicación en grupos que lo prohíban.
- **Cupones y sitios de descuentos.** No se admite tráfico de sitios de cupones.

---

## 4. Por qué estos porcentajes y no otros

**20% durante 12 meses y 10% después** resuelve tres tensiones a la vez:

1. **Suficiente para que valga la pena.** Un consultor no mueve un dedo por 5%. A 20%, cinco clientes son un ingreso mensual que se nota.
2. **Sostenible con tu margen.** A 73% de margen bruto en año 1, la operación aguanta que el canal sea el **100%** de la adquisición.
3. **La cola de permanencia alinea el churn.** El 10% indefinido convierte al aliado en alguien a quien le importa que su cliente siga usando la plataforma. Si la comisión terminara al mes 12, el aliado se desentiende al mes 11.

**Lo que no hicimos, a propósito:**

| Idea | Por qué no |
|---|---|
| Multinivel (comisión por referir aliados) | Se parece a un esquema piramidal, atrae a la gente equivocada y complica la contabilidad. No |
| Comisión sobre consultoría e implementación | Margen bajo y trabajo tuyo. La comisión sale del software, que es lo que escala |
| Bonos por volumen agresivos | Incentivan vender a quien no encaja. El churn resultante cuesta más que el cliente |
| Exclusividad territorial | Imposible de administrar con dos personas, y bloquea mercado |

---

## 5. Riesgo laboral — la trampa a evitar

Un aliado que trabaja con **horario, con tus herramientas, bajo tus instrucciones y con
exclusividad** puede configurar un **contrato realidad**. La contingencia son prestaciones,
aportes e indemnizaciones **retroactivas hasta por tres años**, más la sanción moratoria del
art. 65 del CST.

**Cómo se evita, y hay que ser disciplinado:**

- **Sin exclusividad.** El aliado puede trabajar con quien quiera, incluidos competidores.
- **Sin horario ni cuotas obligatorias.** Metas de nivel sí; cuotas con consecuencia disciplinaria, no.
- **Sin subordinación.** No se le dan órdenes, se le dan materiales y precios.
- **Sin herramientas de trabajo entregadas** más allá del acceso al panel y al material comercial.
- **Remuneración exclusivamente variable**, causada por resultado.
- **Y el vocabulario importa:** aliado, no "asesor comercial"; comisión, no "salario"; panel, no "puesto de trabajo". Un juez lee los correos.

---

## 6. Metas realistas para los primeros 12 meses

| Trimestre | Aliados activos | Clientes referidos acumulados | MRR de canal (plan Profesional) |
|---|---|---|---|
| T1 (lanzamiento) | 5 | 3 | $1.047.000 |
| T2 | 12 | 12 | $4.188.000 |
| T3 | 20 | 28 | $9.772.000 |
| T4 | 30 | 50 | $17.450.000 |

**Supuesto:** cada aliado activo trae ~1,7 clientes al año, y **solo un tercio de los
aliados inscritos referirá alguna vez** — es el comportamiento normal de un programa de
referidos y no significa que esté roto. El objetivo del reclutamiento es llenar el embudo,
no convertir a todos.

**Regla de foco:** dos aliados que traen ocho clientes cada uno valen más que treinta que
traen cero. Cuando aparezcan los dos primeros que funcionan, **dedícales tiempo
desproporcionado**: material a la medida, acompañamiento en visitas, respuesta inmediata.

---

## 7. Qué necesita el aliado el día uno

- [ ] Panel con su código, su enlace y sus referidos en tiempo real
- [ ] Formulario de registro previo de prospectos por NIT
- [ ] Liquidación visible y descargable
- [ ] Kit comercial: presentación, comparativo, casos de uso → [`04-kit-de-reclutamiento.md`](04-kit-de-reclutamiento.md)
- [ ] Cuenta demo permanente con datos de ejemplo, para mostrar sin pedir permiso
- [ ] Canal directo de contacto contigo (WhatsApp, no formulario)
- [ ] Contrato firmado → [`02-contrato-de-referidos.md`](02-contrato-de-referidos.md)

---

## 8. Modelo secundario — plan Canal (descuento por uso)

Para el consultor que prefiere marca propia y controlar el precio final:

| Elemento | Valor |
|---|---|
| Plan Canal | **$590.000/mes por 10 empresas** ($59.000 por empresa) |
| Frente a precio de lista Esencial | Descuento efectivo del **60%** |
| A quién sirve | Consultor con 10+ clientes que quiere una sola factura y márgenes propios |
| Riesgo que asume el consultor | Paga las 10 licencias tenga o no las 10 empresas |
| Compatibilidad | **Excluyente con la comisión por referido** sobre las mismas empresas. Se elige uno |

Ofrécelo solo cuando el consultor lo pida o cuando ya tenga 8+ empresas referidas: es un
descuento mayor que la comisión y no conviene empujarlo por defecto.
