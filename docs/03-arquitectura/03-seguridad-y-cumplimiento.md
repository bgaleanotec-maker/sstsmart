# Seguridad y cumplimiento

La plataforma maneja **datos sensibles de salud ocupacional** (exámenes médicos, incapacidades, restricciones). Eso cambia el nivel de exigencia: no es un CRM.

---

## 1. Checklist de seguridad — en orden de urgencia

### 1.1 Bloqueantes (antes de vender)

| # | Control | Cómo | Estado hoy |
|---|---|---|---|
| **S1** | **CSRF** | `Flask-WTF` con `CSRFProtect(app)` global y token en cada POST | **Ausente.** Los formularios son POST simples: vulnerables por diseño. Es el primer hallazgo de cualquier pentest |
| **S2** | **Headers de seguridad** | `Flask-Talisman`: HSTS, CSP, `X-Content-Type-Options`, `Referrer-Policy`; cookies `Secure` + `HttpOnly` + `SameSite=Lax`. Empieza la CSP en `report-only` | Ausente |
| **S3** | **Rate limiting** | `Flask-Limiter` con backend en **Render Key Value**, no en memoria (o se pierde al escalar). Límites agresivos en login, recuperación de contraseña y **endpoints de IA, que cuestan dinero real por request** | Ausente |
| **S4** | **Contraseñas** | Argon2id (`argon2-cffi`), mínimo 12 caracteres, verificación contra listas de contraseñas filtradas, **sin expiración forzada** (NIST SP 800-63B) | Revisar |
| **S5** | **Aislamiento entre tenants** | RLS + tests automáticos por modelo. Ver [`01-arquitectura-saas-multitenant.md`](01-arquitectura-saas-multitenant.md) | En roadmap T1 |

### 1.2 Datos sensibles de salud

| # | Control | Detalle |
|---|---|---|
| **S6** | **Cifrado a nivel de columna** | Para diagnósticos, restricciones médicas y resultados de exámenes. Clave en variable de entorno **distinta de `SECRET_KEY`**. El cifrado de disco de Render cubre el resto |
| **S7** | **Separación aptitud / diagnóstico** | El empleador ve el **concepto de aptitud** (apto / apto con restricciones / no apto). **No ve el diagnóstico clínico.** Es una regla de modelo de datos, no de interfaz |
| **S8** | **Log forense de accesos** | Tabla append-only `auditoria(empresa_id, usuario_id, accion, entidad, entidad_id, ip, user_agent, ts)`, **sin UPDATE ni DELETE concedidos a `app_user`**. Los compradores B2B preguntan *"¿quién vio el examen médico de este empleado y cuándo?"* y hay que poder responder |
| **S9** | **2FA TOTP obligatorio** | Para `Admin`, `Responsable_SST` y `Abogado`. No opcional |
| **S10** | **Autorización de datos sensibles capturada y auditable** | El tratamiento de datos sensibles exige autorización **explícita**, informando al titular que **no está obligado a otorgarla**. El producto debe capturarla y almacenarla, no darla por supuesta |

### 1.3 Operación

| # | Control | Detalle |
|---|---|---|
| **S11** | **Backups fuera de Render** | El PITR de 7 días **no es un plan de recuperación**: cubre corrupción, no la pérdida de la cuenta. Cron semanal con `pg_dump` cifrado hacia R2, en cuenta distinta. **El rol de backup necesita `BYPASSRLS` o exportarás tablas vacías** |
| **S12** | **DRP probado** | RTO y RPO documentados, y **restauración probada trimestralmente**. Un backup no probado no es un backup |
| **S13** | **Dependencias** | Dependabot + `pip-audit` en CI |
| **S14** | **Secretos** | Solo por env (ya es regla dura del proyecto). En Render: `envVarGroups` + `sync: false`. Rotación documentada |
| **S15** | **Notificación de incidentes** | Procedimiento escrito. La SIC exige reportar incidentes de seguridad **dentro de 15 días hábiles** desde la detección (para quienes están en el RNBD), y los contratos B2B lo exigen siempre |

---

## 2. Lo que pide un comprador B2B colombiano

Ten esto listo **antes** de la primera venta a una empresa de más de 50 trabajadores:

| Documento | Por qué lo piden |
|---|---|
| **Contrato de transmisión / tratamiento de datos (DPA)** donde ellos son responsable y tú encargado | Obligatorio por el art. 25 del Decreto 1377/2013. Sin él, ambos quedan expuestos |
| **Política de Tratamiento de Datos Personales** publicada, con procedimiento de consultas y reclamos | Ley 1581/2012 |
| **Declaración de transferencia internacional** | Render aloja en EE.UU. |
| Evidencia de la **autorización para datos sensibles** que captura el producto | Régimen reforzado de datos de salud |
| Cuestionario de seguridad, matriz de roles, evidencia de backups, plan de continuidad | Práctica de mercado |
| **SLA de disponibilidad** | Sé conservador: no prometas 99,9% si corres en un solo servicio de Render |
| Cláusula de notificación de incidentes | Práctica de mercado |
| Registro en el RNBD, **si aplica** | Solo si tus activos superan 100.000 UVT ($5.237.400.000). Casi seguro **no aplica** |

Sanciones de la SIC: hasta **2.000 SMMLV = $3.501.810.000** (2026), más suspensión o cierre de las operaciones de tratamiento. Es el argumento que el comprador usará para exigirte garantías contractuales — y es real.

> **Novedad regulatoria a vigilar:** hay presión creciente sobre **decisiones automatizadas por IA**, exigiendo transparencia, revisión humana y garantías antidiscriminación. Si el módulo de IA sugiere clasificaciones de riesgo o recomendaciones que afecten a un trabajador, **documenta que hay revisión humana y que la IA no decide sola**.

---

## 3. Trust Center antes que SOC 2

### 3.1 Cuánto cuesta certificarse

| Concepto | Costo |
|---|---|
| SOC 2 Type I completo (startup) | USD 45.000 – 65.000, 10–14 semanas |
| SOC 2 Type II recurrente | USD 40.000 – 80.000/año |
| Solo la auditoría Type II | USD 5.000 – 20.000/año |
| Pentest anual | USD 5.000 – 15.000 |
| Vanta | desde ~USD 10.000/año (Plus 15–30k, Scale hasta 80k) |
| Drata / Secureframe | desde ~USD 7.500/año |
| Costos ocultos (MDM, SSO, gestor de contraseñas) | USD 5.000 – 15.000/año |

### 3.2 El veredicto

**No lo hagas todavía.** SOC 2 tiene sentido cuando estés perdiendo contratos concretos por no tenerlo — típicamente al vender a empresas grandes o multinacionales. Y para pymes colombianas, **ISO 27001 tiene mejor reconocimiento local**: SOC 2 es un estándar fundamentalmente estadounidense y muchos compradores colombianos ni lo conocen.

**Construye en cambio un Trust Center público** — una página con:

- Política de tratamiento de datos personales
- Arquitectura de seguridad (cifrado, aislamiento, control de acceso)
- **Lista de subprocesadores**: Render (EE.UU.), Cloudflare, Google/Anthropic (IA), Resend, Sentry
- Ubicación de los datos y base legal de la transferencia internacional
- Política de backups, RTO/RPO
- Proceso de respuesta a incidentes y canal de reporte
- Certificaciones de los proveedores (Render: ISO 27001, SOC 2 Type 2, EU-US DPF)

**Cubre el 80% de la due diligence de una pyme colombiana por una fracción del costo**, y toda esa documentación se reutiliza el día que sí contrates una plataforma de compliance.

---

## 4. Un cuestionario de auto-verificación

Antes de cada release importante, responde estas ocho preguntas. Si alguna falla, no se despliega.

1. ¿Todos los modelos nuevos tienen `empresa_id` NOT NULL, FK, índice y política RLS?
2. ¿El test de aislamiento entre tenants pasa para **todos** los modelos, incluidos los nuevos?
3. ¿Algún endpoint nuevo devuelve datos sin filtro de tenant?
4. ¿Se agregó algún campo que contenga diagnóstico clínico sin cifrado de columna?
5. ¿Alguna consulta nueva a un LLM envía datos personales identificables?
6. ¿Los formularios nuevos tienen token CSRF?
7. ¿Se agregó algún secreto que no esté en `envVarGroups` con `sync: false`?
8. ¿El último backup se restauró con éxito en los últimos 90 días?

## Fuentes

[SOC 2 Cost 2026 — Cavanex](https://cavanex.com/blog/soc-2-compliance-cost-2026) · [Vanta pricing — Secureleap](https://www.secureleap.tech/blog/vanta-review-pricing-top-alternatives-for-compliance-automation) · [Habeas Data Ley 1581 — RuleX](https://rulex.org/blog/habeas-data-ley-1581-colombia-2026-guia-empresas) · [SIC — Registro Nacional de Bases de Datos](https://www.sic.gov.co/registro-nacional-de-bases-de-datos) · [SIC — Datos sensibles de salud](https://www.sic.gov.co/boletin-juridico-abril-2017/tratamiento-de-los-datos-sensibles-en-casos-relativos-a-la-salud) · [Render Security](https://render.com/security) · [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html)
