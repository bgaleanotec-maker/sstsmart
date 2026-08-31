# Identidad de marca — Cumplia

> **Propuesta, no decisión tomada.** El nombre `Cumplia` está sujeto a la verificación de
> homonimia en el RUES → [`../01-constitucion/00-decision-nombre-y-objeto.md`](../01-constitucion/00-decision-nombre-y-objeto.md).
> Si cambia el nombre, **todas las piezas se regeneran en un minuto**: el script
> [`assets/generar-piezas.py`](assets/generar-piezas.py) tiene el texto de la marca en un
> solo lugar.

---

## 1. Principios de diseño

Los criterios son los de Jakob Nielsen, aplicados a piezas de marca:

1. **Visibilidad del estado del sistema.** Cada pieza dice de qué se trata en la primera línea. Nada de titulares de intriga.
2. **Correspondencia con el mundo real.** El vocabulario es el del jefe de SST y del gerente de pyme: "autoevaluación", "matriz legal", "reporte PESV". No "sinergia", no "transformación digital".
3. **Consistencia y estándares.** Un solo azul, un solo verde, una sola tipografía, una sola estructura de pieza. La consistencia es lo que hace que se reconozca la marca antes de leer el nombre.
4. **Diseño estético y minimalista.** *"Toda unidad de información extra compite con las unidades relevantes y disminuye su visibilidad relativa."* En estas piezas: un dato por imagen.
5. **Reconocer antes que recordar.** El logo en la misma posición siempre; el color de acento con un solo significado (verde = cumplido, ámbar = plazo, rojo = sanción).

---

## 2. El nombre y la arquitectura de marca

```
              CUMPLIA S.A.S.          ← razón social
                    │
                 Cumplia              ← marca, dominio, logo
                    │
   ┌────────────┬───┴────────┬─────────────────┐
Cumplia SST  Cumplia PESV  Cumplia SAGRILAFT  Cumplia Legal
```

**Descriptor:** *Cumplimiento empresarial, en una sola plataforma.*
**Descriptor largo:** *SG-SST · PESV · SAGRILAFT · Acompañamiento jurídico.*

---

## 3. Logo

| Archivo | Uso |
|---|---|
| [`assets/logo-horizontal.png`](assets/logo-horizontal.png) · [`.svg`](assets/logo-horizontal.svg) | Uso principal sobre fondo claro |
| [`assets/logo-horizontal-blanco.png`](assets/logo-horizontal-blanco.png) · [`.svg`](assets/logo-horizontal-blanco.svg) | Sobre fondo azul o fotografía oscura |
| [`assets/logo-vertical.png`](assets/logo-vertical.png) | Espacios cuadrados: presentaciones, sellos |
| [`assets/isotipo-1024.png`](assets/isotipo-1024.png) · [`.svg`](assets/isotipo.svg) | Sin el nombre: favicon, app, avatar |
| [`assets/avatar-400.png`](assets/avatar-400.png) | Foto de perfil de redes |
| [`assets/favicon-512.png`](assets/favicon-512.png) | Favicon del sitio |

**El símbolo:** un visto de bordes redondeados dentro de un arco abierto. El arco no cierra
—el cumplimiento es un proceso continuo, no un estado alcanzado— y su apertura inferior deja
el visto respirando. Funciona a 16 px porque el visto es la única forma que hay que leer.

### Reglas de uso

- **Área de protección:** un espacio libre alrededor equivalente a la altura del isotipo ÷ 2.
- **Tamaño mínimo:** logo horizontal 120 px de ancho · isotipo 24 px.
- **Fondos permitidos:** blanco, niebla (#F4F7F9), azul Cumplia (#103C57) y azul profundo (#0A2638). Sobre fotografía, solo la versión blanca y con una capa oscura al 55% detrás.

### Lo que no se hace

Deformar o cambiar proporciones · rotar · recolorear el isotipo con colores fuera de la
paleta · agregar sombras, degradados o contornos · poner el logo sobre fondos de color medio
donde pierde contraste · escribir el nombre con otra tipografía · usar el isotipo y el
wordmark separados por un espacio distinto al del archivo.

---

## 4. Paleta

Vista en [`assets/paleta-de-color.png`](assets/paleta-de-color.png).

| Rol | Nombre | HEX | RGB | Uso |
|---|---|---|---|---|
| **Primario** | Azul Cumplia | `#103C57` | 16, 60, 87 | Logo, títulos, botones primarios |
| Primario oscuro | Azul profundo | `#0A2638` | 10, 38, 56 | Fondos de pieza, encabezados |
| Primario claro | Azul claro | `#2B6E96` | 43, 110, 150 | Enlaces, estados hover |
| **Acento** | Verde cumplido | `#16A97C` | 22, 169, 124 | Confirmación, "al día", CTA secundario |
| Alerta | Ámbar plazo | `#E9A020` | 233, 160, 32 | Vencimientos próximos |
| Crítico | Rojo sanción | `#D14738` | 209, 71, 56 | Incumplimiento, riesgo alto |
| Texto | Tinta | `#0C1A24` | 12, 26, 36 | Cuerpo sobre fondo claro |
| Texto sec. | Pizarra | `#5B7080` | 91, 112, 128 | Texto secundario, metadatos |
| Borde | Línea | `#DDE5EB` | 221, 229, 235 | Divisores, bordes de tarjeta |
| Fondo | Niebla | `#F4F7F9` | 244, 247, 249 | Fondo de aplicación |

**El color tiene significado y no se usa decorativamente.** Verde = cumplido. Ámbar = por
vencer. Rojo = vencido o sancionable. Si el verde aparece en un gráfico solo porque quedaba
bonito, el usuario deja de creerle al verde.

**Accesibilidad.** Todas las combinaciones de texto sobre fondo de las piezas superan la
relación de contraste **4.5:1** de WCAG AA. **Nunca uses ámbar sobre blanco para texto**: no
alcanza. Ámbar solo sobre azul profundo, o como relleno de forma.

---

## 5. Tipografía

**Inter** para todo. Gratuita, de licencia abierta, diseñada para pantalla, con números
tabulares —importante en una plataforma que muestra fechas, porcentajes y cifras alineadas
en tablas—.

Descarga: https://rsms.me/inter/ · En Google Fonts: `Inter`.

| Uso | Peso | Tamaño de referencia |
|---|---|---|
| Titular de pieza | Black (900) | 72–92 px |
| Título de sección | Bold (700) | 40–58 px |
| Antetítulo / etiqueta | ExtraBold (800), MAYÚSCULAS, +2% de espaciado | 28–34 px |
| Cuerpo | Regular (400) | 32–36 px en piezas · 16 px en web |
| Metadatos | Medium (500) | 26–30 px |

**Alternativa si Inter no está disponible:** Poppins para titulares y Arial/Helvetica para
cuerpo. **Nunca** tipografías con serifas ni manuscritas: el sector está lleno de material
que parece hecho en Word y la diferencia se nota de inmediato.

---

## 6. Estructura de las piezas

Todas siguen la misma retícula, y esa repetición es lo que construye reconocimiento:

```
┌─────────────────────────────────┐
│                                 │  margen 80 px
│  ANTETÍTULO EN MAYÚSCULAS       │  ← ámbar o verde según el tema
│                                 │
│  Titular de una sola idea,      │  ← Black, máximo 3 líneas
│  en dos o tres líneas.          │
│  ▬▬▬                            │  ← barra de acento
│  Cuerpo explicativo, dos o      │  ← Regular, máximo 4 líneas
│  tres frases. Sin adornos.      │
│                                 │
│  [logo]              cumplia.co │
└─────────────────────────────────┘
```

**Una idea por pieza.** Si hay dos datos que valen la pena, son dos piezas.

---

## 7. Piezas listas

### Perfiles y portadas

| Archivo | Dónde va | Medidas |
|---|---|---|
| [`avatar-400.png`](assets/avatar-400.png) | Foto de perfil en LinkedIn, Facebook y YouTube | 400×400 |
| [`linkedin-portada-pagina-1128x191.png`](assets/linkedin-portada-pagina-1128x191.png) | Portada de la **página de empresa** en LinkedIn | 1128×191 |
| [`linkedin-portada-personal-1584x396.png`](assets/linkedin-portada-personal-1584x396.png) | Portada de **tu perfil personal** | 1584×396 |
| [`facebook-portada-1640x624.png`](assets/facebook-portada-1640x624.png) | Portada de la página de Facebook | 1640×624 |
| [`youtube-banner-2560x1440.png`](assets/youtube-banner-2560x1440.png) | Banner del canal. **Todo lo importante está dentro del área segura central de 1546×423** | 2560×1440 |

### Publicaciones

| Archivo | Tema |
|---|---|
| [`post-01-uvt.png`](assets/post-01-uvt.png) | Las multas se liquidan en UVT, no en salarios mínimos |
| [`post-02-autoevaluacion.png`](assets/post-02-autoevaluacion.png) | 31 de julio: autoevaluación en SGRL |
| [`post-03-pesv.png`](assets/post-03-pesv.png) | 6 al 31 de enero: reporte PESV |
| [`post-04-aliados.png`](assets/post-04-aliados.png) | Programa de aliados: 20% de comisión |
| [`post-05-precio.png`](assets/post-05-precio.png) | Precio público, prueba de 14 días (versión clara) |
| [`post-vertical-01-aliados.png`](assets/post-vertical-01-aliados.png) | Aliados, formato vertical |
| [`post-vertical-02-sagrilaft.png`](assets/post-vertical-02-sagrilaft.png) | Umbrales de SAGRILAFT |

### Miniaturas de YouTube

| Archivo | Video |
|---|---|
| [`youtube-miniatura-01-multas.png`](assets/youtube-miniatura-01-multas.png) | ¿Cuánto cuesta una multa de SG-SST? |
| [`youtube-miniatura-02-autoevaluacion.png`](assets/youtube-miniatura-02-autoevaluacion.png) | Autoevaluación 0312 en SGRL, paso a paso |
| [`youtube-miniatura-03-pesv.png`](assets/youtube-miniatura-03-pesv.png) | ¿Su empresa está obligada al PESV? |

---

## 8. Cómo generar piezas nuevas

```bash
cd empresa/05-marketing/assets
pip install pillow
python generar-piezas.py
```

Para una publicación nueva, agrega una línea al final del script:

```python
save(post_cuadrado(
    "ANTETÍTULO",
    "El titular, una sola idea.",
    "Dos o tres frases de contexto.",
    color_kicker=AMBAR),          # VERDE | AMBAR | ROJO
    "post-06-mi-tema.png")
```

**Para cambiar el nombre de la marca:** busca `"cumplia"` en el script — está en
`logo_horizontal()` y `logo_vertical()`. Cambiarlo regenera los 23 archivos.

**Para cambiar la paleta:** el bloque `# Paleta` al inicio del script.

---

## 9. Voz

| Sí | No |
|---|---|
| "El plazo vence el 31 de julio" | "¡No te quedes atrás en tu transformación digital!" |
| "Las multas se liquidan en UVT desde 2022" | "Evita multas millonarias" |
| "Solo 5 de 25 plataformas publican precio. Nosotros sí" | "Somos la solución líder del mercado" |
| "No certificamos su cumplimiento. Le damos la herramienta para gestionarlo" | "Garantizamos su cumplimiento al 100%" |
| Cifras con fuente y fecha | Cifras redondas sin origen |

**La regla de fondo:** el sector está saturado de material que exagera y que además tiene
datos desactualizados (multas en salarios mínimos, resoluciones derogadas, la exención de
economía naranja que ya no existe). **Ser el que dice el dato correcto, con la norma y la
fecha, es la posición más barata y más difícil de copiar que tienes disponible.**
