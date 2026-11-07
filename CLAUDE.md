# Justrabajo — notas para Claude

> **Visión ampliada (oct-2026):** este repo es la base de una **plataforma de apps legales de nicho**
> (SST, PESV, peticiones y tutelas, impuestos, laboral, tránsito…) de una S.A.S. de software, separada de
> la práctica de Brian como abogado persona natural. Antes de construir algo nuevo, leer
> `plataforma/README.md`, `plataforma/04-arquitectura-plataforma.md` (ADR-P1 a P7), las 12 reglas de
> producto de `plataforma/01-estructura-legal-dos-entidades.md` §9 y el backlog
> `plataforma/06-backlog-claude-code.md`. Las decisiones D1-D8 de `plataforma/00-tesis-y-decisiones.md`
> las toma Brian: si una bloquea, preguntar.

App Flask (monolito modular) de gestión SG-SST para pymes colombianas.
Marca: **Justrabajo** (justrabajo.onrender.com). Python del proyecto:
`venv/Scripts/python.exe` (Windows).

## Módulos SaaS (catálogo con precios)
- Catálogo en `app/data/modulos.py` (9 módulos); contratación por empresa en
  `EmpresaModulo` (precio pactado opcional); gating por blueprint en
  `app/modulos.py`. Un blueprint comercial nuevo → entrada en el catálogo.
- Guía estratégica de referencia (30 módulos, jurisprudencia culpa patronal,
  modelo de negocio): `C:\Users\bgale\Downloads\Guia-SST-360deg-Colombia-ampliada.docx.md`.
- Régimen Res. 0312: OJO art. 3 num. 8 — unidad agropecuaria ≤10 trabajadores
  riesgo I-III cumple 21 estándares (campo `Empresa.unidad_agropecuaria`).
- `scripts/init_prod_db.py` tiene una sección de "mini-migraciones aditivas"
  (ALTER TABLE) porque create_all no altera tablas existentes: columna nueva
  en tabla existente → añadirla ahí hasta formalizar Alembic.

## Interfaz (rediseño 23-oct-2026 — leer antes de tocar plantillas)
- Especificación completa en `rediseno-ui/README.md`; la maqueta `rediseno-ui/mockup-panel.html` es la fuente de verdad visual.
- Tema claro v2: colores de seguridad NTC 1461 (azul obligación = marca; rojo, amarillo y verde solo como estado) + grafito; Barlow / Barlow Semi Condensed. Tokens en `rediseno-ui/README.md` §2. Nada de colores sueltos en plantillas. El CRM Legal tiene tema propio (verde botella + latón).
- Componentes Jinja en `app/templates/components/` (medidor, nav_item, kpi, chip, tarjeta). Importarlos `with context`; lo que una macro necesite de Python va como *global* de Jinja en `app/ui.py`, no solo en el context processor.
- Heurísticas de Jakob Nielsen: lo útil primero, cada cifra con su explicación, estados vacíos siempre.
- Estado: UI-0 a UI-2 hechos el 7-nov-2026 (rama `ui/rediseno-panel`); UI-3 pendiente. Plantillas de `admin/` definen `block admin_content` (no `content`). Tema por CDN de Tailwind con tokens inline (deuda: compilar con binario standalone).
- QA de interfaz: `SCHEDULER_ENABLED=0 venv/Scripts/python.exe rediseno-ui/qa_rutas.py` (recorre todas las rutas GET como admin; falla ante 500 o restos del tema oscuro) y `scripts/seed_demo.py` para datos de demostración (solo desarrollo).

## Vertical CRM Legal (23-oct-2026)
- Especificación y backlog en `../crm_legal/README.md` y `../crm_legal/BACKLOG.md` (épicas C0-C7). Va en `app/verticales/crm_legal/`; el motor de plazos en `app/nucleo/plazos/` (portado de `Apis/radar_judicial`).
- Prerrequisito: UI-0 y UI-1 de `rediseno-ui/README.md`.

## Reglas duras
- Roles: usar SIEMPRE `current_user.tiene_rol(...)` + constantes de
  `app/constants.py`. La BD contiene variantes históricas de nombres de rol
  ('Responsable SST', 'ResponsableSST', 'Responsable_SST'); `tiene_rol`
  normaliza. No añadir comparaciones crudas de strings.
- Secretos SOLO por env (`app/config.py`). Nunca incrustar API keys.
- `scripts/legacy/` es código retirado (modelos jurídicos extendidos
  duplicados, servicios nunca conectados, scripts ad-hoc de migración).
  No importar nada desde ahí.
- Hay DOS servicios de notificación activos:
  `app/utils/notificaciones.py` → `NotificationService` (notif. in-app + email)
  `app/services/notificaciones.py` → `NotificacionService` (emails HTML de
  gestión/jurídico). Nombres casi idénticos: cuidado con los imports.

## Verificación
- Boot: `SCHEDULER_ENABLED=0 venv/Scripts/python.exe -c "from app import create_app; create_app('development')"`
- Tests: `venv/Scripts/python.exe -m pytest tests/ -q` (aislamiento, autoevaluación, jurídico, seguridad, sgsst/epp, panel)
- Seed matriz legal: `venv/Scripts/python.exe scripts/seed_matriz_legal.py` (idempotente)

## Normatividad (estado ago-2026)
Res. 2404/2019, Res. 2346/2007 y Res. 652/1356 de 2012 están DEROGADAS
(reemplazos: 2764/2022, 1843/2025, 3461/2025). La autoevaluación de la
Res. 0312/2019 se registra anualmente en la plataforma SGRL del Fondo de
Riesgos Laborales. Fuente de verdad en el repo: `scripts/seed_matriz_legal.py`.

## Multi-tenancy (implementado 2026-08-29 — leer antes de tocar modelos)
- `app/tenancy.py`: TenantMixin + filtro automático por `empresa_id` en SELECTs
  + validación en flush + middleware por request. Un modelo de dominio NUEVO
  debe llevar `TenantMixin` y añadirse a: tests/test_aislamiento_tenants.py
  (MODELOS), scripts/init_prod_db.py (backfill) y scripts/rls_postgres.sql.
  El test de completitud truena si se olvida.
- Sin tenant en contexto (login, scheduler, scripts) NO se filtra — a propósito.
- `empresa_id` es nullable (fase expand); NOT NULL llegará por migración.
- CSRF activo (Flask-WTF): en tests de cliente poner
  `app.config['WTF_CSRF_ENABLED'] = False`. El token se inyecta por JS en
  base.html y admin/base.html; login.html lo trae inline.

## Autoevaluación Res. 0312 (implementado)
- Catálogo de 60 ítems con pesos (suman 100) en `app/data/estandares_0312.py`
  (asserts de integridad al importar). Lógica en
  `app/services/autoevaluacion_service.py`; rutas en `app/routes/autoevaluacion.py`.
- Régimen: `Empresa.calcular_regimen()` (≤10 & riesgo I-III → 7; 11-50 → 21;
  resto o riesgo IV-V → 60). Ítems no exigibles se otorgan con puntaje pleno.

## Despliegue
- `render.yaml` (blueprint: web starter + Postgres 16, Virginia).
  preDeploy = `scripts/init_prod_db.py` (idempotente). CI en
  `.github/workflows/ci.yml`.

## Deuda conocida (no resuelta aún)
- RLS de Postgres escrito (`scripts/rls_postgres.sql`) pero no aplicado; el
  aislamiento hoy es aplicativo. Desarrollo sigue en SQLite.
- Migraciones formales pendientes (migrations/ está desactualizado; el arranque
  usa create_all aditivo).
- `Empleado` y varias tablas de matriz de riesgos siguen semi-huérfanas.
- Facturación/suscripciones no existen (bloqueador B4 del dossier).
