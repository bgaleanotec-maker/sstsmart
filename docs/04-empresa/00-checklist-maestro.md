# Checklist maestro — de cero a facturando

**La ruta completa, en orden, con costos verificados a agosto de 2026.**
Valores base: SMMLV $1.750.905 · SMDLV $58.363 · UVT $52.374 · UVB $12.110 (cámaras de comercio).

Marca cada casilla. Los bloques están en orden de dependencia: no saltes.

---

## Bloque 0 · Hoy mismo (costo $0)

- [ ] **Revocar el Personal Access Token de GitHub** expuesto en la URL del remoto → [`../03-arquitectura/02`](../03-arquitectura/02-despliegue-git-render.md) §0
- [ ] Cambiar el remoto a SSH y activar **secret scanning + push protection**
- [ ] **Registrar el software en la DNDA** — es **GRATUITO**, tarda 15 días hábiles, y es lo primero que pide un inversionista → https://www.derechodeautor.gov.co/es/otros/software
- [ ] Reservar el dominio y las cuentas de redes sociales
- [ ] Verificar la disponibilidad de la marca en el buscador de la SIC antes de radicar

---

## Bloque 1 · Constituir la sociedad (semana 1–2)

**Decisión previa, y es estructural: dos sociedades, no una.** SST Smart SAS (software) y Galeano y Asociados (jurídico). Las razones — tributarias, de responsabilidad, de ejercicio profesional y de valoración — están en [`01-constitucion-y-estructura-societaria.md`](01-constitucion-y-estructura-societaria.md).

- [ ] Redactar el documento privado de constitución de la S.A.S. (Ley 1258/2008)
  - Duración **indefinida** · objeto **indeterminado** · capital = lo que realmente vas a aportar
- [ ] Definir CIIU: **principal 6201**; secundarias 6311, 6202, 7020. **No incluir 6910 en la SaaS**
- [ ] Constituir en línea en la Cámara de Comercio de Bogotá (validación de identidad, formularios RUES, firma electrónica, pago por PSE)
- [ ] La CCB remite la información a la DIAN, que asigna el **NIT**

**Costos según el capital suscrito:**

| Capital suscrito | Matrícula | Inscripción del acto | RUES | Imp. registro 0,7% | **Total** |
|---|---|---|---|---|---|
| $5.000.000 | $66.605 | $72.660 | $8.500 | $35.000 | **~$182.800** |
| $20.000.000 | $193.760 | $72.660 | $8.500 | $140.000 | **~$414.900** |
| $50.000.000 | $448.070 | $72.660 | $8.500 | $350.000 | **~$879.200** |
| $100.000.000 | $665.441 | $72.660 | $8.500 | $700.000 | **~$1.446.600** |

> **No suscribas capital "porque suena serio".** El capital suscrito es simultáneamente la base del impuesto de registro (0,7%) y el punto de partida de tus activos para la matrícula. Suscribir $100M en lugar de $20M cuesta **$1,03 millones extra** sin ningún beneficio.

- [ ] Inscripción de libros: $24.200 · Certificado de existencia y representación: $12.110
- [ ] Abrir cuenta bancaria empresarial

---

## Bloque 2 · DIAN y tributario (semana 2–3)

- [ ] Obtener el **RUT** con las responsabilidades: **05** (renta ordinaria), **07** (retefuente), **42** (contabilidad), **52** (facturador electrónico), **48 o 49** (IVA — ver decisión abajo), **59** (autorretenedor, si aplicas art. 114-1)
- [ ] **DECISIÓN CRÍTICA: la posición de IVA, antes de la primera factura.**
  El art. 476 num. 21 del ET excluye de IVA "computación en la nube". La DIAN la interpreta restrictivamente y exige **autodiagnóstico conforme a la guía técnica de MinTIC, firmado por el responsable técnico** (Concepto 1444/2017). Aplica solo al **proveedor de nube**, no a revendedores (Oficio 900930/2022).
  - **Opción A — facturar sin IVA:** monta el autodiagnóstico MinTIC **ese mismo mes**, documenta la arquitectura multi-tenant y la medición de consumo, y **desagrega precios** (la consultoría sí lleva 19% y va en factura separada).
  - **Opción B — facturar con 19%:** más simple y sin contingencia. **Si no vas a montar la documentación, elige esta.** Una glosa por IVA no facturado sobre tres o cuatro años de suscripciones es existencial para una empresa temprana.
- [ ] Inscribirse en el **RIT** de la Secretaría Distrital de Hacienda (el ICA **no** va en el RUT)
- [ ] **Decidir régimen: ordinario vs. Régimen Simple.**
  **Recomendación: ordinario**, si esperas pérdidas fiscales o inversión en I+D en los primeros años — en el RST **no puedes** compensar pérdidas ni aplicar el descuento del art. 256 ET. Plazo de inscripción al RST para 2026: **27 de febrero** (empresas nuevas: al inscribir el RUT)
- [ ] Habilitarse como **facturador electrónico**: portal DIAN → Habilitación → set de pruebas → producción
- [ ] Contratar proveedor tecnológico con **API** (la solución gratuita de la DIAN no tiene API y hace inviable el cobro recurrente). **Alegra Emprendedor: $13.425/mes** anual
- [ ] Contratar contador. Referencia de mercado: **$300.000–$800.000/mes por entidad** (no hay tarifa regulada)

---

## Bloque 3 · Legal del producto (semana 3–5)

- [ ] **Política de Tratamiento de Datos Personales** publicada y accesible
- [ ] **Aviso de privacidad** en el momento de recolección
- [ ] Mecanismo de **autorización previa, expresa e informada**, con prueba conservable
- [ ] **Autorización reforzada para datos sensibles** (salud ocupacional), informando al titular que **no está obligado a otorgarla**
- [ ] Canal y procedimiento de consultas y reclamos (15 días hábiles, prorrogables 8)
- [ ] **Contrato de transmisión de datos (DPA)** dentro de los T&C o como anexo — obligatorio por el art. 25 del Decreto 1377/2013. **Tú eres ENCARGADO; el cliente es RESPONSABLE**
- [ ] Declarar la **transferencia internacional** (Render, EE.UU.) en la política. EE.UU. está en la lista de países con nivel adecuado (Circular 005/2017 SIC) → **no requiere declaración de conformidad ante la SIC**. Verifica la región real: Virginia u Oregon = EE.UU. ✓ · Frankfurt = Alemania ✓ · **Singapur NO está en la lista**
- [ ] **RNBD:** solo obligatorio si tus activos superan **100.000 UVT = $5.237.400.000**. Casi seguro **no aplica** — pero todo lo demás de este bloque sí
- [ ] **Cesión de derechos patrimoniales de autor** con todo desarrollador y contratista, **retroactivamente si es necesario**. Para empleados hay presunción legal; **para contratistas independientes NO la hay**: sin cesión expresa y escrita, tu due diligence de inversión falla
- [ ] Acuerdo de confidencialidad con desarrolladores
- [ ] **Términos y Condiciones / contrato de licencia SaaS** (licencia no exclusiva e intransferible, planes, renovación automática, suspensión por mora, **limitación de responsabilidad al valor pagado en 12 meses**, ley y jurisdicción colombiana)
- [ ] **SLA** conservador — no prometas 99,9% con un solo servicio de Render
- [ ] **Contrato de servicios entre la SaaS y el bufete**, a precios de mercado
- [ ] Cotizar **póliza de responsabilidad civil profesional (E&O)** con corredor. **[NE]** La prima real no está publicada; el rango de $500.000–$2.000.000 que circula es de RC general, no de E&O

**Propiedad industrial:**

| Trámite | Costo 2026 | Tiempo |
|---|---|---|
| Registro de software (DNDA) | **GRATUITO** | 15 días hábiles |
| Marca, 1.ª clase en línea (SIC) | **$1.347.500** | 4–8 meses sin oposición |
| Cada clase adicional | ~$674.000 | — |
| **Clases 9 + 42 (software + SaaS)** | **~$2.021.500** | — |
| + Clase 45 (servicios jurídicos, si la marca cubre el bufete) | ~$2.695.500 total | — |

*La SIC otorga descuentos para MiPymes — confírmalo al radicar. **[NE]** No pude verificar el porcentaje exacto para 2026.*

---

## Bloque 4 · Infraestructura y despliegue (semana 4–6)

Detalle completo en [`../03-arquitectura/02-despliegue-git-render.md`](../03-arquitectura/02-despliegue-git-render.md).

- [ ] Workspace de Render en plan **Pro (USD 25/mes)** — sin él no hay autoscaling ni preview environments
- [ ] Crear servicios con **`region: virginia`**. **Es irreversible**: no se puede cambiar la región de un servicio
- [ ] `render.yaml` con web + worker + cron + Postgres 16 + Key Value
- [ ] **Dos `DATABASE_URL`**: `app_owner` para migraciones, `app_user` (sin `BYPASSRLS`) para la app
- [ ] Activar **PgBouncer** (integrado, sin costo)
- [ ] Secretos con `sync: false` — nunca en el repo
- [ ] Dominio wildcard `*.sstsmart.co` con TLS automático. Quitar registros `AAAA`; en Cloudflare, **desactivar el proxy en el dominio raíz**
- [ ] Bucket de **Cloudflare R2** con prefijo por tenant
- [ ] CI en GitHub Actions con `autoDeployTrigger: checksPass`
- [ ] Cron semanal de `pg_dump` cifrado hacia R2 (**rol `app_backup` con `BYPASSRLS`**, o exportarás tablas vacías)
- [ ] Sentry + UptimeRobot + PostHog (todos en plan gratuito)
- [ ] Solicitar el **DPA de Render** vía "Request Documents" y guardarlo — te lo van a pedir en due diligence

---

## Bloque 5 · Cobro (semana 5–7)

Detalle en [`04-pagos-y-cobranza-recurrente.md`](04-pagos-y-cobranza-recurrente.md).

- [ ] Abrir cuenta en **Wompi** (2,65% + $700 + IVA — la mejor tarifa del mercado; PSE, Nequi y débito de cuentas Bancolombia)
- [ ] Orquestador de suscripciones: **Treli** (integra nativamente con Alegra) o lógica propia
- [ ] Flujo: pago exitoso → webhook → backend → API de facturación → emisión y validación DIAN → envío con CUFE
- [ ] **Nunca emitas la factura antes de confirmar el pago** — genera IVA e ingreso devengado que tendrás que anular con nota crédito
- [ ] Lógica de *dunning*: reintentos escalonados + recordatorio por email y WhatsApp
- [ ] **Entiende la limitación:** PSE **no permite débito recurrente automático** (exige que el cliente autorice cada transacción en el portal de su banco). Para B2B pyme el modelo realista es **híbrido**: primer pago por PSE, renovaciones por factura electrónica con link de pago y recordatorios

---

## Bloque 6 · Comercial (semana 6–8)

- [ ] **Página de precios pública** — solo 5 de ~25 competidores publican precio. Es un diferenciador sin costo de desarrollo
- [ ] Prueba de 14 días **sin tarjeta**
- [ ] Checkout de autoservicio
- [ ] Trust Center público
- [ ] Diagnóstico gratuito de obligatoriedad PESV (lead magnet)
- [ ] Contenido para la ventana **mayo–julio** (autoevaluación en SGRL) y la de **enero** (reporte PESV)
- [ ] Primeros 3 clientes piloto con descuento de fundador a cambio de testimonio

---

## Presupuesto de arranque

| Concepto | Costo |
|---|---|
| Constitución SST Smart SAS (capital $20M) | $414.900 |
| Constitución de la segunda sociedad | ~$200.000 |
| Libros y certificados | $36.310 |
| Registro de software (DNDA) | **$0** |
| Marca, clases 9 y 42 | $2.021.500 |
| Infraestructura, 3 meses (MVP) | ~$186.000 |
| Facturación electrónica, 3 meses | ~$40.275 |
| Contador, 3 meses (2 entidades) | ~$3.900.000 |
| Cotización de póliza E&O | por cotizar |
| **Total estimado de arranque** | **~$6.800.000** |

**Costo fijo mensual desde el mes 4:** contador ~$1.300.000 · infraestructura ~$558.000 · facturación $13.425 · herramientas ~$350.000 = **~$2.220.000/mes** antes de nómina.

---

## Las seis acciones de mayor impacto

Si solo haces seis cosas de todo este documento:

1. **Revocar el token de GitHub.** Hoy. Es lo único que no admite espera.
2. **Decidir la posición de IVA antes de la primera factura** — y si eliges la exclusión, montar el autodiagnóstico MinTIC ese mismo mes.
3. **Firmar cesiones de derechos patrimoniales** con todo desarrollador y contratista que haya tocado el código, retroactivamente.
4. **Registrar el software en la DNDA.** Es gratuito. No hay excusa.
5. **Incorporar el contrato de transmisión de datos** en los T&C antes del primer cliente que cargue exámenes médicos.
6. **Separar la SaaS del bufete** en dos personas jurídicas, con contrato de servicios entre ellas a precios de mercado.
