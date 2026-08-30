# Arquitectura SaaS multi-tenant — Flask + PostgreSQL

Decisiones de arquitectura para convertir el monolito modular monoempresa en un SaaS que sostenga **50–500 tenants** de tipo pyme.

---

## 1. Decisión: shared-table con `empresa_id` + Row Level Security

### 1.1 Las tres opciones y por qué se descartan dos

| Patrón | Escala real | Ventajas | Por qué NO aquí |
|---|---|---|---|
| **Base de datos por tenant** | <100 | Máximo aislamiento | **Inviable en Render.** Los planes de Postgres hasta 8 GB tienen `max_connections = 100`. Con 200 tenants y pool propio te quedas sin conexiones antes de tener clientes. Además ~8 MB de template por base |
| **Esquema por tenant** | "difícilmente más allá de unos cientos" | Sin filtros en las queries; índices más pequeños | Los catálogos del sistema crecen a millones de filas y **degradan el planner**; y habría que correr Alembic 500 veces por deploy |
| **Tabla compartida con `empresa_id`** | Miles | Una migración para todos; consultas cross-tenant triviales; un solo pool | Hay que filtrar en **cada** query — y un olvido es una fuga de datos. **Por eso se combina con RLS.** |

**Decisión: shared-table + RLS.** El filtro aplicativo es la primera línea; RLS es la red que atrapa el olvido.

El repo ya tiene el gancho: `RiesgoMatriz.empresa_id` existe (aunque sin FK ni índice). El trabajo es propagarlo a las 33 tablas de dominio.

### 1.2 Esquema base

```sql
CREATE TABLE empresas (
  id            SERIAL PRIMARY KEY,
  nit           VARCHAR(20) UNIQUE NOT NULL,
  razon_social  VARCHAR(255) NOT NULL,
  ciiu          VARCHAR(10),
  clase_riesgo  SMALLINT CHECK (clase_riesgo BETWEEN 1 AND 5),
  num_trabajadores INT NOT NULL,
  -- OJO: el Decreto 957/2019 clasifica por INGRESOS; la Res. 0312 por TRABAJADORES.
  -- Se guardan por separado a propósito. No unificar.
  tamano_dec957 VARCHAR(20),
  regimen_estandares SMALLINT,   -- 7 | 21 | 60, derivado
  num_vehiculos INT DEFAULT 0,
  num_conductores INT DEFAULT 0, -- disparadores del upsell PESV
  consultor_id  INT REFERENCES cuentas_canal(id),  -- NULL si es cliente directo
  plan          VARCHAR(30),
  estado        VARCHAR(20),
  creada_en     TIMESTAMPTZ DEFAULT now()
);

-- En cada tabla de dominio:
ALTER TABLE <tabla> ADD COLUMN empresa_id INT NOT NULL REFERENCES empresas(id);
CREATE INDEX ix_<tabla>_empresa ON <tabla>(empresa_id);
```

> **Regla de índices, sin excepción:** **todo índice compuesto empieza por `empresa_id`** — `(empresa_id, fecha DESC)`, `(empresa_id, estado)`. RLS reescribe la query antes de planificar, así que la condición participa en la selección de índices como un `WHERE` normal. Si el índice no empieza por `empresa_id`, no se usa.

---

## 2. Row Level Security — cómo hacerlo bien

### 2.1 Las políticas

```sql
ALTER TABLE riesgo_matriz ENABLE ROW LEVEL SECURITY;
ALTER TABLE riesgo_matriz FORCE  ROW LEVEL SECURITY;   -- crítico: sin esto el owner la ignora

CREATE POLICY tenant_isolation ON riesgo_matriz FOR ALL
  USING      (empresa_id = current_setting('app.empresa_id', true)::int)
  WITH CHECK (empresa_id = current_setting('app.empresa_id', true)::int);
```

### 2.2 Los cinco errores que anulan RLS

Ordenados por frecuencia real en producción:

| # | Error | Consecuencia |
|---|---|---|
| **1** | **`SET` sin `LOCAL`** | El valor persiste en la conexión, y el siguiente request que la reciba del pool **ve los datos del tenant anterior**. Es la causa número uno de fugas |
| **2** | **Conectarse como dueño de la tabla** | El owner ignora RLS por defecto. De ahí `FORCE ROW LEVEL SECURITY` |
| **3** | **`BYPASSRLS` en el rol de la aplicación** | Anula todo. Resérvalo para analítica y soporte |
| **4** | **`current_setting('app.empresa_id')` sin el segundo argumento** | Lanza excepción si falta la clave. Usar siempre la forma de dos argumentos |
| **5** | **Políticas múltiples se combinan con OR, no AND** | Una política permisiva extra abre el acceso |

### 2.3 Dos roles de base de datos

| Rol | Uso | Privilegios |
|---|---|---|
| `app_owner` | Migraciones (Alembic) | Dueño de las tablas. **Solo en `preDeployCommand`** |
| `app_user` | La aplicación | Sin ownership, **sin `BYPASSRLS`**. Es la `DATABASE_URL` de la app |
| `app_backup` | `pg_dump` | **Necesita `BYPASSRLS`** — ver abajo |

> **Verifica esto antes de confiar en tus respaldos:** `pg_dump` y la replicación **respetan RLS**. Si el rol de backup no tiene `BYPASSRLS`, exportarás tablas vacías y no te enterarás hasta el día que necesites restaurar.

### 2.4 Integración con SQLAlchemy

```python
from contextvars import ContextVar
from sqlalchemy import event
from sqlalchemy.orm import Session

current_empresa = ContextVar("current_empresa", default=None)

@event.listens_for(Session, "after_begin")
def _set_tenant(session, transaction, connection):
    eid = current_empresa.get()
    if eid is not None:
        connection.exec_driver_sql(
            "SELECT set_config('app.empresa_id', %s, true)", (str(eid),)
        )   # el tercer argumento `true` = local a la transacción
```

> **Advertencia sobre las guías que vas a encontrar en Google:** varias muestran
> `cursor.execute(f"SET app.current_tenant = {tenant_id}")`.
> Ese código tiene **dos defectos graves**: interpolación por f-string (inyección SQL si `tenant_id` no está validado) y `SET` sin `LOCAL` (el error #1 de arriba). `set_config(..., true)` es el equivalente parametrizable y correcto.

**Complementos necesarios:**

- Un `before_flush` que verifique que ningún objeto nuevo lleve un `empresa_id` distinto al del contexto.
- Un filtro global (`with_loader_criteria`) que inyecte la condición automáticamente, para no depender de que cada consulta la escriba.
- Un middleware que resuelva el tenant desde el subdominio o la sesión y fije el `ContextVar` **antes** de abrir la transacción.

### 2.5 Sobre las librerías

**[NE] No existe un paquete maduro y mantenido en 2026** llamado `sqlalchemy-multi-tenant` o `flask-multitenant`. Existe `flask-rls`, de autor individual y adopción baja.

**Recomendación: escribe ~150 líneas propias y audítalas**, en lugar de depender de un paquete sin comunidad para tu frontera de seguridad. Lo que sí vale la pena construir es la otra pieza:

### 2.6 Tests de aislamiento — la infraestructura que sí importa

```python
# Por CADA modelo del dominio, sin excepciones:
def test_aislamiento(modelo):
    a = crear_empresa("A"); b = crear_empresa("B")
    with tenant(a): registro = crear(modelo)
    with tenant(b):
        assert modelo.query.get(registro.id) is None       # no lo lee
        assert modelo.query.count() == 0                    # no lo cuenta
        with pytest.raises(Exception): actualizar(registro) # no lo escribe
```

Genera este test **automáticamente para los 33 modelos** con una fixture parametrizada. Un modelo nuevo sin `empresa_id` debe romper la suite el día que se crea, no seis meses después en producción.

---

## 3. Migraciones con Alembic

Con shared-table, **una sola migración lineal para todos los tenants**, ejecutada en el `preDeployCommand` de Render.

**Cuatro reglas:**

1. **Versiona las políticas RLS como migraciones** (`op.execute("CREATE POLICY ...")`), con `downgrade` que las elimine. Si no están en Alembic, se pierden al recrear la base.
2. Las migraciones corren como `app_owner`; la app como `app_user`. En Render eso significa **dos `DATABASE_URL` distintas**.
3. **Expand/contract, siempre.** `preDeployCommand` corre antes de conmutar el tráfico, así que la versión vieja del código convive brevemente con el esquema nuevo: añadir columna nullable → desplegar código → backfill → hacer NOT NULL en un deploy posterior. **Nunca renombres ni borres una columna en el mismo deploy que cambia el código.**
4. Migración de datos existentes: crear la empresa 1 con los datos actuales, backfill de `empresa_id = 1` en todas las tablas, luego NOT NULL.

---

## 4. Archivos por tenant

**No uses disco persistente en Render.** Un servicio con disco **no puede escalar a múltiples instancias ni recibir deploys sin downtime** — rompe las dos cosas a la vez.

Object storage con prefijo por tenant (`tenants/{empresa_id}/…`) y URLs prefirmadas de corta vida.

| Proveedor | Almacenamiento | **Egreso** | Free tier |
|---|---|---|---|
| **Cloudflare R2** | $0,015/GB/mes | **$0** | 10 GB, 1M clase A, 10M clase B |
| R2 Infrequent Access | $0,010/GB/mes | $0 (+$0,01/GB recuperación) | — |
| Backblaze B2 | ~$0,007/GB/mes | Gratis hasta 3× el almacenamiento medio; luego $0,01/GB | 10 GB |
| AWS S3 Standard | ~$0,023/GB/mes | **~$0,09/GB** | — |

**Elige R2.** En un SG-SST los usuarios descargan matrices, certificados y exámenes constantemente. Con S3, 500 GB de descargas mensuales cuestan ~USD 45; con R2, **cero**. B2 es más barato en almacenamiento puro, pero su egreso libre está atado a 3× el volumen almacenado, y un SaaS documental descarga mucho más de lo que guarda.

**Reglas de manejo:** nombre de objeto opaco (UUID, nunca el nombre original del archivo, que puede llevar la cédula del trabajador) · URL prefirmada de 5 minutos · validación de tipo MIME y tamaño en el servidor · antivirus en la carga si se aceptan ejecutables (mejor: no aceptarlos).

---

## 5. Multi-tenancy por subdominio

Render **soporta dominios wildcard (`*.sstsmart.co`) con certificado TLS emitido y renovado automáticamente**, siempre que el dominio raíz también apunte a Render. Los CA usados son Let's Encrypt y Google Trust Services — si defines registros CAA, autoriza ambos, **incluyendo emisión wildcard**.

Esto habilita `cliente1.sstsmart.co` **sin aprovisionar nada por tenant**. Y el dominio propio por cliente (`sst.empresa.com`) cuesta USD 0,25/mes de margen — es un excelente argumento de retención en el plan Corporativo y en el canal de consultores con marca propia.

**Dos trampas operativas:** elimina los registros `AAAA` durante la configuración DNS, y si usas Cloudflare, **desactiva el proxy (nube gris) en el dominio raíz** cuando uses wildcard.

**Resolución del tenant, en orden:**

```
1. Subdominio (cliente1.sstsmart.co)  → tenant por defecto
2. Dominio custom (sst.empresa.com)   → lookup en tabla de dominios
3. Sesión del usuario                 → para el consultor que cambia de contexto
4. Sin resolución                     → 404, nunca un tenant por defecto
```

> **Nunca** un fallback silencioso a "la primera empresa". Ese es el bug que expone datos.

---

## 6. Consola de consultor — el modelo de datos del canal

```
cuentas_canal    (id, nombre, tipo{consultor|firma}, plan, max_empresas,
                  subdominio, logo_url, activa)
canal_usuario    (cuenta_canal_id, usuario_id, rol_canal{owner|consultor|lectura})
-- empresas.consultor_id apunta aquí
```

**Reglas de negocio, y son las que retienen al consultor:**

- El consultor ve el agregado de sus empresas; la empresa **nunca** ve las de otro cliente del consultor.
- La facturación es al consultor, no a las empresas. Las empresas no tienen acceso a facturación.
- Una empresa no puede migrar a cuenta directa **sin autorización del consultor** — es lo que responde su objeción de "¿y si me sacan del medio?".
- La actualización normativa se propaga a todas las empresas del consultor en una sola operación.
- El cambio de contexto **fija el `ContextVar` y nunca desactiva RLS**. El consultor es un usuario con acceso a N tenants, no un superusuario.

---

## 7. Arquitectura de despliegue

```
                    Cloudflare (DNS + CDN de estáticos, PoP en Bogotá)
                                    │
                    ┌───────────────┴───────────────┐
                    │   Render — región Virginia    │
                    ├───────────────────────────────┤
   *.sstsmart.co →  │  web (gunicorn, 2+ instancias, autoscaling)
                    │  worker (APScheduler → escalamiento, alertas)
                    │  cron  (vigilancia normativa, indicadores, backup a R2)
                    │  Postgres 16 (+ PgBouncer integrado, sin costo)
                    │  Key Value (Valkey 8) — rate limiting, caché, colas
                    └───────────────────────────────┘
                                    │
                         Cloudflare R2 (archivos por tenant)
```

**PgBouncer viene integrado en Render, sin costo adicional**, en modo *transaction pooling*, activable desde el dashboard o `render.yaml` (requiere reinicio de pocos minutos). Límite por defecto: 30.000 conexiones cliente contra PgBouncer y `max_connections - 10` hacia la base. *Nota: varios artículos de terceros afirman que Render no tiene pooler — es información desactualizada.*

**Consecuencia de transaction pooling:** no puedes usar sentencias preparadas a nivel de sesión ni `SET` de sesión — razón adicional por la que `set_config(..., true)` (local a la transacción) es la forma correcta.

---

## 8. Decisiones registradas

| # | Decisión | Alternativa descartada | Razón |
|---|---|---|---|
| ADR-1 | Shared-table + RLS | Schema-per-tenant, DB-per-tenant | `max_connections=100` en Render; degradación del planner con miles de esquemas |
| ADR-2 | RLS propio en ~150 líneas | `flask-rls` u otro paquete | Ningún paquete maduro en 2026; es la frontera de seguridad, no se delega |
| ADR-3 | Cloudflare R2 | S3, B2, disco de Render | Egreso gratuito; el disco rompe zero-downtime y escalado |
| ADR-4 | Subdominio wildcard | Path-based (`/t/cliente1`) | TLS wildcard automático en Render; cookies aisladas por origen |
| ADR-5 | Región Virginia | Oregon, Ohio | Menor latencia hacia Colombia. **No se puede cambiar después** |
| ADR-6 | Postgres también en desarrollo | Seguir con SQLite | RLS no existe en SQLite; el aislamiento no se podría probar |
| ADR-7 | PWA | App móvil nativa | Cubre foto, geolocalización y offline sin dos tiendas de aplicaciones |

## Fuentes

[PlanetScale — Approaches to tenancy in Postgres](https://planetscale.com/blog/approaches-to-tenancy-in-postgres) · [QueryPlane — Postgres RLS in practice](https://queryplane.com/blog/postgres-row-level-security-in-practice/) · [Render — Connection pooling](https://render.com/docs/postgresql-connection-pooling) · [Render — Creating & connecting Postgres](https://render.com/docs/postgresql-creating-connecting) · [Render — Custom domains](https://render.com/docs/custom-domains) · [Cloudflare R2 pricing](https://developers.cloudflare.com/r2/pricing/) · [Backblaze B2 pricing](https://www.backblaze.com/cloud-storage/pricing)
