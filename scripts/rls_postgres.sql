-- Row Level Security por tenant (docs/03-arquitectura/01 §2).
-- Ejecutar como app_owner en Postgres UNA VEZ tras el backfill de empresa_id.
-- La app debe fijar el tenant por transacción:
--   SELECT set_config('app.empresa_id', '<id>', true);
-- (set_config con true = local a la transacción; NUNCA usar SET sin LOCAL.)
--
-- Roles esperados:
--   app_owner  → migraciones (dueño de tablas; RLS lo cubre gracias a FORCE)
--   app_user   → la aplicación (sin ownership, sin BYPASSRLS)
--   app_backup → pg_dump (CON BYPASSRLS, o los respaldos salen vacíos)

DO $$
DECLARE
  t text;
BEGIN
  FOREACH t IN ARRAY ARRAY[
    'usuarios', 'empleados', 'condiciones_inseguras', 'eventos',
    'riesgo_matriz', 'controles', 'requisitos_legales',
    'consultas_juridicas', 'cursos', 'gestion_reportes',
    'autoevaluaciones', 'acciones_mejora'
  ] LOOP
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', t);
    EXECUTE format('ALTER TABLE %I FORCE ROW LEVEL SECURITY', t);
    EXECUTE format('DROP POLICY IF EXISTS tenant_isolation ON %I', t);
    EXECUTE format($p$
      CREATE POLICY tenant_isolation ON %I FOR ALL
        USING      (empresa_id = current_setting('app.empresa_id', true)::int)
        WITH CHECK (empresa_id = current_setting('app.empresa_id', true)::int)
    $p$, t);
  END LOOP;
END $$;

-- Verificación rápida:
-- SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname='public';
