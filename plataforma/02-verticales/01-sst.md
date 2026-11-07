# Vertical 1 — SST (SG-SST) · marca Justrabajo

**Estado:** construyendo, en producción en Render (`justrabajo.onrender.com`). Es la **vertical ancla** de la plataforma y la única con código maduro.

## Dónde está todo
| Tema | Documento |
|---|---|
| Contexto y reglas del código | `CONTEXTO.md`, `CLAUDE.md` (raíz del repo) |
| Mercado, competencia, segmentos | `docs/01-mercado/` |
| Producto, roadmap 24 meses | `docs/02-producto/` |
| Arquitectura multiempresa | `docs/03-arquitectura/` |
| Precios, modelo financiero a $30M | `docs/05-monetizacion/` |
| Constitución de la S.A.S. | `empresa/` |

## Su papel en la plataforma
1. **Motor de caja recurrente**: en el escenario base, el ingreso del mes cruza $30M en el mes 20 (`docs/05-monetizacion/02`).
2. **Dueña del núcleo**: multiempresa (`app/tenancy.py`), catálogo de módulos con precio (`app/data/modulos.py`), gating (`app/modulos.py`), IA (`app/services/gemini_service.py`), notificaciones, módulo jurídico. Las verticales nuevas se montan sobre esto (ver `../04-arquitectura-plataforma.md`).
3. **Fuente del retainer jurídico B2B** del abogado (`docs/02-producto/04`), que es la línea con mejor relación entre horas y caja estable.

## Lo que cambia con la visión de plataforma
- El **módulo `juridico`** pasa a ser la **consola del abogado** de toda la plataforma (no solo SST): expediente, cupo, SLA, control de conflictos, firma con tarjeta profesional.
- El catálogo `MODULOS` deja de ser solo SST: cada vertical registra sus módulos con `vertical` y `segmento` (B2B/B2C).
- **Conflicto de interés**: las empresas con retainer quedan como contrapartes bloqueadas para las verticales laboral y tránsito (`../01-estructura-legal-dos-entidades.md` §6).

## Pendientes que siguen abiertos (de `CONTEXTO.md`)
Nombre definitivo · pricing público · cobro Wompi + factura DIAN · Postgres dev + Alembic + RLS activo · archivos en R2 · unificar los dos servicios de notificación.
