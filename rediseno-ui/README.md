# Rediseño visual de Justrabajo — paquete para Claude Code

> Pedido por Brian el 23-oct-2026: "quiero que SST se vea mejor así" (referencia: `referencia-inspiracion.jpg`).
> Este documento es **la especificación completa** para ejecutar el rediseño sin volver a preguntar.
> Lo que propone Claude está marcado como propuesta; lo que falta decidir, en §11.

**Antes de tocar código:** leer `../CLAUDE.md` y `../CONTEXTO.md` §3 (reglas duras). Nada aquí las reemplaza.

> **Estado de ejecución (7-nov-2026, rama `ui/rediseno-panel`):** UI-0, UI-1 y UI-2 **hechos**; UI-3 (consola del consultor) pendiente.
> - Tokens v2 en `app/static/css/style.css` (variables CSS) y en el `tailwind.config` inline de `base.html` (**alternativa 2 de §2.5**: CDN con tokens; la compilación con el binario standalone queda como deuda).
> - Componentes en `app/templates/components/` (`medidor`, `nav_item`, `kpi`, `chip`, `tarjeta`), importados `with context`; las funciones que usan las macros (`puntos_arco`, `fecha_corta`…) están registradas como *globals* de Jinja en `app/ui.py`.
> - Servicios: `app/services/panel.py` (`datos_panel`, `puntos_arco`, `nivel_de`, `faltan_para_aceptable`, `acciones_prioritarias`), `app/services/vencimientos.py`, `app/data/hitos_normativos.py` (todos los hitos con `[VERIFICAR]` hasta que Brian confirme la fuente), `Empresa.ultima_actualizacion` (propiedad).
> - Las 75 plantillas migradas (`auth/login.html` era código muerto y se eliminó; `login.html`, `landing.html`, `sgsst/politica_imprimir.html` y `formacion/certificado.html` quedan fuera de alcance como dice §3). `admin/base.html` ahora hereda de `base.html` y agrega pestañas; sus hijas usan `block admin_content`. Las 12 plantillas que eran páginas HTML completas (admin/matriz/*, reportes/*) se convirtieron al layout.
> - QA (§9.2) sin Playwright: `rediseno-ui/qa_rutas.py` recorre las 86 rutas GET con el admin y falla ante 500; capturas en `rediseno-ui/capturas-qa/`. Datos de demostración: `scripts/seed_demo.py`. Pruebas: `tests/test_panel.py` (9).
> - Pendiente de revisión manual fina: `controles/*` y `formacion/*` conservan insignias de colores y la portada tipo catálogo; títulos `<title>` genéricos en varias listas. Lighthouse no se corrió (sin navegador con auditoría en esta sesión).

---

## 0. Archivos de este paquete

| Archivo | Para qué |
|---|---|
| `README.md` | Esta especificación |
| `mockup-panel.html` | Maqueta navegable del panel principal (**v2**). **Es la fuente de verdad visual**: abrirla en el navegador y copiar medidas, colores y textos |
| `captura-escritorio.png` · `captura-movil.png` | Cómo debe verse a 1366 px y a 390 px |
| `referencia-inspiracion.jpg` | Anuncio de otra empresa que Brian vio. **Solo inspiración de estructura** (barra lateral oscura, medidor, niveles explicados). No copiar su marca, colores ni textos |

---

## 1. Objetivo

Pasar de un tema oscuro genérico a un **panel claro, tipo "puntaje"**, que responda en 5 segundos la pregunta del cliente: *"¿cómo voy y qué hago ahora?"*.

Qué se toma de la referencia:
1. Barra lateral oscura fija con marca, plan y navegación por tareas.
2. Franja superior de color + fila de datos de identificación (empresa, NIT, fecha de corte, avatar).
3. **Medidor semicircular** con la cifra grande y el nivel en palabras.
4. Bloque que **explica qué significa** la cifra y la escala de niveles con "Tu nivel" resaltado.

Qué se agrega (heurísticas de Jakob Nielsen):
- **Visibilidad del estado:** cifra + nivel + "te faltan N puntos".
- **Reconocer antes que recordar:** cada cifra trae su explicación al lado.
- **Llamado a la acción único y concreto** bajo el medidor ("Ver las N acciones que más suben tu puntaje").
- **"Lo que vence pronto"** con chips de color + texto (nunca solo color).

---

## 2. Sistema de diseño — versión 2 (23-oct-2026, reemplaza la v1 azul noche + ámbar)

Brian pidió algo "muy profesional, que no se vea hecho por IA" y basado en teoría del color. La v1 queda en `mockup-panel-v1.html` solo como historial.

### 2.1 Por qué estos colores
- **Los colores de seguridad ya tienen significado.** NTC 1461 / ISO 3864 asignan rojo = prohibición/peligro, amarillo = advertencia, verde = condición segura y azul = obligación. El usuario de SST los lee sin aprender nada. La interfaz los usa **solo con ese significado**: nunca un rojo decorativo.
- **Azul obligación es la marca.** El SG-SST es una obligación legal: el azul comunica deber, confianza y orden, y es el único color "de marca" (botones, enlace activo, logotipo).
- **Regla 60-30-10.** 60 % neutros grafito y blanco, 30 % superficies y texto, 10 % color (azul en acciones y semáforo en estados). Si una pantalla tiene más color que eso, sobra color.
- **Neutros grafito, no azul marino.** El grafito da el tono industrial y de herramienta. El azul queda libre para significar "acción".
- **Contraste AA.** El amarillo nunca se usa como texto sobre blanco: para texto va `amarillo-texto`.
- **Diferenciación.** El CRM Legal usa otra familia (verde botella y latón); los dos productos no deben confundirse.

### 2.2 Tokens
| Token | Valor | Uso |
|---|---|---|
| `grafito-900` | `#1d2125` | Barra lateral, títulos, aguja del medidor |
| `grafito-700` | `#33393f` | Texto de cuerpo secundario |
| `grafito-500` | `#5a636c` | Etiquetas y texto auxiliar |
| `linea` | `#dde1e5` | Bordes y reglas |
| `fondo` | `#f3f4f6` | Fondo de página |
| `superficie` | `#ffffff` | Paneles |
| `azul` / `azul-hover` / `azul-suave` | `#1b4f91` / `#163f74` / `#e8eef7` | Marca, botón primario, avatar |
| `rojo` | `#c62828` | Crítico, vencido |
| `amarillo` / `amarillo-texto` / `amarillo-suave` | `#f2b705` / `#7a5600` / `#fef6dc` | Moderado, vence pronto |
| `verde` | `#1e7b46` | Aceptable, a tiempo |

### 2.3 Tipografía
- **Barlow** para texto e interfaz y **Barlow Semi Condensed** para títulos y cifras. Su diseño viene de la señalización vial y de seguridad: encaja con SST y se lee bien en tablas densas. Google Fonts, pesos 400/500/600 y 500/600/700.
- Escala: 30 (h1) · 19 (h2) · 15 (cuerpo) · 13-14 (auxiliar). Cifras del medidor a 76 px. `font-variant-numeric: tabular-nums` en fechas y cifras.

### 2.4 Reglas de forma (para que no parezca plantilla)
- **Un solo protagonista:** el medidor. Lo demás es sobrio.
- **Sin tarjetas repetidas con sombra.** Paneles con borde de 1 px, radio de 8 px y sin sombra. Las cifras van en una franja con divisiones, no en cuatro tarjetas.
- **Sin degradados, sin etiquetas en MAYÚSCULAS, sin flechas "→" en los botones, sin emojis.** Textos en tipo oración.
- Los botones dicen exactamente lo que hacen ("Ver las 9 acciones pendientes").
- Iconos de Font Awesome solo donde ayudan a escanear; el menú puede ir sin iconos.

### 2.5 Implementación
1. **Propuesta:** dejar el CDN de Tailwind y compilar con el **binario standalone de Tailwind** (sin Node), con los tokens en `theme.extend.colors` y `fontFamily`. Salida en `app/static/css/app.css`, versionada; agregar el comando al `buildCommand` de `render.yaml`.
2. Alternativa para la fase 1: CDN con los tokens en el `tailwind.config` inline de `base.html`. Anotar la deuda.
3. Exponer los tokens también como variables CSS en `:root` (como la maqueta), para el SVG del medidor.

> **Ajustes del resto del documento con la v2:** donde la §3, la §4 y la §7 digan `marca-900`, `acento`, `texto` o `texto-2`, usar `grafito-900`, `azul`, `grafito-900` y `grafito-500`. La franja superior de color con degradado **se elimina**: el encabezado es blanco con el selector de empresa (ver la maqueta). El medidor lleva **aguja** y marcas en 60 y 85. Las cifras van en franja, no en tarjetas.

## 3. Estructura de pantalla (layout) — `app/templates/base.html`

```
┌──────────────┬──────────────────────────────────────────────┐
│ BARRA        │ Franja: Mis módulos ▾ · Próximo hito · Ayuda  │
│ LATERAL      ├──────────────────────────────────────────────┤
│ 248 px       │ Empresa | NIT | Última actualización | (AV)   │
│ marca-900    ├──────────────────────────────────────────────┤
│              │ <main> máx. 1100 px · flashes · contenido     │
└──────────────┴──────────────────────────────────────────────┘
```

**Barra lateral** (de arriba hacia abajo):
1. Logo "**Jus**trabajo" + subtítulo con el nombre y rol del usuario.
2. Insignia del plan (`Plan <nombre> · N módulos`; para consultor: `N/M empresas`).
3. Selector de empresa activa — **solo se muestra si el usuario tiene más de una empresa** (ver §6). Con una sola empresa no aparece.
4. Navegación agrupada: *(sin título)* Puntaje · Autoevaluación · Plan anual → **Gestión**: Reportes · EPP · Matriz legal · Controles · Jurídico · Formación → **Administración** (solo Admin): Usuarios y catálogos · Plan.
   - Cada ítem respeta el gating actual `{% if 'x' in modulos_activos %}`.
   - Ítem activo: fondo `acento`, texto `marca-900`, negrita. Determinarlo con `request.blueprint` (macro `nav_item(endpoint, icono, texto, modulo=None)`).
5. Abajo: "Cerrar sesión".

**Franja superior** (44 px, degradado `marca-800 → marca-700`): "Mis módulos ▾" (lleva a `admin.suscripcion` si es Admin; si no, a una página de módulos de solo lectura), **próximo hito normativo** (ver §5.6) y "Ayuda" (enlace a `admin/manual.html` o `mailto:` `[POR COMPLETAR]`).

**Fila de datos:** Empresa (razón social) · NIT · Última actualización (fecha del último cambio relevante, ver §5) · avatar con iniciales.

**Celular (< 860 px):**
- La barra lateral se oculta y se abre con un **botón hamburguesa** en la franja (drawer con overlay, se cierra con Esc y al tocar fuera). La maqueta solo la oculta: el drawer es obligatorio, sin él no hay navegación en celular.
- La fila de datos pasa a 2 columnas; los KPI a 2 columnas; el medidor no supera el ancho de pantalla.
- Sin scroll horizontal en ninguna pantalla a 360 px.

**Flashes:** mismo comportamiento de hoy, con colores claros (`critico`/`aceptable`/`marca-700` al 10 % de fondo y texto oscuro).

**Login y landing:** fuera del alcance de la fase 1 (la landing ya tiene diseño propio). `auth/login.html` extiende `base.html`: crear `base_publica.html` sin barra lateral para que no se rompa.

---

## 4. Panel principal — `dashboard/index.html` + `routes/dashboard.py`

Copiar la maqueta. Bloques en orden:

### 4.1 Encabezado
- `h1`: **"Así va tu SG-SST"**.
- Subtítulo: "Tu puntaje sale de la autoevaluación de la Res. 0312 de 2019 ({{ regimen }} estándares). Mejóralo cerrando las acciones pendientes."

### 4.2 Tarjeta "Tu puntaje" (medidor)
- Fuente: la `Autoevaluacion` más reciente (`order_by(anio.desc())`).
- Semicírculo de 0 a 100, con tres tramos fijos que siguen la clasificación de `app/data/estandares_0312.py`: **crítico < 60 · moderadamente aceptable 60-85 · aceptable > 85**.
- Marcador (círculo blanco con borde `marca-900`) en la posición del puntaje.
- **Fórmula del arco** (viewBox `0 0 220 130`, centro `(110,115)`, radio 90): para un puntaje `s`, ángulo `θ = 180° − 1,8·s`; punto `x = 110 + 90·cos θ`, `y = 115 − 90·sin θ`. Puntos de corte: 60 → `(137.8, 29.4)` · 85 → `(190.2, 74.1)`.
  - Hacer una **macro Jinja** `components/medidor.html` con parámetro `puntaje`, que calcule los puntos en Python (filtro o función en un `context_processor`), no en JS. Así sirve también para el PDF y el correo.
- Debajo: la cifra (52 px, 800), el **nivel en palabras** con su color de texto y "de 100 · autoevaluación {{ anio }}".
  - Si la autoevaluación está `EN_CURSO`: mostrar el puntaje con la etiqueta **"Provisional — autoevaluación en curso"** y el CTA "Continuar autoevaluación".
- **CTA:** "Ver las N acciones que más suben tu puntaje →" → `autoevaluacion.resultado` (o una vista nueva filtrada). N = ítems `NO_CUMPLE` de esa autoevaluación.
  - Orden de "las que más suben": por `puntaje` del ítem en `ESTANDARES` (mayor primero). Es una propuesta de priorización; mostrar el puntaje que suma cada ítem.
- Recuadro de definiciones (texto de la maqueta).
- `aria-label` en el SVG: "Puntaje {{ s }} de 100, nivel {{ nivel }}".

### 4.3 Tarjeta "Nivel de cumplimiento"
- Tres niveles con punto de color, rango y qué implica. El nivel actual va resaltado con `acento-suave` y la insignia "Tu nivel".
- "Te faltan N puntos para 'aceptable'": `N = ceil(85.01 − puntaje)`; si ya es aceptable, "Mantén el nivel".
- Los textos de "qué implica" de cada nivel son **propuesta** y deben revisarse contra el art. 28 de la Res. 0312 antes de publicar `[VERIFICAR]`.

### 4.4 Fila de 4 KPI
| KPI | Fuente | Subtexto |
|---|---|---|
| Acciones abiertas | `AccionMejora.estado != 'Cerrada'` | "N vencidas" (`fecha_limite < hoy`) |
| Reportes abiertos | consulta actual de `CondicionInsegura` | "de N este año" |
| Requisitos legales | `RequisitoLegal.query.count()` | "N actualizados este mes" (`fecha_actualizacion` en el mes) |
| Trabajadores | `Empresa.num_trabajadores` | "Régimen de {{ regimen_estandares }} estándares" |

Cada KPI es un enlace a su módulo, y solo se muestra si el módulo está activo. Si quedan menos de 4, la grilla se ajusta.

### 4.5 "Lo que vence pronto" (máx. 6 filas, ordenadas por fecha)
Unir en un servicio nuevo `app/services/vencimientos.py → proximos_vencimientos(limite=6)`:
- `PlanTrabajoActividad` no ejecutada → `fecha_programada`
- `AccionMejora` abierta → `fecha_limite`
- `EntregaEPP` → `fecha_reposicion`
- `Control` activo → `proximo_seguimiento`
- Hitos normativos (§5.6)

Chip: **Vencida** (`critico`) · **En N días** con N ≤ 30 (`moderado`) · **En N días** con N > 30 (`aceptable`). Cada fila enlaza a su registro. Estado vacío: "No tienes vencimientos en los próximos 90 días."

### 4.6 Estados vacíos (obligatorios)
- **Sin autoevaluación:** el medidor se ve en gris con "—" y el texto "Aún no tienes puntaje. Haz la autoevaluación (15-30 min) para ver dónde estás." + botón "Empezar autoevaluación".
- **Módulo de autoevaluación no contratado:** tarjeta con candado "Activa el módulo de autoevaluación para ver tu puntaje" → `admin.suscripcion`.

---

## 5. Datos y servicios nuevos

1. `app/services/panel.py → datos_panel(empresa)`: devuelve un dict con todo lo del §4 y deja `routes/dashboard.py` delgado. Con pruebas unitarias.
2. `app/services/vencimientos.py` (§4.5).
3. Macro `components/medidor.html` + función `puntos_arco(s)`.
4. Macro `components/nav_item.html`, `components/kpi.html`, `components/chip.html`, `components/tarjeta.html`.
5. `Empresa.ultima_actualizacion` (propiedad, sin columna nueva): la fecha más reciente entre la autoevaluación, los reportes y los requisitos.
6. `app/data/hitos_normativos.py`: lista versionada `(codigo, nombre, regla_fecha, modulo, norma)`. Iniciales, **todas con `[VERIFICAR]` hasta que Brian confirme la fuente**:
   - Reporte anual del PESV: ventana del 6 al 31 de enero (Circ. 0034/2026, según `CONTEXTO.md` §4).
   - Registro de la autoevaluación en la plataforma SGRL: hasta el 31 de julio (Circ. 027/2026, según `CONTEXTO.md` §4).
   - La franja muestra el próximo hito aplicable a los módulos activos.

No hay columnas nuevas en la fase 1. Si alguna resulta necesaria: mini-migración aditiva en `scripts/init_prod_db.py` (regla dura 6).

---

## 6. Consola del consultor (multiempresa) — fase 2

Es lo que convierte el rediseño en el producto que se arrienda a consultores (decisión del 23-oct: SST general para arrendar). Está en el roadmap (`CONTEXTO.md` §3, ítem 3).

- Modelos nuevos **sin `TenantMixin`** porque cruzan tenants (regla dura 8): `Consultor` (usuario, plan, tope de empresas) y `ConsultorEmpresa` (consultor_id, empresa_id, rol, activo).
- `init_tenancy._resolver_tenant`: si el usuario es consultor, usar `session['empresa_activa']` **solo si** existe un `ConsultorEmpresa` activo para esa empresa. Si no, la `empresa_id` propia. Prueba de aislamiento obligatoria en `tests/test_aislamiento_tenants.py`: un consultor no puede abrir una empresa que no tiene asignada, ni cambiando el parámetro.
- Selector de empresa en la barra lateral: POST con CSRF a `/consola/empresa-activa`.
- Vista "Todas mis empresas": tabla con razón social, puntaje (minimedidor o barra), nivel, acciones vencidas y próximo vencimiento, ordenable por "más urgente". Es la pantalla que más vende a consultores.
- Insignia del plan: "Plan Consultor · N/M empresas"; al llegar al tope, aviso y enlace a mejorar plan.
- **Marca blanca (fase 3, no ahora):** logo y color de acento por consultor.

---

## 7. Migración del resto de plantillas (76 en total)

Al pasar `base.html` a tema claro, las demás plantillas quedan con texto blanco sobre fondo claro. Se migran todas en la misma rama, **antes de hacer merge**.

Tabla de equivalencias (aplicar con un script de reemplazo y luego revisar a mano cada pantalla):

| Hoy (oscuro) | Ocurrencias | Nuevo (claro) |
|---|---:|---|
| `text-white` | 478 | `text-grafito-900` — **ojo:** dentro de botones primarios se queda `text-white` |
| `text-slate-300` | 162 | `text-grafito-700` |
| `text-slate-400` | 280 | `text-grafito-500` |
| `text-slate-500` | 123 | `text-grafito-500` |
| `bg-slate-800`, `bg-slate-800/60` | 161 | `bg-superficie` + `border border-linea` (sin sombra) |
| `bg-slate-900` | 120 | `bg-fondo` |
| `border-slate-700` | 195 | `border-linea` |
| `bg-white/5`, `hover:bg-white/10` | 27 | `bg-fondo`, `hover:bg-fondo` |
| clases `glass*` de `static/css/style.css` | 90 | reescribir en `style.css` como tarjeta clara |
| `text-amber-400` | — | `text-amarillo-texto` |
| `text-emerald-400` / `text-red-400` | — | `text-verde` / `text-rojo` |

Orden: `base.html` → `dashboard` → `autoevaluacion` → `sgsst` → `epp` → `reportes` → `matriz_legal` → `controles` → `juridico` → `formacion` → `admin/*` (tiene su propio `base.html`: unificarlo con el layout nuevo).

Una vez convertidas, quitar `class="dark"` de `<html>` y `darkMode` de la configuración. Modo oscuro: fuera de alcance.

---

## 8. Accesibilidad (WCAG 2.1 AA)

- Contraste ≥ 4,5:1 en texto normal. Sobre blanco, el amarillo `#f0a020` **no** pasa: para texto usar `moderado-texto` (`#a86a00`).
- El nivel nunca depende solo del color: siempre el texto "Crítico / Moderadamente aceptable / Aceptable".
- Navegable con teclado: foco visible (anillo `acento` de 2 px), drawer con Esc, `aria-current="page"` en el ítem activo.
- Áreas táctiles ≥ 44 px en celular.
- `lang="es"`, títulos jerárquicos (un solo `h1` por pantalla).

---

## 9. Criterios de aceptación (definición de terminado)

1. El panel a 1366 px y a 390 px coincide con `captura-escritorio.png` y `captura-movil.png` (mismas secciones, orden y textos; los datos son reales).
2. Las 76 plantillas renderizan sin texto invisible: script de Playwright que recorre todas las rutas GET con el usuario `admin@sst.local`, toma capturas en `rediseno-ui/capturas-qa/` y **falla si hay un error 500**. Revisar las capturas una por una.
3. Estados vacíos (§4.6) verificados con una empresa nueva sin datos.
4. Pruebas nuevas: `tests/test_panel.py` (puntos del arco en 0, 60, 72, 85 y 100; nivel y "te faltan N"; vencimientos ordenados y limitados; KPI ocultos sin módulo) y, en la fase 2, aislamiento del consultor.
5. `pytest tests/ -q` en verde (46 pruebas actuales + nuevas) y arranque limpio con `SCHEDULER_ENABLED=0`.
6. Lighthouse en el panel: accesibilidad ≥ 90.
7. Sin colores sueltos nuevos en plantillas (grep de `#[0-9a-f]{6}` en `templates/` sin resultados nuevos).
8. `CONTEXTO.md` actualizado (§3, §8, bitácora) y `python _sistema/cerebro.py` ejecutado desde `empresa/`.

---

## 10. Orden de trabajo sugerido (una rama por fase)

| Fase | Rama | Contenido | Esfuerzo estimado (propuesta) |
|---|---|---|---|
| UI-0 | `ui/tokens` | Tokens, Tailwind compilado (o CDN con tokens), componentes Jinja | 0,5 día |
| UI-1 | `ui/layout-panel` | `base.html` nuevo + drawer móvil + panel completo + servicios + pruebas | 1,5 días |
| UI-2 | `ui/migracion-plantillas` | Las 76 plantillas + QA con Playwright | 2 días |
| UI-3 | `ui/consola-consultor` | §6 completo con pruebas de aislamiento | 2-3 días |

UI-0 a UI-2 pueden ir en un solo PR si se revisan las capturas. UI-3 va aparte porque toca el aislamiento de tenants.

---

## 11. Decisiones pendientes de Brian (no bloquean UI-0 a UI-2)

| # | Decisión | Propuesta de Claude |
|---|---|---|
| D-UI1 | Nombre en pantalla: Justrabajo o Cumplia (`CONTEXTO.md` §1) | Seguir con **Justrabajo** en la UI; los tokens hacen barato cambiarlo |
| D-UI2 | Paleta | **Resuelta en v2** (23-oct): colores de seguridad NTC 1461 con azul obligación como marca |
| D-UI3 | ¿Se elimina el modo oscuro? | Sí por ahora; se puede volver con los mismos tokens |
| D-UI4 | Textos de "qué implica cada nivel" | Revisarlos contra el art. 28 de la Res. 0312 |
| D-UI5 | Enlace de "Ayuda" | WhatsApp de soporte o correo de la S.A.S. cuando exista |

## 12. Lo que no se hace en este rediseño
- No se toca la lógica de cálculo de la autoevaluación ni la matriz legal.
- No se cambian modelos existentes ni el esquema de BD (solo en UI-3, modelos nuevos de consultor).
- No se copian marca, logo, colores ni textos del anuncio de referencia.
- No se usa el `venv/` ni secretos del `.env`.
