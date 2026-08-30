# SST Smart — Dossier de negocio, producto y arquitectura

Investigación, arquitectura y plan de negocio para convertir el proyecto `sst-project-v2`
en un SaaS vendible en Colombia. Estado de la investigación: **30 de agosto de 2026**.

## Cómo leer este dossier

| Si quieres… | Empieza por |
|---|---|
| El panorama completo en 15 minutos | [`00-resumen-ejecutivo.md`](00-resumen-ejecutivo.md) |
| Saber si hay mercado y de qué tamaño | [`01-mercado/01-mercado-sgsst-colombia.md`](01-mercado/01-mercado-sgsst-colombia.md) |
| Saber contra quién compites y a qué precio | [`01-mercado/02-analisis-competitivo.md`](01-mercado/02-analisis-competitivo.md) |
| Entender la oportunidad de seguridad vial | [`01-mercado/03-mercado-pesv-seguridad-vial.md`](01-mercado/03-mercado-pesv-seguridad-vial.md) |
| Saber qué falta en el producto | [`02-producto/01-diagnostico-producto-actual.md`](02-producto/01-diagnostico-producto-actual.md) |
| Construir la arquitectura multiempresa | [`03-arquitectura/01-arquitectura-saas-multitenant.md`](03-arquitectura/01-arquitectura-saas-multitenant.md) |
| Crear la empresa y desplegar | [`04-empresa/00-checklist-maestro.md`](04-empresa/00-checklist-maestro.md) |
| Ver cómo se llega a $30M/mes | [`05-monetizacion/02-modelo-financiero-30M.md`](05-monetizacion/02-modelo-financiero-30M.md) |

## Índice completo

### 00 · Resumen
- [`00-resumen-ejecutivo.md`](00-resumen-ejecutivo.md) — tesis, cifras clave, decisiones y riesgos

### 01 · Mercado
- [`01-mercado-sgsst-colombia.md`](01-mercado/01-mercado-sgsst-colombia.md) — universo empresarial, regulación, multas, TAM/SAM/SOM, canales
- [`02-analisis-competitivo.md`](01-mercado/02-analisis-competitivo.md) — 25+ competidores, precios reales, seis huecos de mercado
- [`03-mercado-pesv-seguridad-vial.md`](01-mercado/03-mercado-pesv-seguridad-vial.md) — Res. 40595/2022, Circular 0034/2026, tamaño y competencia
- [`04-segmentacion-y-buyer-personas.md`](01-mercado/04-segmentacion-y-buyer-personas.md) — ICP, personas, mensajes y objeciones

### 02 · Producto
- [`01-diagnostico-producto-actual.md`](02-producto/01-diagnostico-producto-actual.md) — auditoría del repo y brecha hacia SaaS
- [`02-roadmap-24-meses.md`](02-producto/02-roadmap-24-meses.md) — releases por trimestre atados al plan comercial
- [`03-especificacion-modulo-pesv.md`](02-producto/03-especificacion-modulo-pesv.md) — 24 pasos, modelo de datos, reutilización del SG-SST
- [`04-especificacion-servicios-juridicos.md`](02-producto/04-especificacion-servicios-juridicos.md) — matriz legal viva, retainer, límites del ejercicio profesional

### 03 · Arquitectura
- [`01-arquitectura-saas-multitenant.md`](03-arquitectura/01-arquitectura-saas-multitenant.md) — multi-tenancy, RLS, migraciones, archivos
- [`02-despliegue-git-render.md`](03-arquitectura/02-despliegue-git-render.md) — render.yaml, entornos, CI/CD, costos de infraestructura
- [`03-seguridad-y-cumplimiento.md`](03-arquitectura/03-seguridad-y-cumplimiento.md) — checklist de seguridad, Trust Center, due diligence

### 04 · Empresa (paso a paso)
- [`00-checklist-maestro.md`](04-empresa/00-checklist-maestro.md) — **la ruta completa, en orden, con costos**
- [`01-constitucion-y-estructura-societaria.md`](04-empresa/01-constitucion-y-estructura-societaria.md)
- [`02-tributario-y-facturacion.md`](04-empresa/02-tributario-y-facturacion.md)
- [`03-datos-personales-y-propiedad-intelectual.md`](04-empresa/03-datos-personales-y-propiedad-intelectual.md)
- [`04-pagos-y-cobranza-recurrente.md`](04-empresa/04-pagos-y-cobranza-recurrente.md)
- [`05-calendario-de-obligaciones.md`](04-empresa/05-calendario-de-obligaciones.md)

### 05 · Monetización
- [`01-pricing-y-empaquetado.md`](05-monetizacion/01-pricing-y-empaquetado.md) — planes, add-ons, política de descuentos
- [`02-modelo-financiero-30M.md`](05-monetizacion/02-modelo-financiero-30M.md) — tres escenarios, mes a mes, hasta $30M
- [`03-unit-economics-y-metricas.md`](05-monetizacion/03-unit-economics-y-metricas.md) — CAC, LTV, payback, tablero de KPIs
- [`04-plan-comercial-gtm.md`](05-monetizacion/04-plan-comercial-gtm.md) — canales, contenido, canal de consultores, playbook de venta

## Convenciones

- **[V]** dato verificado con fuente citada · **[E]** estimación propia · **[NE]** no encontrado.
- Todos los pesos son COP de 2026. SMMLV 2026 = $1.750.905 · UVT 2026 = $52.374 · UVB 2026 = $12.110.
- Cuando una cifra no pudo verificarse en fuente primaria, el documento lo dice en lugar de estimarla.
