# Cesión de derechos patrimoniales de autor y acuerdo de confidencialidad

> **Esto es lo que hace fallar una due diligence.**
>
> El artículo 20 de la Ley 23 de 1982, **tal como quedó tras la Ley 1915 de 2018**, cubre las
> obras creadas tanto en un **contrato de trabajo** como en un **contrato de prestación de
> servicios**, y presume —salvo pacto en contrario— la transferencia de los derechos
> patrimoniales al empleador o encargante. Es un cambio importante y bastante material
> comercial (y no poca asesoría) sigue describiendo el régimen anterior a 2018.
>
> **Entonces, ¿para qué firmar la cesión?** Porque la presunción está acotada: opera *"en la
> medida necesaria para el ejercicio de las actividades habituales"* del encargante **en la
> época de creación de la obra**. Eso deja tres huecos que a una empresa de software le
> importan: (i) los usos futuros que no eran actividad habitual cuando se creó el código;
> (ii) la **oponibilidad frente a terceros**, que se gana con la inscripción del acto en la
> DNDA; y (iii) la prueba misma del alcance, que en una due diligence no se discute con una
> presunción sino con un documento.
>
> Y en tu caso hay un segundo frente: la socia SST que aporta matrices, listas de chequeo y
> contenido normativo. **Eso también es obra protegida.**

---

## 1. Quién tiene que firmar

| Persona | ¿Firma cesión? | ¿Firma NDA? | Notas |
|---|---|---|---|
| Tú, como fundador | **Sí** | No hace falta | Escribiste el código antes de que la sociedad existiera. **Sin cesión, el código es tuyo como persona natural, no de la S.A.S.** Es el caso más olvidado y el más grave |
| Socia SST | **Sí** | **Sí** | Matrices, procedimientos, plantillas y contenido normativo son obra protegida |
| Desarrollador contratista | **Sí** | **Sí** | Hay presunción desde la Ley 1915/2018, pero acotada a las actividades habituales de la época. Firma **antes** del primer commit |
| Desarrollador empleado | Sí, por confirmación | Sí | La presunción existe; se confirma por escrito en el contrato para fijar el alcance |
| Diseñador de logo o piezas | **Sí** | No necesariamente | El logo es obra protegida. Sin cesión, no puedes registrarlo como marca con tranquilidad |
| Afiliado del programa | No | Sí, cláusula en el contrato | No crea obra; sí accede a información comercial |

**Y hazlo retroactivo.** El documento sirve aunque la obra ya esté creada.

---

## 2. Contrato de cesión de derechos patrimoniales de autor

---

**CONTRATO DE CESIÓN DE DERECHOS PATRIMONIALES DE AUTOR**

Entre **`[LLENAR: nombre]`**, mayor de edad, identificado con cédula de ciudadanía `[   ]`,
en adelante **EL CEDENTE**, y **`[LLENAR: RAZÓN SOCIAL]` S.A.S.**, NIT `[   ]`, representada
por `[   ]`, en adelante **LA CESIONARIA**, se celebra el presente contrato:

**PRIMERA — OBJETO Y MODALIDADES.** EL CEDENTE transfiere a LA CESIONARIA, de manera
**total, definitiva e irrevocable**, los **derechos patrimoniales de autor** que le
corresponden sobre las obras descritas en la cláusula segunda, en las siguientes modalidades,
que se enuncian de forma expresa:

a) **Reproducción** por cualquier medio y en cualquier soporte, incluida la fijación digital.
b) **Transformación**, adaptación, arreglo, corrección, actualización y creación de obras derivadas.
c) **Traducción** a cualquier idioma o lenguaje de programación.
d) **Distribución** pública, incluida la venta, el arrendamiento y el préstamo.
e) **Comunicación pública** y **puesta a disposición** del público por redes, incluida la explotación en modalidad de software como servicio (SaaS).
f) **Licenciamiento y sublicenciamiento** a terceros, total o parcial.
g) Importación y exportación de ejemplares.

<!-- El art. 31 de la Decisión Andina 351 de 1993 limita la transferencia a las modalidades
     EXPRESAMENTE previstas en el contrato. Una fórmula genérica del tipo "cualquier forma
     de utilización conocida o por conocerse" es la que se cae en una due diligence. Por eso
     se enumeran. Si aparece una modalidad nueva, se firma un otrosí: cuesta una hoja. -->

**SEGUNDA — OBRAS CEDIDAS.** La cesión comprende:

a) El **código fuente y objeto** del software `[LLENAR: nombre]`, en todas sus versiones,
   incluidas las anteriores a la fecha de este contrato.
b) La documentación técnica, diagramas, modelos de datos y arquitectura.
c) Las interfaces gráficas, diseños, iconografía y elementos visuales.
d) Las bases de datos, matrices normativas, listas de chequeo, procedimientos, formatos y
   contenidos elaborados para la plataforma.
e) `[LLENAR: agregar lo específico del cedente]`
f) Toda obra derivada, actualización, corrección o nueva versión que EL CEDENTE elabore
   durante la vigencia de su relación con LA CESIONARIA. **[NE]** La cesión de obra futura
   está acotada temporalmente por la Ley 23 de 1982 (se cita habitualmente un límite de
   cinco años; **no verifiqué el artículo exacto**). Para no depender de este literal,
   **firma un anexo de confirmación de cesión al cierre de cada año o de cada versión
   mayor**: es una hoja y elimina la discusión.

**TERCERA — ALCANCE TERRITORIAL Y TEMPORAL.** La cesión es para **todos los países del
mundo** y por **todo el término de protección legal** de los derechos cedidos, incluidas sus
prórrogas.

**CUARTA — CONTRAPRESTACIÓN.** La cesión se entiende retribuida con `[LLENAR: la
remuneración pactada / la participación accionaria / la suma de $___, que EL CEDENTE declara
recibida a satisfacción]`. Las partes declaran que la contraprestación es justa y suficiente.

> **No dejes esta cláusula en blanco ni pongas "a título gratuito" sin más.** Una cesión sin
> causa onerosa expresa es más atacable. Si no hay pago en dinero, di que la contraprestación
> es la participación accionaria o la remuneración del contrato de servicios.

**QUINTA — DERECHOS MORALES.** EL CEDENTE conserva sus **derechos morales**, que son
inalienables e irrenunciables conforme al art. 30 de la Ley 23 de 1982. **Autoriza** a LA
CESIONARIA a divulgar las obras sin mención de su nombre cuando ello sea usual en la
explotación comercial de software.

**SEXTA — GARANTÍAS DEL CEDENTE.** EL CEDENTE declara y garantiza que:

a) Es el **único titular** de los derechos cedidos y tiene plena capacidad para cederlos.
b) Las obras son **originales** y no infringen derechos de terceros.
c) No ha cedido, licenciado ni gravado previamente los mismos derechos.
d) **Todo componente de terceros incorporado** (bibliotecas, frameworks, código abierto) está
   debidamente licenciado y se relaciona en el **Anexo A**, con indicación de su licencia.
e) **No incorporó código sujeto a licencias copyleft fuertes** (GPL, AGPL) que puedan obligar
   a liberar el código propietario, salvo lo expresamente indicado en el Anexo A.

> **El literal (e) importa de verdad.** Una dependencia AGPL en un SaaS puede obligar a
> publicar el código fuente. Es de las cosas que un comprador o un inversionista revisa con
> herramienta automática, y aparece.

**SÉPTIMA — INDEMNIDAD.** EL CEDENTE mantendrá indemne a LA CESIONARIA frente a cualquier
reclamación de terceros derivada del incumplimiento de las garantías de la cláusula sexta.

**OCTAVA — ENTREGA.** EL CEDENTE entrega el código fuente, credenciales, documentación y
todo elemento necesario para la explotación autónoma de las obras, y se obliga a no
conservar copias salvo autorización escrita.

**NOVENA — REGISTRO Y OPONIBILIDAD.** Las partes **se obligan** a inscribir este contrato y
las obras cedidas en el **Registro Nacional de Derecho de Autor** de la Dirección Nacional de
Derecho de Autor. **La inscripción del acto es lo que lo hace oponible frente a terceros**;
sin ella, la cesión produce efectos entre las partes pero es discutible frente a un tercero
—que es exactamente el escenario de una due diligence—. EL CEDENTE prestará la colaboración
que el trámite requiera.

**DÉCIMA — LEY Y JURISDICCIÓN.** Ley colombiana. Jueces de Bogotá D.C.

Se firma en Bogotá D.C., el `[   ]`.

<br>

**EL CEDENTE** ________________________  ·  **LA CESIONARIA** ________________________
`[nombre]` C.C. `[   ]`                     `[representante legal]` C.C. `[   ]`

---

**ANEXO A — Componentes de terceros**

| Componente | Versión | Licencia | ¿Copyleft fuerte? |
|---|---|---|---|
| `[ej. Flask]` | `[   ]` | BSD-3-Clause | No |
| `[   ]` | `[   ]` | `[   ]` | `[   ]` |

> Genera este anexo con `pip freeze` y una herramienta de licencias (`pip-licenses`), no a
> mano. Guárdalo actualizado: es el documento que te pedirán en la primera due diligence.

---

## 3. Acuerdo de confidencialidad (NDA)

---

**ACUERDO DE CONFIDENCIALIDAD**

Entre `[LLENAR: RAZÓN SOCIAL]` S.A.S., NIT `[   ]` (**LA EMPRESA**) y `[LLENAR: nombre]`,
C.C. `[   ]` (**EL RECEPTOR**):

**PRIMERA — INFORMACIÓN CONFIDENCIAL.** Toda información técnica, comercial, financiera,
estratégica o de clientes a la que EL RECEPTOR acceda: código fuente y arquitectura ·
credenciales y configuraciones · listas y datos de clientes y prospectos · precios,
márgenes y modelo financiero · **datos personales alojados en la plataforma** · planes de
producto y hoja de ruta · condiciones del programa de afiliados.

**SEGUNDA — OBLIGACIONES.** EL RECEPTOR se obliga a: (i) mantener estricta reserva; (ii) usar
la información **exclusivamente** para el desarrollo de sus funciones; (iii) no reproducirla
ni extraerla fuera de los sistemas autorizados; (iv) devolver o destruir toda copia al
terminar la relación; (v) notificar de inmediato cualquier divulgación no autorizada.

**TERCERA — EXCLUSIONES.** No es confidencial la información que sea o llegue a ser pública
sin culpa del RECEPTOR, la que ya obraba legítimamente en su poder antes de la relación, la
recibida legítimamente de un tercero sin deber de reserva, o cuya divulgación sea ordenada
por autoridad competente —caso en el cual EL RECEPTOR lo notificará previamente a LA EMPRESA,
si la ley lo permite.

**CUARTA — DATOS PERSONALES.** EL RECEPTOR reconoce que la plataforma aloja **datos sensibles
de salud** de trabajadores de terceros, y se obliga a tratarlos conforme a la Ley 1581 de
2012 y a las instrucciones de LA EMPRESA. **El acceso a datos de producción sin necesidad
funcional acreditada constituye incumplimiento grave.**

**QUINTA — VIGENCIA.** Durante la relación y por **tres (3) años** después de terminada. Para
**secretos empresariales y datos personales, la obligación es indefinida**.

**SEXTA — NO SOLICITACIÓN.** Durante la relación y por **doce (12) meses** después, EL
RECEPTOR se abstendrá de inducir a clientes o colaboradores de LA EMPRESA a terminar su
relación con ella.

> **Ojo con el alcance.** Una cláusula de no competencia amplia (impedirle trabajar en el
> sector) es de dudosa exigibilidad en Colombia frente al derecho al trabajo. La **no
> solicitación** —no llevarse clientes ni compañeros— sí es defendible. Pide lo segundo, no
> lo primero.

**SÉPTIMA — INCUMPLIMIENTO.** El incumplimiento faculta a LA EMPRESA para terminar la
relación con justa causa y para reclamar los perjuicios causados, sin perjuicio de las
acciones penales que correspondan.

**OCTAVA — LEY Y JURISDICCIÓN.** Ley colombiana. Jueces de Bogotá D.C.

Firmado en Bogotá D.C., el `[   ]`.

<br>

**LA EMPRESA** ________________  ·  **EL RECEPTOR** ________________

---

## 4. Orden de firma — no se improvisa

1. **Tu propia cesión, primero.** Antes que cualquier otra. El código que escribiste antes de constituir la sociedad es tuyo como persona natural —no hubo empleador ni encargante que activara presunción alguna—; hay que pasarlo a la S.A.S. de forma expresa.
2. **NDA + cesión de la socia SST**, antes de que aporte contenido normativo o plantillas.
3. **NDA + cesión de cualquier contratista**, antes del primer acceso al repositorio.
4. **Archivo.** Todos los firmados en `empresa/documentos-oficiales/cesiones/`, respaldados en la nube. Escaneados y legibles.
5. **Anexo A actualizado** cada vez que se agregue una dependencia nueva.

---

## Fuentes

[Ley 23 de 1982](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=3431) ·
[Ley 1915 de 2018](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=87356) ·
[Decisión Andina 351 de 1993](https://www.derechodeautor.gov.co/documents/10181/182597/351.pdf) ·
[DNDA — registro de obras](https://www.derechodeautor.gov.co/es/otros/software)
