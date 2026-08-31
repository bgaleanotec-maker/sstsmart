# El trámite en la Cámara de Comercio de Bogotá, paso a paso

**Es 100% virtual.** No hay que ir a ninguna sede ni pasar por notaría. Tiempo real de
diligenciamiento: 45–90 minutos. Tiempo de respuesta: 2 a 5 días hábiles.

---

## Antes de empezar — ten esto a la mano

- [ ] Nombre verificado en el **RUES** (sin homonimia) → [`00-decision-nombre-y-objeto.md`](00-decision-nombre-y-objeto.md) §3
- [ ] Documento de constitución en **PDF**, con todos los `[LLENAR]` reemplazados
- [ ] Cartas de aceptación de principal y suplente en PDF
- [ ] Cédula escaneada, ambas caras, legible
- [ ] Correo electrónico **del dominio propio** (no gmail) para notificación judicial
- [ ] Medio de pago habilitado para **PSE**
- [ ] Celular con señal: hay validación de identidad con envío de código

> **El correo de notificación judicial es en serio.** Es la dirección a la que llegan
> notificaciones de la DIAN, de la SIC y de juzgados. Un correo que no revisas es cómo se
> pierden términos. Usa uno del dominio (`legal@tudominio.co`) y redirígelo a donde sí leas.

---

## Paso 1 · Crear cuenta y validar identidad

1. https://www.ccb.org.co → **Trámites y consultas** → **Crear empresa** → *Constitución virtual de S.A.S.*
2. Regístrate con tu cédula y correo. Confirma el correo.
3. **Validación biométrica** contra la Registraduría: foto del documento y selfie con prueba de vida.

**Si la biometría falla** (pasa con frecuencia con documentos antiguos o mala iluminación):
usa luz frontal, fondo liso, quítate los lentes. Si falla tres veces, el sistema ofrece
una ruta alterna con verificación por preguntas. No abandones el trámite: reabrir uno
nuevo pierde lo diligenciado.

---

## Paso 2 · Formulario RUES

Los datos exactos están tabulados en [`00-decision-nombre-y-objeto.md`](00-decision-nombre-y-objeto.md) §6. Los campos donde la gente se equivoca:

| Campo | Cuidado |
|---|---|
| **Razón social** | Escríbela **exactamente** como aparece en los estatutos, incluida la puntuación de "S.A.S." Una diferencia mínima genera devolución |
| **Activos totales** | Aquí va **$5.000.000** (el capital pagado). Este número liquida la matrícula. No pongas activos que no tienes |
| **CIIU principal** | **6201**. El buscador del formulario es literal: escribe "desarrollo de sistemas informáticos" |
| **CIIU secundarios** | 6311, 7020, 6202 |
| **Personal ocupado** | 1 |
| **Dirección comercial** | Puede ser tu residencia. Debe coincidir con la del documento de constitución |
| **¿Matricula establecimiento de comercio?** | **NO.** Una plataforma SaaS no lo requiere, y matricularlo cuesta $48.400 anuales de más |

---

## Paso 3 · PreRUT

Dentro del mismo flujo. La CCB lo transmite a la DIAN y esta asigna el **NIT**. No hay que
ir a la DIAN a hacer fila: ese paso desapareció.

Diligencia con cuidado la **actividad económica** y la **responsabilidad tributaria
inicial**; se puede corregir después en el portal de la DIAN, pero corregir cuesta tiempo.

---

## Paso 4 · Cargar y firmar los documentos

1. Adjunta el acto de constitución y las cartas de aceptación.
2. **Firma electrónica**: la plataforma envía un código al celular y al correo de cada firmante. La firma electrónica de la CCB confiere **presunción de autenticidad** — es lo que reemplaza la notaría.
3. Si hay suplente, él recibe su propio enlace de firma. **El trámite no avanza hasta que firme.** Avísale antes.

---

## Paso 5 · Liquidación y pago

Con capital suscrito de **$5.000.000** y activos declarados de $5.000.000:

| Concepto | Base | Valor |
|---|---|---|
| Matrícula mercantil | $24.220 + 8.477 × (5.000.000 / 1.000.000) | **$66.605** |
| Inscripción del documento de constitución | 6 UVB | **$72.660** |
| Formulario RUES | 0,7 UVB | **$8.500** |
| Impuesto de registro Bogotá — acto con cuantía | 0,7% × $5.000.000 | **$35.000** |
| **Total a pagar** | | **$182.765** |

Opcionales, en el mismo trámite o después:

| Concepto | Base | Valor |
|---|---|---|
| Inscripción del libro de accionistas | 2 UVB | $24.220 |
| Certificado de existencia y representación legal | 1 UVB | $12.110 |

Pago por **PSE**. Guarda el comprobante: es gasto deducible del primer ejercicio.

---

## Paso 6 · Espera y respuesta

**2 a 5 días hábiles.** Llega por correo:

- Número de **matrícula mercantil**
- **NIT** asignado por la DIAN
- Certificado de existencia y representación legal descargable

### Si devuelven la solicitud

Casi siempre es una de estas cinco, y todas se corrigen sin pagar de nuevo:

| Causa | Arreglo |
|---|---|
| Homonimia del nombre | Cambia el nombre. Por eso se verifica en RUES **antes** |
| Un `[LLENAR]` sin reemplazar | Revisa el PDF con búsqueda de texto: `Ctrl+F` → `[LLENAR]` → debe dar **cero** resultados |
| Capital: autorizado, suscrito y pagado no cuadran | Suscrito ≤ autorizado. Pagado ≤ suscrito. Número de acciones × valor nominal = capital suscrito |
| Falta la aceptación de un designado | Adjuntar la carta faltante |
| Dirección del formulario ≠ dirección del documento | Igualarlas, carácter por carácter |

---

## Paso 7 · Inmediatamente después — el mismo día

- [ ] Descargar el certificado de existencia y representación legal (PDF con código de verificación)
- [ ] Guardar todo en una carpeta `empresa/documentos-oficiales/` respaldada en la nube
- [ ] Ir a la DIAN a **formalizar el RUT** → [`../02-dian-y-facturacion/01-rut-y-responsabilidades.md`](../02-dian-y-facturacion/01-rut-y-responsabilidades.md)
- [ ] Iniciar el **registro del software en la DNDA** (gratis, 15 días hábiles — entre antes empiece, mejor) → [`../03-legal-producto/05-registro-software-dnda.md`](../03-legal-producto/05-registro-software-dnda.md)
- [ ] Inscribirse en el **RIT** de la Secretaría Distrital de Hacienda

---

## Y una fecha que no se olvida

**Renovación de la matrícula mercantil: antes del 31 de marzo de cada año.**

Se liquida con la misma tabla, sobre los activos totales al 31 de diciembre anterior. **El
impuesto de registro no aplica a la renovación.** La sanción por no renovar llega a **17
SMMLV = $29.765.385**, pero el daño real es otro: aparecer **"No renovada"** en el RUES.
Un cliente mediano que pide tu certificado y ve eso, cancela la compra ese mismo día.

Ponle recordatorio al calendario ahora, con alerta el **1 de febrero**.

---

## Fuentes

[CCB — Constitución virtual de S.A.S.](https://www.ccb.org.co/es/servicios/crea-tu-empresa/constituye-tu-empresa/constitucion-virtual-sas) ·
[CCB — Guía de constitución (PDF)](https://assets.ctfassets.net/n1ptkpqt763u/2qPY8BkR0Awl2GgbTeQQri/1ed118cb5a6cf3ba9a9f61099d53ac81/GuiaRM_01.pdf) ·
[CCB — Tarifas de registros públicos](https://www.ccb.org.co/es/tramites-y-consultas/sobre-registros/tarifas) ·
[RUES](https://www.rues.org.co) ·
[Renovación hasta el 31 de marzo de 2026](https://bogota.gov.co/mi-ciudad/desarrollo-economico/renovacion-de-matricula-mercantil-en-bogota-hasta-31-de-marzo-de-2026)
