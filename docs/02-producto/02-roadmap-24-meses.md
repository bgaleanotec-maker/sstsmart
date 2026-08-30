# Roadmap 24 meses — producto atado al plan comercial

Cada release existe porque desbloquea un ingreso concreto. La columna "desbloquea" es la razón de ser de la fila.

---

## Trimestre 1 (meses 1–3) · **R1 — Fundación multiempresa**

**Meta comercial:** 4 cuentas de pago · MRR $1,07M · primeros pilotos con descuento de fundador.

| Entregable | Desbloquea |
|---|---|
| Revocar PAT de GitHub; remoto a SSH; secret scanning activado | Cierra un riesgo activo |
| Migración del entorno de desarrollo a **Postgres 16** | Precondición técnica de todo lo demás |
| **Suite de tests** de las 20 rutas críticas (auth, reportes, controles, matriz legal, jurídico) | Red de seguridad para el refactor |
| **Flask-WTF (CSRF)** + Flask-Limiter + Flask-Talisman + Argon2id | Desbloquea conversaciones con compradores medianos |
| Modelo **`Empresa`** + `empresa_id` NOT NULL con FK e índice en las 33 tablas | Precondición del canal |
| **RLS en Postgres** con `FORCE`, dos roles de BD, `set_config(..., true)` | Aislamiento real, no solo aplicativo |
| **Tests automáticos de aislamiento entre tenants** (por cada modelo: A no ve filas de B) | Lo que hace confiable el punto anterior |
| Unificar los dos servicios de notificación | Elimina una fuente garantizada de bugs |
| Blueprint de Render: staging + producción, región **Virginia** | Infraestructura reproducible |
| CI en GitHub Actions con `autoDeployTrigger: checksPass` | Nada llega a producción sin pasar tests |

> **Riesgo del trimestre:** el refactor multi-tenant es el cambio más peligroso de todo el roadmap. Hacerlo con 1 archivo de test es cómo se filtran datos entre clientes. Los tests van **antes**, no después.

---

## Trimestre 2 (meses 4–6) · **R2 — El primer módulo que se vende solo**

**Meta comercial:** 14 cuentas · MRR $4,50M · producto multiempresa en producción.

| Entregable | Desbloquea |
|---|---|
| **Módulo de autoevaluación Res. 0312** (7/21/60, puntaje, plan de mejora derivado, exportación SGRL, PDF para la ARL, histórico anual) | **El gancho de adquisición de la ventana mayo–julio** |
| **Indicadores del art. 30**: frecuencia, severidad, mortalidad, prevalencia, incidencia EL, ausentismo, calculados desde eventos | Reporte obligatorio que hoy se hace a mano |
| **Suscripciones y facturación**: planes, ciclo de cobro, Wompi + orquestador, integración con facturación electrónica vía API | Permite cobrar |
| Onboarding autoservicio: registro, prueba de 14 días sin tarjeta, checkout | Elimina el "agendar demo" que mata la conversión pyme |
| **Página de precios pública** | Diferenciador competitivo sin costo de desarrollo (solo 5 de ~25 publican precio) |
| Migración de archivos a **Cloudflare R2** con prefijo por tenant y URLs prefirmadas | Quita el disco persistente, que rompe zero-downtime y escalado |
| Exportación completa de datos por empresa | Argumento de venta y exigencia contractual |

---

## Trimestre 3 (meses 7–9) · **R3 — Abrir el canal**

**Meta comercial:** 23 cuentas · MRR $8,07M · primer consultor con cartera migrada.

| Entregable | Desbloquea |
|---|---|
| **Consola de consultor**: semáforo de cumplimiento de N empresas en una pantalla, cambio de contexto en un click, alertas agregadas | **El segmento #1** |
| Propagación de actualizaciones normativas a todas las empresas de un consultor | La razón por la que el consultor cambia de Excel a esto |
| Plantillas y "empresa modelo" clonable | Reduce a minutos el alta de cada nueva empresa del consultor |
| Marca propia para el canal: subdominio y logo (wildcard TLS de Render, costo marginal ~USD 0,25/mes) | Argumento de retención del consultor |
| **FURAT/FUREL** con recordatorio de 2 días hábiles | El flujo de máxima urgencia cuando ocurre un accidente |
| **PWA** con captura de foto, geolocalización y cola offline | Cierra el hueco #5; hasta el software gratis de la ARL tiene app |

---

## Trimestre 4 (meses 10–12) · **R4 — Seguridad vial**

**Meta comercial:** 32 cuentas · MRR $12,49M · primer add-on PESV vendido.

| Entregable | Desbloquea |
|---|---|
| **Módulo PESV, fase 1**: vehículos, conductores, control documental con alertas de vencimiento, checklist preoperacional móvil, plan de mantenimiento | El add-on de mayor margen |
| **Generación del paquete de reporte** para la Circular 0034 (MinTrabajo) y SISI/PESV | **Campaña de enero**: el forcing event anual |
| Diagnóstico gratuito de obligatoriedad PESV (imán de leads) | El mejor generador de leads del mercado, trivial de construir |
| **COPASST y Comité de Convivencia** bajo Res. 3461/2025 (actas, periodos, quejas confidenciales, trámite ≤65 días) | Norma de sep-2025: dolor fresco |
| Trust Center público | Cubre el 80% de la due diligence de pymes |

---

## Trimestre 5 (meses 13–15) · **R5 — El diferencial jurídico**

**Meta comercial:** 41 cuentas · MRR $17,10M · retainer jurídico con 15%+ de attach.

| Entregable | Desbloquea |
|---|---|
| **Matriz legal viva**: ciclo de vida por norma (vigente/derogada/modificada), fecha de verificación, norma que reemplaza, y **propagación del impacto** a documentos, controles y evidencias de cada empresa | **El hueco #1 del mercado** — y lo que ningún competidor de software puede copiar |
| Flujo de retainer jurídico: cupo de consultas por plan, SLA por prioridad, concepto firmado por abogado, expediente | Convierte margen de bufete en MRR |
| **IA que ejecuta, no que conversa**: generar matriz IPEVR desde la descripción del cargo; redactar borrador de investigación desde el FURAT; recalcular el plan anual cuando cambia una norma | Deja atrás a los cinco chatbots del mercado |
| Módulo PESV fase 2: pasos 6, 10, 13, 21, 22 (riesgos viales, formación, investigación de siniestros, estadística, auditoría anual con lista de verificación de los 24 pasos) | Sube el add-on PESV al nivel estándar/avanzado |

---

## Trimestre 6 (meses 16–18) · **R6 — Empresa mediana**

**Meta comercial:** 51 cuentas · MRR $22,13M.

| Entregable | Desbloquea |
|---|---|
| **Multi-sede y contratistas** con responsabilidad solidaria | El plan Corporativo ($749.000) |
| **SSO (SAML/OIDC)** y 2FA obligatorio para roles administrativos | Requisito de compra de empresas de 51–200 |
| API pública documentada + webhooks | Integraciones que pide el comprador mediano |
| Gestión del cambio, adquisiciones y proveedores | Estándares del régimen de 60 |
| Cifrado a nivel de columna para diagnósticos clínicos; separación estricta entre **concepto de aptitud** (lo ve el empleador) y **diagnóstico** (no) | Cumplimiento de datos sensibles, Ley 1581 |

---

## Trimestres 7–8 (meses 19–24) · **R7/R8 — Escala y defensa**

**Meta comercial:** 64 cuentas · MRR $29,69M · ingreso mensual $36,19M.

| Entregable | Desbloquea |
|---|---|
| Autoscaling y alta disponibilidad de Postgres en Render | Estabilidad con 60+ tenants |
| Benchmarking anónimo entre empresas del mismo sector y clase de riesgo | Feature de retención que solo se puede construir con base instalada — y que **requiere anonimización irreversible** para no convertirte en responsable del tratamiento |
| Módulo PESV nivel avanzado; ISO 39001 | Empresas de transporte grandes |
| Alertas normativas como producto independiente (freemium de captación) | Canal de adquisición de bajo costo |
| Certificados y formación con validez ante auditoría | Upsell del módulo de formación |
| Evaluación de ISO 27001 (no SOC 2 — tiene mejor reconocimiento local) | Solo si se están perdiendo contratos concretos por no tenerlo |

---

## Regla de priorización permanente

Ante cualquier funcionalidad propuesta, en este orden:

1. ¿Desbloquea un ingreso concreto y nombrado, o solo "mejora el producto"?
2. ¿Lo pidió un cliente que paga, o lo pidió un prospecto que no ha pagado nunca?
3. ¿Cierra uno de los seis huecos del mercado, o compite en un terreno donde ya hay cinco competidores?
4. ¿Se puede reutilizar del SG-SST existente (como el PESV, 60–70%), o hay que construirlo de cero?

Si no pasa las cuatro, va al backlog.
