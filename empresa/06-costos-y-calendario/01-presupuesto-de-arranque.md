# Presupuesto de arranque — la ruta bajo $1.000.000

**Valores base (agosto 2026):** SMMLV $1.750.905 · UVT $52.374 · UVB (cámaras de comercio)
$12.110 · SMDLV $58.363.

---

## 1. Desembolso para existir y poder facturar

| # | Concepto | Costo | ¿Obligatorio? | Cuándo |
|---|---|---|---|---|
| 1 | Matrícula mercantil CCB (activos $5.000.000) | $66.605 | Sí | Semana 1 |
| 2 | Inscripción del documento de constitución (6 UVB) | $72.660 | Sí | Semana 1 |
| 3 | Formulario RUES (0,7 UVB) | $8.500 | Sí | Semana 1 |
| 4 | Impuesto de registro Bogotá (0,7% de $5.000.000) | $35.000 | Sí | Semana 1 |
| 5 | Inscripción del libro de accionistas (2 UVB) | $24.220 | Sí | Semana 1 |
| 6 | Certificado de existencia y representación (1 UVB) | $12.110 | Sí | Semana 2 |
| 7 | RUT, NIT, firma electrónica DIAN, RIT Bogotá | **$0** | Sí | Semana 2 |
| 8 | Registro del software en la DNDA | **$0** | Sí | Semana 2 |
| 9 | Habilitación como facturador electrónico | **$0** | Sí | Semana 3 |
| 10 | Facturación electrónica, 3 meses (solución gratuita DIAN) | **$0** | Sí | Semana 3 |
| 11 | Dominio `.co`, 1 año **[NE]** | ~$60.000 | Sí | Semana 1 |
| 12 | Contador público — armado inicial y firma **[NE]** | ~$400.000 | Sí | Mes 1–3 |
| 13 | Infraestructura 3 meses (planes gratuitos + margen) | $0–$100.000 | Sí | Mes 1 |
| | **TOTAL** | **$679.095 – $779.095** | | |

**Margen dentro del millón: entre $220.000 y $320.000.** No lo gastes todavía.

> **Nota de cifras.** La inscripción de libros se liquida a 2 UVB = **$24.220** ($12.110 × 2). El dossier de `docs/04-empresa/` la trae como $24.200; es un redondeo, no una tarifa distinta. Toda esta carpeta usa el valor calculado.

---

## 2. Lo que se aplaza a propósito

Ninguna de estas es un descuido. Cada una tiene un disparador escrito.

| Concepto | Costo | Por qué se aplaza | **Cuándo dejar de aplazarlo** |
|---|---|---|---|
| **Registro de marca, clases 9 y 42 (SIC)** | ~$2.021.500 | Dos tercios del presupuesto total. La marca no protege un producto que todavía no está en el mercado | **10 clientes pagos**, o el día que alguien use un nombre parecido |
| Contador mensual | $300.000–$800.000/mes **[NE]** | Una sociedad sin operación no genera trabajo contable mensual real | **Primer mes con más de 5 facturas emitidas** |
| Segunda sociedad (jurídica) | ~$200.000 + contabilidad separada | El componente jurídico lo prestas hoy como persona natural | **Retainer jurídico > $3M/mes sostenido** |
| Plan Render Pro (USD 25/mes ≈ **$110.000/mes** a TRM 4.400 **[NE]**) | ~$110.000/mes | Autoscaling y preview environments no sirven con cero tráfico | **Cuando el tráfico o el número de tenants lo exija**, no con el primer cliente |
| Proveedor de facturación con API | $13.425/mes en adelante | La solución gratuita de la DIAN basta para los primeros clientes | **Más de 20 facturas al mes**, o renovaciones en fechas dispersas |
| Póliza de responsabilidad civil profesional (E&O) | **[NE]** — no cotizada | Sin clientes no hay exposición | **Primer cliente corporativo que la exija** |
| Publicidad pagada | — | El contenido orgánico todavía no dice qué mensaje funciona | **Cuando una publicación orgánica genere demos de forma repetible** |

**[NE]** El rango de $500.000–$2.000.000 que circula para pólizas E&O corresponde a
responsabilidad civil general, no a errores y omisiones. Cotiza con corredor cuando llegue el
momento; no presupuestes con ese número.

---

## 3. Costo fijo mensual, por etapa

### Etapa 0 — sociedad constituida, sin clientes

| Concepto | Mensual |
|---|---|
| Infraestructura (planes gratuitos) | $0 |
| Facturación electrónica (solución DIAN) | $0 |
| Contador | $0 (por trámite) |
| Dominio | ~$5.000 (prorrateado) |
| **Total** | **~$5.000/mes** |

**Ese es el punto de toda esta ruta:** la empresa puede existir, estar al día y poder
facturar **sin quemar tu salario** mientras el producto y el canal se construyen.

### Etapa 1 — primeros clientes (1 a 10)

| Concepto | Mensual |
|---|---|
| Infraestructura — Render Starter (USD 7/mes ≈ **$31.000**) + Cloudflare R2 (free tier) **[NE]** | ~$31.000 |
| Facturación electrónica (Alegra Emprendedor) | $13.425 |
| Contador mensual | ~$400.000 **[NE]** |
| Dominio y correo | ~$25.000 |
| **Total** | **~$470.000/mes** |

> **[NE] Sobre las cifras de infraestructura.** USD 7 y USD 25 son los precios de lista de
> Render; la conversión usa **TRM 4.400**, que hay que actualizar. No confundas Starter (USD 7)
> con Pro (USD 25): son cifras muy distintas y verlas iguales en un presupuesto es señal de
> que alguien copió una fila.

**Punto de equilibrio.** Dos clientes en plan Profesional facturan $698.000/mes. Si llegaron
por venta directa, cubren el costo fijo de ~$470.000 con holgura. **Si llegaron por canal**,
hay que descontar la comisión del 20% ($139.600) y el costo de infraestructura por tenant
($25.000 × 2 = $50.000 **[NE]**): quedan $508.400, que todavía alcanzan, pero sin holgura.
**Con tres clientes el equilibrio es cómodo en cualquiera de los dos escenarios.**

### Etapa 2 — canal activo (10 a 30 clientes)

Se suman las comisiones de aliados (20% de la facturación referida) y el plan Render Pro.
El modelo completo está en `python scripts/modelo_financiero.py` del repositorio.

---

## 4. Las tres decisiones que más plata mueven

### 4.1 Capital suscrito: $5.000.000, no $20.000.000

| Capital suscrito | Matrícula | Inscripción | RUES | Imp. registro | **Total** |
|---|---|---|---|---|---|
| **$5.000.000** | $66.605 | $72.660 | $8.500 | $35.000 | **$182.765** |
| $20.000.000 | $193.760 | $72.660 | $8.500 | $140.000 | $414.920 |
| $50.000.000 | $448.070 | $72.660 | $8.500 | $350.000 | $879.230 |

Suscribir $20M en lugar de $5M cuesta **$232.155 más el primer día, y nada a cambio.**
"Se ve más serio" no es un beneficio: nadie mira el capital suscrito de una S.A.S. nueva.

### 4.2 Una sociedad, no dos

Ahorro inmediato: ~$200.000 de constitución. **Ahorro real: la contabilidad mensual de una
segunda entidad**, entre $300.000 y $800.000 al mes, todos los meses, con o sin operación.
En un año son entre $3,6M y $9,6M.

### 4.3 Registro de marca aplazado

Ahorro: **$2.021.500**. Riesgo asumido: el sistema marcario colombiano es **atributivo** —la
marca es de quien la registra primero, no de quien la usa primero—. Mitigaciones en
[`../03-legal-producto/05-registro-software-dnda.md`](../03-legal-producto/05-registro-software-dnda.md) §6:
verificación previa en SIPI, dominio y redes registrados, evidencia fechada de uso.

---

## 5. Cuándo sí gastar el margen que queda

En este orden, y solo cuando aparezca el disparador:

1. **Contador mensual**, en cuanto haya facturación real. Un error tributario del primer año cuesta más que un año de honorarios.
2. **Proveedor de facturación con API**, cuando facturar a mano pase de 2 horas al mes.
3. **Render Starter o Pro**, con el primer cliente en producción.
4. **Registro de marca**, con 10 clientes pagos.

**No gastes en:** logo profesional (ya hay uno en
[`../05-marketing/assets/`](../05-marketing/assets/)), sitio web hecho por terceros, publicidad
antes de saber qué mensaje funciona, oficina, o herramientas de ventas antes de tener a quién
venderle.

---

## 6. Lo que no está costeado y hay que confirmar

| Concepto | Estado |
|---|---|
| Cuota de manejo de cuenta bancaria empresarial | **[NE]** Varía por banco y por campaña. Compara al menos tres. Pregunta por cuota de manejo, costo de transferencias ACH y saldo mínimo |
| Honorarios contables | **[NE]** No hay tarifa regulada. $300.000–$800.000/mes por entidad es referencia de mercado en Bogotá |
| Prima de póliza E&O | **[NE]** No publicada. Requiere cotización con corredor |
| Descuento MiPyme en tasas de la SIC | **[NE]** Existe; no verifiqué el porcentaje vigente para 2026. Pregúntalo al radicar |
| Precio del dominio `.co` | **[NE]** Varía por registrador y promoción |
| Costo de infraestructura por tenant | **[NE]** Estimado en $25.000/mes. Mídelo con datos reales |

**No uses ninguna de estas cifras en una proyección que le muestres a alguien** sin
confirmarla primero.
