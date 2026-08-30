# Resumen ejecutivo

**Fecha:** 30 de agosto de 2026 · **Proyecto:** SST Smart (repo `sst-project-v2`)
**Meta declarada:** ingreso medio mensual ≥ **$30.000.000 COP** en 18–24 meses.

---

## 1. La tesis en cinco frases

1. En Colombia hay **1.227.399 empresas afiliadas al sistema de riesgos laborales** [V, Fasecolda/CCS 2025]; de ellas unas **260.000 están obligadas a 21 o 60 estándares mínimos**, que es el trabajo que ningún Excel sostiene [E].
2. Entre 2022 y 2025 se **derogaron cinco normas estructurales del SG-SST** (Res. 2404/2019, 2346/2007, 652 y 1356 de 2012, y el régimen de licencias). Toda matriz legal armada antes de 2025 está desactualizada — ese es el dolor verificable y fechado que se vende.
3. El mercado tiene **seis huecos abiertos**: nadie une SG-SST con jurídico de verdad, nadie resuelve bien la autoevaluación de la Res. 0312, **nadie tiene módulo PESV completo**, nadie sirve al canal de consultores con multi-tenancy real, casi nadie tiene captura móvil de campo, y **solo 5 de ~25 competidores publican precio**.
4. La **Circular 0034 del 30 de marzo de 2026** obliga por primera vez a las empresas *no transportadoras* a reportar anualmente sus indicadores de PESV al Ministerio del Trabajo. Es un evento de cumplimiento nuevo, fechado y masivo, sin oferta de software que lo resuelva.
5. La formación jurídica no es un adorno: es el diferenciador que ningún competidor de software puede copiar. Pero debe venderse desde **una sociedad distinta** a la del software, por razones tributarias, de responsabilidad y de ejercicio profesional.

## 2. Cifras que sostienen la tesis

| Dato | Valor | Fuente |
|---|---|---|
| Empresas afiliadas al SGRL | 1.227.399 | CCS/Fasecolda, cierre 2025 [V] |
| Trabajadores afiliados | 13.510.827 | CCS/Fasecolda 2025 [V] |
| Empresas con 11–50 trabajadores (21 estándares) | ~151.000 | Proyección sobre estructura Fasecolda 2020 [E] |
| Empresas con >50 o riesgo IV–V (60 estándares) | ~109.000 | Idem [E] |
| Accidentes de trabajo 2025 | 534.444 (1.464/día) | CCS 2025 [V] |
| Muertes laborales 2025 | 438, **+16,8%** vs 2024 | CCS 2025 [V] |
| Multa por incumplimiento SST, pequeña empresa | $8,27M – $27,6M | Dec. 1072 art. 2.2.4.11 en UVT (Dec. 2642/2022) [V] |
| Multa por AT mortal, mediana empresa | $208M – $551M | Idem [V] |
| Empresas obligadas a PESV (transporte) | ~10.300, **43% sin reportar** | Supertransporte 2024 [V] |
| Muertes viales 2025 | >8.600; Q1-2026 **+20,1%** | ANSV [V] |
| Costo de implementar SG-SST vía consultor (pequeña) | $1,5M – $3,5M + $349k–$680k/mes | Mentora, Proestrategia 2026 [V] |
| Costo de diseñar un PESV vía consultor | $8M – $20M | Cotizaciones de mercado [E sobre base V] |

## 3. Las decisiones que este dossier recomienda

| # | Decisión | Por qué |
|---|---|---|
| 1 | **Dos sociedades:** SST Smart SAS (software) y Galeano y Asociados (jurídico) | Régimen Simple castiga los servicios profesionales (7,3–8,3% y tope de 12.000 UVT); separa responsabilidad; hace la SaaS invertible |
| 2 | **Multi-tenancy shared-table** (`empresa_id`) + **Row Level Security** en Postgres | Schema-per-tenant no pasa de unos cientos; DB-per-tenant revienta el `max_connections=100` de Render |
| 3 | **Precio público** entre **$149.000 y $749.000/mes por empresa**, nunca por trabajador | Solo 5 de ~25 competidores publican precio; el modelo por trabajador se lee como impuesto al crecimiento |
| 4 | **Canal de consultores como motor #1** | Un consultor administra 5–40 empresas; menor CAC, mayor LTV, y ninguna plataforma revisada lo sirve bien |
| 5 | **Módulo PESV como segundo motor** | Cero competidores SG-SST lo tienen completo; forcing event anual desde 2026 |
| 6 | **Retainer jurídico como add-on recurrente**, no como proyecto | Convierte margen de bufete en MRR; ancla de precio: Legis silvIA a $159.664/mes |
| 7 | **Región Virginia en Render**, decidida antes del primer deploy | No se puede cambiar después; ~50 ms menos que Oregon hacia Bogotá |
| 8 | **Habilitar CSRF (Flask-WTF) antes de vender** | Es el primer hallazgo de cualquier pentest y bloquea due diligence |

## 4. La ruta a $30M/mes (escenario base)

| Hito | Mes | MRR | Ingreso total del mes | Cuentas |
|---|---:|---:|---:|---:|
| Primeros clientes de pago | 3 | $1,07M | $3,51M | 4 |
| Producto multiempresa en producción | 6 | $4,50M | $7,60M | 14 |
| Primer canal de consultores activo | 12 | $12,49M | $16,91M | 32 |
| **Ingreso mensual cruza $30M** | **20** | $24,3M | **$30,6M** | 57 |
| **MRR cruza $30M** | **24–25** | **$29,7M** | **$36,19M** | 64 |

- **ARR mes 24:** $356.331.357 · **ARPA:** $461.329/mes · **Utilidad operativa mes 24:** ~$9,2M
- Escenario conservador (altas −30%, churn 3%): $18,9M de MRR en el mes 24 — llega a $30M hacia el mes 33.
- Escenario agresivo (altas +35%, churn 1,5%): MRR cruza $30M en el **mes 18**.

**Advertencia honesta:** $30M/mes de *ingreso* no es $30M/mes de *utilidad*. En el escenario base, el mes 24 deja ~$9,2M de utilidad operativa después de una nómina de $18,8M. Para que **la utilidad** sea $30M/mes se necesitan ingresos del orden de **$65–70M/mes**, lo que corre el horizonte a 36 meses o exige mayor precio medio. El detalle está en [`05-monetizacion/02-modelo-financiero-30M.md`](05-monetizacion/02-modelo-financiero-30M.md).

## 5. Los cinco riesgos que hay que mirar de frente

1. **Las ARL regalan software.** ALISSTA (Positiva), Colmena Gestión, Ridsso (Sura) y Guardián de la Productividad (Bolívar) son gratuitos para afiliados y cubren el caso de uso central de la microempresa. **Mitigación:** no competir en el tramo de 7 estándares; atacar 21/60, multiempresa, PESV y jurídico, donde esas herramientas no llegan, y vender la independencia de la ARL como valor (cambiar de ARL no debe costar perder el historial documental).
2. **El producto todavía es monoempresa.** Sin multi-tenancy no existe el canal de consultores, que es la mejor oportunidad del mercado. Es el bloqueador número uno del plan comercial.
3. **Riesgo jurídico del producto.** Si la matriz legal cita una norma derogada y un cliente es sancionado, la exposición es real. **Mitigación:** procedimiento documentado de vigilancia normativa, fecha de última actualización visible por norma, disclaimers, límite contractual de responsabilidad y póliza E&O.
4. **Datos sensibles de salud.** Exámenes médicos e incapacidades son datos sensibles bajo la Ley 1581/2012: exigen autorización explícita, cifrado y log de accesos. El producto debe separar el **concepto de aptitud** (que el empleador sí ve) del **diagnóstico clínico** (que no).
5. **El token de GitHub está expuesto en la URL del remoto.** El `origin` del repo tiene un Personal Access Token embebido. **Revocarlo hoy** y pasar el remoto a SSH — es la única acción de esta lista que no admite espera. Procedimiento en [`03-arquitectura/02-despliegue-git-render.md`](03-arquitectura/02-despliegue-git-render.md).

## 6. Los primeros 30 días

| Día | Acción | Documento |
|---|---|---|
| 1 | Revocar el PAT de GitHub y migrar el remoto a SSH | `03-arquitectura/02` |
| 1–3 | Habilitar CSRF, rate limiting y headers de seguridad | `03-arquitectura/03` |
| 3–10 | Implementar `empresa_id` + RLS en todas las tablas de dominio | `03-arquitectura/01` |
| 5 | Registrar el software en la DNDA (gratuito) | `04-empresa/03` |
| 7–15 | Constituir SST Smart SAS en la CCB (~$180k–$450k) | `04-empresa/01` |
| 10 | Definir la posición de IVA (19% vs. exclusión art. 476 num. 21) | `04-empresa/02` |
| 15 | Radicar la marca en la SIC, clases 9 y 42 (~$2,02M) | `04-empresa/03` |
| 15–25 | Desplegar el blueprint de Render (staging + producción) | `03-arquitectura/02` |
| 20 | Publicar la página de precios con checkout de autoservicio | `05-monetizacion/01` |
| 25–30 | Cerrar los 3 primeros clientes piloto con descuento de fundador | `05-monetizacion/04` |
