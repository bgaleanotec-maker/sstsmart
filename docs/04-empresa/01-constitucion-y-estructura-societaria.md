# Constitución y estructura societaria

> Costos verificados a agosto de 2026. UVB (cámaras de comercio) = **$12.110** · SMDLV = **$58.363**.

---

## 1. Por qué S.A.S. y no otra cosa

| Figura | Por qué no |
|---|---|
| **Persona natural** | Responsabilidad ilimitada con todo tu patrimonio; no puedes recibir inversión por acciones; tributas en la cédula general con tarifa marginal hasta **39%**. Inviable para un SaaS |
| **ESAL** | No distribuye excedentes ni tiene accionistas. Incompatible con capital de riesgo. Solo si el proyecto es genuinamente sin ánimo de lucro |
| **S.A.S.** | Responsabilidad limitada al aporte · basta un accionista · objeto indeterminado y duración indefinida · libertad estatutaria para acciones con voto múltiple, preferentes, vesting, drag y tag-along · **es lo que exige cualquier fondo o ángel colombiano** |

---

## 2. Dos sociedades, no una

**Recomendación: SST Smart SAS (software) + Galeano y Asociados (jurídico), separadas.**

### 2.1 Las seis razones

1. **Responsabilidad cruzada.** Un error en un concepto jurídico del bufete no debe poder ejecutarse contra el activo intangible de la SaaS: el código, la marca, los contratos de suscripción. Y al revés.
2. **Régimen tributario.** En el Régimen Simple, los servicios jurídicos caen en el grupo de *"servicios profesionales y de consultoría con predominio del factor intelectual"*: **7,3%–8,3%, con tope de 12.000 UVT**. Las actividades de software pueden caer en grupos con tarifas mucho menores. **Mezclarlas arrastra toda la facturación al grupo más caro y al tope más bajo.**
3. **ICA distinto.** La tarifa de profesiones liberales (306) y la de desarrollo de sistemas (304) no son iguales. Ver [`02-tributario-y-facturacion.md`](02-tributario-y-facturacion.md).
4. **Valoración e inversión.** Ningún inversionista compra participación en una entidad que además presta servicios jurídicos personalísimos: la due diligence se vuelve inmanejable.
5. **Deber de reserva profesional.** Los datos de clientes del bufete están cubiertos por secreto profesional; los de la SaaS, por la Ley 1581. Son regímenes distintos y conviene que vivan en personas jurídicas distintas.
6. **Ejercicio de la abogacía.** El Decreto 196 de 1971 estructura la abogacía como ejercicio de **personas naturales con tarjeta profesional**. Una SAS de software no "ejerce la abogacía"; el bufete sí presta el servicio jurídico.

### 2.2 Lo que cuesta

Segunda sociedad: **~$180.000–$450.000** de constitución + renovación anual + contabilidad separada (**$300.000–$800.000/mes por entidad** en Bogotá — referencia de mercado, no tarifa regulada).

**Es barato frente a lo que evita.**

### 2.3 La estructura

```
   SST Smart SAS                         Galeano y Asociados
   ─────────────                         ───────────────────
   • Dueña del código                    • Concepto jurídico firmado
   • Dueña de la marca                   • Retainer jurídico
   • Contratos de suscripción            • Implementación SG-SST
   • CIIU 6201 principal                 • Diseño PESV
   • Facturación del SaaS                • Defensa administrativa
                    ▲                            ▲
                    └──── contrato de ───────────┘
                       prestación de servicios
                     (curaduría normativa, a
                      precios de mercado)
```

> **Cuidado con la vinculación económica.** Si hay control común, el contrato entre ambas debe estar a precios de mercado y documentado, por las reglas de precios de transferencia y para evitar que la DIAN lo reclasifique. Que lo revise tu contador.

---

## 3. Constituir la S.A.S. — paso a paso

### 3.1 Documento privado, no escritura pública

La Ley 1258 de 2008 permite constituir por **documento privado** inscrito en el registro mercantil. Solo se exige **escritura pública** cuando se aportan bienes inmuebles o bienes cuya transferencia la requiera. Para una SaaS con aportes en dinero, el documento privado basta.

Debe llevar **presunción de autenticidad**: reconocimiento ante notario o firma electrónica en la plataforma de la CCB.

### 3.2 Contenido mínimo (art. 5 Ley 1258/2008)

- Nombre, documento y domicilio de los accionistas
- Razón social + "SAS" o "Sociedad por Acciones Simplificada"
- Domicilio principal y sucursales
- **Término de duración: indefinido** (recomendado)
- **Objeto social: indeterminado** — "cualquier actividad lícita" (recomendado: evita reformar estatutos al pivotar)
- Capital **autorizado, suscrito y pagado**, con plazo de pago no mayor a **2 años**
- Forma de administración, facultades del representante legal, e identificación de administradores

### 3.3 La decisión de capital — no la tomes a la ligera

El capital suscrito es simultáneamente:
- la base del **impuesto de registro (0,7%)**, y
- el punto de partida de tus **activos** para liquidar la matrícula mercantil.

**Suscribe lo que realmente vas a aportar.** Suscribir $100M "porque suena serio" en lugar de $20M cuesta **$1,03 millones extra** el primer día, sin ningún beneficio.

### 3.4 Trámite en la CCB

100% virtual: validación de identidad → formularios RUES y Registro Único Empresarial → firma electrónica de los accionistas → pago por PSE. **La CCB remite la información a la DIAN, que asigna el NIT** (el PreRUT presencial ya no se usa; el flujo está integrado).

---

## 4. Tarifas 2026 de la Cámara de Comercio de Bogotá

### 4.1 Matrícula mercantil

| Rango de activos | Fórmula |
|---|---|
| ≤ $78.715.000 | $24.220 + 8.477 × (Activos / $1.000.000) |
| $78.715.001 – $302.750.000 | $575.225 + 4.238,5 × (Act. − $78.715.000)/1M |
| $302.750.001 – $787.150.000 | $1.359.347,5 + 1.211 × (Act. − $302.750.000)/1M |
| $787.150.001 – $7.871.500.000 | $1.843.747,5 + 544,95 × (Act. − $787.150.000)/1M |

### 4.2 Otros conceptos

| Concepto | Base | Valor |
|---|---|---|
| Formulario RUES | 0,7 UVB | **$8.500** |
| Inscripción de actos y documentos (el doc. de constitución) | 6 UVB | **$72.660** |
| Inscripción de libros | 2 UVB | $24.200 |
| Certificado de existencia y representación legal | 1 UVB | $12.110 |
| Certificado de matrícula mercantil | 0,5 UVB | $6.055 |
| Mutación / cambio de datos | 2 UVB | $24.200 |
| Matrícula de establecimiento de comercio (misma jurisdicción, activos ≤ $78,7M) | — | $48.400 |
| **Impuesto de registro Bogotá — acto con cuantía** | 0,7% del capital suscrito | variable |
| Impuesto de registro — acto sin cuantía | 4 SMDLV | **$233.454** |

> Una SaaS normalmente **no necesita matricular establecimiento de comercio**.

### 4.3 Escenarios completos

| Capital suscrito | Matrícula | Inscripción | RUES | Imp. registro | **Total** |
|---|---|---|---|---|---|
| $5.000.000 | $66.605 | $72.660 | $8.500 | $35.000 | **~$182.800** |
| $20.000.000 | $193.760 | $72.660 | $8.500 | $140.000 | **~$414.900** |
| $50.000.000 | $448.070 | $72.660 | $8.500 | $350.000 | **~$879.200** |
| $100.000.000 | $665.441 | $72.660 | $8.500 | $700.000 | **~$1.446.600** |

---

## 5. Renovación anual

- **Plazo: hasta el 31 de marzo** de cada año.
- Se liquida con la **misma tabla** de la matrícula, sobre los activos totales al 31 de diciembre del año anterior.
- **El impuesto de registro no aplica** a la renovación (está exento).

**Sanción por no renovar:** la SIC puede imponer multas de hasta **17 SMMLV = $29.765.385** (2026). Pero el daño mayor es operativo: aparecer "No renovada" en el RUES **bloquea licitaciones, crédito y onboarding con clientes corporativos**. Un cliente mediano que te pide el certificado de existencia y ve "No renovada" cancela la compra.

---

## 6. Códigos CIIU

| Código | Descripción | Uso |
|---|---|---|
| **6201** | Actividades de desarrollo de sistemas informáticos (planificación, análisis, diseño, programación, pruebas) | **PRINCIPAL** |
| 5820 | Edición de programas de informática | Considerar si el ingreso es puro licenciamiento de producto empaquetado — **el 6201 excluye expresamente la edición comercial de software** |
| 6202 | Consultoría informática y administración de instalaciones | Secundaria (implementación en cliente) |
| 6209 | Otras actividades de TI y servicios informáticos | Secundaria (soporte, mesa de ayuda) |
| **6311** | Procesamiento de datos, alojamiento (hosting) y actividades relacionadas | Secundaria — **relevante si vas a argumentar la exclusión de IVA por cloud computing** |
| 7020 | Consultoría de gestión | Secundaria (consultoría SG-SST no jurídica) |
| 6910 | Actividades jurídicas | **NO ponerlo en la SaaS.** Va en el bufete |

**Beneficio adicional del 6201:** está clasificado en **riesgo ARL clase I** (código 1620101, tarifa mínima 0,522%), lo que abarata la nómina frente a códigos de riesgo mayor.

---

## 7. Errores que cuestan caro

| Error | Consecuencia |
|---|---|
| Objeto social determinado y detallado | Reforma de estatutos (con costo y tiempo) cada vez que pivotas |
| Duración a término fijo | Renovación innecesaria; riesgo de disolución por vencimiento |
| Capital suscrito inflado | Impuesto de registro y matrícula más altos, sin beneficio |
| Incluir CIIU 6910 en la SaaS | Confunde el régimen tributario y la clasificación de riesgo ARL |
| Una sola sociedad para software y jurídico | Todas las razones de §2 |
| No renovar antes del 31 de marzo | Multa de hasta $29,7M y bloqueo comercial |
| No documentar el contrato entre las dos sociedades | Riesgo de reclasificación por la DIAN |

## Fuentes

[CCB — Tarifas de registros públicos](https://www.ccb.org.co/es/tramites-y-consultas/sobre-registros/tarifas) · [CCB — Guía de constitución SAS](https://assets.ctfassets.net/n1ptkpqt763u/2qPY8BkR0Awl2GgbTeQQri/1ed118cb5a6cf3ba9a9f61099d53ac81/GuiaRM_01.pdf) · [Ámbito Jurídico — Tarifas cámaras de comercio 2026 (UVB $12.110)](https://www.ambitojuridico.com/noticias/tributario/mercantil-propiedad-intelectual-y-arbitraje/estas-son-las-tarifas-de-las) · [Tarifa registros públicos 2026 (PDF)](https://ccmmna.org.co/wp-content/uploads/Tarifa-registros-publicos-2026.pdf) · [Ley 1258 de 2008](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=34130) · [Impuesto de registro](https://impuestos-gov.com/departamentales/registro/) · [Renovación 2026 y multa](https://sistepos.com/renovacion-camara-de-comercio-2026-tarifas-plazos-y-la-multa-por-no-pagar-a-tiempo/) · [Bogotá.gov.co — Renovación hasta 31 de marzo](https://bogota.gov.co/mi-ciudad/desarrollo-economico/renovacion-de-matricula-mercantil-en-bogota-hasta-31-de-marzo-de-2026) · [CIIU 6201 y clase de riesgo ARL](https://www.ciiu.co/codigo-ciiu-6201-actividades-de-desarrollo-de-sistemas-informaticos-planificacion-analisis-diseno-programacion-pruebas) · [Decreto 196 de 1971](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=66493)
