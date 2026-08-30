# SST Smart — notas para Claude

App Flask (monolito modular) de gestión SG-SST para pymes colombianas.
Python del proyecto: `venv/Scripts/python.exe` (Windows).

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
- Tests: `venv/Scripts/python.exe -m pytest tests/ -q` (10 tests jurídico)
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
