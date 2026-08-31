# De cero a factura electrónica válida

**Ruta austera para un fundador único.** Cinco fases, ~3 semanas de calendario,
~12 horas de trabajo real, **menos de $1.000.000 COP** de desembolso.

Todo el trámite es en línea. No hay que ir a ninguna ventanilla ni a notaría.

---

## §0 · Por qué esta ruta es distinta a la de `docs/04-empresa/`

El dossier de negocio recomendaba **dos sociedades** (una de software, una jurídica) y
un arranque de ~$6,8 millones. Esa recomendación sigue siendo correcta **para cuando
haya ingresos**. Hoy no la puedes ejecutar, y ejecutarla mal es peor que aplazarla.

| Decisión del dossier | Qué hacemos ahora | Por qué | Cuándo revisarla |
|---|---|---|---|
| Dos sociedades | **Una sola S.A.S.** de software y plataforma | La segunda sociedad cuesta constitución + renovación + contabilidad separada todos los meses, sin ingresos que la sostengan | Cuando el retainer jurídico facture > $3M/mes de forma sostenida |
| Servicios jurídicos dentro del grupo | **Fuera de la S.A.S.** — los prestas como persona natural con tu tarjeta profesional, y facturas aparte | El Decreto 196/1971 estructura la abogacía como ejercicio de persona natural; meter CIIU 6910 en la SaaS enreda el régimen tributario y la clase de riesgo ARL sin darte nada a cambio | Al crear la segunda sociedad |
| Registro de marca en clases 9 y 42 (~$2M) | **Aplazado.** Solo DNDA (gratis) + dominio | $2M es dos tercios del presupuesto total y la marca no protege nada si no hay producto en el mercado | Cuando haya 10 clientes pagos o alguien intente copiarte el nombre |
| Contador desde el mes 1 ($300k–800k/mes) | **Contador por trámite**, mensualizado cuando empiece a haber movimiento | Una S.A.S. sin operación no genera trabajo contable mensual real. Sí necesitas contador público para firmar estados financieros y para la primera declaración | En el primer mes con más de 5 facturas emitidas |
| Capital suscrito $20M | **$5.000.000** | El capital suscrito es la base del impuesto de registro (0,7%) y del cálculo de la matrícula. Suscribir $20M en vez de $5M cuesta **$232.155 más** el primer día, sin ningún beneficio | En una ronda o al pedir crédito |
| Plan Render Pro (USD 25/mes) | **Plan gratuito / Starter** hasta el primer cliente pago | El autoscaling y los preview environments son irrelevantes con cero tráfico | Con el primer cliente en producción |

**Lo que NO se recorta, pase lo que pase:** el registro DNDA (es gratis), la política de
tratamiento de datos (es obligatoria y su ausencia es sancionable por la SIC), la
autorización reforzada para datos de salud ocupacional, y la habilitación como facturador
electrónico antes de cobrarle a alguien.

---

## §1 · Mapa de las cinco fases

```
FASE 0        FASE 1              FASE 2            FASE 3              FASE 4
Decidir  →    Constituir     →    DIAN         →    Facturar      →    Vender
día 0         días 1–5            días 5–10         días 10–18         semana 4+

nombre        documento           RUT + NIT         habilitación       T&C publicados
capital       privado             responsab.        set de pruebas     pasarela de pago
objeto        firma electr.       firma DIAN        1.ª factura        afiliados
CIIU          pago PSE            RIT Bogotá        validada           lanzamiento
IVA           matrícula           cuenta banco
$0            ~$183.000           $0                ~$0–$40.000        variable
```

---

## FASE 0 · Decisiones (día 0 — 2 horas, $0)

Ninguna de estas se puede cambiar después sin pagar. Resuélvelas antes de abrir el
formulario de la Cámara de Comercio.

### 0.1 Nombre — `[DECIDIR]`

Trabajo detallado en [`01-constitucion/00-decision-nombre-y-objeto.md`](01-constitucion/00-decision-nombre-y-objeto.md).
Resumen del método:

1. Elige 3 candidatos de la shortlist.
2. Verifica **homonimia** en el RUES: https://www.rues.org.co → "Consultar nombre". Si el nombre exacto ya está matriculado en cualquier cámara del país, la CCB rechaza la solicitud.
3. Verifica que el **dominio `.co` esté libre** (https://www.dominio.co o cualquier registrador).
4. Verifica en el buscador de la SIC (https://sipi.sic.gov.co) que no haya una marca idéntica registrada en clases 9, 35, 42 o 45. **Aunque aplacemos el registro, no queremos construir sobre un nombre que otro ya tiene.**
5. Reserva de inmediato: dominio + usuario de LinkedIn + página de Facebook + canal de YouTube. Toma 30 minutos y evita perder el nombre.

### 0.2 Capital — **suscribe $5.000.000**

| Concepto | Valor |
|---|---|
| Capital autorizado | $50.000.000 (no cuesta nada tenerlo alto; es solo el techo estatutario) |
| **Capital suscrito** | **$5.000.000** ← esta es la cifra que cuesta |
| Capital pagado | $5.000.000 al momento de la constitución, o parcial con plazo máximo de 2 años |

El capital suscrito es simultáneamente base del impuesto de registro (0,7%) y punto de
partida de los activos para liquidar la matrícula mercantil. Deja el autorizado alto y el
suscrito en lo que realmente vas a aportar.

### 0.3 Objeto social — **indeterminado**

Literal recomendado: *"La sociedad podrá realizar cualquier actividad lícita, comercial o
civil, en Colombia o en el exterior."* (art. 5 num. 5 Ley 1258/2008).

Un objeto detallado obliga a reformar estatutos —con costo y tiempo— cada vez que pivotas.
Con una plataforma que va a tocar SG-SST, SAGRILAFT, PESV y servicios legales, vas a pivotar.

### 0.4 CIIU

| Código | Actividad | Rol |
|---|---|---|
| **6201** | Desarrollo de sistemas informáticos | **PRINCIPAL** — además es riesgo ARL clase I (0,522%), el más barato |
| 6311 | Procesamiento de datos y hosting | Secundaria — necesaria si algún día argumentas la exclusión de IVA por computación en la nube |
| 6202 | Consultoría informática | Secundaria |
| 7020 | Consultoría de gestión | Secundaria — cubre la consultoría SG-SST y SAGRILAFT no jurídica |
| ~~6910~~ | ~~Actividades jurídicas~~ | **NO incluir.** Va en tu ejercicio como persona natural |

### 0.5 Duración — **indefinida**

### 0.6 Administración — representante legal único, con suplente

Nómbrate representante legal principal. Designa un **suplente** aunque sea un familiar de
confianza: si te enfermas o viajas, sin suplente la sociedad queda paralizada y sacar un
certificado nuevo cuesta tiempo.

### 0.7 Domicilio — Bogotá D.C.

La dirección puede ser tu residencia. No necesitas matricular establecimiento de comercio:
una plataforma SaaS no lo requiere.

---

## FASE 1 · Constituir la S.A.S. (días 1–5 — 3 horas, ~$183.000)

Guía pantalla por pantalla en [`01-constitucion/03-tramite-ccb-en-linea.md`](01-constitucion/03-tramite-ccb-en-linea.md).

1. **Redacta el documento privado** a partir de [`01-constitucion/01-documento-privado-constitucion.md`](01-constitucion/01-documento-privado-constitucion.md). Reemplaza todos los `[LLENAR]`.
2. Entra a **https://www.ccb.org.co** → Trámites virtuales → Crear empresa. Necesitas cuenta registrada.
3. Validación de identidad (biometría contra la Registraduría).
4. Diligencia el **formulario RUES** y el **Registro Único Empresarial**.
5. Adjunta el documento privado y **fírmalo electrónicamente** en la plataforma. La firma electrónica de la CCB le da presunción de autenticidad — **no necesitas notaría**.
6. Diligencia el **PreRUT** dentro del mismo flujo (la CCB lo transmite a la DIAN).
7. Paga por PSE.

**Costo con capital suscrito de $5.000.000:**

| Concepto | Valor |
|---|---|
| Matrícula mercantil | $66.605 |
| Inscripción del documento de constitución (6 UVB) | $72.660 |
| Formulario RUES (0,7 UVB) | $8.500 |
| Impuesto de registro Bogotá (0,7% del capital suscrito) | $35.000 |
| **Subtotal constitución** | **~$182.765** |
| Inscripción del libro de accionistas (2 UVB) | $24.220 |
| Certificado de existencia y representación legal (1 UVB) | $12.110 |
| **Total Fase 1** | **~$219.095** |

**Salida esperada (2 a 5 días hábiles):** matrícula mercantil activa, **NIT asignado por
la DIAN**, y certificado de existencia y representación legal descargable.

> **Si la CCB devuelve la solicitud**, casi siempre es por una de tres cosas: homonimia del
> nombre, un `[LLENAR]` que quedó sin reemplazar en el documento, o la dirección de
> notificación mal formateada. Corriges y reenvías sin costo adicional.

---

## FASE 2 · DIAN y municipio (días 5–10 — 3 horas, $0)

Detalle en [`02-dian-y-facturacion/01-rut-y-responsabilidades.md`](02-dian-y-facturacion/01-rut-y-responsabilidades.md).

### 2.1 Formalizar el RUT

La CCB ya transmitió los datos y la DIAN asignó el NIT, pero el RUT queda con
responsabilidades incompletas. Debes entrar a formalizarlo.

1. https://muisca.dian.gov.co → **Habilitar cuenta** (como representante legal de la persona jurídica).
2. Solicita el **Instrumento de Firma Electrónica (IFE)** — es **gratuito** y se genera en línea.
3. Actualiza el RUT con las responsabilidades:

| Código | Responsabilidad | ¿Va? |
|---|---|---|
| **05** | Renta, régimen ordinario | Sí |
| **07** | Retención en la fuente | Sí |
| **42** | Obligado a llevar contabilidad | Sí |
| **52** | Facturador electrónico | Sí |
| **48 / 49** | Responsable / No responsable de IVA | **Ver §2.3** |
| 19 | Productor de servicios exentos | Solo si vas a exportar el SaaS |

### 2.2 RIT Bogotá — no se olvida

El ICA **no** se inscribe en el RUT. Se hace en el **Registro de Información Tributaria**
de la Secretaría Distrital de Hacienda: https://www.haciendabogota.gov.co → Oficina Virtual.
Es gratuito y toma 20 minutos. Actividad 6201 → agrupación 304 → **9,66 por mil**
(confírmala en el RIT al inscribirte; la tabla de terceros no es fuente oficial **[NE]**).

### 2.3 Decisión de IVA — `[DECIDIR]` antes de la primera factura

Análisis completo en [`02-dian-y-facturacion/02-decision-iva-y-regimen.md`](02-dian-y-facturacion/02-decision-iva-y-regimen.md).

**Recomendación para este arranque: inscríbete como responsable de IVA (código 48) y
factura con 19%.**

La exclusión del art. 476 num. 21 del ET para computación en la nube existe, pero la DIAN
la interpreta restrictivamente y exige un autodiagnóstico conforme a la guía técnica de
MinTIC firmado por el responsable técnico (Concepto 1444/2017). Montar y mantener esa
documentación es trabajo real que hoy no tienes tiempo de hacer. Y como tus clientes son
empresas responsables de IVA, **el 19% es descontable para ellos**: no te encarece la venta.

Una glosa por IVA no facturado sobre tres años de suscripciones es existencial para una
empresa de una persona. La exclusión te ayuda en flujo de caja, no en precio. Puedes
migrar a la exclusión más adelante, cuando la documentación exista.

### 2.4 Régimen: **ordinario**, no Simple

En el Régimen Simple no puedes compensar pérdidas fiscales ni aplicar el descuento del
art. 256 ET por I+D. Una plataforma en año 1–2 casi siempre tiene pérdidas, y tú vas a
invertir en desarrollo. Además, la calificación del desarrollo de software como "servicio
técnico" (1,6–4,5%) frente a "consultoría con predominio intelectual" (7,3–8,3%, con tope
de 12.000 UVT) **no es evidente y la DIAN ha sido inconsistente**. No apuestes la
tributación de la empresa a esa clasificación.

### 2.5 Cuenta bancaria

Documentos que piden todos los bancos: certificado de existencia y representación legal
(menos de 30 días), RUT actualizado, cédula del representante legal y, en algunos casos,
declaración de origen de fondos. **[NE]** Las tarifas de manejo de cuentas jurídicas
cambian por banco y por campaña; compara al menos tres antes de abrir. Pregunta
específicamente por **cuota de manejo, costo de transferencias ACH y si exigen saldo mínimo**.

---

## FASE 3 · Facturación electrónica (días 10–18 — 4 horas, $0–$40.000)

Guía completa en [`02-dian-y-facturacion/03-habilitacion-facturador-electronico.md`](02-dian-y-facturacion/03-habilitacion-facturador-electronico.md).

Marco vigente: **Resolución 000165 de 2023** (anexo técnico v1.9), consolidada por la
**Resolución 000227 del 23 de septiembre de 2025**.

1. Portal DIAN → **Sistema de Facturación Electrónica** → Habilitación.
2. Registra el software: propio, gratuito de la DIAN, o de un proveedor tecnológico.
3. **Set de pruebas**: la DIAN te exige emitir un lote de documentos de prueba (facturas y notas) que deben validarse sin rechazo.
4. Habilitación en **producción**. Solicita el rango de numeración.
5. Emite una factura real de $1.000 a tu propio NIT para confirmar que el CUFE se genera y el correo llega.

**Qué proveedor usar con presupuesto cero** — comparativa en
[`02-dian-y-facturacion/04-proveedores-comparativa.md`](02-dian-y-facturacion/04-proveedores-comparativa.md).

| Opción | Costo | API | Cuándo usarla |
|---|---|---|---|
| **Solución gratuita DIAN** | $0 | **No** | Fase 0 de ventas: primeros 1–5 clientes facturados a mano. Perfectamente legal |
| **Factus** | Por paquetes de documentos; sandbox gratuito ilimitado. **[NE]** precio no publicado, se cotiza por WhatsApp | Sí | Cuando quieras automatizar y el volumen sea bajo |
| **Alegra Emprendedor** | $13.425/mes en plan anual (~$161.100/año) | Sí | Cuando ya haya cobro recurrente y quieras contabilidad integrada |

> **Empieza con la solución gratuita de la DIAN.** Es válida y suficiente para los primeros
> clientes. Automatizar la facturación antes de tener a quién facturarle es la forma más
> común de gastar los primeros $200.000 en nada.
>
> **Verifica una cosa antes de contar con ella para todo:** que emita **documento soporte en
> adquisiciones a no obligados a facturar**. Lo vas a necesitar para pagar la primera
> comisión a un aliado que no facture, y sin ese documento el gasto no es deducible. **[NE]**

**Cuidado con una regla que circula mal.** Se oye mucho "no factures hasta que te paguen".
**Como regla general es falsa y peligrosa:** la obligación de facturar nace con la venta o la
prestación del servicio (arts. 615 y 616-1 ET), y el IVA en servicios se causa en la fecha
**más temprana** entre la emisión de la factura, la terminación del servicio y el pago (art.
429 lit. c ET). Diferir la factura no evita la causación: produce **omisión de facturación**,
que es sancionable, y deja al cliente sin soporte de su IVA descontable.

Lo que sí es cierto, y es lo que hay que hacer bien:

1. **Factura conforme a la causación legal**, no conforme a la caja. Consúltalo con tu contador para el modelo de suscripción concreto.
2. **Cobra por anticipado.** Es la solución real al problema de caja en un SaaS: el cliente paga y en ese mismo acto se factura el periodo.
3. **No causes la comisión del aliado hasta confirmar el pago.** Ahí sí la regla aplica sin matices → [`04-programa-afiliados/01-diseno-del-programa.md`](04-programa-afiliados/01-diseno-del-programa.md) §3.3.
4. **Usa notas crédito** para anulaciones y devoluciones, no para tapar una factura que no debió emitirse.

---

## FASE 4 · Legal del producto y cobro (días 15–25 — 5 horas, ~$60.000)

Todos los textos están redactados en [`03-legal-producto/`](03-legal-producto/). Solo hay que
llenar los `[LLENAR]` y publicarlos.

- [ ] **Registrar el software en la DNDA** — https://www.derechodeautor.gov.co/es/otros/software · **gratuito**, 15 días hábiles. Hazlo el mismo día que tengas el NIT. → [`03-legal-producto/05-registro-software-dnda.md`](03-legal-producto/05-registro-software-dnda.md)
- [ ] Publicar **Términos y Condiciones** en `/terminos` → [`03-legal-producto/01-terminos-y-condiciones.md`](03-legal-producto/01-terminos-y-condiciones.md)
- [ ] Publicar **Política de Tratamiento de Datos Personales** en `/privacidad`, con el **anexo de encargo (DPA)** incluido. Obligatorio por el art. 25 del Decreto 1377/2013. **Tú eres ENCARGADO; el cliente es RESPONSABLE.**
- [ ] Implementar el **aviso de privacidad** y la casilla de **autorización previa, expresa e informada**, con registro conservable (fecha, hora, IP, versión del texto aceptada)
- [ ] **Autorización reforzada para datos sensibles** (exámenes médicos ocupacionales), informando al titular que **no está obligado a otorgarla**
- [ ] Canal de consultas y reclamos publicado — **consultas: 10 días hábiles, prorrogables 5 · reclamos: 15 días hábiles, prorrogables 8** (arts. 14 y 15 de la Ley 1581 de 2012)
- [ ] Declarar la **transferencia internacional** a Estados Unidos (Render, región Virginia). EE.UU. está en la lista de países con nivel adecuado de protección (Circular 005/2017 SIC) → **no requiere declaración de conformidad ante la SIC**
- [ ] **RNBD**: solo obligatorio si los activos superan 100.000 UVT = $5.237.400.000. **No te aplica.** Todo lo demás de esta fase sí
- [ ] Registrar dominio `.co` (~$40.000–$60.000/año **[NE]**, varía por registrador y por promoción)
- [ ] Cuenta en **Wompi** para recaudo (2,65% + $700 + IVA por transacción; sin costo de apertura ni mensualidad)

> **Ojo con PSE:** no permite débito recurrente automático. Para B2B pyme el modelo
> realista es híbrido — primer pago por PSE o tarjeta, renovaciones por factura electrónica
> con link de pago y recordatorios por correo y WhatsApp.

---

## FASE 5 · Vender (semana 4 en adelante)

- [ ] Página de precios **pública** — según el análisis competitivo del dossier, solo 5 de ~25 competidores publican precio **[NE]**. Es un diferenciador que no cuesta desarrollo; **antes de usarlo como afirmación pública, vuelve a contarlo tú mismo y anota la fecha del conteo**
- [ ] Prueba de 14 días **sin tarjeta**
- [ ] Lanzar el **programa de afiliados SST** → [`04-programa-afiliados/`](04-programa-afiliados/)
- [ ] Ejecutar el **plan de 8 semanas** en LinkedIn, Facebook y YouTube → [`05-marketing/03-plan-de-lanzamiento-8-semanas.md`](05-marketing/03-plan-de-lanzamiento-8-semanas.md)
- [ ] Primeros 3 clientes piloto con descuento de fundador a cambio de testimonio grabado

**Las dos ventanas comerciales del año, con fecha fija:**

| Ventana | Fechas | Qué se vence |
|---|---|---|
| **PESV** | 6 al 31 de **enero** | Reporte del Plan Estratégico de Seguridad Vial (Circular 0034/2026) **[NE]** |
| **Autoevaluación SG-SST** | mayo a julio, plazo **31 de julio** | Autoevaluación de estándares mínimos en la plataforma SGRL (Circular 027/2026) **[NE]** |

> **[NE] Estas dos fechas sostienen todo el calendario comercial y todo el plan de contenido.**
> Provienen del dossier del repositorio, no de fuente primaria. **Consigue el número y la
> fecha de la circular en la fuente oficial antes de publicar cualquier pieza que las cite** —
> la propia regla de esta carpeta dice que un `[NE]` no va en material comercial.

Toda la campaña orbita alrededor de esas dos fechas. Hoy es **30 de agosto de 2026**: la
próxima ventana grande es enero. Tienes cuatro meses para llegar a ella con producto,
contenido acumulado y una red de afiliados armada. Ese es el objetivo real del trimestre.

---

## §6 · Presupuesto total de esta ruta

| Concepto | Costo |
|---|---|
| Constitución en CCB (capital suscrito $5M) | $182.765 |
| Inscripción de libro de accionistas | $24.220 |
| Certificado de existencia y representación | $12.110 |
| RUT, NIT, firma electrónica DIAN, RIT | **$0** |
| Registro del software en la DNDA | **$0** |
| Habilitación como facturador electrónico | **$0** |
| Dominio `.co`, 1 año | ~$60.000 **[NE]** |
| Facturación electrónica, 3 meses (solución DIAN) | **$0** |
| Contador público — armado inicial y firma **[NE]** | ~$400.000 |
| Infraestructura, 3 meses (planes gratuitos; margen para pasar a Starter) | ~$0–$100.000 |
| **Total de arranque** | **~$679.000 – $779.000** |

Queda margen dentro del millón. **No lo gastes en registro de marca todavía**; guárdalo
para los primeros meses de contador cuando empiece el movimiento.

**Costo fijo mensual mientras no haya clientes:** prácticamente **$0**. Ese es el punto
de toda esta ruta: que la empresa pueda existir sin quemarte el salario mientras el
producto y el canal se construyen.

---

## §7 · Las seis cosas que importan más que las otras

1. **Verifica la homonimia del nombre antes de cualquier otra cosa.** Todo lo demás cuelga de ahí — dominio, redes, logo, dirección de correo.
2. **Registra el software en la DNDA el día que tengas el NIT.** Es gratis, tarda 15 días, y es lo primero que pregunta cualquiera que quiera invertir o comprar.
3. **Decide la posición de IVA antes de emitir la primera factura**, no después. Cambiar de posición retroactivamente es una nota crédito por cada factura y una conversación incómoda con cada cliente.
4. **Firma la cesión de derechos patrimoniales** con cualquier persona que toque el código — empezando por ti mismo, e incluida la socia SST si aporta contenido, plantillas o matrices. Desde la Ley 1915 de 2018 hay presunción de transferencia también para contratistas, pero **acotada a las actividades habituales del encargante en la época de creación** y **no oponible a terceros sin inscripción en la DNDA**. El documento escrito es lo que se revisa en una due diligence.
5. **Incorpora el contrato de encargo (DPA)** en los T&C antes del primer cliente que suba un examen médico ocupacional. Son datos sensibles de salud.
6. **Renueva la matrícula mercantil antes del 31 de marzo** de cada año. La multa llega a 17 SMMLV ($29.765.385), pero el daño real es aparecer "No renovada" en el RUES: un cliente mediano que pide el certificado y ve eso, cancela la compra.

---

## Fuentes

[Ley 1258 de 2008](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=34130) ·
[CCB — Tarifas de registros públicos](https://www.ccb.org.co/es/tramites-y-consultas/sobre-registros/tarifas) ·
[RUES — consulta de nombre](https://www.rues.org.co) ·
[DIAN — MUISCA](https://muisca.dian.gov.co) ·
[DNDA — registro de software](https://www.derechodeautor.gov.co/es/otros/software) ·
[SIC — SIPI, consulta de marcas](https://sipi.sic.gov.co) ·
[Secretaría Distrital de Hacienda — ICA y RIT](https://www.haciendabogota.gov.co/es/impuestos/impuesto-de-industria-y-comercio-ica) ·
[DIAN Oficio 900930 de 2022 — IVA cloud computing](https://normograma.dian.gov.co/dian/compilacion/docs/oficio_dian_900930_2022.htm) ·
[Factus — proveedor tecnológico con API](https://www.factus.com.co/) ·
[Alegra — precios](https://www.alegra.com/colombia/precios/) ·
[Régimen Simple 2026](https://siemprealdia.co/colombia/impuestos/regimen-simple-de-tributacion/) ·
[Renovación de matrícula hasta el 31 de marzo](https://bogota.gov.co/mi-ciudad/desarrollo-economico/renovacion-de-matricula-mercantil-en-bogota-hasta-31-de-marzo-de-2026)
