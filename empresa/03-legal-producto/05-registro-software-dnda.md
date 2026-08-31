# Registro del software en la DNDA

**Costo: $0.** Tiempo: **15 días hábiles**. Es el mejor retorno por peso invertido de toda
esta carpeta, porque no cuesta ninguno.

---

## 1. Qué es y qué no es

**Qué es.** Un registro **declarativo** ante la Dirección Nacional de Derecho de Autor que
deja constancia pública de la existencia de la obra, de su fecha y de su titular.

**Qué no es.** No es constitutivo del derecho: en Colombia el derecho de autor nace con la
creación, no con el registro. Tampoco es una patente ni una marca.

**Entonces, ¿para qué sirve?** Para **probar la titularidad y la fecha** cuando alguien la
discuta. Es la primera pregunta de cualquier due diligence de inversión o de compra, y el
documento que soporta una acción por copia. En un litigio, la diferencia entre tener el
certificado y no tenerlo es la diferencia entre exhibir un documento oficial y tener que
reconstruir la autoría con commits.

---

## 2. Momento correcto

**El día que tengas el NIT.** Antes no puedes registrar a nombre de la sociedad, y registrar
a nombre personal obliga después a inscribir la cesión.

Y **antes de la primera demo pública**. No hay obligación legal de anterioridad, pero es
sano que la fecha del registro anteceda a la primera divulgación amplia.

---

## 3. Qué se necesita

- [ ] **NIT** y certificado de existencia y representación legal
- [ ] **Cesión de derechos firmada por ti** a favor de la sociedad → [`04-cesion-derechos-y-nda.md`](04-cesion-derechos-y-nda.md). Sin ella, la sociedad no es titular y el registro queda mal hecho
- [ ] **Resumen del software**: nombre, versión, lenguaje, entorno, funcionalidad, fecha de creación
- [ ] **Muestra del código fuente**: primeras y últimas páginas del código, o el archivo completo según lo que pida el formulario
- [ ] Nombre de los autores personas naturales

> **Sobre el código que se sube.** Se registra una **muestra representativa**, no el
> repositorio completo. Elige archivos que evidencien la arquitectura y la lógica propia —
> modelos, servicios de dominio, reglas de negocio— y **no incluyas secretos**: revisa que no
> haya credenciales, tokens ni cadenas de conexión en lo que subas. El expediente es
> consultable.

---

## 4. Paso a paso

1. https://www.derechodeautor.gov.co/es/otros/software
2. Crear usuario en el sistema de registro en línea.
3. Seleccionar **Registro de obra — Soporte lógico (software)**.
4. Diligenciar:
   - **Titular**: `[RAZÓN SOCIAL]` S.A.S., NIT
   - **Autor(es)**: personas naturales que escribieron el código
   - **Forma de adquisición del derecho por el titular**: *cesión* (adjuntar el contrato)
   - Datos técnicos: lenguaje, entorno, versión, fecha de creación
   - Descripción funcional
5. Adjuntar la muestra de código y el contrato de cesión.
6. Radicar. **No hay pago.**
7. Esperar ~15 días hábiles. Llega el certificado en PDF.

---

## 5. Después del registro

- [ ] Guardar el certificado en `empresa/documentos-oficiales/dnda/`
- [ ] Anotar el **número de registro** — va en la propuesta comercial y en la due diligence
- [ ] Incluir el aviso de derechos en el repositorio y en el pie de la aplicación:
      `© [año] [RAZÓN SOCIAL] S.A.S. Todos los derechos reservados. Registro DNDA [número].`
- [ ] **Registrar las versiones mayores** cuando cambie sustancialmente la obra. Cada registro sigue siendo gratuito

---

## 6. Qué NO cubre este registro — y qué hacer con eso

| Activo | Protección | Costo 2026 | ¿Ahora? |
|---|---|---|---|
| Código fuente | **DNDA — derecho de autor** | **$0** | **Sí, ya** |
| Nombre comercial y logo | **Marca — SIC**, clases 9 y 42 | $1.347.500 la primera clase, ~$674.000 cada clase adicional (≈ **$2.021.500** por las dos) | **No todavía** |
| Nombre de dominio | Registro de dominio | ~$60.000/año **[NE]** | **Sí, ya** |
| Base de datos estructural | Derecho de autor sobre la estructura | $0, con el mismo registro | Sí |
| Método de negocio | **No patentable** en Colombia | — | — |

**Sobre la marca.** Aplazarla es una decisión consciente de presupuesto, no un descuido, y
tiene un riesgo real: **el sistema marcario colombiano es atributivo** —la marca es de quien
la registra primero, no de quien la usa primero—. Mitigación mientras tanto:

1. **Verifica en SIPI antes de adoptar el nombre** que no exista una marca idéntica o
   confundible en clases 9, 35, 42 y 45. Ya está en
   [`../01-constitucion/00-decision-nombre-y-objeto.md`](../01-constitucion/00-decision-nombre-y-objeto.md) §3.
2. **Registra el dominio y las redes de inmediato.** Uso público documentado y continuo.
3. **Guarda evidencia fechada del uso** (publicaciones, facturas, contratos): sirve para
   oponerse a un registro posterior de mala fe.
4. **Presupuesta el registro para el trimestre en que llegues a 10 clientes pagos**, o
   antes si alguien empieza a usar un nombre parecido.

**[NE]** La SIC otorga descuentos para MiPymes en tasas de propiedad industrial; no pude
verificar el porcentaje exacto vigente para 2026. **Pregúntalo al radicar** — puede cambiar
significativamente el cálculo.

---

## Fuentes

[DNDA — registro de software](https://www.derechodeautor.gov.co/es/otros/software) ·
[Ley 23 de 1982](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=3431) ·
[Decisión Andina 351 de 1993](https://www.derechodeautor.gov.co/documents/10181/182597/351.pdf) ·
[SIC — SIPI, consulta de signos distintivos](https://sipi.sic.gov.co) ·
[SIC — tasas de propiedad industrial](https://www.sic.gov.co/tramites-y-servicios-propiedad-industrial)
