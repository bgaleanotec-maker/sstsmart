# Arquitectura de la plataforma multivertical

> Para Claude Code. Parte del estado real del repo (oct-2026): monolito Flask modular,
> `app/tenancy.py` (TenantMixin + filtro por `empresa_id`), catálogo `app/data/modulos.py`,
> gating `app/modulos.py`, `app/services/gemini_service.py`, dos servicios de notificación,
> módulo `juridico`. Respeta las **reglas duras** de `CLAUDE.md` y las 12 reglas de producto de
> `01-estructura-legal-dos-entidades.md` §9.

## 1. Forma general

```
                        ┌──────────────────────────── una app Flask (Render, Virginia) ────────────────────────────┐
  Landings por marca ─► │  app/verticales/                                                                         │
  (SEO por vertical)    │   sst/ · pesv/ · peticiones_tutelas/ · impuestos/ · laboral/ · transito/ · …            │
                        │        │ usan                                                                            │
                        │  app/core/  ← NÚCLEO COMPARTIDO                                                          │
                        │   cuentas (tenant) · plazos · documentos · expediente · derivación · conflictos         │
                        │   ia (guardrails) · pagos (Wompi) · notificaciones (correo, WhatsApp, in-app) · auditoría│
                        └───────────────┬───────────────────────────────┬──────────────────────────────────────────┘
                                        │ HTTP                          │
                         Apis/radar_judicial (vigilancia a demanda)   Proveedores: SendGrid, Meta WhatsApp, Gemini,
                                                                       Wompi, facturación DIAN, RUNT vía contrato/intermediario
```

**Principio:** una vertical nueva = un blueprint + plantillas + reglas de plazo + entradas en el catálogo. Todo lo demás lo da el núcleo.

## 2. Decisiones de arquitectura (ADR)

| # | Decisión | Alternativa descartada | Por qué |
|---|---|---|---|
| **ADR-P1** | **Monorepo en `sst-project-v2`**, una sola app Flask, verticales como paquetes en `app/verticales/<v>/` | Un repo o servicio por vertical | Un solo desarrollador; despliegue, auth, cobro y tests compartidos. Se separa un servicio solo si su carga lo exige (como ya ocurre con Radar Judicial) |
| **ADR-P2** | **La cuenta personal B2C es un tenant**: se reutiliza la tabla `empresas` con una columna `tipo_cuenta` ∈ {`organizacion`, `personal`, `practica_juridica`} | Tabla de personas fuera de la tenencia | Reutiliza TenantMixin, RLS y el test de aislamiento sin código nuevo. Registrar un usuario B2C crea su tenant personal |
| **ADR-P3** | **La derivación al abogado es un modelo cruzado explícito** (`Derivacion`, sin TenantMixin, como los modelos de aliados) que copia un **expediente** al tenant `practica_juridica` solo con consentimiento | Dar al abogado acceso directo a los datos del usuario | Muro de datos (Ley 1581; Ley 1123 art. 34 lit. f), revocable y auditable |
| **ADR-P4** | **La IA no cita normas ni jurisprudencia por su cuenta.** Toda cita sale de una `biblioteca_juridica` curada y verificada; la IA solo redacta hechos y ordena argumentos | Dejar que el LLM cite | Alucinaciones (T-323/2024); lección DoNotPay; responsabilidad profesional |
| **ADR-P5** | **Motor de plazos propio** con catálogo de reglas con fuente normativa; festivos con la librería `holidays` (Colombia) + tabla de excepciones verificada cada año | Calcular plazos en cada vertical | Un error de plazo es el riesgo profesional más caro; un solo lugar probado |
| **ADR-P6** | **Fuentes públicas solo por vía autorizada**: API oficial, contrato (RUNT 2.0), intermediario autorizado o consulta a demanda del titular. Nunca raspado ni evasión de captchas | Scrapers | SIC Res. 63771/2022; Ley 1273/2009 art. 269A. Igual que Radar Judicial |
| **ADR-P7** | **Marcas por vertical, un backend**: landings en rutas propias (`/tutelas`, `/dian`…) y luego dominios propios apuntando a la misma app con tema por host | Una app por marca | SEO y confianza por nicho sin multiplicar infraestructura |

| **ADR-P8** | **Firma App se porta por módulos a este monorepo** como consola del abogado (tenant `practica_juridica`) y luego como SaaS para otros abogados. No se porta `judicial_scraper.py` | Mantener dos apps Flask | Un solo núcleo de tenencia, conflictos, plazos y pagos |
| **ADR-P9** | **El Cerebro Legal es un servicio aparte** (`empresa/Apis/cerebro_legal`, FastAPI + Postgres + pgvector) que la plataforma consume por HTTP para citas, playbooks y estrategias. La `biblioteca_juridica` del núcleo (§3.3) se alimenta de él cuando exista; mientras tanto, se llena a mano con verificación | Meter la búsqueda jurídica en la app web | Se reutiliza en Firma App, Radar y la bóveda de Obsidian; carga distinta |
| **ADR-P10** | **Radar Judicial → Cerebro → consola**: los eventos de Radar se envían al Cerebro, que devuelve una sugerencia (borrador) a la consola del abogado | Lógica de estrategia dentro de Radar | Separación de responsabilidades |

## 3. Núcleo (`app/core/`) — módulos y modelo de datos

### 3.1 Cuentas
- `Empresa.tipo_cuenta` (nuevo, mini-migración aditiva en `scripts/init_prod_db.py`). Valores por defecto: filas existentes = `organizacion`.
- Registro B2C: crea `Empresa(tipo_cuenta='personal', nombre=<usuario>)` + `Usuario` con rol `Titular` (constante nueva en `app/constants.py`; usar siempre `tiene_rol`).
- La práctica del abogado es un tenant `practica_juridica` con rol `Abogado`.
- El catálogo `MODULOS` gana campos `vertical`, `segmento` (`B2B`/`B2C`), `tipo_precio` (`mensual`/`unidad`) y `tipos_cuenta` permitidos. El gating de `app/modulos.py` respeta `tipos_cuenta`.

### 3.2 Plazos (`app/core/plazos.py`)
```
calendario         (codigo{general|judicial|dian}, descripcion)
festivo            (fecha, calendario_codigo, fuente, verificado_en)          -- excepciones y vacancias
regla_plazo        (codigo, vertical, descripcion, cantidad, unidad{dias_habiles|dias_calendario|meses|anios},
                    calendario_codigo, norma_fuente, articulo, verificada_por, verificada_en, activa)
plazo              (TenantMixin; caso_id, regla_codigo, fecha_inicio, fecha_vence, estado{abierto|cumplido|vencido},
                    alerta_dias=[7,3,1])
```
API: `calcular_vencimiento(regla_codigo, fecha_inicio) -> date` y `dias_restantes(plazo)`. Reglas iniciales (todas nacen con `estado='pendiente_verificacion'` hasta que Brian las verifique, historia E2.0):

| Código | Regla | Unidad | Fuente |
|---|---|---|---|
| `peticion_general` | 15 | días hábiles | Ley 1755/2015 art. 14 |
| `peticion_documentos` | 10 | días hábiles | Ídem |
| `peticion_consulta` | 30 | días hábiles | Ídem |
| `tutela_fallo` | 10 | días (hábiles según jurisprudencia `[VERIFICAR]`) | Decreto 2591/1991 art. 29 |
| `tutela_impugnacion` | 3 | días hábiles `[VERIFICAR]` | Decreto 2591/1991 art. 31 |
| `dian_emplazamiento_declarar` | 1 | mes `[VERIFICAR]` | art. 715 ET |
| `dian_emplazamiento_corregir` | 1 | mes `[VERIFICAR]` | art. 685 ET |
| `dian_requerimiento_ordinario` | `[VERIFICAR plazo y artículo]` | — | arts. 684-686 ET |
| `dian_requerimiento_especial` | 3 | meses | art. 707 ET |
| `dian_reconsideracion` | 2 | meses | art. 720 ET |
| `cpaca_nulidad_restablecimiento` | 4 | meses | CPACA art. 164 |
| `adres_reclamacion` | 1 | año | Decreto 780/2016 art. 2.6.1.4.4.1 |
| `soat_aseguradora` | 2 | años | C.Co. art. 1081 |
| `pcl_solicitud` | 18 | meses | `[VERIFICAR fuente]` |
| `pesv_reporte_mintrabajo` | según último dígito del NIT | fecha fija | Circular 0034/2026 `[VERIFICAR]` | **Cada regla con su fuente y fecha de verificación visibles.** Si una regla no está verificada, la interfaz lo dice.

Pendiente de criterio jurídico antes de codificar `[VERIFICAR]`: cómo afectan la vacancia judicial y la Semana Santa a cada término; cómputo de meses en el ET.

### 3.3 Documentos (`app/core/documentos.py`)
```
plantilla          (codigo, vertical, version, cuerpo_jinja, campos_json, revisada_por_abogado_id,
                    revisada_en, lista_blanca{bool}, activa)
biblioteca_juridica(id, tipo{norma|sentencia|concepto}, referencia, extracto, url_oficial,
                    verificada_por, verificada_en, vigente{bool})
documento_generado (TenantMixin; caso_id, plantilla_codigo, plantilla_version, datos_json,
                    citas_ids[], generado_con_ia{bool}, modelo_ia, fecha, archivo_url, hash)
```
- Salida DOCX y PDF (ReportLab ya está; añadir `python-docx`).
- Pie obligatorio: aviso de autoservicio, etiqueta de IA (modelo y fecha) y "revise y firme".
- `lista_blanca=False` → la plantilla solo la puede usar el rol `Abogado`.

### 3.4 Expediente, derivación y conflictos
```
caso               (TenantMixin; vertical, tipo, estado, titular_usuario_id, contraparte_id, creado_en)
evento_caso        (TenantMixin; caso_id, tipo, fecha, detalle_json)            -- máquina de estados por vertical
contraparte        (nit_o_cedula_normalizado, nombre, tipo)                       -- catálogo global, sin tenant
derivacion         (SIN TenantMixin; caso_origen_id, tenant_origen_id, practica_id, autorizacion_texto,
                    autorizada_en, revocada_en, estado{solicitada|aceptada|rechazada_conflicto|cerrada})
autorizacion_datos (TenantMixin; usuario_id, finalidad, texto_version, otorgada_en, revocada_en, sensible{bool})
conflicto_bloqueo  (practica_id, contraparte_id, motivo{cliente_retainer|cliente_b2b|empleador|otro}, desde)
auditoria_acceso   (usuario_id, accion, entidad, entidad_id, en, ip)
```
- **Control de conflictos** al aceptar una derivación: si la contraparte del caso está en `conflicto_bloqueo` de la práctica → `rechazada_conflicto`, y al usuario se le ofrecen alternativas (directorio, Defensoría).
- Las empresas con retainer (módulo `juridico` activo) se registran automáticamente como bloqueo `cliente_retainer`.
- Registrar los modelos nuevos con TenantMixin en `tests/test_aislamiento_tenants.py`, `scripts/init_prod_db.py` y `scripts/rls_postgres.sql` (regla dura 5). Los que no llevan TenantMixin, documentados como excepción (regla dura 8).

### 3.5 IA con guardrails (`app/core/ia.py`, envuelve `gemini_service`)
- Plantillas de prompt versionadas por vertical.
- **Minimización**: no se envían datos sensibles (salud, lesiones, datos tributarios identificables) al proveedor sin autorización `sensible=True` y contrato de transmisión vigente; si no, se redacta antes de enviar.
- La salida nunca agrega citas: el redactor recibe `citas_ids` de la biblioteca y solo puede referirlas.
- Cada llamada registra modelo, versión de prompt, fecha y hash de la salida.
- Revisión humana obligatoria antes de que algo llegue al usuario como "recomendación".

### 3.6 Pagos y facturación (`app/core/pagos.py`)
- Wompi para suscripciones B2B, compras únicas B2C y suscripciones B2C.
- Aceptación expresa de inicio inmediato (excepción al retracto, art. 47 Ley 1480) guardada con texto y fecha.
- Cancelación de suscripción en un clic.
- Factura electrónica de la S.A.S. vía proveedor (ver `empresa/02-dian-y-facturacion/`). **Los honorarios del abogado nunca pasan por la pasarela de la S.A.S.**

### 3.7 Notificaciones
Unificar `app/utils/notificaciones.py` y `app/services/notificaciones.py` (deuda conocida) en `app/core/notificaciones/` con canales correo (SendGrid), WhatsApp (Meta Cloud API; reutilizar ideas de `firma_app/app/services/whatsapp_service.py`) e in-app. Alertas de plazos 7/3/1 días.

## 4. Lo que se reutiliza de otras carteras (y lo que no)
| Pieza | Origen | Decisión |
|---|---|---|
| Vigilancia de procesos | `Apis/radar_judicial` | Consumir por HTTP (consulta a demanda o buzón Ley 2213). Nunca monitoreo automático por robot |
| WhatsApp, agenda, CRM de prospectos | `firma_app` | Portar ideas y servicios revisados a la consola del abogado |
| `judicial_scraper.py` (Selenium para saltar WAF/CAPTCHA) | `firma_app` | **No portar.** Incompatible con ADR-P6 |
| Matriz legal viva | `sst-project-v2` | Se generaliza en `biblioteca_juridica` + `regla_plazo` |

## 5. Seguridad y cumplimiento por defecto
- Datos sensibles cifrados en reposo (campo o archivo) y acceso auditado.
- Archivos a Cloudflare R2 con prefijo por tenant (roadmap R2 del dossier).
- Estudio de impacto de privacidad antes de lanzar tutelas de salud y accidentes (Circular SIC 002/2024).
- Retención mínima: borrar datos de casos cerrados según la política publicada.
- Tests: aislamiento entre tenants (incluidas cuentas personales), derivación sin autorización = 403, conflicto bloquea, plazos con casos de festivos.
