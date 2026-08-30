# Datos personales, propiedad intelectual y contratos

> Verificado a agosto de 2026. **UVT 2026 = $52.374** · SMMLV = $1.750.905.

---

## 1. Habeas data — Ley 1581 de 2012

**Estado normativo:** el proyecto de ley 274/2025C que reformaba la Ley 1581 (radicado el 27-ago-2025, aprobado en primer debate el 28-oct-2025) fue **ARCHIVADO** conforme al art. 190 de la Ley 5 de 1992. **No hay reforma vigente: la Ley 1581 sigue tal cual**, junto con el Decreto 1377 de 2013 (compilado en el Decreto 1074 de 2015).

### 1.1 Obligaciones que no dependen de tu tamaño

- **Política de Tratamiento de Información** publicada y accesible
- **Aviso de privacidad** en el momento de la recolección
- **Autorización previa, expresa e informada** del titular, con prueba conservable
- Canal y procedimiento de consultas y reclamos: **15 días hábiles** para consultas; **15 días hábiles** para reclamos, prorrogables 8
- Medidas de seguridad técnicas, humanas y administrativas
- Designar un área o responsable de protección de datos

### 1.2 RNBD — la buena noticia

Están obligadas a registrar bases de datos en el **Registro Nacional de Bases de Datos** de la SIC:
- las personas jurídicas **públicas**, y
- las sociedades y ESAL **privadas con activos totales superiores a 100.000 UVT = $5.237.400.000**.

> **Tu SaaS temprana casi con certeza NO está obligada al RNBD.** El Gobierno redujo el universo de obligados precisamente por esto. **Pero sigues obligado a todo lo de §1.1** — la exención es solo del registro en la plataforma.

Si algún día superas el umbral: bases nuevas → registro en **2 meses** · actualización anual por cambios no sustanciales → **2 de enero a 31 de marzo** · cambios sustanciales → primeros **10 días hábiles** del mes siguiente · **reporte semestral de reclamos** → 20 de febrero y 25 de agosto · **incidentes de seguridad → 15 días hábiles** desde la detección.

**Sanciones de la SIC:** hasta **2.000 SMMLV = $3.501.810.000** (2026), más cierre temporal o definitivo de las operaciones de tratamiento.

---

## 2. Tu posición: eres ENCARGADO, no responsable

Cuando una pyme cliente carga en la plataforma los exámenes médicos ocupacionales de sus empleados:

| Rol | Quién | Qué significa |
|---|---|---|
| **Responsable** | La empresa cliente | Decide la finalidad y los medios del tratamiento |
| **Encargado** | **SST Smart** | Trata los datos por cuenta del responsable |

El paso de datos del cliente a ti es una **TRANSMISIÓN** (no transferencia), y el **art. 25 del Decreto 1377/2013 exige un contrato de transmisión de datos personales** que estipule: alcance, finalidades, obligaciones del encargado (aplicar la política del responsable, garantizar seguridad, tramitar consultas, **devolver o suprimir los datos al terminar**), y prohibición de usarlos para fines propios.

> **Consecuencia comercial directa:** ese contrato debe estar **dentro de tus Términos y Condiciones o como anexo (DPA) firmado con cada cliente**. Sin él, tú y tu cliente están ambos expuestos — y todo comprador mediano te lo va a pedir en la due diligence.

### 2.1 La trampa del benchmarking

Si usas los datos de los empleados de tus clientes para **entrenar modelos, generar benchmarks sectoriales o cualquier finalidad propia**, dejas de ser encargado y **te conviertes en responsable**, con todo el régimen de autorizaciones directas encima.

El roadmap contempla benchmarking anónimo entre empresas del mismo sector (T7–T8). Para hacerlo sin cambiar de rol necesitas **anonimización irreversible** — no seudonimización, no "quitar el nombre" — o autorización específica de cada titular. **Consúltalo antes de construirlo, no después.**

---

## 3. Datos sensibles de salud ocupacional

Exámenes médicos ocupacionales e incapacidades son **datos sensibles** (art. 5 Ley 1581: datos relativos a la salud). Régimen reforzado:

- **Autorización explícita** del titular, **informándole que no está obligado a autorizar** datos sensibles (art. 6 Ley 1581 y art. 6 Decreto 1377/2013)
- **Prohibido condicionar** una actividad al suministro de datos sensibles
- Medidas de seguridad reforzadas y **trazabilidad de accesos**
- Es dato de **circulación restringida**

### 3.1 Lo que esto obliga en el diseño del producto

| Requisito | Implementación |
|---|---|
| Cifrado en reposo y en tránsito | TLS de Render + **cifrado a nivel de columna** para diagnósticos y restricciones, con clave distinta de `SECRET_KEY` |
| Control de acceso por rol | El módulo de exámenes médicos no es visible para todos los roles |
| Log de auditoría de cada consulta | Tabla append-only: quién vio qué historia ocupacional y cuándo |
| **Separación aptitud / diagnóstico** | El empleador ve el **concepto de aptitud** (apto / apto con restricciones / no apto). **No ve el diagnóstico clínico.** Es una regla de modelo de datos |
| Retención limitada | Política de retención documentada y ejecutada |
| Captura auditable de la autorización | El producto la almacena; no se da por supuesta |

Detalle técnico en [`../03-arquitectura/03-seguridad-y-cumplimiento.md`](../03-arquitectura/03-seguridad-y-cumplimiento.md).

---

## 4. Transferencia internacional — Render está en EE.UU.

La **Circular Externa 005 de 2017 de la SIC** lista los países con nivel adecuado de protección. **Estados Unidos ESTÁ en esa lista** (junto con los Estados miembros de la UE, Reino Unido, Costa Rica, México, Perú, Corea del Sur, Islandia, Noruega y Serbia — 35 países en total).

> **Conclusión operativa: alojar en Render con región en EE.UU. no requiere declaración de conformidad ante la SIC.** Es una transferencia a país con nivel adecuado.

**Pero cumple igual:**

1. **Verifica la región real de tus servicios:**

| Región de Render | País | ¿Nivel adecuado? |
|---|---|---|
| Virginia, Ohio, Oregon | EE.UU. | ✅ Sí |
| Frankfurt | Alemania | ✅ Sí |
| **Singapur** | Singapur | ❌ **NO está en la lista** |

Si usaras Singapur o cualquier destino no listado, necesitarías invocar una excepción del art. 26 (consentimiento expreso e inequívoco del titular, o ejecución del contrato) o presentar **declaración de conformidad** ante la SIC.

2. **Declara los destinos internacionales** en tu Política de Tratamiento.
3. **Principio de responsabilidad demostrada:** contrato con Render (solicita el DPA vía "Request Documents" en el dashboard y **guárdalo**), evidencia de medidas de seguridad, y **registro de subencargados**.
4. **Lo mismo aplica a todo tu stack**: proveedor de email (Resend), analítica (PostHog), LLMs (Google, Anthropic, OpenAI), backups (Cloudflare R2). Cada uno es un subencargado que debe estar en tu lista pública.

---

## 5. Propiedad intelectual

### 5.1 Costos 2026

| Trámite | Entidad | Costo | Tiempo |
|---|---|---|---|
| **Registro de soporte lógico (software)** | DNDA | **GRATUITO** | 15 días hábiles |
| Registro de marca, 1.ª clase, en línea | SIC | **$1.347.500** | 4–8 meses sin oposición |
| Registro de marca, 1.ª clase, físico | SIC | $1.638.500 | — |
| Clase adicional en la misma solicitud | SIC | ~$674.000 | — |
| Oposición a solicitud de tercero | SIC | $616.000 | — |
| Cambio de titular o domicilio | SIC | $73.500 en línea | — |

*Base: Resolución SIC 77243 de 2025 (+5,19% IPC), vigente desde el 1-ene-2026.*

> **[NE]** Dos fuentes secundarias reportan $1.347.500 y $1.348.500 para la primera clase. **Verifica el valor exacto en la tabla oficial de tasas de signos distintivos de la SIC antes de pagar.** La SIC otorga **descuentos para MiPymes, personas naturales y entidades educativas** — confirma tu elegibilidad al radicar; puede reducir sustancialmente el costo. No pude verificar el porcentaje exacto para 2026.

### 5.2 Clases de Niza

| Clase | Cubre | ¿Necesaria? |
|---|---|---|
| **Clase 42** | **SaaS, diseño y desarrollo de software** | **Esencial** |
| **Clase 9** | Software descargable | **Sí** |
| Clase 45 | Servicios jurídicos | Solo si la marca también cubre el bufete |

Clases 9 + 42: **~$2.021.500** · con la 45: **~$2.695.500**.

### 5.3 Registra el software en la DNDA. Hoy.

**Es gratuito.** No constituye el derecho (que nace con la creación), pero es **prueba idónea de titularidad y fecha**, y es lo primero que pide un inversionista en due diligence. Trámite en línea: https://www.derechodeautor.gov.co/es/otros/software

---

## 6. Contratos que necesitas antes de vender

| # | Contrato | Contenido crítico |
|---|---|---|
| 1 | **Términos y Condiciones / licencia SaaS** | Licencia de uso **no exclusiva e intransferible** (no venta) · planes y precios · renovación automática · política de suspensión por mora · **limitación de responsabilidad** · ley y jurisdicción colombiana |
| 2 | **SLA** | Disponibilidad comprometida, ventanas de mantenimiento, **créditos de servicio como remedio exclusivo**. **Sé conservador: no prometas 99,9% si corres en un solo servicio de Render** |
| 3 | **DPA / contrato de transmisión de datos** | Obligatorio por el art. 25 del Decreto 1377/2013 (§2) |
| 4 | **Cesión de derechos patrimoniales de autor** | **Ver §6.1 — es el más importante y el más olvidado** |
| 5 | Confidencialidad y no competencia con desarrolladores | — |
| 6 | Contrato de servicios entre la SaaS y el bufete | A precios de mercado, documentado |

### 6.1 La cesión de derechos — donde fallan las due diligence

En Colombia **el derecho de autor nace en cabeza del autor persona natural**.

| Vínculo | Presunción legal |
|---|---|
| **Empleado** | Sí — presunción de transferencia al empleador (art. 28 Ley 1450 de 2011 y Ley 23 de 1982) |
| **Contratista independiente** | **NO hay presunción suficiente.** Necesitas **cesión expresa y escrita**, con detalle de los derechos cedidos, territorio y duración |

> **Sin esos documentos, tu due diligence de inversión falla — y no es un problema que se arregle después, porque para entonces el contratista ya se fue o ya sabe que tiene poder de negociación.** Firma las cesiones **retroactivamente** con todo el que haya tocado el código, esta semana.

---

## 7. Responsabilidad profesional

### 7.1 El escenario a prevenir

Un cliente es sancionado por el Ministerio del Trabajo porque tu matriz legal seguía citando la Res. 2404/2019, derogada en 2022. La exposición es contractual y potencialmente extracontractual.

### 7.2 El marco de la abogacía

El **Decreto 196 de 1971** (Estatuto del Ejercicio de la Abogacía) y la **Ley 1123 de 2007** (Código Disciplinario del Abogado) estructuran el ejercicio como actividad de **personas naturales con título y tarjeta profesional**, bajo la jurisdicción disciplinaria de la Comisión Nacional de Disciplina Judicial, con deberes de lealtad, competencia, reserva y honradez, y **faltas tipificadas por publicidad y captación indebida de clientela**.

**¿Un abogado puede vender asesoría jurídica por suscripción?** **Sí** — no hay prohibición de ese modelo de remuneración. Lo regulado es *cómo* se ejerce y se publicita:

- El servicio jurídico lo presta **un abogado titulado e identificado**, no "la plataforma"
- La publicidad **no puede ser engañosa ni prometer resultados**
- No se puede captar clientela por medios indecorosos ni **pagar comisiones a terceros por referir clientes**
- El deber de reserva es del abogado

### 7.3 La arquitectura que resuelve esto

| **La SAS de software vende** | **El bufete vende** |
|---|---|
| Licencia de uso de software | Concepto jurídico |
| Información normativa estructurada | Representación |
| Automatización documental | Asesoría personalizada |
| Plantillas y formatos | Revisión y firma de un abogado |

### 7.4 Controles obligatorios en el producto

1. *"El contenido normativo de esta plataforma es informativo y no constituye asesoría jurídica ni sustituye el concepto de un profesional."*
2. *"La responsabilidad del cumplimiento del SG-SST recae en el empleador conforme al Decreto 1072 de 2015."*
3. **Fecha de última actualización visible en cada norma** de la matriz legal, con procedimiento documentado de vigilancia normativa.
4. **Limitación contractual de responsabilidad** al valor pagado en los últimos 12 meses. Válida entre comerciantes, **pero no oponible frente a dolo o culpa grave**.
5. Todo concepto jurídico sale con **nombre y tarjeta profesional del abogado** que lo firma.

### 7.5 Póliza E&O

Disponible en Colombia; SBS Seguros y otros corredores ofrecen líneas para abogados y para tecnología.

> **[NE] La prima real de una E&O para SaaS legal no está publicada.** El rango de **$500.000 a $2.000.000 anuales** que circula corresponde a **RC general/extracontractual de pequeñas empresas**, no a E&O tecnológico con valores asegurados altos. **Presupuesta la cotización con corredor, no el rango.**

## Fuentes

[Ley 1581 de 2012](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981) · [RNBD 2026: obligados, plazos y sanciones](https://www.tusdatos.co/blog/registro-nacional-de-bases-de-datos-rnbd-aspectos-importantes-para-este-2026) · [SIC — RNBD](https://www.sic.gov.co/registro-nacional-de-bases-de-datos) · [Circular Externa 005 de 2017 — países con nivel adecuado](https://normograma.dian.gov.co/dian/compilacion/docs/circular_superindustria_0005_2017.htm) · [Cámara de Representantes — PL 274/2025C archivado](https://www.camara.gov.co/proteccion-de-datos-personales-093/) · [SIC — Datos sensibles de salud](https://www.sic.gov.co/boletin-juridico-abril-2017/tratamiento-de-los-datos-sensibles-en-casos-relativos-a-la-salud) · [DNDA — Registro de software](https://www.derechodeautor.gov.co/es/otros/software) · [SIC — Tasas de signos distintivos 2026](https://www.sic.gov.co/tasas-signos-distintivos) · [Ámbito Jurídico — Tasas SIC 2026](https://www.ambitojuridico.com/noticias/comercial/mercantil-propiedad-intelectual-y-arbitraje/sic-actualiza-tasas-de-propiedad) · [Resolución SIC 77243 de 2025](https://www.ramosabogados.co/uncategorized/tasas-actualizadas-sic-2026-cuanto-cuestan-los-tramites-de-propiedad-industrial-en-colombia/) · [Ley 1123 de 2007](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=22962) · [SBS Seguros — RC profesional para abogados](https://www.sbseguros.co/empresas/lineas-financieras/seguro-responsabilidad-profesional/abogados) · [Render Security y subprocesadores](https://render.com/security)
