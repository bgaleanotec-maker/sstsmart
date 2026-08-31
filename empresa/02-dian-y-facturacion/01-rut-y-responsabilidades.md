# RUT, firma electrónica y RIT

Todo lo de esta página es **gratuito**. Toma unas tres horas repartidas en dos o tres días,
porque hay esperas de sistema.

---

## 1. El NIT ya existe — el RUT hay que terminarlo

Cuando la CCB aprueba la constitución, transmite los datos a la DIAN y esta **asigna el
NIT**. Pero el RUT queda con las responsabilidades del PreRUT, que casi siempre están
incompletas. Hay que entrar a formalizarlo.

### 1.1 Habilitar la cuenta en el portal DIAN

1. https://muisca.dian.gov.co → **Usuario Registrado** → *¿Nuevos usuarios?* → **Habilitar cuenta**
2. Ingresa como **Representante legal** de la persona jurídica (no "a nombre propio").
3. Datos: tipo de documento del representante legal, número, NIT de la sociedad.
4. Crea contraseña. Confirma por correo.

> **Error frecuente:** entrar "a nombre propio" con tu cédula. Eso te da acceso a tu RUT de
> persona natural, no al de la sociedad. Tienen que ser dos accesos distintos.

### 1.2 Solicitar el Instrumento de Firma Electrónica (IFE)

Dentro del portal, en **Firma Electrónica**. Es **gratuito** y se genera en línea. Sin él
no puedes presentar declaraciones ni habilitarte como facturador.

Guarda la contraseña del IFE en el gestor de contraseñas, no en un papel. Recuperarla es
un trámite y hay meses en que el portal se congestiona.

---

## 2. Responsabilidades a inscribir en el RUT

Casilla 53 del RUT. Estas son las que van para esta sociedad:

| Código | Responsabilidad | ¿Va? | Por qué |
|---|---|---|---|
| **05** | Impuesto de renta y complementario, régimen ordinario | **Sí** | Decisión tomada: régimen ordinario, no Simple. Ver [`02-decision-iva-y-regimen.md`](02-decision-iva-y-regimen.md) §3 |
| **07** | Retención en la fuente a título de renta | **Sí** | Vas a practicar retención cuando pagues comisiones a afiliados y honorarios a contratistas |
| **42** | Obligado a llevar contabilidad | **Sí** | Toda sociedad comercial lo está |
| **52** | Facturador electrónico | **Sí** | Requisito para habilitarte |
| **48** | Responsable de IVA | **Sí** — decisión recomendada | Ver [`02-decision-iva-y-regimen.md`](02-decision-iva-y-regimen.md) §2 |
| ~~49~~ | ~~No responsable de IVA~~ | No | Alternativa a la 48; excluyentes entre sí |
| 19 | Productor de bienes y servicios exentos | Solo si exportas | Necesaria para pedir devolución del IVA descontable en exportación de servicios |
| 59 | Autorretenedor especial de renta | **[NE] PREGUNTA OBLIGADA AL CONTADOR** | La autorretención especial (Decreto 2201/2016, arts. 1.2.6.6 y ss. del DUR 1625/2016) se predica de las sociedades nacionales que cumplan las condiciones del **art. 114-1 ET**. Circula la idea de que "sin empleados no aplica", pero **no pude verificar el estado actual de la doctrina de la DIAN sobre ese punto**. Si aplica, **se autorretiene sobre cada ingreso desde la primera factura** y se declara mensualmente. Es el error tributario más caro y más silencioso de esta ruta: resuélvelo antes de facturar |
| 47 | Régimen Simple | **No** | Ver §3 de [`02-decision-iva-y-regimen.md`](02-decision-iva-y-regimen.md) |

### Cómo se actualiza

Portal DIAN → **Registro Único Tributario** → *Actualizar RUT* → casilla 53 → firmar con el
IFE. Sale un RUT nuevo en PDF con fecha de la actualización. **Ese es el que piden bancos,
clientes y proveedores.**

---

## 3. RIT — Bogotá. El paso que todo el mundo olvida

**El ICA no se inscribe en el RUT.** Se hace en el **Registro de Información Tributaria**
de la Secretaría Distrital de Hacienda.

1. https://www.haciendabogota.gov.co → **Oficina Virtual** → registro de contribuyente
2. Datos: NIT, certificado de existencia, actividad económica, dirección
3. Declara la actividad **6201** → agrupación **304**

| Actividad | Agrupación | Tarifa por mil |
|---|---|---|
| 6201 desarrollo de sistemas informáticos | 304 | **9,66 ‰** **[NE]** |
| 6202 consultoría informática | 302 | 8,66 ‰ **[NE]** |
| 6311 procesamiento de datos y hosting | 304 | 9,66 ‰ **[NE]** |

> **[NE] Advertencia.** Estas tarifas provienen de tablas de terceros; no logré confirmar
> la fila exacta del 6201 en la Cartilla ICA oficial de la Secretaría. **Confírmala en el
> RIT al inscribirte**, antes de la primera declaración. Es un dato que se cita mal con
> frecuencia y una tarifa equivocada mantenida durante un año se corrige con una
> declaración de corrección y sanción.

**Otros datos de ICA:** sobretasa bomberil del 1% del ICA si los ingresos netos superan
43.498 UVT · base mínima de retención de ICA por servicios: 4 UVT = **$209.496**.

Es gratuito y toma unos 20 minutos.

---

## 4. Otras inscripciones — cuáles aplican y cuáles no

| Trámite | ¿Aplica hoy? | Cuándo aplicaría |
|---|---|---|
| **ARL** | No, sin empleados | Antes del primer día de trabajo del primer empleado. CIIU 6201 = riesgo clase I, tarifa 0,522% |
| **Caja de compensación** | No | Con el primer empleado. Es el 4% y **se paga siempre**, incluso con la exoneración del art. 114-1 |
| **RNBD** (Registro Nacional de Bases de Datos, SIC) | **No** | Solo si los activos superan 100.000 UVT = $5.237.400.000 |
| **Registro de proveedor tecnológico DIAN** | No | Solo si vendieras facturación electrónica a terceros |
| **Habilitación como facturador electrónico** | **Sí** | Ver [`03-habilitacion-facturador-electronico.md`](03-habilitacion-facturador-electronico.md) |
| **RUB — Registro Único de Beneficiarios Finales** (DIAN) | **Sí, y se olvida siempre** | Toda S.A.S. debe reportar sus beneficiarios finales (Resolución DIAN 000164 de 2021). El plazo se cuenta desde la inscripción en el RUT y es corto. **[NE] Confirma el término exacto en la resolución vigente** — la sanción por omisión es la del art. 658-3 ET y se acumula |
| **Nómina electrónica** | No | Obligatoria desde el primer empleado |

---

## 5. Checklist de la fase

- [ ] Cuenta DIAN habilitada como representante legal
- [ ] Instrumento de Firma Electrónica generado y contraseña guardada
- [ ] RUT actualizado con responsabilidades 05, 07, 42, 52, 48
- [ ] RUT en PDF descargado y guardado
- [ ] RIT de Bogotá inscrito, tarifa de ICA **confirmada en el portal**
- [ ] **RUB — beneficiarios finales reportado** dentro del plazo de la Resolución DIAN 000164 de 2021
- [ ] Preguntado al contador si aplica la **responsabilidad 59 (autorretención especial)** con cero empleados
- [ ] Recordatorio de calendario: **declaración de ICA bimestral o anual** según régimen asignado

---

## Fuentes

[DIAN — MUISCA](https://muisca.dian.gov.co) ·
[Secretaría Distrital de Hacienda — ICA](https://www.haciendabogota.gov.co/es/impuestos/impuesto-de-industria-y-comercio-ica) ·
[ICA Bogotá — Resolución SDH-000265 de 2021](https://bogota.gov.co/mi-ciudad/hacienda/se-actualizan-actividades-y-tarifas-de-ica) ·
[Exoneración de parafiscales art. 114-1 ET](https://actualicese.com/exonerados-de-aportes-parafiscales-en-2026/)
