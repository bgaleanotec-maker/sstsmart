# Despliegue — Git + Render

Precios y capacidades verificados en render.com el **30 de agosto de 2026**.

---

## 0. ACCIÓN URGENTE — token de GitHub expuesto

El remoto del repositorio tiene un Personal Access Token embebido en la URL:

```
origin  https://github_pat_11BWHZ…@github.com/bgaleanotec-maker/sstsmart.git
```

**Procedimiento oficial de GitHub, en orden estricto:**

**Paso 1 — Revocar. Hoy. Es lo único urgente.**
GitHub lo dice explícitamente: *"si el dato sensible es un secreto, el primer paso es revocarlo y/o rotarlo"*. Ve a **Settings → Developer settings → Personal access tokens** y bórralo. Una vez revocado, el token ya no da acceso — **y eso puede cerrar el incidente sin reescribir historia**.

**Paso 2 — Limpiar el remoto local.** El token vive en `.git/config` de cada clon:

```bash
git remote set-url origin git@github.com:bgaleanotec-maker/sstsmart.git
git config --unset credential.helper
```

**Paso 3 — Verificar si además está en el historial.** Normalmente **no** lo está: `.git/config` no se versiona.

```bash
git log -p -S 'github_pat_' --all
git grep -I 'ghp_\|github_pat_' $(git rev-list --all)
```

Si no aparece nada, **ya terminaste**. Revocar + arreglar el remoto fue suficiente.

**Paso 4 — Solo si sí está en commits.** GitHub recomienda `git-filter-repo` ≥ 2.47 (no BFG, que ya no aparece en su documentación):

```bash
echo 'github_pat_TOKENEXPUESTO==>***REMOVED***' > ../passwords.txt
git filter-repo --sensitive-data-removal --replace-text ../passwords.txt
git push --force --mirror origin
```

Tras el force push, todos los colaboradores deben **re-clonar**: un `pull` sobre historia reescrita reintroduce los commits viejos.

**Paso 5 — GitHub Support.** El force push no elimina objetos alcanzables por pull requests ni vistas cacheadas. Support puede desreferenciar PRs, correr GC del lado servidor y purgar caché. *Caveat oficial: solo asisten cuando el riesgo no se mitiga rotando credenciales — otra razón por la que el paso 1 es el que importa.*

**Paso 6 — Auditar** el audit log de la cuenta y la organización durante la ventana de exposición.

**Prevención permanente:** activa **secret scanning + push protection** en el repositorio (GitHub bloquea el push de un token detectado antes de que llegue al servidor), añade `.env` a `.gitignore` desde ya, y corre `gitleaks` como pre-commit hook.

---

## 1. Estrategia Git

**GitHub Flow**, no GitFlow. Para 1–3 personas, las ramas `develop`/`release`/`hotfix` son sobrecarga pura.

| Rama | Destino | Trigger |
|---|---|---|
| `main` | **Producción** | `autoDeployTrigger: checksPass` — no despliega si el CI falla |
| `staging` | **Staging** (blueprint y base de datos propios) | Auto-deploy en commit |
| `feature/*` | **Preview environment** por PR | Automático, expira a los 7 días |

**Nunca compartas base de datos entre entornos.**

**Protección de `main`:** PR obligatorio · 1 aprobación (o revisión propia diferida si trabajas solo) · status checks obligatorios · **push forzado bloqueado** · historial lineal · secret scanning y push protection activos.

**Mensajes de commit.** El historial actual tiene cinco commits titulados *"Descripción de tus cambios"*. Adopta Conventional Commits (`feat:`, `fix:`, `chore:`) — cuesta cero y aparece en cualquier due diligence.

---

## 2. Precios de Render (agosto 2026, USD)

### 2.1 Plan de workspace — se suma a todo lo demás

| Plan | Precio | Incluye |
|---|---|---|
| Hobby | $0 | 5 GB de ancho de banda, PITR 3 días, 1 asiento, soporte comunitario |
| **Pro** | **$25/mes** | 25 GB, **PITR 7 días**, asientos ilimitados, soporte por email/chat, **desbloquea autoscaling y preview environments** |
| Scale | $499/mes | 1 TB, add-on de SLA |

Excedente de ancho de banda: **$0,15/GB**.

> **El workspace Pro no es opcional.** Sin él no hay autoescalado, no hay entornos de preview por PR, y la ventana de recuperación puntual es de 3 días en lugar de 7.

### 2.2 Servicios web

| Instancia | CPU | RAM | $/mes |
|---|---|---|---|
| Free | <1 | 512 MB | 0 |
| Starter | <1 | 512 MB | 7 |
| Standard | 1 | 2 GB | 25 |
| — | 2 | 4 GB | 85 |
| Pro | 2 | 8 GB | 135 |
| Pro Plus | 2 | 16 GB | 200 |
| Pro Max | 4 | 16 GB | 225 |
| Pro Ultra | 8 | 16 GB | 300 |

*Render migró a identificadores por recurso (`0.5c-512mb`, `1c-2g`…), que es lo que se usa en `render.yaml`. Los nombres comerciales conviven con la nomenclatura nueva y el mapeo no es lineal — **verifica el `plan:` exacto en el dashboard antes de fijarlo en el blueprint**.*

### 2.3 Postgres

Almacenamiento **aparte, a $0,30/GB/mes** en todos los planes de pago.

| Plan | CPU | RAM | $/mes | Máx. conexiones |
|---|---|---|---|---|
| Free | — | 256 MB | 0 (1 GB) | — |
| Micro | <1 | 256 MB | 6 | 100 |
| Small | <1 | 1 GB | 19 | 100 |
| **Standard** | 1 | 2 GB | **40** | 100 |
| Standard+ | 1 | 4 GB | 55 | 100 |
| Medium | 2 | 4 GB | 75 | 100 |
| **Medium+** | 2 | 8 GB | **100** | 200 |
| Large | 2 | 16 GB | 160 | 200–400 |
| XL | 4 | 16 GB | 200 | 400 |

Versiones PostgreSQL 13 a 18. **PgBouncer integrado sin costo adicional**, modo transaction pooling.

**Backups y PITR:** PITR continuo en todas las bases de pago; ventana de **3 días (Hobby) o 7 días (Pro)** — depende del plan del *workspace*, no de la base. La recuperación crea una instancia nueva, no sobrescribe. Backups lógicos manuales descargables, retenidos 7 días. **El plan Free no tiene ninguna recuperación** y la base se borra al expirar.

**Alta disponibilidad:** standby con replicación asíncrona, failover automático tras 30 s, misma URL. Requiere ≥1 CPU y PG ≥13. **Cuesta el doble** (el standby se factura igual que la primaria). Limitaciones: ~1 ms extra de latencia, posible pérdida de los últimos segundos de escrituras, y **el standby no es consultable** — para escalar lecturas hacen falta read replicas, que se facturan aparte.

### 2.4 Otros recursos

| Recurso | Precio |
|---|---|
| Key Value (Valkey 8) | $0 (25 MB) · $10 (256 MB) · $32 (1 GB) · $135 (5 GB) |
| Workers y private services | Misma tabla que servicios web |
| Cron jobs | $0,00016 – $0,02315 por minuto de ejecución |
| **Disco persistente** | $0,25/GB/mes — **no usar**: rompe zero-downtime y escalado horizontal |
| Dominios personalizados | 2 incluidos (Hobby), 15 (Pro), 25 (Scale); adicionales **$0,25/mes** |
| Workflows | $0,05 – $1,50/hora |

### 2.5 Región — decisión irreversible

Disponibles: **Oregon, Ohio, Virginia, Frankfurt, Singapur**. **No hay región en Sudamérica.**

**Elige Virginia (us-east)**: es el punto de amarre de los cables submarinos del Caribe. Estimación de ingeniería (no dato citado): Bogotá→Virginia ~60–90 ms RTT · →Ohio ~70–100 ms · →Oregon ~110–140 ms. En una app Flask con plantillas server-side y varias queries, esos ~50 ms de diferencia se multiplican por cada round-trip y se notan.

> **Dos restricciones duras:** los servicios en regiones distintas **no se comunican por red privada**, y **no se puede cambiar la región de un servicio** — hay que recrear y migrar. Decídelo antes del primer deploy.

**Mitigación de latencia:** pon los estáticos detrás de Cloudflare (tiene PoP en Bogotá) para que solo el HTML cruce al norte.

### 2.6 Cumplimiento

Render tiene **ISO 27001, SOC 2 Type 2, DPA conforme a GDPR, HIPAA** (con soporte dedicado) y certificación **EU-US Data Privacy Framework**. Infraestructura sobre AWS, GCP, Cloudflare y ClickHouse Inc., **con todos los subprocesadores en Estados Unidos**.

Implicación legal colombiana: EE.UU. **está** en la lista de países con nivel adecuado de protección de la Circular Externa 005/2017 de la SIC, así que **no requiere declaración de conformidad**. Pero sigue siendo transferencia internacional y hay que declararla en la política de tratamiento y firmar el DPA con Render (se solicita vía "Request Documents" en el dashboard — **guarda copia, te lo van a pedir en due diligence**). Detalle en [`../04-empresa/03`](../04-empresa/03-datos-personales-y-propiedad-intelectual.md).

---

## 3. render.yaml

```yaml
services:
  - name: sst-web
    type: web
    runtime: python
    region: virginia
    plan: standard
    buildCommand: pip install -r requirements.txt
    preDeployCommand: flask db upgrade        # corre como app_owner, antes del switch
    startCommand: gunicorn -w 4 -k gthread --timeout 60 "app:create_app('production')"
    healthCheckPath: /healthz
    autoDeployTrigger: checksPass             # no despliega si el CI falla
    scaling:
      minInstances: 2
      maxInstances: 5
      targetCPUPercent: 70
    envVars:
      - key: DATABASE_URL                     # app_user, SIN BYPASSRLS
        fromDatabase: { name: sst-db, property: connectionString }
      - key: SECRET_KEY
        generateValue: true
      - key: GEMINI_API_KEY
        sync: false                           # se pide al crear; nunca en el repo
      - key: WOMPI_PRIVATE_KEY
        sync: false
      - key: COLUMN_ENCRYPTION_KEY            # distinta de SECRET_KEY
        sync: false
      - fromGroup: sst-shared

  - name: sst-worker
    type: worker
    runtime: python
    region: virginia
    plan: starter
    startCommand: python -m app.tasks.worker
    envVars:
      - fromGroup: sst-shared

  - name: sst-vigilancia-normativa
    type: cron
    runtime: python
    region: virginia
    schedule: "0 11 * * *"                    # 06:00 Bogotá (UTC-5)
    startCommand: python scripts/vigilancia_normativa.py
    envVars:
      - fromGroup: sst-shared

  - name: sst-backup-r2
    type: cron
    runtime: python
    region: virginia
    schedule: "0 8 * * 0"                     # domingo 03:00 Bogotá
    startCommand: python scripts/backup_a_r2.py   # usa el rol app_backup (BYPASSRLS)

databases:
  - name: sst-db
    region: virginia
    plan: standard
    postgresMajorVersion: "16"

envVarGroups:
  - name: sst-shared
    envVars:
      - key: FLASK_ENV
        value: production
      - key: R2_BUCKET
        value: sstsmart-tenants

previews:
  generation: automatic
  expireAfterDays: 7
```

**Notas:**

- **`sync: false`** es el mecanismo correcto para secretos: el valor se solicita interactivamente al crear el servicio y nunca vive en Git.
- **`envVarGroups`** comparte configuración entre web, worker y cron sin duplicarla.
- **`preDeployCommand`** corre en una instancia separada, antes de conmutar el tráfico. Por eso las migraciones deben ser expand/contract.
- **Preview environments:** crean copia completa del entorno por PR, se actualizan con cada commit y se destruyen al cerrar el PR. Requieren **workspace Pro**. Se facturan prorrateados por segundo; usa `previewPlan` reducido. **Las bases se crean vacías** — usa `initialDeployHook` para sembrar (`scripts/seed_matriz_legal.py` ya es idempotente, es ideal para esto).

---

## 4. CI en GitHub Actions

```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_PASSWORD: test }
        options: >-
          --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
        ports: ['5432:5432']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.13' }
      - run: pip install -r requirements.txt
      - run: flask db upgrade
      - run: pytest tests/ -q
      - run: pytest tests/test_aislamiento_tenants.py -q   # bloqueante
      - run: pip-audit
      - run: gitleaks detect --no-git
```

Free: **2.000 min/mes** + 500 MB de artefactos. Excedente: Linux 2-core **$0,006/min**. Con una suite de un par de minutos, 2.000 minutos cubren cientos de builds — no será un costo relevante.

---

## 5. Presupuesto de infraestructura

| Etapa | Componentes | USD/mes | COP/mes (a 4.100) |
|---|---|---|---|
| **MVP / beta** | Web Starter $7 + PG Micro $6 + workspace Hobby $0 + Resend/Sentry/UptimeRobot/PostHog gratuitos + R2 ~$1 | **~$15** | ~$62.000 |
| **Producción, 50 tenants** | Workspace Pro $25 + Web Standard $25 + Worker Starter $7 + PG Standard $40 + 20 GB $6 + KV 256 MB $10 + Resend $20 + R2 $3 | **~$136** | ~$558.000 |
| **Escala, 200–500 tenants** | Workspace Pro $25 + 2× Web Pro $270 + Worker $25 + PG Medium+ $100 + HA $100 + 200 GB $60 + KV 1 GB $32 + Sentry $26 + Resend $20 + R2 $15 | **~$673** | ~$2.759.000 |

**Stack complementario, precios 2026:**

| Categoría | Recomendación | Precio |
|---|---|---|
| Email transaccional | **Resend** (3.000/mes gratis; Pro $20 por 50k) → migrar a **Amazon SES** ($0,10/1.000) si superas ~200k/mes | $0 → $20 |
| Errores | **Sentry** free (5k errores) → Team $26 | $0 → $26 |
| Uptime | **UptimeRobot** free (50 monitores, 5 min) | $0 |
| Analítica de producto | **PostHog** free (1M eventos, 5k replays, 1M feature flags) | $0 |
| Soporte | **Crisp** free (2 agentes) → Mini $45. Precio **por workspace, no por asiento** | $0 → $45 |
| IA | **Gemini 2.5 Flash-Lite: $0,10 / $0,40** por millón de tokens (in/out) | ~$8 por 10.000 consultas |

> **Alerta de presupuesto a 12+ meses:** los precios de **Gemini 3.6 y 3.7 Flash son promocionales hasta el 31-dic-2026 y se duplican el 1-ene-2027** ($0,75→$1,50 in, $3,75→$7,50 out). Si modelas costos a dos años, usa las cifras de 2027.
>
> Alternativas por costo: GPT-5.6-Luna ($0,10/$0,60) · Claude Haiku 4.5 ($1/$5, pero con **prompt caching a 0,1× en lectura**, lo que cambia la ecuación si tus prompts incluyen la matriz legal como contexto fijo y voluminoso). Batch API de Anthropic y OpenAI: **−50%**.
>
> **La IA no será tu costo dominante.** El cómputo y la base de datos sí.

---

## 6. Cuándo dejar Render

Quédate mientras el cuello de botella sea producto, no infraestructura. Considera migrar cuando:

- Necesites presencia en Sudamérica o multi-región activa (Render no tiene región sudamericana; Fly.io tiene 18).
- El gasto mensual pase de ~USD 800–1.000 **y** tengas a alguien que sepa operar ECS/EKS.
- Un comprador grande exija residencia de datos en Colombia o LATAM.

Para 50–500 pymes con tráfico en horario laboral colombiano, Render está holgadamente dentro de rango. *(Nota: circula la afirmación de que Render "no tiene CLI nativo" — es falsa; existe el CLI oficial `render-oss/cli`, activo hasta v2.8.0.)*

## Fuentes

[Render Pricing](https://render.com/pricing) · [Blueprint Spec](https://render.com/docs/blueprint-spec) · [Regions](https://render.com/docs/regions) · [Custom Domains](https://render.com/docs/custom-domains) · [Scaling](https://render.com/docs/scaling) · [Deploys](https://render.com/docs/deploys) · [Preview Environments](https://render.com/docs/preview-environments) · [Postgres Backups](https://render.com/docs/postgresql-backups) · [Postgres HA](https://render.com/docs/postgresql-high-availability) · [Connection Pooling](https://render.com/docs/postgresql-connection-pooling) · [Key Value](https://render.com/docs/key-value) · [Security](https://render.com/security) · [GitHub — Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) · [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions) · [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) · [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing) · [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) · [Resend](https://resend.com/pricing) · [Sentry](https://sentry.io/pricing/) · [PostHog](https://posthog.com/pricing) · [Crisp](https://crisp.chat/en/pricing/)
