# `empresa/` — Todo lo necesario para constituir la sociedad y empezar a facturar

Carpeta de trabajo, no de lectura. Cada archivo es una plantilla que se llena, un
trámite que se marca, o una pieza que se publica.

**Perfil para el que está escrita:** un solo fundador, con empleo de tiempo completo,
presupuesto de arranque **inferior a $1.000.000 COP**, que constituye **una sola S.A.S.**
que opera como plataforma de cumplimiento empresarial (SG-SST, SAGRILAFT/PTEE y
servicios legales) en modelo de suscripción.

> Esta carpeta **reemplaza para efectos operativos** el plan de `docs/04-empresa/`, que
> asumía dos sociedades y ~$6,8M de arranque. Aquel documento sigue siendo válido como
> referencia técnica y como destino a 12–18 meses; este es el camino que se puede
> ejecutar este mes. Las diferencias están explicadas en
> [`00-GUIA-PASO-A-PASO.md`](00-GUIA-PASO-A-PASO.md) §0.

---

## Cómo usar esta carpeta

1. Lee **[`00-GUIA-PASO-A-PASO.md`](00-GUIA-PASO-A-PASO.md)** de principio a fin una vez. Son 5 fases y ~3 semanas de calendario, con unas 12 horas de trabajo real.
2. Decide el nombre en [`01-constitucion/00-decision-nombre-y-objeto.md`](01-constitucion/00-decision-nombre-y-objeto.md). Todo lo demás depende de eso.
3. Ejecuta fase por fase. No saltes: hay dependencias estrictas (sin NIT no hay RUT, sin RUT no hay habilitación de facturador).

---

## Índice

### 01 · Constitución
| Archivo | Qué es |
|---|---|
| [`00-decision-nombre-y-objeto.md`](01-constitucion/00-decision-nombre-y-objeto.md) | Shortlist de razones sociales, verificación de homonimia, objeto y CIIU |
| [`01-documento-privado-constitucion.md`](01-constitucion/01-documento-privado-constitucion.md) | **Plantilla lista para llenar** — estatutos completos de S.A.S. unipersonal |
| [`02-actas-y-aceptaciones.md`](01-constitucion/02-actas-y-aceptaciones.md) | Cartas de aceptación de cargo, plantilla de acta y formato del libro de accionistas |
| [`03-tramite-ccb-en-linea.md`](01-constitucion/03-tramite-ccb-en-linea.md) | El trámite en la CCB, pantalla por pantalla, con costos |

### 02 · DIAN y facturación electrónica
| Archivo | Qué es |
|---|---|
| [`01-rut-y-responsabilidades.md`](02-dian-y-facturacion/01-rut-y-responsabilidades.md) | Códigos exactos a inscribir y por qué |
| [`02-decision-iva-y-regimen.md`](02-dian-y-facturacion/02-decision-iva-y-regimen.md) | Las dos decisiones que no se pueden deshacer barato |
| [`03-habilitacion-facturador-electronico.md`](02-dian-y-facturacion/03-habilitacion-facturador-electronico.md) | De cero a primera factura validada, paso a paso |
| [`04-proveedores-comparativa.md`](02-dian-y-facturacion/04-proveedores-comparativa.md) | Qué proveedor tecnológico usar con $0 de presupuesto |

### 03 · Legal del producto
| Archivo | Qué es |
|---|---|
| [`01-terminos-y-condiciones.md`](03-legal-producto/01-terminos-y-condiciones.md) | Contrato de licencia SaaS, redactado y listo para publicar |
| [`02-politica-tratamiento-datos.md`](03-legal-producto/02-politica-tratamiento-datos.md) | Política Ley 1581, con anexo de encargo (DPA) |
| [`03-avisos-y-autorizaciones.md`](03-legal-producto/03-avisos-y-autorizaciones.md) | Aviso de privacidad y autorización reforzada para datos de salud |
| [`04-cesion-derechos-y-nda.md`](03-legal-producto/04-cesion-derechos-y-nda.md) | Cesión de derechos patrimoniales y acuerdo de confidencialidad |
| [`05-registro-software-dnda.md`](03-legal-producto/05-registro-software-dnda.md) | Registro del código en la DNDA — gratuito, 15 días |

### 04 · Programa de afiliados SST
| Archivo | Qué es |
|---|---|
| [`01-diseno-del-programa.md`](04-programa-afiliados/01-diseno-del-programa.md) | Economía de las comisiones, reglas, niveles y anti-fraude |
| [`02-contrato-de-referidos.md`](04-programa-afiliados/02-contrato-de-referidos.md) | Contrato de corretaje mercantil, listo para firmar |
| [`03-especificacion-tecnica.md`](04-programa-afiliados/03-especificacion-tecnica.md) | Modelo de datos, atribución y liquidación para implementar en Flask |
| [`04-kit-de-reclutamiento.md`](04-programa-afiliados/04-kit-de-reclutamiento.md) | Cómo conseguir los primeros 10 afiliados, con mensajes escritos |

### 05 · Marketing y lanzamiento
| Archivo | Qué es |
|---|---|
| [`01-identidad-de-marca.md`](05-marketing/01-identidad-de-marca.md) | Logo, paleta, tipografía y reglas de uso |
| [`02-mensajes-y-propuesta-de-valor.md`](05-marketing/02-mensajes-y-propuesta-de-valor.md) | Qué decimos, a quién, y qué **no** decimos |
| [`03-plan-de-lanzamiento-8-semanas.md`](05-marketing/03-plan-de-lanzamiento-8-semanas.md) | Calendario editorial con fechas y responsables |
| [`04-copies-linkedin.md`](05-marketing/04-copies-linkedin.md) | 16 publicaciones escritas, listas para copiar y pegar |
| [`05-copies-facebook.md`](05-marketing/05-copies-facebook.md) | 12 publicaciones + estrategia de grupos |
| [`06-guiones-youtube.md`](05-marketing/06-guiones-youtube.md) | 6 guiones completos, con estructura, miniatura y descripción |
| [`assets/`](05-marketing/assets/) | Logos, banners, plantillas de post y miniaturas en PNG y SVG |

### 06 · Dinero y fechas
| Archivo | Qué es |
|---|---|
| [`01-presupuesto-de-arranque.md`](06-costos-y-calendario/01-presupuesto-de-arranque.md) | El presupuesto real, línea por línea, bajo $1.000.000 |
| [`02-calendario-de-obligaciones.md`](06-costos-y-calendario/02-calendario-de-obligaciones.md) | Qué se vence y cuándo, para los próximos 12 meses |

---

## Antes de firmar o publicar — verificaciones pendientes

Este paquete pasó por una revisión adversarial que encontró y corrigió varios errores de
derecho. Lo que quedó **abierto** está listado aquí, en orden de daño potencial. Ninguna de
estas se resuelve leyendo: hay que ir a la fuente.

| # | Qué verificar | Dónde | Por qué importa |
|---|---|---|---|
| 1 | **Homonimia del nombre** en el RUES y marcas en SIPI | https://www.rues.org.co · https://sipi.sic.gov.co | Bloquea la constitución y todo lo demás |
| 2 | **¿Aplica la responsabilidad 59** (autorretención especial de renta) con cero empleados? | Contador, antes de la primera factura | Si aplica, se autorretiene desde la primera factura. Es el error tributario más caro y más silencioso de esta ruta |
| 3 | **Plazo del RUB** (beneficiarios finales, Res. DIAN 000164/2021) | Resolución vigente | Sanción del art. 658-3 ET, que se acumula |
| 4 | **Umbrales de SAGRILAFT** y sectores del régimen de medidas mínimas | Circular Básica Jurídica de Supersociedades | Va en piezas de LinkedIn, Facebook y YouTube. Un dato mal aquí destruye lo único que nos diferencia |
| 5 | **Circulares 0034 y 027 de 2026** (fechas de PESV y autoevaluación) | Fuente oficial | Sostienen el calendario comercial completo |
| 6 | **¿La solución gratuita de la DIAN emite documento soporte?** | Portal DIAN, 10 minutos | Si no, hay que presupuestar un proveedor desde la primera comisión de aliado |
| 7 | **Momento de causación de la factura** en un modelo de suscripción | Contador | "No factures hasta que te paguen" es un consejo equivocado y sancionable |
| 8 | **Tarifas de retención** sobre comisiones (y si eres agente de retención de ICA) | Contador | Determina la primera liquidación de aliados |
| 9 | **Riesgo de recalificación como agencia comercial** del contrato de aliados | Abogado mercantilista | Prestación del art. 1324 C.Co |
| 10 | **Tarifa de matrícula de la CCB** con el capital elegido | Simulador de la CCB | Es la cifra más grande del presupuesto |

---

## Convención de marcado

- **[NE]** — dato **no verificado** en fuente primaria. No usarlo en material comercial ni en una declaración sin confirmar.
- **[LLENAR]** — campo que tú debes completar antes de usar el documento.
- **[DECIDIR]** — decisión pendiente que bloquea el paso siguiente.

Valores base usados en toda la carpeta (agosto 2026):
**SMMLV $1.750.905** · **UVT $52.374** · **UVB (cámaras de comercio) $12.110** · **SMDLV $58.363**

---

## Lo primero, mañana

Tres cosas, en este orden, y ninguna cuesta dinero:

1. **Verificar el nombre en el RUES** (https://www.rues.org.co) y en SIPI (https://sipi.sic.gov.co). Sin esto, todo lo demás está en el aire → [`01-constitucion/00-decision-nombre-y-objeto.md`](01-constitucion/00-decision-nombre-y-objeto.md) §3
2. **Reservar dominio y usuarios de redes** el mismo día que el nombre pase la verificación
3. **Revocar el Personal Access Token de GitHub** expuesto en la URL del remoto y pasar a SSH. Es lo único de todo el plan que no admite espera → [`../docs/03-arquitectura/02-despliegue-git-render.md`](../docs/03-arquitectura/02-despliegue-git-render.md)
