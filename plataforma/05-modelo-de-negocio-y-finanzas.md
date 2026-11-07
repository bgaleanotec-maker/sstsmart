# Modelo de negocio y finanzas

> Todo número de esta página es **[E] supuesto** salvo que diga otra cosa. **Mes 1 = mes de constitución de la S.A.S. (supuesto: nov-2026)**: mes 12 ≈ oct-2027, mes 24 ≈ oct-2028. El modelo es reproducible:
> `python plataforma/modelo/modelo_plataforma.py --horas 60`. Cambiar supuestos en el propio script.
> El modelo SaaS B2B (SST + PESV + retainer) es el de `docs/05-monetizacion/02-modelo-financiero-30M.md`; aquí no se rehace, se le suma la capa nueva.

## 1. Quién cobra qué

| Fuente | Entidad | Tipo | Precio de referencia | Estado |
|---|---|---|---|---|
| Suscripción SST (planes o módulos) | S.A.S. | MRR B2B | $149.000-749.000/mes | Pricing público pendiente (D6) |
| Add-on PESV | S.A.S. | MRR B2B | $99.000-499.000/mes por nivel | `02-verticales/02-pesv.md` |
| Peticiones y tutelas premium (chequeo automático, sin revisión humana) | S.A.S. | Unidad B2C | $30.000-80.000 con IVA | Hipótesis |
| Seguimiento de plazos y desacato | S.A.S. | MRR B2C | $15.000-30.000/mes | Hipótesis |
| Calendario tributario | S.A.S. | MRR B2C/pyme | $19.900-49.900/mes por NIT | Hipótesis |
| Informe automático DIAN / calculadora premium de accidente (sin recomendación) | S.A.S. | Unidad B2C | $49.000 / $79.000 | Hipótesis |
| Retainer jurídico SST/PESV | **Abogado** | MRR B2B | $190.000-1.290.000/mes | `docs/02-producto/04` |
| Defensa DIAN | **Abogado** | Por caso | $350.000-4.000.000 | Hipótesis |
| Tutela compleja (impugnación, desacato, pensión) | **Abogado** | Por caso | ~$400.000 | Hipótesis |
| Laboral y accidentes | **Abogado** | Cuota litis 20-30% (+ fijo) | Según recuperado | Hipótesis; cobro en 12-24 meses |
| Proyectos (implementación SG-SST, diseño PESV, auditorías) | S.A.S. o abogado según su naturaleza | Proyecto | $1,9M-6,9M | `docs/02-producto/04` |

**Reglas:** la S.A.S. no cobra por derivar. Los honorarios no pasan por la pasarela de la S.A.S. Si el abogado usa la plataforma, paga tarifa SaaS de mercado.

## 2. La hora de abogado: valor y techo

| Línea | Ticket | Horas/caso | P(cobro) | Rezago | Valor esperado/hora |
|---|---:|---:|---:|---:|---:|
| Defensa DIAN (70% ordinario / 30% especial) | $1.135.000 | 7 | 100% | 0 | **$162.143** |
| Tutela compleja | $400.000 | 2,5 | 100% | 0 | $160.000 |
| Retainer SST/PESV (cliente-mes) | $400.000 | 3 | 100% | 0 | $133.333 |
| Accidente RC (25% de $25M) | $6.250.000 | 30 | 60% | 12 | $125.000 |
| Laboral (25% de $15M) | $3.750.000 | 25 | 60% | 15 | $90.000 |

**Asignación de horas** (así lo calcula el script): primero el retainer, porque es un compromiso mensual ya vendido; después, las líneas de mayor valor por hora.

| Corte | Horas que pide la demanda | Con 60 h/mes (Brian solo) | Con 160 h/mes (Brian + abogado de ~100 h) |
|---|---:|---|---|
| Mes 12 (≈ oct-2027) | 83 | Atiende 7 retainers y 5 casos DIAN; deja 7 tutelas complejas sin atender. **Caja: $8,9M/mes** | Atiende todo. **Caja: $12,8M/mes** |
| Mes 24 (≈ oct-2028) | 228 | Los 15 retainers consumen 45 h; quedan 2 casos DIAN. **Caja: $8,3M/mes** | Deja sin atender solo la cuota litis. **Caja: $23,4M/mes**, menos ~$5,1M del abogado junior = ~$18,3M |

**Conclusiones:**
- **La práctica de Brian solo se estanca en ~$8-9M/mes.** Más retainers no suben el ingreso: desplazan casos DIAN que pagan más por hora. Precio del retainer, cupo de consultas y biblioteca de respuestas (`docs/02-producto/04` §3-4) son la palanca para que cada cliente consuma menos de 3 h.
- **La cuota litis no cabe** en ningún escenario sin un abogado adicional. Es coherente con la regla de abrir esas líneas solo cuando haya capacidad (`03-priorizacion-y-secuencia.md` §2).
- **Con un abogado de tiempo completo, la práctica supera el tope de no responsable de IVA** (3.500 UVT ≈ $183M al año) en el mes 24 (~$280M al año). Desde ahí los honorarios llevan IVA o conviene la sociedad de abogados (`01-estructura-legal-dos-entidades.md` §8).
- Las tres palancas, en orden: **(1) mezcla** (DIAN, tutelas complejas, retainer con cupo); **(2) productividad** (herramientas de la consola que bajen las horas por caso); **(3) capacidad** (abogado junior o asociados cuando la demanda supere la capacidad dos meses seguidos).

## 3. Consolidado por entidad (escenario de supuestos)

El retainer se pasa de la S.A.S. al abogado, que es quien lo factura. Los precios B2C se toman con IVA y se netean (÷ 1,19 y menos la pasarela de 3,15%). Abogado: 60 h/mes.

| Corte | S.A.S.: SaaS B2B sin retainer | S.A.S.: capa B2C neta | **S.A.S. total** | Abogado (caja) | **Grupo (caja)** |
|---|---:|---:|---:|---:|---:|
| Mes 12 (≈ oct-2027) | $14.110.000 | $5.947.729 | **$20.057.729** | $8.875.000 | **$28.932.729** |
| Mes 24 (≈ oct-2028) | $30.712.440 | $22.971.355 | **$53.683.795** | $8.270.000 | **$61.953.795** |

Con 160 h de abogado, el grupo llega a $32,9M (mes 12) y $77,0M (mes 24), antes de restar el costo del abogado adicional. Detalle: `modelo/salida_60h.md` y `modelo/salida_160h.md`.

Volúmenes B2C supuestos (mes 12 → 24): tutelas premium 80 → 250/mes · suscripciones de seguimiento 60 → 250 · calendario tributario 30 → 150 NIT · informes DIAN automáticos 25 → 80 · calculadoras premium de accidente 0 → 30.

**Cómo leerlo:**
- Con estos supuestos, la meta de **$30M de ingreso del grupo no se cumple en el mes 12** (~$28,9M en caja). Se cruza poco después, y la S.A.S. sola pasa los $30M antes del mes 24. Pero todo depende de la conversión B2C, que **es lo primero que hay que medir**.
- 250 tutelas premium al mes son ~0,25% de las ~100.000 tutelas mensuales del país. No es una cuota heroica, pero exige tráfico orgánico real.
- Ingreso no es utilidad: el dossier calcula ~25% de margen operativo en el SaaS al mes 24. La capa B2C suma costos de adquisición e IA que todavía no están medidos.
- La cuota litis queda en cero en el escenario de 60 h. Si se abre, su caja llega entre 12 y 24 meses después.
- **Los productos B2C de la S.A.S. son herramientas automáticas sin recomendación sobre el caso** (informe del acto, calculadora, chequeo de soportes). El criterio humano lo cobra el abogado, no la S.A.S. (`01-estructura-legal-dos-entidades.md` §2).

## 4. Unidades necesarias para $5M/mes netos en la S.A.S.

| Producto | Precio con IVA | Neto por unidad | Unidades al mes |
|---|---:|---:|---:|
| Tutela o petición premium | $49.900 | $40.612 | ~123 |
| Seguimiento de plazos y desacato | $19.900 | $16.196 | ~309 suscriptores |
| Calendario tributario | $29.900 | $24.335 | ~205 NIT |
| Informe automático DIAN | $49.000 | $39.879 | ~125 |
| Calculadora premium de accidente | $79.000 | $64.295 | ~78 |

Del lado del abogado, $5M/mes son ~4-5 casos DIAN (~31 h) o ~12 retainers (~37 h).

## 5. Métricas que deciden (tablero mensual)
- S.A.S.: MRR B2B y B2C, conversión gratis → pago por vertical, CAC por canal, churn, costo de IA por documento.
- Abogado: horas usadas vs. disponibles, valor por hora real por línea, días a cobro, casos rechazados por conflicto.
- Grupo: ingreso total, utilidad, caja.

## 6. Supuestos más frágiles (validar primero)
1. Conversión B2C a pago en tutelas y peticiones (piso gratis).
2. Horas reales por caso DIAN (medirlas en los primeros 5 casos manuales).
3. Valor recuperado medio y probabilidad de éxito en laboral y accidentes (sin fuente pública).
4. Horas/mes que Brian puede dedicar (D4).
