# SST Smart — Plataforma SaaS de Gestión SG-SST (Colombia)

Software de gestión del Sistema de Gestión de Seguridad y Salud en el Trabajo
para pymes colombianas, alineado con el Decreto 1072/2015 y la Resolución
0312/2019 (estándares mínimos).

## Módulos

| Módulo | Blueprint | Qué hace |
|---|---|---|
| **Autoevaluación 0312** | `/autoevaluacion` | Régimen automático (7/21/60 estándares), diligenciamiento ítem por ítem, puntaje y valoración (art. 28), plan de mejoramiento derivado, export CSV para el registro en SGRL |
| Reportes | `/reportes` | Condiciones inseguras con foto, asignación automática al gestor según matriz de riesgos, SLA y escalamiento |
| Controles | `/controles` | Ciclo de vida de controles (planificado → implementado → verificado → efectivo), jerarquía de controles, seguimientos periódicos |
| Matriz Legal | `/matriz-legal` | Requisitos legales SST, valoración jurídica (probabilidad × impacto), evidencias versionadas, log forense |
| Jurídico | `/juridico` | Consultas jurídicas con SLA por prioridad, asignación a abogado, conceptos y PDF |
| Formación | `/formacion` | Catálogo de cursos estilo Netflix, exámenes, certificados, ranking SST |
| Admin | `/admin` | Usuarios, catálogos (dependencias, tipos), matriz probabilidad×severidad, reglas de escalamiento, gestión de cursos |
| IA | `/ia` | Chat experto SST y análisis de imágenes con Gemini |

## Arquitectura (monolito modular)

```
app/
├── config.py        # Configuración por entorno (secretos SOLO en env)
├── constants.py     # Roles canónicos y grupos de permiso (único punto de verdad)
├── models/          # SQLAlchemy, un archivo por dominio
├── routes/          # Blueprints (controladores delgados)
├── services/        # Lógica de negocio (gestión de reportes, notificaciones, Gemini)
├── tasks/           # Scheduler APScheduler (escalamiento automático)
├── utils/           # Notificaciones in-app + email
└── templates/       # Jinja2 (Tailwind)
scripts/
├── seed_matriz_legal.py   # Matriz legal SST Colombia actualizada (2026)
└── legacy/                # Código retirado y scripts ad-hoc históricos
```

Reglas del proyecto:
- **Roles**: nunca comparar `current_user.rol == '...'` a mano; usar
  `current_user.tiene_rol(...)` con las constantes de `app/constants.py`
  (normaliza variantes históricas como `Responsable SST` / `ResponsableSST`).
- **Secretos**: solo variables de entorno (ver `.env.example`). Nada de keys
  en el código.
- **Migraciones**: en desarrollo `db.create_all()`; en producción usar
  `flask db upgrade` (Flask-Migrate).

## Puesta en marcha

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env          # completar keys
python run.py                   # crea admin@sst.local / admin123
python scripts/seed_matriz_legal.py
```

## Normatividad incorporada (verificada ago-2026)

Núcleo: Ley 1562/2012 · Decreto 1072/2015 (cap. 2.2.4.6 y multas 2.2.4.11) ·
Res. 0312/2019 (7/21/60 estándares + autoevaluación anual en plataforma SGRL,
Circulares 009/2025 y 027/2026).

Cambios recientes que la matriz ya refleja:
- Psicosocial: **Res. 2764/2022** (derogó la 2404/2019)
- Exámenes médicos: **Res. 1843/2025** (derogó la 2346/2007)
- Comités de convivencia: **Res. 3461/2025** (derogó 652 y 1356 de 2012)
- Reforma laboral **Ley 2466/2025** y jornada 42 h desde 15-jul-2026 (Ley 2101/2021)
- Acoso sexual laboral: Ley 2365/2024 · Desconexión: Ley 2191/2022

Detalle completo y fuentes: `scripts/seed_matriz_legal.py`.

## Seguridad y multi-tenancy (implementado)

- **CSRF** global (Flask-WTF) — el token se inyecta a los formularios y a los
  `fetch` desde las plantillas base. **Rate limiting** en login/token.
  Cabeceras de seguridad y `/healthz`.
- **Multi-tenancy aplicativa** (`app/tenancy.py`, ~150 líneas propias, ADR-2):
  modelo `Empresa`, `empresa_id` con FK+índice en 12 modelos de dominio,
  filtro automático por tenant en cada SELECT (`with_loader_criteria`),
  asignación/validación en cada flush, y middleware que resuelve el tenant
  por request (reset de ContextVar SIEMPRE — sin herencias entre requests).
  Tests de aislamiento parametrizados por modelo + test de completitud que
  truena si un modelo tenant nuevo no está cubierto.
- **RLS en Postgres**: políticas listas en `scripts/rls_postgres.sql`
  (aplicar tras el backfill; ver docs/03-arquitectura/01 §2).

## Despliegue (Render)

`render.yaml` (blueprint MVP: web starter + Postgres 16 en Virginia).
`preDeployCommand` ejecuta `scripts/init_prod_db.py` (idempotente: tablas,
empresa 1, admin, backfill de `empresa_id`, matriz legal 2026).
CI en GitHub Actions (boot + 37 tests) con `autoDeployTrigger: checksPass`.

## Roadmap restante (docs/02-producto/02-roadmap-24-meses.md)

1. Postgres también en desarrollo + migraciones formales (Alembic) + RLS activo.
2. Facturación y suscripciones (Wompi) + onboarding autoservicio.
3. Consola de consultor (multiempresa) + propagación normativa.
4. Indicadores art. 30 · FURAT/FUREL · COPASST y Convivencia (Res. 3461/2025).
5. Módulo PESV (Res. 40595/2022 + Circular 0034/2026).
