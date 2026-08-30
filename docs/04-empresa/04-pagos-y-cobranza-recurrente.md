# Pagos y cobranza recurrente

> Verificado a agosto de 2026.

**El problema central del SaaS B2B en Colombia:** tus clientes pyme no pagan con tarjeta de crédito, y **PSE no permite débito recurrente automático**. Todo el diseño de cobro parte de ahí.

---

## 1. Comparativa de pasarelas

| Pasarela | Comisión tarjeta | PSE | Recurrencia nativa | Dispersión | Nota |
|---|---|---|---|---|---|
| **Wompi** (Bancolombia) | **2,65% + $700 + IVA** (Plan Avanzado) | Sí | Vía tokenización + orquestador; **Nequi y débito de cuentas Bancolombia** | Rápida | Puntos Colombia 4,43% + $700. Plan Gateway: 0% Wompi, negocias con cada adquirente |
| **Bold** | **2,99% + $900** en línea (0–$10M/mes); 3,59% + $900 ($10–20M/mes) | Sí | Limitada | Día hábil siguiente antes de 10 a.m. (Cuenta Bold) o inmediata | Cuenta digital y facturación electrónica incluidas. >$20M/mes: tarifa negociada |
| **ePayco** | **3,29% + $700 + IVA**; 2,68% + $900 preferencial Davivienda (requiere ~$20M/mes) | Sí; <$60.000 → $2.000 fijo + IVA | Sí (tokenización) | Retiro $6.500 + IVA | +22 medios de pago |
| **PayU Latam** | ~3,49% + $900 | Sí | Sí (tokenización, líder regional) | Variable | Antifraude robusto |
| **Mercado Pago** | Variable según plazo de acreditación | Sí | Sí (preapproval) | Inmediata / 14 / 30 días | Comisión baja con acreditación diferida |
| **dLocal** | Custom, típicamente 3–5% | Sí | Sí | T+2 a T+14 | Mid-market/enterprise, proceso de ventas, sin autoservicio |
| **Stripe** | — | No | — | — | **NO disponible para empresas colombianas en 2026.** Solo vía LLC en EE.UU. |
| **Paddle** (merchant of record) | **5% + US$0,50** (≈6% efectivo) | No | Sí | — | Asume IVA/sales tax global |
| **Lemon Squeezy** (MoR) | 5% + US$0,50 + 1,5% internacional (≈6,6%) | No | Sí | 1% en payouts no-US | Igual que Paddle |
| **Treli** | Custom | Vía pasarela | **Sí — es su producto** | Vía pasarela | Orquestador de suscripciones sobre Wompi/PayU/ePayco/PlaceToPay + **integración nativa con Alegra** |

---

## 2. PSE recurrente — la limitación real

**PSE no sirve para cobro recurrente automático.** Arquitectónicamente exige que el cliente sea **redirigido al portal de su banco y autorice cada transacción individualmente**. No hay tokenización ni mandato permanente en el flujo PSE estándar.

### Las tres alternativas

| Opción | Cómo funciona | Realidad en pyme colombiana |
|---|---|---|
| **1. Tokenización de tarjeta** | Capturas la tarjeta una vez, guardas el token en la pasarela, cobras periódicamente | **La penetración de tarjeta de crédito en pymes colombianas es baja.** Cuenta con fallos de cobro |
| **2. Débito automático ACH con mandato** | El cliente autoriza a su banco un débito permanente. Es lo que Wompi ofrece para cuentas Bancolombia y Nequi | **Cobertura limitada a esos ecosistemas** |
| **3. Híbrido — el realista para B2B pyme** | Primer pago por PSE o transferencia; para renovaciones, **factura electrónica con link de pago** (PSE/tarjeta) enviada por email y WhatsApp, con recordatorios automáticos | Cobro recurrente "asistido", no automático — **pero funciona con el medio de pago que tus clientes realmente tienen** |

> **Diseña para el modelo 3 desde el día uno.** Construir solo para tarjeta te va a costar la mitad de las renovaciones. Y ofrece incentivo al pago anual (2 meses gratis): resuelve el problema de recurrencia once veces al año.

---

## 3. Recomendación

**Wompi + orquestador de suscripciones.**

**Por qué Wompi:**
- **La mejor tarifa del mercado**: 2,65% + $700 + IVA
- PSE + Nequi + débito de cuentas Bancolombia en un solo proveedor
- **El respaldo de Bancolombia reduce la fricción de confianza con pymes** — un factor real en un mercado donde el gerente desconfía de meter datos bancarios en una web que no conoce
- Dispersión rápida

**Orquestador:** **Treli** (integra nativamente con Alegra, que es tu proveedor de facturación electrónica) o lógica propia. La decisión depende de cuánto quieras construir: la gestión de ciclos, prorrateos, cambios de plan, dunning y conciliación es más trabajo del que parece.

**Reserva Paddle o Lemon Squeezy** solo si vas a vender fuera de Colombia y quieres externalizar la carga fiscal global. Su ~6% efectivo es caro para el mercado local y **no soportan PSE**, que es el medio de pago que tus clientes usan.

---

## 4. Arquitectura de cobro

```
Suscripción creada
       ↓
Ciclo de facturación (mensual o anual)
       ↓
┌──────────────────────────────────────────────┐
│ ¿Tiene método tokenizado?                    │
│   Sí → cobro automático                      │
│   No → factura electrónica con link de pago  │
│        + email + WhatsApp                    │
└──────────────────────────────────────────────┘
       ↓
Webhook de pago exitoso
       ↓
Backend valida y registra
       ↓
API de facturación (Alegra) → emisión → validación DIAN
       ↓
Envío al cliente con el CUFE
```

> **Regla dura: nunca emitas la factura antes de confirmar el pago.** Una factura emitida y no pagada genera **IVA e ingreso fiscal devengado** que tendrás que anular con nota crédito. A escala, eso convierte tu contabilidad en un problema.

---

## 5. Dunning — la secuencia de cobranza

La retención de ingresos se pierde tanto por churn voluntario como por **fallos de cobro no gestionados**. Diseña la secuencia antes de tener el primer cliente.

| Día | Acción | Canal |
|---|---|---|
| −7 | Aviso de renovación próxima con monto | Email |
| 0 | Intento de cobro / envío de factura con link | Email + WhatsApp |
| +3 | Recordatorio 1 | Email + WhatsApp |
| +7 | Recordatorio 2 + aviso de suspensión | Email + WhatsApp + llamada si el ticket >$500.000 |
| +10 | Reintento de cobro automático | Sistema |
| +15 | **Suspensión del acceso** (datos intactos, exportación disponible) | Email |
| +45 | Aviso de eliminación programada | Email |
| +90 | Eliminación conforme a la política de retención | Sistema |

**Nunca elimines datos sin aviso previo y sin ventana de exportación.** Es una obligación de la Ley 1581 (devolver o suprimir al terminar) y es lo que evita una reclamación.

---

## 6. Política de precios y cobro

| Regla | Razón |
|---|---|
| **Precio en COP, publicado, con IVA claramente indicado** | Solo 5 de ~25 competidores publican precio. Es un diferenciador sin costo |
| **Pago anual con 2 meses gratis (≈17% de descuento)** | Resuelve el problema de recurrencia de PSE once veces al año y mejora el flujo de caja |
| **Prueba de 14 días sin tarjeta** | El "agendar demo" mata la conversión en pyme |
| **Sin permanencia mínima** | Kawak, CumpleSST y HoldingSoft+ lo ofrecen; no puedes ser el único que ata |
| **Exportación completa de datos al terminar** | Argumento de venta, exigencia contractual y obligación legal |
| **Nunca cobrar por trabajador** | Ningún competidor colombiano lo hace; la pyme lo lee como impuesto al crecimiento |
| **Facturas separadas: software (SST Smart SAS) y jurídico (bufete)** | Dos NIT, dos regímenes. Ver [`01-constitucion-y-estructura-societaria.md`](01-constitucion-y-estructura-societaria.md) |

---

## 7. Costo real de la pasarela sobre el modelo

Con comisión de **2,65% + $700 + IVA ≈ 3,15% efectivo** sobre el ticket medio:

| Ingreso mensual | Costo de pasarela |
|---|---|
| $5.000.000 | ~$157.500 |
| $15.000.000 | ~$472.500 |
| $30.000.000 | ~$945.000 |
| $36.000.000 | ~$1.134.000 |

Está incluido en el modelo financiero de [`../05-monetizacion/02-modelo-financiero-30M.md`](../05-monetizacion/02-modelo-financiero-30M.md).

> **Palanca de optimización:** empujar el pago anual reduce el número de transacciones (el componente fijo de $700) y mejora el flujo de caja. A ticket de $149.000 mensual, los $700 representan un 0,47% adicional; en pago anual, se diluyen a 0,04%.

## Fuentes

[Wompi — planes y tarifas](https://soporte.wompi.co/hc/es-419/articles/360020957133) · [Bold — tarifas](https://bold.co/tarifas) · [ePayco — comisiones (ComparaPagos, jul-2026)](https://comparapagos.lat/pasarelas/epayco/) · [Comparativa de pasarelas 2026 — BytechHub](https://bytechhub.com/blog/pasarelas-de-pago-en-colombia-comparativa-2026/) · [Stripe no soportado en Colombia](https://mazinooyolo.com/blog/stripe-account-in-colombia/) · [dLocal fees 2026](https://comparepsp.com/providers/dlocal/) · [Merchant of record pricing 2026](https://fungies.io/merchant-of-record-pricing-guide-2026/) · [PSE y débito recurrente — Mouv](https://www.mouvlatam.com/recursos/recaudo-pse-empresas) · [Treli — tarifas y pasarelas](https://treli.co/tarifas/) · [BTO Digital — comparativa de 12 pasarelas](https://btodigital.com/pasarelas-pago-colombia-comparativa-guia-negocio/) · [Alegra — precios](https://www.alegra.com/colombia/precios/)
