# Especificación — Módulo PESV (Resolución 40595 de 2022)

Base normativa y de mercado en [`../01-mercado/03-mercado-pesv-seguridad-vial.md`](../01-mercado/03-mercado-pesv-seguridad-vial.md).

**Premisa de diseño:** el PESV **no es un sistema paralelo, es un módulo del SG-SST** — la Ley 1503/2011 art. 12 y la Res. 0312/2019 art. 32 exigen la articulación, y la Res. 40595 mapea cada paso contra artículos del Decreto 1072/2015. Entre **60% y 70% del PESV se resuelve reutilizando** política, matriz de riesgos, plan de capacitación, plan de emergencias, investigación de incidentes, auditoría interna y mejora continua que ya existen en el producto. Lo específico son los objetos: **vehículos, conductores, vías y desplazamientos**.

---

## 1. Alcance por fases

| Fase | Trimestre | Pasos cubiertos | Nivel soportado |
|---|---|---|---|
| **1** | T4 (meses 10–12) | 1–5, 9, 16, 17, 19, 20, 24 + control documental de conductores | **Básico** |
| **2** | T5 (meses 13–15) | 6, 7, 8, 10, 11, 12, 13, 21, 22, 23 | **Estándar** |
| **3** | T7–T8 (meses 19–24) | 14, 15, 18 + ISO 39001 | **Avanzado** |

---

## 2. Determinación de obligatoriedad y nivel

Es la primera pantalla y también el **imán de leads** (versión pública gratuita).

**Entradas:** vehículos automotores propios · vehículos no automotores (bicicletas incluidas) · arrendados, leasing, renting · de contratistas · **particulares de empleados usados en gestiones laborales** · número de conductores · misionalidad (M1 transporte / M2 otra).

**Reglas:**

```
obligado = (total_unidades > 10) OR (conductores >= 2)
```

| Nivel | M1 | M2 |
|---|---|---|
| Básico | 11–19 vehículos o 2–19 conductores | 11–49 vehículos o 2–49 conductores |
| Estándar | 20–50 vehículos o 20–50 conductores | 50–100 vehículos o 50–100 conductores |
| Avanzado | >50 vehículos o >50 conductores | >100 vehículos o >100 conductores |

> **Antes de codificar el conteo de pasos por nivel:** las fuentes secundarias dan tres cifras distintas (13/21/24, 15/19/24, 18/22/24) y la propia resolución tiene inconsistencias tipográficas en sus tablas 2 y 6. **Validar contra el anexo técnico oficial.** El total de 24 pasos y el orden básico<estándar<avanzado sí están verificados.

**Salida pública (lead magnet):** *"Su empresa SÍ está obligada a tener PESV en nivel Básico. Le aplican N de los 24 pasos, debe reportar indicadores al Ministerio del Trabajo entre el 6 y el 31 de enero según su NIT, y su exposición sancionatoria es de $X a $Y."* Captura de correo para el informe completo.

---

## 3. Modelo de datos

Todas las tablas llevan `empresa_id` NOT NULL con FK e índice, y política RLS, según [`../03-arquitectura/01`](../03-arquitectura/01-arquitectura-saas-multitenant.md).

```
pesv_plan            (empresa_id, misionalidad, nivel, año, estado, lider_usuario_id,
                      fecha_diagnostico, fecha_ultima_actualizacion)
pesv_paso            (plan_id, numero 1..24, aplica_bool, estado, responsable_id,
                      fecha_limite, porcentaje_avance, articulo_1072_relacionado)
pesv_evidencia       (paso_id, documento_id → tabla documental existente, version, hash)
pesv_comite          (plan_id, acta_id, periodo_inicio, periodo_fin)  ← reutiliza actas

vehiculo             (empresa_id, placa, tipo, modelo, propiedad{propio|arrendado|leasing|
                      contratista|particular_empleado}, kilometraje, activo)
vehiculo_documento   (vehiculo_id, tipo{SOAT|RTM|poliza|tarjeta_operacion|FUEC},
                      numero, fecha_expedicion, fecha_vencimiento, archivo_id)
vehiculo_inspeccion  (vehiculo_id, conductor_id, fecha, tipo{preoperacional|periodica},
                      resultado, hallazgos_json, foto_ids, lat, lon, offline_sync_id)
vehiculo_mantenimiento (vehiculo_id, tipo{preventivo|correctivo}, km_programado,
                      fecha_programada, fecha_ejecucion, taller, costo, archivo_id)

conductor            (empresa_id, empleado_id → Empleado, tipo_vinculacion, activo)
conductor_documento  (conductor_id, tipo{licencia|examen_medico|examen_psicosensometrico|
                      curso_manejo_defensivo|antecedentes_RUNT},
                      categoria, fecha_expedicion, fecha_vencimiento, archivo_id)
conductor_comportamiento (conductor_id, fecha, tipo, descripcion, fuente{telemetria|
                      observacion|comparendo}, gravedad)

siniestro_vial       (empresa_id, fecha, vehiculo_id, conductor_id, gravedad,
                      terceros_involucrados, causa_raiz, es_at_bool, furat_id,
                      costo_estimado, plan_accion_id)
ruta                 (empresa_id, origen, destino, riesgos_json, frecuencia)
desplazamiento       (ruta_id, conductor_id, vehiculo_id, fecha, autorizado_por)

pesv_indicador       (plan_id, codigo, periodo{mensual|trimestral|anual},
                      numerador, denominador, valor, meta, fecha_corte)
pesv_reporte         (plan_id, destino{MinTrabajo_C0034|SISI_PESV}, periodo,
                      fecha_generacion, fecha_envio, archivo_id, acuse_id)
```

**Reutilización explícita — no duplicar:**

| Objeto PESV | Se apoya en lo que ya existe |
|---|---|
| Paso 3 y 4 (política, liderazgo) | Módulo de política y revisión por la dirección del SG-SST |
| Paso 6 (riesgos viales) | Estructura de `matriz_riesgos` / IPEVR |
| Paso 10 (formación) | Módulo `formacion` (cursos, exámenes, certificados) |
| Paso 12 (emergencias) | Plan de emergencias del SG-SST |
| Paso 13 (investigación de siniestros) | `metodologias_investigacion` + flujo de eventos |
| Paso 19 (archivo documental) | Gestor documental con versionado y log forense |
| Paso 22 (auditoría) | Módulo de auditoría interna |
| Paso 24 (comunicación) | `NotificationService` |
| Conductor | `Empleado` (hoy semi-huérfano — el PESV es la razón para activarlo) |

---

## 4. Funcionalidades por valor comercial

### 4.1 Alto valor, alta automatización — construir primero

**Control documental de conductores y vehículos con alertas de vencimiento.**
Licencia, SOAT, RTM, exámenes médicos ocupacionales, psicosensométrico, curso de manejo defensivo, tarjeta de operación, FUEC. Alertas a 60 / 30 / 15 / 7 / 0 días, por correo y en la app, al responsable y al conductor.

> **Contexto que lo hace vendible:** el 55,8% del parque automotor colombiano no tiene RTM vigente y el 47% no tiene SOAT vigente. Ningún cliente puede operar esto en Excel a escala, y es lo primero que mira un verificador.

**Checklist preoperacional móvil (paso 16).**
PWA con cola offline: el conductor abre, marca, adjunta foto, firma; se sincroniza cuando hay señal. Bloqueo de salida si hay hallazgo crítico. Geolocalización y sello de tiempo.

**Plan de mantenimiento por kilometraje (paso 17).**
Programación por km u horas, alertas, registro de ejecución con factura del taller, hoja de vida del vehículo.

**Indicadores y generación del reporte (paso 20).** — *la máxima palanca comercial*
Cálculo automático de los indicadores exigidos, con periodicidad mensual, trimestral y anual, y **generación del paquete de reporte** para:
- **Circular 0034/2026 (MinTrabajo)** — misionalidad 2, entre el 6 y el 31 de enero según último dígito del NIT.
- **SISI/PESV (Supertransporte, Res. 5178/2023)** — misionalidad 1, formulario anual + indicadores al décimo día hábil.

El sistema debe **calcular la fecha exacta de cada empresa a partir de su NIT** y avisar con 30, 15 y 5 días de anticipación. Esa alerta, por sí sola, justifica el add-on.

**Archivo y retención documental (paso 19).**
Repositorio con trazabilidad, versionado y control de vigencias — es lo que se muestra en una verificación.

### 4.2 Alto valor, automatización media — segunda ola

- **Pasos 13 y 21** — formulario de investigación de siniestros, análisis causal (reutilizar `metodologias_investigacion`), registro estadístico, y **enlace automático al FURAT cuando el siniestro es accidente de trabajo**.
- **Paso 10** — matriz de competencias del conductor, plan anual de formación, asistencia, certificados.
- **Paso 6** — matriz de riesgo vial sobre la estructura de identificación de peligros existente.
- **Paso 22** — **auditoría anual con lista de verificación de los 24 pasos**, informe y plan de acción. El software puede generar el 80% del paquete. Recordar que el auditor debe ser **persona distinta al líder del PESV**, con competencia documentada (ISO 19011): el sistema debe validarlo y dejar constancia.

### 4.3 Bajo esfuerzo, alto cumplimiento percibido — rellenar rápido

Pasos 1–4 (designación del líder, actas del comité, política firmada, evidencia de liderazgo), 15 (rutogramas y planificación de desplazamientos) y 14 (análisis de vías). Plantillas parametrizadas con los datos de la empresa.

---

## 5. Empaquetado y precio

| Add-on | Nivel PESV | Precio/mes | Incluye |
|---|---|---|---|
| **PESV Básico** | Básico (≤19 veh. o ≤49 en M2) | **$199.000** | Pasos de fase 1, hasta 20 vehículos y 20 conductores, reporte C0034 |
| **PESV Estándar** | Estándar | **$399.000** | Fase 1 + 2, hasta 60 vehículos, reporte SISI/PESV, auditoría anual |
| **PESV Avanzado** | Avanzado | **$699.000** | Todo, vehículos ilimitados, ISO 39001, contratistas |
| **Diseño e implementación del PESV** (servicio del bufete, una vez) | cualquiera | **$4.900.000** | Contra los $8M–$20M del mercado |

**Requiere plan Profesional o superior** — el PESV no se vende suelto, porque su valor depende de la articulación con el SG-SST que exige el art. 32.

> **Argumento de precio, verificable:** una consultoría de PESV cuesta entre $8 y $20 millones e implica de 2 a 4 meses. El add-on cuesta $2,4M–$8,4M **al año** e incluye el reporte de indicadores, que la consultoría no cubre porque es mensual y trimestral, no anual.

---

## 6. Campañas asociadas

| Ventana | Acción |
|---|---|
| **Noviembre–diciembre** | "Prepare su reporte PESV de enero". Diagnóstico gratuito de obligatoriedad |
| **6–31 de enero** | Campaña por último dígito del NIT: *"Su fecha es el X de enero"*. Máxima urgencia del año |
| **Febrero–marzo** | Upsell a clientes SG-SST existentes que declararon flota en el onboarding |
| **Todo el año** | Diagnóstico público de obligatoriedad como lead magnet permanente |

**Dato de onboarding obligatorio:** preguntar siempre por número de vehículos y de conductores al dar de alta una empresa. Es el disparador del upsell y cuesta un campo.

---

## 7. Lo que este módulo NO hace

- **No es un GPS ni un sistema de telemetría.** Se integra con ellos (Rodando en Línea, Wialon, Traccar), no los reemplaza. Decirlo explícitamente evita la objeción *"ya tengo software de flota"*.
- **No emite certificaciones.** La Res. 40595 no crea un esquema de certificación por tercero acreditado; el cumplimiento es autogestionado y se evidencia documentalmente. Esa es, de hecho, la condición que hace viable el producto.
- **No sustituye al líder del PESV ni al auditor interno.** La norma exige personas con competencia documentada. El software genera la evidencia; la responsabilidad sigue siendo del empleador.
