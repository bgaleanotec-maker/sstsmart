# Diagnóstico del producto actual

Auditoría del repositorio `sst-project-v2` al **30 de agosto de 2026**, contrastada contra lo que el mercado exige (ver [`../01-mercado/02-analisis-competitivo.md`](../01-mercado/02-analisis-competitivo.md)).

---

## 1. Qué hay hoy

| Métrica | Valor |
|---|---|
| Archivos Python (app + scripts, sin `legacy/`) | 35 · **6.432 líneas** |
| Plantillas Jinja2 | 64 |
| Modelos SQLAlchemy | 14 archivos · **33 tablas** |
| Blueprints | 9 (`admin`, `auth`, `controles`, `dashboard`, `formacion`, `ia`, `juridico`, `matriz_legal`, `reportes`) |
| Rutas | **92** (46 solo en `admin.py`) |
| Tests | **1 archivo** (`test_juridico.py`, 10 tests) |
| Base de datos | SQLite en desarrollo; `psycopg2` comentado en `requirements.txt` |
| Roles | 7 canónicos, con normalización histórica en `Usuario.tiene_rol()` |

**Módulos funcionales:** reportes de condiciones inseguras con foto y escalamiento por SLA · ciclo de vida de controles (planificado → implementado → verificado → efectivo) · matriz legal con valoración jurídica, evidencias versionadas y log forense · consultas jurídicas con SLA y generación de PDF · formación con cursos, exámenes, certificados y ranking · administración de catálogos y reglas de escalamiento · IA con Gemini (chat experto y análisis de imágenes).

**Lo que está bien hecho y hay que conservar:**

- La disciplina de `app/constants.py` como único punto de verdad de roles, con `tiene_rol()` normalizando variantes históricas. Es exactamente la clase de decisión que evita una deuda cara.
- Secretos solo por variable de entorno (`app/config.py`).
- `scripts/seed_matriz_legal.py` es idempotente y está actualizado a agosto de 2026, con las derogatorias resueltas. **Ese archivo es, hoy, el activo diferencial del producto.**
- La separación en `scripts/legacy/` del código retirado, con la regla explícita de no importar desde ahí.
- El módulo jurídico existe y funciona: es lo que ningún competidor tiene.

---

## 2. La brecha hacia un SaaS vendible

Ordenada por lo que bloquea ingresos, no por lo que es más fácil.

### 2.1 Bloqueadores duros (sin esto no se puede vender)

| # | Brecha | Impacto comercial | Documento |
|---|---|---|---|
| **B1** | **Sin multi-tenancy.** Una sola empresa por base de datos. Solo `riesgo.py` tiene `empresa_id`, y sin FK ni índice. No existe el modelo `Empresa` | **Mata el canal de consultores**, que es la mejor oportunidad del mercado. Y obliga a un despliegue por cliente, lo que es económicamente inviable | [`../03-arquitectura/01`](../03-arquitectura/01-arquitectura-saas-multitenant.md) |
| **B2** | **CSRF no habilitado** (no hay Flask-WTF; los formularios son POST simples) | Primer hallazgo de cualquier pentest. Bloquea due diligence con cualquier comprador mediano | [`../03-arquitectura/03`](../03-arquitectura/03-seguridad-y-cumplimiento.md) |
| **B3** | **No existe el módulo de autoevaluación de la Res. 0312** (7/21/60 estándares con puntaje y plan de mejora) | Es **el único entregable con consecuencia regulatoria anual** y el gancho de adquisición de la ventana mayo–julio. Sin esto no hay campaña | §3 de este documento |
| **B4** | **Sin registro de pago ni facturación.** No hay planes, suscripciones, ni integración con pasarela | No se puede cobrar | [`../04-empresa/04`](../04-empresa/04-pagos-y-cobranza-recurrente.md) |
| **B5** | **Token de GitHub expuesto en la URL del remoto** (`origin` con `github_pat_…`) | Riesgo de seguridad activo. **Revocar hoy** | [`../03-arquitectura/02`](../03-arquitectura/02-despliegue-git-render.md) |

### 2.2 Brechas de producto (frenan el precio, no el cobro)

| # | Brecha | Consecuencia |
|---|---|---|
| P1 | **Sin módulo PESV** | Se pierde el add-on de mayor margen y menor competencia del mercado |
| P2 | **Sin indicadores del art. 30 de la Res. 0312** (frecuencia, severidad, mortalidad, prevalencia, incidencia EL, ausentismo) | Son de reporte obligatorio y hoy hay que calcularlos a mano |
| P3 | **Sin FURAT/FUREL** con recordatorio de 2 días hábiles (Res. 156/2005 + 2851/2015) | Falta el flujo que más urgencia genera cuando ocurre un accidente |
| P4 | **Sin COPASST ni Comité de Convivencia** bajo la Res. 3461/2025 | Norma nueva de sep-2025 con trámite de queja ≤65 días. Es dolor fresco |
| P5 | **Sin captura móvil offline** con foto y geolocalización | El reporte de condiciones inseguras ocurre en el piso de planta. Hasta el software gratis de la ARL tiene app nativa |
| P6 | **`Empleado` y buena parte de las tablas de matriz de riesgos están semi-huérfanas** (definidas, poco usadas por rutas) | El módulo de riesgos no es utilizable de punta a punta |
| P7 | **Dos servicios de notificación con nombres casi idénticos** (`utils/notificaciones.NotificationService` y `services/notificaciones.NotificacionService`) | Fuente garantizada de bugs de import. Unificar |
| P8 | **Sin exportación de datos del cliente** | Es argumento de venta ("sus datos son suyos") y es exigencia contractual |

### 2.3 Deuda técnica y operativa

| # | Deuda | Nota |
|---|---|---|
| D1 | **1 archivo de test para 92 rutas** | Sin red de seguridad para refactorizar hacia multi-tenancy — que es exactamente el refactor más peligroso que se puede hacer |
| D2 | **SQLite en desarrollo, `db.create_all()`** | RLS y los tipos de Postgres no existen en SQLite. El entorno de desarrollo debe migrar a Postgres **antes** del refactor multi-tenant, o el aislamiento no se puede probar |
| D3 | **`admin.py` con 46 rutas** | Archivo monolítico; conviene dividir por dominio antes de que crezca más |
| D4 | **Sin CI** | Ninguna verificación automática antes de desplegar |
| D5 | **Historial de git con 5 commits titulados "Descripción de tus cambios"** | Irrelevante para el usuario, relevante para due diligence y para el propio equipo |
| D6 | **Archivos subidos sin estrategia de almacenamiento** (`uploads/`) | Un disco persistente en Render rompe los despliegues sin downtime y el escalado horizontal simultáneamente. Debe ir a object storage |

---

## 3. Los cuatro módulos que faltan y que valen dinero

Priorizados por **ingreso desbloqueado por unidad de esfuerzo**.

### 3.1 Autoevaluación Res. 0312 — máxima prioridad

**Por qué:** es el hueco #2 del mercado. Ningún competidor ofrece el flujo completo, tiene fecha límite anual (31 de julio, plataforma SGRL) y es una sola pantalla bien hecha.

**Alcance mínimo:**
- Determinación automática del régimen aplicable (7 / 21 / 60) a partir de número de trabajadores × clase de riesgo — **ojo con la doble clasificación del Decreto 957/2019: es por trabajadores, no por ingresos**.
- Ítem por ítem, con calificación, justificación y **evidencia adjunta enlazada al documento real del sistema** (no un archivo suelto).
- Cálculo del puntaje y clasificación: **crítico <60 · moderado 61–85 · aceptable >85**.
- **Plan de mejoramiento derivado automáticamente** de los ítems no cumplidos, con responsable y fecha.
- Exportación en formato compatible con el registro en SGRL, y PDF firmado para enviar a la ARL.
- Histórico anual comparable año contra año.

### 3.2 Multi-tenancy y consola de consultor

**Por qué:** desbloquea el segmento #1. Sin esto, el plan comercial de este dossier no se sostiene.

**Alcance mínimo:** modelo `Empresa` · `empresa_id` NOT NULL con FK e índice en las 33 tablas de dominio · RLS en Postgres · scoping por sesión · **consola multiempresa** con semáforo de cumplimiento por cliente y cambio de contexto en un click · propagación de actualizaciones normativas a todas las empresas del consultor. Detalle técnico en [`../03-arquitectura/01`](../03-arquitectura/01-arquitectura-saas-multitenant.md).

### 3.3 Módulo PESV

**Por qué:** hueco #3, cero competencia integrada, forcing event anual desde 2026, y **60–70% reutilizable** de lo que ya existe. Especificación completa en [`03-especificacion-modulo-pesv.md`](03-especificacion-modulo-pesv.md).

### 3.4 Matriz legal viva

**Por qué:** hueco #1 y el diferenciador que la formación jurídica hace defendible.

**Lo que falta sobre lo que ya existe:** `seed_matriz_legal.py` es un volcado estático. Convertirlo en un **ciclo de vida**: cada norma con estado (vigente / derogada / modificada), fecha de última verificación, norma que la reemplaza, y **propagación del impacto** — cuando una norma se deroga, el sistema marca automáticamente qué documentos, controles y evidencias de cada empresa quedan afectados y genera las tareas de actualización. Detalle en [`04-especificacion-servicios-juridicos.md`](04-especificacion-servicios-juridicos.md).

---

## 4. Orden de ejecución recomendado

No es negociable el orden de los tres primeros: cada uno depende del anterior.

| Orden | Qué | Por qué en ese lugar |
|---|---|---|
| **0** | Revocar el PAT de GitHub; remoto a SSH | Riesgo activo. Hoy |
| **1** | Migrar el entorno de desarrollo a **Postgres** | RLS no existe en SQLite; sin esto no se puede probar el aislamiento |
| **2** | **Tests de las rutas críticas** antes de tocar los modelos | El refactor multi-tenant sin red de seguridad es cómo se pierden datos de clientes |
| **3** | **CSRF, rate limiting y headers** de seguridad | Barato, rápido, y desbloquea conversaciones comerciales |
| **4** | **Multi-tenancy + RLS + tests de aislamiento entre tenants** | El refactor grande, con la red ya puesta |
| **5** | **Autoevaluación Res. 0312** | El primer módulo que se puede vender solo |
| **6** | Facturación y suscripciones | Para cobrar |
| **7** | Consola de consultor | Abre el canal |
| **8** | Módulo PESV | Add-on de mayor margen |
| **9** | Matriz legal viva + indicadores art. 30 | Consolida el diferencial |

Cronograma con trimestres y releases en [`02-roadmap-24-meses.md`](02-roadmap-24-meses.md).

---

## 5. Lo que NO hay que construir

- **App móvil nativa.** Una PWA con captura de foto, geolocalización y cola offline cubre el caso de uso (reporte de condiciones inseguras e inspección preoperacional) a una fracción del costo, y se despliega sin pasar por dos tiendas de aplicaciones.
- **Integraciones con ERP y nómina** antes de tener 50 clientes. Es el pozo sin fondo clásico del B2B temprano.
- **SOC 2.** Ver [`../03-arquitectura/03`](../03-arquitectura/03-seguridad-y-cumplimiento.md): un Trust Center cubre el 80% de la due diligence de pymes colombianas por una fracción del costo.
- **Un chatbot de IA más.** VERA, SOFÍA, PAULA, IngesIA y Copilot ya existen y todos hacen lo mismo: conversar sobre la norma. **La IA aquí debe *ejecutar*** — generar la matriz IPEVR desde la descripción del cargo, redactar la investigación desde el FURAT, recalcular el plan anual cuando cambia una norma. Si no ejecuta, no la construyas.
