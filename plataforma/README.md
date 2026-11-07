# `plataforma/` — de SaaS de SST a plataforma de apps legales de nicho

> Corte: **13-oct-2026**. Este paquete amplía el dossier de `docs/` (SST y PESV, ago-2026)
> a la visión completa: **una S.A.S. de apps de nicho a gran escala** (SST, PESV, tutelas,
> accidentes de tránsito, impuestos y otras) y **una práctica jurídica de Brian como abogado
> persona natural** que representa a los clientes que lo necesitan.
> Lo escribió Claude a partir de investigación web con fuentes; **Claude Code lo toma desde aquí**.

## Cómo leerlo

| Si eres… | Lee |
|---|---|
| Brian, 15 minutos | [`00-tesis-y-decisiones.md`](00-tesis-y-decisiones.md) |
| Brian, antes de vender o de derivar un cliente | [`01-estructura-legal-dos-entidades.md`](01-estructura-legal-dos-entidades.md) |
| Quien priorice qué construir | [`03-priorizacion-y-secuencia.md`](03-priorizacion-y-secuencia.md) |
| **Claude Code, antes de escribir código** | [`04-arquitectura-plataforma.md`](04-arquitectura-plataforma.md) → [`06-backlog-claude-code.md`](06-backlog-claude-code.md) |
| Quien revise los números | [`05-modelo-de-negocio-y-finanzas.md`](05-modelo-de-negocio-y-finanzas.md) y `modelo/modelo_plataforma.py` |

## Índice

| Archivo | Contenido |
|---|---|
| [`00-tesis-y-decisiones.md`](00-tesis-y-decisiones.md) | La tesis, cifras clave, las 8 decisiones que hay que tomar y el foco recomendado |
| [`01-estructura-legal-dos-entidades.md`](01-estructura-legal-dos-entidades.md) | S.A.S. de software vs. abogado persona natural: Decreto 196/1971, Ley 1123/2007, derivación lícita, IA, consumidor, datos, tributario, conflictos de interés |
| `02-verticales/` | Una ficha por vertical: mercado, normas, competencia, monetización, MVP, riesgos |
| ↳ [`01-sst.md`](02-verticales/01-sst.md) | Puntero al dossier existente y su lugar en la plataforma |
| ↳ [`02-pesv.md`](02-verticales/02-pesv.md) | Actualización oct-2026 y correcciones al dossier |
| ↳ [`03-tutelas-y-peticiones.md`](02-verticales/03-tutelas-y-peticiones.md) | El motor de alto volumen: petición → tutela → desacato |
| ↳ [`04-accidentes-de-transito.md`](02-verticales/04-accidentes-de-transito.md) | SOAT/ADRES, responsabilidad civil y fotomultas |
| ↳ [`05-impuestos.md`](02-verticales/05-impuestos.md) | Defensa ante la DIAN y calendario tributario (no renta masiva) |
| ↳ [`06-verticales-candidatas.md`](02-verticales/06-verticales-candidatas.md) | Laboral, centrales de riesgo, insolvencia, propiedad horizontal, pensiones |
| ↳ [`07-penal.md`](02-verticales/07-penal.md) | Víctimas en querellables, conciliación, reparación y penal-SST para empleadores |
| ↳ [`08-firma-app.md`](02-verticales/08-firma-app.md) | Firma App como consola del abogado y producto para abogados |
| **Cerebro Legal + Radar de Oportunidades** | Servicio aparte en `empresa/Apis/cerebro_legal/` (jurisprudencia verificada, líneas, estrategias con Radar, oportunidades de cada fallo) |
| [`03-priorizacion-y-secuencia.md`](03-priorizacion-y-secuencia.md) | Puntaje por vertical, secuencia, calendario de ventanas, la restricción de horas de abogado |
| [`04-arquitectura-plataforma.md`](04-arquitectura-plataforma.md) | Núcleo común + verticales; cuentas personales; muro de datos; motor de plazos; IA; ADR |
| [`05-modelo-de-negocio-y-finanzas.md`](05-modelo-de-negocio-y-finanzas.md) | Fuentes de ingreso por entidad, precios, valor por hora de abogado, escenarios |
| [`06-backlog-claude-code.md`](06-backlog-claude-code.md) | Épicas e historias con criterios de aceptación, en orden, para ejecutar en este repo |
| [`07-riesgos-y-pendientes.md`](07-riesgos-y-pendientes.md) | Registro de riesgos, lista `[VERIFICAR]` y derechos de petición por radicar |
| [`fuentes.md`](fuentes.md) | Todas las fuentes consultadas, por tema |
| `modelo/` | `modelo_plataforma.py` y sus salidas con 60 h y 160 h de abogado al mes |

## Convenciones
- `[V]` verificado con fuente citada · `[E]` estimación o supuesto propio · `[VERIFICAR]` no confirmado en fuente oficial.
- Pesos COP 2026. SMMLV 2026 $1.750.905 · UVT 2026 $52.374.
- Lo que **propone** Claude va como propuesta. Las **decisiones** las toma Brian y se anotan en §7 del `CONTEXTO.md` del repo.
- Antes de usar una cifra o una norma en material comercial o en un escrito: verificarla en la fuente oficial.
