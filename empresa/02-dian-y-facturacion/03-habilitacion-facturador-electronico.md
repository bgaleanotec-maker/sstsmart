# Habilitación como facturador electrónico — de cero a factura validada

**Costo: $0.** Tiempo: 3–4 horas de trabajo repartidas en 3 a 7 días, según cuánto tarde
el set de pruebas.

---

## 1. Marco vigente

- **Resolución 000165 de 2023**, anexo técnico de facturación electrónica **v1.9**
- **Resolución 000227 de 2025** **[NE]**, que consolidó las normas dispersas del sistema de facturación. La fecha exacta (23 de septiembre de 2025) y el número de normas consolidadas provienen de fuente secundaria; verifícalos en el portal de la DIAN si los vas a citar públicamente

**Documentos del sistema de facturación electrónica:**

| Documento | Cuándo lo vas a usar |
|---|---|
| **Factura electrónica de venta** | Cada suscripción cobrada |
| **Nota crédito** | Anulaciones, devoluciones, descuentos posteriores |
| Nota débito | Ajustes al alza |
| **Documento soporte en adquisiciones a no obligados a facturar** | **Pago de comisiones a afiliados que no facturen** — ver [`../04-programa-afiliados/`](../04-programa-afiliados/) |
| Nómina electrónica | Desde el primer empleado |
| Documento equivalente electrónico | Casos específicos |
| RADIAN | Registro de la factura como título valor, para factoring. No lo necesitas todavía |

---

## 2. Prerrequisitos

- [ ] NIT asignado y RUT actualizado con **responsabilidad 52 (facturador electrónico)**
- [ ] **Instrumento de Firma Electrónica (IFE)** activo
- [ ] Cuenta DIAN habilitada como representante legal
- [ ] Decidido el software: propio, gratuito de la DIAN, o de proveedor tecnológico → [`04-proveedores-comparativa.md`](04-proveedores-comparativa.md)

---

## 3. Paso a paso

### Paso 1 · Registro en el servicio de facturación

1. https://catalogo-vpfe.dian.gov.co (o desde MUISCA → **Sistema de Facturación Electrónica**)
2. Ingresa como persona jurídica, con NIT y el usuario del representante legal.
3. Acepta los términos y condiciones del servicio.

### Paso 2 · Configuración de datos

- Datos del obligado a facturar (se traen del RUT)
- **Correo de recepción de facturas electrónicas** — configúralo con cuidado: ahí llegan las facturas que te emitan tus proveedores, y son la base de tu IVA descontable
- Datos del software: nombre, identificador y PIN. Si usas un proveedor, él te los da

### Paso 3 · Asociar el software

| Ruta | Qué haces |
|---|---|
| **Software gratuito DIAN** | Se selecciona directamente en el portal. No requiere set de pruebas propio |
| **Proveedor tecnológico** (Factus, Alegra, etc.) | El proveedor ya está habilitado; asocias su software a tu NIT desde el portal, o él lo hace por ti |
| **Software propio** | Registras tu software, obtienes ID y PIN, y **debes superar el set de pruebas tú mismo** contra el ambiente de habilitación |

### Paso 4 · Set de pruebas (solo software propio o proveedor nuevo)

La DIAN exige emitir un lote de documentos de prueba —facturas de venta con distintos
escenarios (con y sin IVA, con descuentos, con retenciones) y notas crédito y débito— que
deben ser **validados sin rechazo** contra el ambiente de habilitación.

**Qué falla habitualmente:**

| Falla | Causa |
|---|---|
| Rechazo por firma XAdES inválida | Certificado mal cargado o cadena incompleta |
| Rechazo por CUFE mal calculado | Orden o formato de los campos del hash |
| Rechazo por rango de numeración | Prefijo o consecutivo fuera del rango autorizado |
| Rechazo por tributos | Códigos de tributo (01 IVA, 06 ReteFuente…) mal mapeados |

> **Si eliges un proveedor tecnológico ya habilitado, este paso lo saltas casi completo.**
> Es la razón principal para no construir el emisor propio en el arranque: el set de
> pruebas puede costarte dos semanas de trabajo de desarrollo que hoy valen más en el
> producto.

### Paso 5 · Habilitación en producción

Superado el set de pruebas, el portal habilita el ambiente de producción.

### Paso 6 · Solicitar rango de numeración

MUISCA → **Numeración de facturación** → solicitar autorización.

- Define un **prefijo** (ej. `FE`) y un rango generoso: pedir 1.000 números no cuesta más que pedir 100, y quedarse sin rango a mitad de mes es un problema evitable
- La resolución de numeración tiene **vigencia** (habitualmente 24 meses **[NE]**, confírmalo en el acto de autorización). Anota la fecha de vencimiento en el calendario

### Paso 7 · Factura de prueba real

Emite una factura real de valor bajo a tu propio NIT y verifica:

- [ ] Se genera el **CUFE**
- [ ] El PDF representación gráfica y el **XML** llegan por correo
- [ ] El documento aparece como **"Validado"** en el portal de la DIAN
- [ ] El código QR resuelve correctamente

Hasta que esos cuatro puntos estén, no le cobres a un cliente.

---

## 4. Datos del comprador — la novedad útil de la Res. 000227

La Resolución 000227 de 2025 limita a **tres los datos exigibles al comprador**:

1. Tipo y número de identificación
2. Nombre o razón social
3. Correo electrónico

Y la DIAN expone un **servicio para autocompletar nombre y correo a partir del NIT**.

**Aprovéchalo en el checkout.** Cada campo que quitas del formulario de suscripción sube la
conversión. Pedir NIT y autocompletar el resto es mejor experiencia que pedir seis campos.

---

## 5. Integración con el cobro recurrente

```
pago exitoso en la pasarela
        ↓  webhook
   tu backend Flask
        ↓  API del proveedor de facturación
   emisión del documento
        ↓
   validación DIAN
        ↓
   envío al cliente con CUFE + XML + PDF
```

### Tres reglas

1. **Factura según la causación legal, no según la caja.** La obligación de facturar nace con la venta o la prestación del servicio (arts. 615 y 616-1 ET) y el IVA en servicios se causa en la fecha **más temprana** entre emisión, terminación del servicio y pago (art. 429 lit. c ET). "No facturo hasta que me paguen" es un consejo frecuente y equivocado: no evita la causación, produce **omisión de facturación** —sancionable— y deja al cliente sin soporte de su IVA descontable. **La solución al problema de caja es cobrar por anticipado**, no aplazar la factura. Define con tu contador el momento exacto de causación para tu modelo de suscripción, antes del primer cobro.
2. **Emite la factura en el mismo acto del cobro anticipado**, disparada por el webhook de pago. Así la causación y la caja coinciden y no hay que decidir nada caso por caso.
3. **Guarda el XML, no solo el PDF.** El XML firmado es el documento; el PDF es una representación gráfica. En una revisión de la DIAN piden el XML. Consérvalos **cinco años**.

---

## 6. Mientras no haya API — el flujo manual es perfectamente válido

Para los primeros clientes:

1. El cliente paga por PSE o transferencia
2. Confirmas el pago
3. Emites la factura desde el portal gratuito de la DIAN (5 minutos)
4. El sistema la envía al correo del cliente

Cinco clientes son 25 minutos al mes. Automatizar antes de eso es optimizar un problema
que no tienes.

**El umbral para automatizar:** cuando la facturación manual te tome más de **2 horas al
mes**, o cuando tengas renovaciones recurrentes en fechas distintas. Ahí sí, proveedor con
API.

---

## 7. Checklist

- [ ] Responsabilidad 52 en el RUT
- [ ] IFE activo
- [ ] Software asociado en el portal DIAN
- [ ] Set de pruebas superado (si aplica)
- [ ] Habilitación en producción confirmada
- [ ] Rango de numeración autorizado, con **fecha de vencimiento en el calendario**
- [ ] Factura de prueba real emitida, validada y recibida por correo
- [ ] Correo de **recepción** de facturas de proveedores configurado
- [ ] Carpeta de respaldo de XML con retención de 5 años

---

## Fuentes

[DIAN — Sistema de facturación electrónica](https://catalogo-vpfe.dian.gov.co) ·
[Facturación electrónica 2026 — marco vigente](https://siemprealdia.co/colombia/impuestos/sistema-de-facturacion-electronica-en-colombia/) ·
[Resolución 000227 de 2025](https://www.sai-open.com/nueva/facturacion-electronica-colombia-2026-resolucion-000227/) ·
[Factus — documentación de API](https://developers.factus.com.co/)
