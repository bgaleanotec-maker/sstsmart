# Backlog para Claude Code

> Orden de ejecución propuesto; las fases son las de `plataforma/03-priorizacion-y-secuencia.md` §4. Rutas escritas desde la raíz del repo. Antes de empezar cualquier épica: leer `CLAUDE.md` (reglas duras),
> `plataforma/04-arquitectura-plataforma.md` (ADR-P1 a P7) y las 12 reglas de producto de
> `plataforma/01-estructura-legal-dos-entidades.md` §9.

## Cómo trabajar
1. **Una épica por rama** (`feat/E<n>-<slug>`), PR con descripción y checklist de aceptación.
2. **Tests primero** en lo que toca tenencia, plazos, derivación y pagos.
3. Verificación mínima en cada PR: boot (`SCHEDULER_ENABLED=0 … create_app('development')`) + `pytest tests/ -q`.
4. Modelo nuevo con TenantMixin → registrarlo en `tests/test_aislamiento_tenants.py`, `scripts/init_prod_db.py` y `scripts/rls_postgres.sql`. Migraciones: **hasta que termine E0.1**, columna nueva en tabla existente = mini-migración aditiva en `scripts/init_prod_db.py`; **después de E0.1, todo cambio de esquema va en Alembic** y se actualiza `CLAUDE.md`.
5. Ninguna cita normativa en plantillas o textos sin entrada en `biblioteca_juridica` con `verificada_por`. Si no está verificada, **no se publica**: se deja `[VERIFICAR]` y se avisa a Brian.
6. Al cerrar una épica: actualizar `CONTEXTO.md` del repo (estado, decisiones, bitácora) y correr `python ../_sistema/cerebro.py` desde la raíz de `empresa/`.
7. Decisiones D1-D8 (`00-tesis-y-decisiones.md`) que bloqueen una historia → **preguntar a Brian**, no asumir.

---

## Fase 0 · Fundación (oct-dic 2026)

### E0 — Cobro y base técnica (bloquea todo lo comercial)
| Historia | Criterios de aceptación |
|---|---|
| E0.1 Postgres 16 en desarrollo y Alembic formal | `flask db upgrade` desde cero crea el esquema; CI corre contra Postgres |
| E0.2 RLS activo (`scripts/rls_postgres.sql`) con `FORCE`, roles `app_owner`/`app_user`, `set_config(..., true)` | Test: con el rol de app, una consulta cruda sin filtro no devuelve filas de otro tenant |
| E0.3 `empresa_id` NOT NULL tras backfill | Migración contract; tests de aislamiento verdes |
| E0.4 Pagos Wompi: suscripción mensual B2B, **suscripción mensual B2C** y compra única | Webhook idempotente; estados `pendiente/aprobado/rechazado`; reintentos; tests con fixtures de Wompi para los tres tipos |
| E0.5 Aceptación de inicio inmediato y cancelación en un clic | Texto y fecha guardados; la cancelación corta la renovación sin soporte humano |
| E0.6 Unificar los dos servicios de notificación en `app/core/notificaciones/` | Un solo import en todo el código; tests de envío con backend falso |
| E0.7 Archivos a Cloudflare R2 con prefijo por tenant | Subida/descarga con URL prefirmada; nada en el disco de Render |
| E0.8 Factura electrónica de la S.A.S. vía proveedor tecnológico (ver `empresa/02-dian-y-facturacion/`) | Cada pago aprobado genera factura con IVA 19% y se guarda el **CUFE** devuelto; prueba en el ambiente de habilitación de la DIAN. **Bloqueada por D1/D2** (la S.A.S. debe existir) |

### E1 — Núcleo de cuentas personales (ADR-P2)
| Historia | Criterios de aceptación |
|---|---|
| E1.1 `Empresa.tipo_cuenta` ∈ {organizacion, personal, practica_juridica}, por defecto `organizacion` | Migración (Alembic si E0.1 ya terminó); filas existentes intactas |
| E1.2 Registro B2C: crea tenant `personal` + usuario `Titular` | Constante de rol en `app/constants.py`; `tiene_rol('Titular')`; test de aislamiento entre dos personas |
| E1.3 Catálogo con `vertical`, `segmento`, `tipo_precio`, `tipos_cuenta` | El gating niega un módulo B2B a una cuenta personal y viceversa (test) |
| E1.4 Autorización de datos versionada (`autorizacion_datos`) | Texto versionado; sensible separado; revocación efectiva (test) |
| E1.5 Bitácora `auditoria_acceso` | Lista de campos sensibles en `app/data/campos_sensibles.py` (inicial: diagnósticos y datos de salud, historia clínica, lesiones, datos tributarios del contribuyente, cédula de terceros, datos de menores); cada lectura de esos campos queda registrada (test). Las verticales agregan sus campos a esa lista |

### E3 — PESV con reporte MinTrabajo (fecha dura: enero de 2027)
Especificación base: `docs/02-producto/03-especificacion-modulo-pesv.md` + correcciones de `plataforma/02-verticales/02-pesv.md`.
| Historia | Criterios de aceptación |
|---|---|
| E3.1 Autodiagnóstico de nivel por misionalidad, vehículos y conductores | Activa solo los pasos que aplican (18/22/24); rangos M2 parametrizados (pendientes de verificar) |
| E3.2 24 pasos con evidencias y plan anual compartido con SG-SST | Una tarea del plan aparece en ambos módulos sin duplicarse |
| E3.3 Conductores y vehículos con vencimientos (licencia, SOAT, RTM, mantenimiento) | Alertas 30/15/5 días |
| E3.4 Preoperacional PWA offline con foto, firma y bloqueo por falla crítica | Funciona sin red y sincroniza; exporta Excel |
| E3.5 Siniestros: registro único AT + siniestro vial | Un evento alimenta FURAT/indicadores SST e indicadores PESV |
| E3.6 Indicadores Tabla 10 y **resumen para el formulario de MinTrabajo** | Pantalla y CSV con los indicadores de la Tabla 10 (paso 20, Res. 40595/2022) en el orden del formulario; test con datos semilla y valores esperados calculados a mano. **Antes:** Brian entrega la lista de campos del formulario y la fórmula de cada indicador. Recordatorio por último dígito del NIT vía motor de plazos (regla `pesv_reporte_mintrabajo`) |
| E3.7 `pesv_reporte` con destinos extensibles (MinTrabajo, SISI, VIGIA) | Agregar un destino no exige migración de esquema |
| E3.8 Página de precios PESV | Precios de `02-verticales/02-pesv.md` §4, sujetos a D6 |

---

## Fase 1 · Motor B2C (ene-mar 2027)

### E2 — Motor de plazos y documentos (ADR-P4, ADR-P5)
| Historia | Criterios de aceptación |
|---|---|
| **E2.0 (bloqueante, la hace Brian)** Verificar reglas y citas iniciales | Code genera `plataforma/verificacion/reglas_y_citas.csv` con cada regla de `04-arquitectura` §3.2 y cada cita del seed (columnas: código, texto, fuente, URL, `verificada_por`, `verificada_en`, observación). Brian la llena; un comando la importa. Mientras tanto, las reglas existen con `estado='pendiente_verificacion'`, visibles en desarrollo y bloqueadas en producción |
| E2.1 `app/core/plazos.py` con calendarios, festivos (`holidays` CO) y excepciones | Tests con festivos móviles, fin de año y Semana Santa; cada regla con `norma_fuente` |
| E2.2 Catálogo inicial de reglas (`app/data/plazos_catalogo.py`) | Las de `04-arquitectura` §3.2; solo se activan en producción las importadas como verificadas en E2.0 |
| E2.3 `biblioteca_juridica` + seed inicial (Decreto 2591/1991, Ley 1755/2015, Decreto 333/2021, Ley 1751/2015, T-760/2008) | Cada entrada con URL oficial y verificador |
| E2.4 `app/core/documentos.py`: plantillas Jinja versionadas → DOCX y PDF | Pie con aviso de autoservicio y etiqueta de IA; hash del documento |
| E2.5 `app/core/ia.py` sobre `gemini_service` | Redacción de datos sensibles sin autorización; la salida no puede introducir citas fuera de `citas_ids` (test con salida simulada) |
| E2.6 Expediente: `caso`, `evento_caso`, `plazo`, alertas 7/3/1 | Un caso muestra su línea de tiempo y próximos vencimientos |

### E4 — Peticiones y tutelas (salud + petición)
Especificación: `plataforma/02-verticales/03-tutelas-y-peticiones.md` §7.
| Historia | Criterios de aceptación |
|---|---|
| E4.1 Triaje guiado con reglas duras (otro medio, inmediatez, duplicado, laboral/pensional complejo) | Casos fuera de lista blanca no generan tutela y ofrecen derivar (tests por regla) |
| E4.2 Derecho de petición por tipo y entidad (EPS, Colpensiones, Movilidad) | Plazo calculado por el motor; alerta "ya puede tutelar" |
| E4.3 Tutela de salud estándar y por petición no respondida | Incluye juramento art. 37. **Clave de duplicado:** mismo usuario + mismo NIT de entidad accionada + mismo tipo de pretensión dentro de 90 días (`[E]`, ajustable) → bloquea y explica la temeridad (test) |
| E4.4 Asistente de radicación: juez competente (Decreto 333/2021) y paquete para Tutela en Línea | El usuario envía; la app guarda el acuse que él sube |
| E4.5 Seguimiento de cumplimiento y desacato en un clic | Genera el incidente del art. 52 desde el fallo cargado |
| E4.6 Monetización: petición gratis, tutela premium, suscripción de seguimiento | Precios configurables; aceptación de inicio inmediato |
| E4.7 Landing `/tutelas` con contenido y sin promesas de resultado | Revisión contra reglas 1 y 3 de producto |

### E5 — Calendario tributario
| Historia | Criterios de aceptación |
|---|---|
| E5.1 NIT + municipio → obligaciones nacionales y de ICA | Datos de calendario cargados por año con fuente (Decreto nacional, Res. SDH Bogotá); empezar por Bogotá |
| E5.2 Alertas 7/3/1 por correo y WhatsApp | Usa el motor de notificaciones |
| E5.3 Calculadora de extemporaneidad (art. 641 ET) e intereses | Tests con casos resueltos a mano por Brian |
| E5.4 Botón "¿me afecta?" → diagnóstico DIAN | Crea un caso para la consola del abogado solo con autorización |

---

## Fase 2 · Herramientas del abogado (abr-jun 2027)

### E6 — Consola del abogado (evoluciona el módulo `juridico`)
| Historia | Criterios de aceptación |
|---|---|
| E6.1 Tenant `practica_juridica` y rol `Abogado` | El abogado ve solo expedientes derivados con autorización vigente |
| E6.2 `derivacion` cruzada con consentimiento y revelación del vínculo | Sin autorización → 403 (test); revocar corta el acceso a datos nuevos |
| E6.3 **Control de conflictos** (`contraparte`, `conflicto_bloqueo`) | Empresas con retainer se bloquean solas; derivación contra ellas → `rechazada_conflicto` con alternativas al usuario |
| E6.4 Cupo y SLA del retainer (de `docs/02-producto/04` §4) | Contador visible; excedente ofrecido, no rechazado |
| E6.5 Firma con nombre, tarjeta profesional y fecha en todo concepto | Plantillas de abogado (`lista_blanca=False`) solo para rol `Abogado` |
| E6.6 Tablero de horas por línea y valor por hora | Alimenta la decisión de capacidad (`05-modelo` §2) |
| E6.7 Cliente HTTP de Radar Judicial (consulta a demanda) | Respeta `MONITOREO_AUTOMATICO=false`; nunca scraping |

### E7 — Defensa DIAN en la app
Especificación: `plataforma/02-verticales/05-impuestos.md` §4.A.
| Historia | Criterios de aceptación |
|---|---|
| E7.1 Lector del acto (PDF) → tipo, notificación, cuantía, año gravable, vencimiento | ≥ 90% de acierto en tipo de acto y fecha de notificación sobre los casos reales de la Fase 0 (anonimizados); si no llega, el abogado confirma cada campo |
| E7.2 Conciliador exógena vs. formulario 210 | Marca diferencias; el abogado confirma |
| E7.3 Simulador de sanciones y reducciones | Tests con casos calculados a mano |
| E7.4 Generador de respuesta y recurso (plantillas de abogado) | Solo rol `Abogado`; citas solo desde la biblioteca |

### E8 — Centrales de riesgo (reutiliza E2 y E4) · **por especificar: no ejecutar hasta tener criterios**
Reclamo ante la fuente, queja ante la SIC y tutela de habeas data, con cálculo de caducidad del dato (Ley 2157/2021 `[VERIFICAR términos]`).

---

## Fases 3 y 4 · Laboral, insolvencia y tránsito (jul-2027 en adelante) · **por especificar: no ejecutar**
Se especifican al cerrar la Fase 2 y se abren **solo** con D3 decidido y capacidad de abogado disponible (ver `03-priorizacion-y-secuencia.md` §4).
- **E9 Laboral**: calculadora de liquidación, indemnización art. 64 y moratoria art. 65; derivación con control de conflictos estricto.
- **E10 Insolvencia**: calculadora de capacidad de pago y plan (activo InsolvenciaYA del cerebro).
- **E11 Accidentes** (Fase 4): guía, pruebas, plazos y calculadora gratis; calculadora premium sin recomendación; derivación solo a petición del usuario, con periodo de reflexión y solo si hay abogado asociado; nada de notificaciones de venta jurídica.
- **E12 Fotomultas** (Fase 4): revisión de autorización de la cámara y de la notificación; escrito sin promesa de resultado.

### E13 — Firma App portada como consola del abogado (Fase 2, junto con E6)
Ver `plataforma/02-verticales/08-firma-app.md`. Portar por módulos: clientes y prospectos → citas y agenda → honorarios del abogado → WhatsApp. **No** portar `judicial_scraper.py`. Criterio: Brian gestiona sus casos reales en la consola durante 4 semanas sin volver a `firma_app/`. **Por especificar en detalle antes de abr-2027.**

### E14 — Penal (Fase 2)
Ver `plataforma/02-verticales/07-penal.md` §4: triaje querellable/oficio, querella guiada, alertas (6 meses, conciliación, 30 días), seguimiento del NUNC y módulo "evento grave" en SST. **Por especificar en detalle antes de abr-2027.**

### Cerebro Legal (servicio aparte)
Backlog propio en `empresa/Apis/cerebro_legal/06-backlog-claude-code.md` (C0-C5). C0 y C1 corren en paralelo con las Fases 0-1 de este repo.

## Definición de terminado (todas las épicas)
- Tests verdes y cobertura de los caminos de error.
- Reglas de producto 1-12 revisadas en la interfaz.
- Textos visibles al usuario revisados contra Ley 1480 (sin promesas, precio con IVA).
- `CONTEXTO.md` y cerebro actualizados.
