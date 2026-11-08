---
cartera: sst-project-v2
nombre: SST — Justrabajo
tipo: producto
estado: construyendo
prioridad: P1
entidad: Cumplia/Justrabajo S.A.S.
puntaje:
siguiente_paso: Brian revisa los PR de ui/rediseno-panel (tema claro) y feat/E15-cumplimiento (SARLAFT/PTEE/datos), verifica las normas del catálogo de cumplimiento (E15.1) y decide D-C1 precio; luego Code hace UI-3 consola del consultor y E0 cobro con Wompi
actualizado: 2026-11-08
---

# CONTEXTO — sst-project-v2 (Justrabajo / SST Smart / Cumplia)

> Documento único de contexto. Corte: **12-oct-2026**. Para retomar el proyecto
> (o pasárselo a otra persona o a otra IA) sin releer los ~180 archivos.
> Fuentes de detalle entre `backticks`.

---

## 1. Qué es, en una frase

SaaS Flask de gestión del **SG-SST** (Decreto 1072/2015, Res. 0312/2019) para
pymes colombianas, vendido **por módulos y por empresa**, con un diferenciador
que la competencia no puede copiar: **el componente jurídico** (Brian es abogado)
y una matriz legal viva con las derogatorias 2022-2026 ya resueltas.

**Meta del dueño:** ingreso medio mensual ≥ **$30M COP en 18-24 meses**, operando
solo y con empleo de tiempo completo (presupuesto de arranque < $1M).

### Nombres — ojo, hay tres
| Nombre | Dónde aparece | Estado |
|---|---|---|
| **SST Smart** | repo GitHub (`sstsmart`), `docs/`, README | Nombre histórico. Descartado para material nuevo (encierra la empresa en el segmento que las ARL regalan). |
| **Justrabajo** | código actual (landing, `CLAUDE.md`, `justrabajo.onrender.com`) | Marca del producto tras el rebrand (commit `6b1c103`). |
| **Cumplia S.A.S.** | `empresa/` (marca paraguas + submarcas SST/PESV/SAGRILAFT/Legal) | **Propuesta**, pendiente verificar homonimia en RUES. |

➡ **Decisión pendiente:** unificar Justrabajo vs. Cumplia antes de constituir la SAS y registrar dominio.

---

## 2. Mapa del repositorio

```
sst-project-v2/
├── app/            Código Flask (monolito modular) — ver §3
├── scripts/        init_prod_db.py, seed_matriz_legal.py, modelo_financiero.py, rls_postgres.sql, legacy/ (NO importar)
├── tests/          5 archivos, 46 tests (aislamiento tenants, autoevaluación, jurídico, seguridad, sgsst/epp)
├── docs/           Dossier de negocio: 23 docs, ~44k palabras (30-ago-2026) — §5
├── empresa/        Ruta ejecutable para constituir la SAS y salir a vender — §6
├── libro/          Tratado de SST y Responsabilidad Patronal, 2.344 págs — §7  (⚠ sin versionar en git)
├── migrations/     Alembic DESACTUALIZADO (no usar todavía)
├── instance/sst.db SQLite de desarrollo
├── render.yaml     Blueprint Render (web starter + Postgres 16, Virginia)
├── CLAUDE.md       Reglas para agentes de IA (leer siempre)
└── CONTEXTO.md     Este archivo
```

---

## 3. Producto (estado técnico)

### Stack
Python · Flask 3 · SQLAlchemy · Flask-Login/JWT · Flask-WTF (CSRF) · Flask-Limiter ·
APScheduler · ReportLab · SendGrid · Gemini (IA) · Tailwind/Jinja2 · Postgres 16 en prod,
**SQLite en dev**. Deploy en **Render** (Virginia) con `preDeploy = scripts/init_prod_db.py`.
CI en `.github/workflows/ci.yml`.

### Módulos comerciales (catálogo en `app/data/modulos.py`)
| Código | Módulo | Precio lista/mes |
|---|---|---:|
| `sgsst` | Política SST + plan anual + indicadores art. 30 | $130.000 |
| `epp` | Kardex EPP y dotación (4 deberes, SL854-2023) | $100.000 |
| `autoevaluacion` | Autoevaluación Res. 0312 (7/21/60) + export SGRL | $150.000 |
| `reportes` | Condiciones inseguras con foto, SLA, escalamiento | $120.000 |
| `matriz_legal` | Matriz legal viva con valoración jurídica | $150.000 |
| `controles` | Ciclo de vida de controles y riesgos | $120.000 |
| `formacion` | Cursos, exámenes, certificados, ranking | $100.000 |
| `juridico` | Consultas con abogado, SLA, conceptos PDF | $200.000 |
| `ia` | Análisis de fotos + experto SST (Gemini) | $80.000 |
| `cumplimiento` | SARLAFT transporte, PTEE, SAGRILAFT y datos personales (8-nov-2026) | $180.000 (propuesta, D-C1) |
| `crm_legal` | CRM Legal con vigilancia (vertical `/legal`) | $49.900 |

Descuento por volumen: 3-4 módulos −10% · 5-7 −15% · 8+ −20%.
Contratación por empresa en `EmpresaModulo` (precio pactado opcional); gating por blueprint en `app/modulos.py`.
Landing pública con **simulador de multas** (D.1072 cap. 2.2.4.11 + art. 216 CST) como lead magnet.

> ⚠ Este pricing por módulo **difiere** del pricing por planes del dossier
> (Esencial $149k · Profesional $349k · Corporativo $749k · Canal $590k). Hay que decidir cuál se publica.

### Lo ya implementado
- **Multi-tenancy aplicativa** (`app/tenancy.py`): `TenantMixin`, filtro automático por `empresa_id`, validación en flush, middleware por request. Test de completitud que truena si un modelo nuevo no está cubierto.
- **Seguridad:** CSRF global, rate limiting en login, cabeceras, `/healthz`, ProxyFix en Render.
- **Autoevaluación 0312:** 60 ítems con pesos (suman 100) en `app/data/estandares_0312.py`; régimen automático con `Empresa.calcular_regimen()`; **art. 3 num. 8**: unidad agropecuaria ≤10 trab. riesgo I-III → 21 estándares (`Empresa.unidad_agropecuaria`).
- **Matriz legal 2026** actualizada (`scripts/seed_matriz_legal.py`, idempotente) — fuente de verdad normativa del repo.
- **Rediseño visual v2 (7-nov-2026, rama `ui/rediseno-panel`, UI-0 a UI-2):** tema claro con colores de seguridad NTC 1461 y Barlow; layout con barra lateral y drawer móvil (`base.html`); panel "Así va tu SG-SST" con medidor de la autoevaluación, escala de niveles, franja de cifras y "Lo que vence pronto" (`app/services/panel.py`, `app/services/vencimientos.py`, `app/data/hitos_normativos.py`); 75 plantillas migradas; `admin/base.html` unificado con pestañas. QA: `rediseno-ui/qa_rutas.py` (86 rutas GET, 0 fallos), capturas en `rediseno-ui/capturas-qa/`, `tests/test_panel.py`. Detalle en `rediseno-ui/README.md` (bloque "Estado de ejecución").
- **Módulo de cumplimiento (8-nov-2026, rama `feat/E15-cumplimiento`):** SARLAFT transporte (completo o RMS), PTEE, SAGRILAFT y datos personales/RNBD como programas habilitables por empresa dentro del módulo `cumplimiento`: requisitos por etapa con evidencia y revisión periódica, oficial de cumplimiento con SIREL, matriz de riesgos (inherente/residual), contrapartes con debida diligencia (lista ONU automática opcional, consulta manual registrada, bloqueo ante coincidencia), reportes con fecha límite y diagnóstico "¿me aplica?" con umbrales parametrizados. Todas las normas y fechas nacen `[VERIFICAR]`. Ficha en `plataforma/02-verticales/09-cumplimiento.md`.

### Reglas duras (no romper)
1. Roles: **siempre** `current_user.tiene_rol(...)` + constantes de `app/constants.py`.
2. Secretos **solo** por variables de entorno (`app/config.py`).
3. Nada se importa de `scripts/legacy/`.
4. Dos servicios de notificación con nombres casi idénticos: `app/utils/notificaciones.py → NotificationService` vs `app/services/notificaciones.py → NotificacionService`.
5. Modelo de dominio nuevo → `TenantMixin` + registrarlo en `tests/test_aislamiento_tenants.py`, `scripts/init_prod_db.py` (backfill) y `scripts/rls_postgres.sql`.
6. Columna nueva en tabla existente → mini-migración aditiva en `scripts/init_prod_db.py` (hasta formalizar Alembic).
7. Blueprint comercial nuevo → entrada en el catálogo de módulos.
8. Modelos de **aliados** NO llevan `TenantMixin` (cruzan tenants por definición).

### Comandos (Windows)
```bash
venv/Scripts/python.exe run.py                                  # local :5000 (admin@sst.local / admin123)
SCHEDULER_ENABLED=0 venv/Scripts/python.exe -c "from app import create_app; create_app('development')"
venv/Scripts/python.exe -m pytest tests/ -q
venv/Scripts/python.exe scripts/seed_matriz_legal.py
python scripts/modelo_financiero.py --esc                       # 3 escenarios financieros
```

### Deuda técnica y bloqueadores abiertos
| # | Pendiente | Por qué importa |
|---|---|---|
| 1 | **Facturación/suscripciones (Wompi) + onboarding autoservicio** | Sin esto no se puede cobrar (bloqueador B4). |
| 2 | Postgres en desarrollo + **Alembic formal** + `empresa_id NOT NULL` | RLS no existe en SQLite. |
| 3 | **Aplicar RLS** (`scripts/rls_postgres.sql`): `FORCE`, roles `app_owner`/`app_user`, `set_config(..., true)` | Hoy el aislamiento es solo aplicativo. |
| 4 | Archivos a **Cloudflare R2** (no disco de Render) | El disco rompe zero-downtime y escalado. |
| 5 | Unificar los dos servicios de notificación | Fuente garantizada de bugs. |
| 6 | `Empleado` y tablas de matriz de riesgos semi-huérfanas | Limpieza de modelo. |
| 7 | `render.yaml` con `autoDeployTrigger: commit` → pasar a `checksPass` | El PAT no tenía scope `workflow`. Verificar que el PAT fue **revocado** (el remoto ya no lo trae en la URL) y migrar a SSH. |
| 8 | Versionar `libro/` (hoy untracked) o excluirlo con `.gitignore` | Son PDFs/DOCX pesados; decidir. |

### Roadmap siguiente (`docs/02-producto/02-roadmap-24-meses.md`)
1. Postgres dev + Alembic + RLS activo
2. Facturación (Wompi) + onboarding + página de precios con checkout
3. **Consola de consultor** multiempresa + propagación normativa (canal #1)
4. FURAT/FUREL · COPASST y Convivencia (Res. 3461/2025) · PWA de captura en campo
5. **Módulo PESV** (Res. 40595/2022 + Circular 0034/2026)

---

## 4. Normatividad clave (estado 2026)

- **Derogadas:** Res. 2404/2019 → **2764/2022** (psicosocial) · Res. 2346/2007 y 1918/2009 → **1843/2025** (exámenes médicos) · Res. 652 y 1356/2012 → **3461/2025** (convivencia) · RETIE 90708/2013 → **40117/2024**.
- **Nuevas:** Ley 2452/2025 (nuevo CPTSS, vigente abr-2026) · Ley 2466/2025 (reforma laboral) · Ley 2477/2025 · Decreto 1040/2026 (acoso laboral) · jornada 42 h desde 15-jul-2026.
- **Multas SG-SST en UVT** (Dec. 2642/2022), no en SMMLV — casi todo el material del sector lo dice mal.
- Autoevaluación 0312 se registra **anualmente en la plataforma SGRL** (plazo 31-jul; Circ. 027/2026).
- PESV: reporte anual también para **no transportadoras** (Circ. 0034/2026, ventana 6-31 enero).

---

## 5. Negocio (`docs/`)

Índice: `docs/README.md` · resumen: `docs/00-resumen-ejecutivo.md`. Datos marcados `[NE]` = no verificados, **no usar en material comercial**.

- **Mercado:** 1,23M empresas afiliadas al SGRL; ~260k obligadas a 21/60 estándares.
- **Competidor real en microempresa:** las ARL regalan software (ALISSTA, Colmena, Ridsso, Guardián) → **no competir en 7 estándares**.
- **Huecos explotables:** matriz legal viva · autoevaluación 0312 exportable a SGRL · **PESV** (nadie lo tiene completo) · canal de consultores multiempresa · precio público (solo 5 de ~25 lo publican).
- **Segmentos:** pymes 10-200 empleados · consultores SST (mejor CAC/LTV) · transporte/flotas (PESV).
- **Ventanas comerciales:** **6-31 enero** (PESV) y **mayo-julio** (autoevaluación SGRL).
- **Modelo financiero (base):** ingreso del mes cruza $30M en el **mes 20**; MRR cruza $30M en el mes 24-25 (64 cuentas, ARPA ~$461k). Ojo: $30M de ingreso ≈ $9M de utilidad.
- **Arquitectura decidida (ADR-1 a 7):** shared-table + RLS; región Virginia (irreversible); R2 para archivos; índices compuestos empiezan por `empresa_id`.

---

## 6. Empresa (`empresa/`) — reemplaza operativamente a `docs/04-empresa/`

Ruta completa: `empresa/00-GUIA-PASO-A-PASO.md`.

- **Una sola S.A.S.** (no dos). Jurídico como persona natural con TP; segunda sociedad cuando el retainer jurídico > $3M/mes sostenido.
- **CIIU 6201** principal + 6311, 7020, 6202. **Sin 6910**.
- Capital suscrito $5M (autorizado $50M). Constitución CCB ≈ **$182.765** ($219.075 con libros y certificado).
- **IVA:** responsable, facturar con **19%** (se descarta exclusión art. 476 num. 21 ET). **Régimen ordinario**, no Simple.
- Facturación con la **solución gratuita de la DIAN** al inicio. **RUB** obligatorio.
- Registro de marca SIC aplazado hasta 10 clientes pagos (mitigación: DNDA + dominio + evidencia de uso).
- **Programa de aliados:** 20% de lo pagado sin IVA × 12 meses, 10% de por vida, 25% al llegar a 10 clientes. Naturaleza: **corretaje** (art. 1340 C.Co), cuidando no caer en agencia (art. 1317).
- Documentos listos: estatutos, actas, T&C, política de datos, avisos, cesión de derechos/NDA, registro DNDA, contrato de referidos, kit de marca (23 piezas; `generar-piezas.py` las regenera si cambia el nombre), plan de lanzamiento 8 semanas (Facebook, LinkedIn, YouTube).

### Errores jurídicos ya corregidos — no reintroducir
1. Causal de disolución por pérdidas **derogada** (Ley 2069/2020 art. 4 → negocio en marcha).
2. Accionista único: **parágrafo art. 17 Ley 1258**; revisor fiscal: par. 2 art. 13 Ley 43/1990.
3. Ley 1915/2018: la presunción de cesión **sí** cubre contratos de prestación de servicios.
4. Decisión Andina 351 art. 31: cesión solo por modalidades **expresamente enumeradas**.
5. "No factures hasta que te paguen" es falso: cobrar por anticipado, no aplazar la factura.
6. Riesgo de **agencia comercial** en el contrato de aliados.
7. Falta del **RUB** (Res. DIAN 000164/2021).
8. SAGRILAFT: completo desde **40.000 SMMLV**; medidas mínimas desde 30.000.
9. DUR tributario = **Decreto 1625/2016** (el 1080/2015 es Cultura).
10. Autorretención especial (resp. 59): verificar, no asumir que no aplica.

---

## 7. El tratado (`libro/`)

*Tratado de SST y Responsabilidad Patronal en Colombia* (1-sep-2026): **2.344 págs, ~1,02M palabras**, 120 capítulos + 10 anexos (A-J), en PDF, DOCX y Markdown (`libro/manuscrito/`).
- **Parte VII (caps. 47-64):** responsabilidad patronal — art. 216 CST, culpa, prueba, nexo, liquidación del daño con fórmulas.
- **Marcas `[VERIFICAR]`** (≈1.200-1.280) inventariadas en el **Anexo J**: se cierran consultando la fuente, nunca borrándolas.
- Taller replicable en `libro/_taller/` (convenciones, encargo, índice maestro, flujo de 6 fases de agentes, `ensamblar.py`).
- Sinergia con el producto: alimenta el módulo jurídico, la matriz legal y el contenido de marketing (autoridad del abogado).

---

## 8. Próximas decisiones y acciones (prioridad)

0. **Rediseño visual:** UI-0 a UI-2 **hechos** el 7-nov-2026 en la rama `ui/rediseno-panel` (PR abierto; fusionarlo despliega el tema claro en producción). Falta **UI-3** (consola del consultor multiempresa, §6 de `rediseno-ui/README.md`) y las decisiones D-UI1, D-UI4 y D-UI5 de §11 (nombre en pantalla, textos de cada nivel frente al art. 28, enlace de Ayuda). Propuestas de Claude pendientes de confirmar: Tailwind por CDN con tokens (en vez del binario standalone) y QA de rutas con el cliente de Flask (en vez de Playwright).

0bis. **Cumplimiento (E15):** MVP hecho el 8-nov-2026 (PR de `feat/E15-cumplimiento`, apilado sobre `ui/rediseno-panel`). Brian: verificar normas y fechas del catálogo (E15.1: Res. 2328/2025, 4607/2026, Circular 20265330000054/2026, Res. 14673/2025 y 7038/2026, RNBD), decidir D-C1 precio ($180.000/mes propuesto), D-C3 red de oficiales externos y D-C4 cobro de cartera (vertical propia o dentro del CRM Legal). Ver `plataforma/02-verticales/09-cumplimiento.md` §4-6.
1. **Elegir nombre definitivo** (Justrabajo vs. Cumplia) → verificar RUES y dominio → constituir la SAS.
2. **Elegir pricing público** (por módulos del código vs. planes del dossier).
3. Implementar **cobro** (Wompi + factura DIAN) — sin esto no hay MRR.
4. Postgres dev → Alembic → RLS activo.
5. Cerrar 3 clientes piloto con descuento de fundador antes de la ventana **ene-2027 (PESV)**; preparar campaña mayo-jul 2027 (autoevaluación).
6. Confirmar revocación del PAT de GitHub, pasar a SSH y CI a `checksPass`.
7. Decidir si `libro/` entra al repo.

---

## 8bis. Visión de plataforma (14-oct-2026)

Brian redefinió el negocio en **dos entidades**:
- **S.A.S. de apps de nicho a gran escala** (software): SST y PESV (B2B) y verticales B2C como peticiones y tutelas, impuestos, accidentes de tránsito y otras.
- **Práctica jurídica de Brian como abogado persona natural** (con su tarjeta profesional, marca Galeano y Asociados), que representa a quien lo necesite.

Este repo pasa a ser la **base de la plataforma**. El análisis completo, para que Claude Code lo ejecute, está en **`plataforma/`**:
tesis y decisiones D1-D8 · estructura legal (Ley 1123/2007, derivación lícita, conflictos de interés) · una ficha por vertical · priorización · arquitectura (núcleo + verticales, ADR-P1 a P7) · modelo financiero (`plataforma/modelo/modelo_plataforma.py`) · backlog E0-E12 · riesgos y pendientes `[VERIFICAR]`.

Hallazgos que cambian el plan:
1. La práctica de Brian solo, con 60 h/mes, se estanca en ~$8-9M/mes; la escala viene de la S.A.S.
2. Conflicto de interés entre los clientes del retainer (empleadores) y las verticales laboral y tránsito: hace falta un control de conflictos.
3. La derivación app → abogado debe ser opcional, revelada y sin comisión (Ley 1123 art. 30 nums. 5 y 7).

## 9. Para agentes de IA que trabajen aquí
- Leer **`CLAUDE.md`** antes de tocar código; respetar §3 "Reglas duras".
- Antes de estrategia/precio/roadmap: leer el doc correspondiente en `docs/`.
- Antes de cualquier documento societario, contractual o tributario: revisar los 10 errores de §6.
- Antes de contenido jurídico sobre SST/culpa patronal: leer el capítulo en `libro/manuscrito/` y el Anexo J.
- Verificación mínima tras cambios: boot + `pytest tests/ -q`.
- Para trabajo de plataforma (verticales nuevas, núcleo, derivación): `plataforma/06-backlog-claude-code.md`.

## 10. Bitácora
- 2026-11-08: módulo **cumplimiento** (SARLAFT transporte, PTEE, SAGRILAFT, datos personales) construido en `feat/E15-cumplimiento` a partir de la pauta de Doctux que vio Brian: catálogo con 43 requisitos y umbrales parametrizados, 5 tablas tenant `cumpl_*`, listas ONU, diagnóstico "¿me aplica?", KPI y vencimientos en el panel, 10 pruebas (128 en total), QA 90 rutas. Precio $180.000/mes es propuesta. Ideas afines (cobro de cartera, canal de denuncias, red de oficiales, reforma laboral) anotadas en `ideas/BANDEJA.md`. Fuentes y pendientes en `plataforma/02-verticales/09-cumplimiento.md`.
- 2026-11-07: vertical **CRM Legal** montada en `/legal` (`app/verticales/crm_legal/`, `app/nucleo/plazos/`, 3 tablas tenant nuevas, módulo `crm_legal` en el catálogo, `Empresa.tipo_cuenta`). Nueva config `testing` (SQLite en memoria) porque las pruebas borraban `instance/sst.db`. 114 pruebas en verde. Detalle en `../crm_legal/CONTEXTO.md`.
- 2026-11-07: rediseño visual UI-0 a UI-2 ejecutado (rama `ui/rediseno-panel`): tokens v2, componentes, panel con medidor, 75 plantillas migradas, `admin/base.html` unificado, QA de 86 rutas y `tests/test_panel.py`. Se corrigieron de paso dos plantillas que nunca existieron (`configuracion/ia.html`, `juridico/normativa.html`) y un filtro inválido en `matriz_legal/detalle.html`. Nota: una sesión paralela (CRM Legal) escribe en este mismo árbol (`app/verticales/`, `app/nucleo/`); el commit del rediseño incluye solo sus propios archivos.
- 2026-10-23: decisión de dos cajas (S.A.S. de tecnología sin servicios jurídicos + práctica legal de Brian). Nuevos `empresa/07-estructura-y-contratos/` y estatutos para dos accionistas (`empresa/01-constitucion/01b-...`).
- 2026-10-23: rediseño v2 (paleta de colores de seguridad NTC 1461, Barlow, sin tarjetas repetidas ni degradados), pedido por Brian para que se vea más profesional.
- 2026-10-23: paquete de rediseño visual en `rediseno-ui/` (especificación, maqueta HTML, capturas escritorio/celular, referencia). SST queda elegido como una de las dos apps para arrendar sin dejar Vanti.
- 2026-10-14: análisis de plataforma multivertical entregado en `plataforma/` (investigación web con fuentes y revisión independiente).
