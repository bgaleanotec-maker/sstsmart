# Qué proveedor de facturación electrónica usar con presupuesto cero

---

## 1. La recomendación, primero

**Arranca con la solución gratuita de la DIAN. Migra a un proveedor con API cuando la
facturación manual te cueste más de dos horas al mes.**

Automatizar la facturación antes de tener a quién facturarle es la forma más común de
gastar los primeros $200.000 en nada. El emisor no es tu producto.

**Con una salvedad que puede adelantar la migración:** si la solución gratuita **no emite
documento soporte en adquisiciones a no obligados a facturar**, vas a necesitar un proveedor
desde la **primera liquidación de comisiones a un aliado que no facture** — no desde las 20
facturas al mes. Sin ese documento el gasto no es deducible. **Verifícalo en el portal de la
DIAN antes de lanzar el programa de aliados**; son diez minutos y mueve el presupuesto.

---

## 2. Comparativa

| Opción | Costo | API | Set de pruebas | Cuándo usarla |
|---|---|---|---|---|
| **Solución gratuita DIAN** | **$0** | **No** | No requiere | **Fase 0: clientes 1 a 5.** Es válida legalmente y emite documentos con plena validez. **[NE] Verifica dos cosas antes de contar con ella:** (1) que emita **documento soporte en adquisiciones a no obligados a facturar** — lo necesitas para pagar comisiones de aliados y que el gasto sea deducible; (2) si tiene condiciones o límites de acceso por tamaño del obligado |
| **Factus** | Por **paquetes de documentos**; sandbox compartido gratuito e ilimitado para pruebas. **[NE]** No publica precios: se cotizan por WhatsApp | **Sí**, REST, con SDKs de comunidad | Lo aporta el proveedor | **Fase 1: automatización con volumen bajo.** El modelo por paquete encaja con facturación irregular |
| **Alegra — plan Emprendedor** | **$13.425/mes** en plan anual (~$161.100/año) · facturas de venta ilimitadas · certificado digital y usuario contador incluidos | **Sí** | Lo aporta el proveedor | **Fase 2: cobro recurrente estable.** Integra con Treli para suscripciones y con el módulo contable |
| Alegra — plan Pyme | $37.425/mes | Sí | — | Con nómina y más volumen |
| Siigo, Dataico, Facture, Carvajal | **[NE]** No publican tarifas comparables de forma abierta; requieren cotización | Sí | Sí | Cuando ya haya volumen que justifique negociar |

---

## 3. Por qué la solución gratuita de la DIAN sirve al principio y no después

**Sirve porque:** es gratuita, emite documentos con plena validez legal, no requiere set de
pruebas propio, y la interfaz es suficiente para emitir una factura en cinco minutos.

**Deja de servir cuando:** no tiene API. No puedes disparar la emisión desde un webhook de
la pasarela, ni generar la factura automáticamente al renovar una suscripción, ni
conciliar. Con cobro recurrente real es inviable.

**El umbral concreto:** más de **20 facturas al mes**, o renovaciones en fechas dispersas.

---

## 4. Criterios de selección cuando llegue el momento de migrar

Ordenados por lo que realmente duele después:

1. **API REST documentada, con sandbox.** Sin sandbox, cada prueba es una factura real que hay que anular.
2. **Webhooks de estado del documento.** Que el proveedor te avise cuándo la DIAN validó o rechazó, en lugar de tener que preguntar por *polling*.
3. **Emisión de documento soporte** para adquisiciones a no obligados a facturar. **Lo vas a necesitar para pagar comisiones a afiliados** que no emitan factura.
4. **Modelo de precio por documento, no por usuario.** Una plataforma emite muchas facturas y tiene un solo usuario administrador.
5. **Notas crédito por API.** Cancelaciones y prorrateos son parte normal de un SaaS por suscripción.
6. **Exportación del XML firmado**, no solo del PDF.

---

## 5. Cómo no quedar atrapado en un proveedor

El emisor debe ser una **pieza reemplazable** del backend, no una dependencia atravesada
en todo el código.

```python
# app/facturacion/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ResultadoFactura:
    cufe: str
    numero: str
    xml_url: str
    pdf_url: str
    estado: str          # "validada" | "rechazada" | "pendiente"

class ProveedorFacturacion(ABC):
    """Contrato único. Cambiar de proveedor = una clase nueva, cero cambios afuera."""

    @abstractmethod
    def emitir_factura(self, venta) -> ResultadoFactura: ...

    @abstractmethod
    def emitir_nota_credito(self, factura, motivo, valor) -> ResultadoFactura: ...

    @abstractmethod
    def emitir_documento_soporte(self, pago_a_no_obligado) -> ResultadoFactura: ...

    @abstractmethod
    def consultar_estado(self, cufe: str) -> str: ...
```

Implementaciones: `ProveedorDIANManual` (registra lo que emitiste a mano), `ProveedorFactus`,
`ProveedorAlegra`. El resto de la aplicación solo conoce `ProveedorFacturacion`.

**Esto son dos horas de trabajo hoy y evita una semana de refactor el día que cambies de
proveedor** — que va a pasar, porque el primero se elige por precio y el segundo por
funcionalidad.

---

## 6. Costos publicados de Alegra (planes anuales, 2026)

| Plan | Facturación electrónica | Contabilidad | Nómina |
|---|---|---|---|
| Emprendedor | **$13.425/mes** | $56.175/mes | $22.425/mes (1–10 empleados) |
| Pyme | $37.425 | $122.925 | $51.750 (11–20) |
| Pro | $74.925 | $188.175 | $104.250 (21–45) |
| Plus | $134.925 | $239.925 | $194.250 (45–90) |

---

## 7. Declaración de lo que no pude verificar

- **[NE] Precios de Factus.** El sitio no los publica; remite a WhatsApp. El sandbox compartido sí es gratuito e ilimitado, y la API está documentada públicamente.
- **[NE] Precios de Siigo, Dataico, Facture y Carvajal.** No publican tarifas comparables.
- **[NE] Vigencia de la resolución de numeración** (usualmente citada como 24 meses). Confírmala en el acto de autorización que emita la DIAN.

---

## Fuentes

[Factus — sitio oficial](https://www.factus.com.co/) ·
[Factus — documentación de API](https://developers.factus.com.co/) ·
[Alegra — precios Colombia](https://www.alegra.com/colombia/precios/) ·
[DIAN — sistema de facturación electrónica](https://catalogo-vpfe.dian.gov.co)
