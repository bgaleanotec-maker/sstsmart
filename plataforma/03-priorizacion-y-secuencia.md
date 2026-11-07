# Priorización y secuencia de verticales

> Puntajes **propuestos por Claude** con la rúbrica del cerebro (`empresa/ideas/CONTEXTO.md`: 6 criterios de 1 a 5; ≥ 24 candidata a foco, 18-23 validar, < 18 bandeja). Brian los confirma o corrige (decisión D5).

## 1. Puntaje

| Vertical | Dolor y mercado | Ventaja injusta | Costo de arranque | Tiempo al primer peso | Riesgo legal (inverso) | Sinergia | **Total** |
|---|---|---|---|---|---|---|---|
| SST (Justrabajo) | 5 | 5 | 5 (ya construido) | 4 | 4 | 5 | **28** |
| PESV | 5 | 4 | 4 | 5 (ventana ene-2027) | 4 | 5 | **27** |
| Defensa DIAN (abogado + app) | 4 | 5 | 5 (arranca manual) | 5 | 4 | 3 | **26** |
| Centrales de riesgo / habeas data | 3 | 4 | 5 (motor de tutelas) | 3 | 4 | 5 | **24** |
| Insolvencia persona natural | 4 | 5 | 4 | 3 | 4 | 4 | **24** |
| Peticiones y tutelas | 3 (piso gratis) | 4 | 5 | 3 | 3 (datos de salud) | 5 | **23** |
| Laboral (liquidación y despido) | 4 | 5 | 5 | 2 (cuota litis) | 3 (conflicto con SST) | 4 | **23** |
| Calendario tributario | 3 | 3 | 4 | 3 | 5 | 3 | **21** |
| Propiedad horizontal (cobro) | 3 | 3 | 4 | 3 | 5 | 3 | **21** |
| Fotomultas | 4 | 3 | 4 | 3 | 2 (lección Juzto) | 4 | **20** |
| Accidentes de tránsito | 4 | 4 | 3 | 2 (caja de 12-24 meses) | 2 (art. 30 num. 7) | 3 | **18** |
| Penal-SST para empleadores (add-on del retainer) | 4 | 5 | 5 | 4 | 3 | 5 | **26** |
| Penal víctimas (querellables, conciliación, reparación) | 4 | 3 | 5 | 3 | 3 (calamidad) | 4 | **22** |
| Firma App (consola del abogado; luego SaaS para abogados) | 3 | 4 | 4 (código existente) | 3 | 4 | 5 | **23** |
| Cerebro Legal + Radar de Oportunidades | 4 | 5 | 5 (arranca manual) | 3 | 4 (fuentes) | 5 | **26** |

**Lectura:** las tutelas no son las de mayor puntaje por sí solas, pero **construyen el motor** que hace baratas a centrales de riesgo, fotomultas, laboral e insolvencia. Por eso van antes que su puntaje sugiere.

**Cerebro Legal y Radar de Oportunidades no esperan a ninguna fase:** la vigilancia semanal de fallos arranca ya, sin código (skill `vigilar-fallos`), y su backlog de código (C0-C5, en `empresa/Apis/cerebro_legal/06-backlog-claude-code.md`) corre en paralelo: C0-C1 en las Fases 0-1, C2-C4 en la Fase 2.

## 2. La restricción que manda: horas de abogado

Valor esperado por hora `[E]` (`modelo/salida_60h.md`):

| Línea | Valor/hora | Cobro |
|---|---:|---|
| Defensa DIAN | $162.000 | Inmediato |
| Tutela compleja | $160.000 | Inmediato |
| Retainer SST/PESV | $133.000 | Mensual recurrente |
| Accidente (cuota litis, P = 60%) | $125.000 | 12-24 meses |
| Laboral (cuota litis, P = 60%) | $90.000 | 12-18 meses |

- Con **60 h/mes**, la práctica de Brian se estanca en **~$8-9M/mes en caja**. La demanda supuesta pide 83 h en el mes 12 y 228 h en el mes 24. El retainer va primero porque es un compromiso ya vendido, y cada retainer nuevo desplaza casos DIAN.
- **Regla operativa:** abrir una línea de cuota litis solo cuando haya horas libres demostradas por 2 meses seguidos, o un abogado asociado (contrato entre abogados, honorarios por trabajo real; nunca por haber recomendado).
- **Palanca de producto:** cada hora que la app ahorra (lector de actos, plantillas revisadas, expediente armado) sube el valor por hora. Por eso el backlog prioriza herramientas para el abogado, no solo para el usuario final.

## 3. Calendario de ventanas que ordena la secuencia

| Fecha | Evento | Vertical |
|---|---|---|
| Desde nov-2026 | Fin de la temporada de renta (26-oct según Portafolio y Accounter; Siigo dice 23-oct `[VERIFICAR]`); empiezan omisos y requerimientos | Defensa DIAN |
| Ene-2027 | Reporte PESV de misionalidad 2 a MinTrabajo, escalonado por último dígito del NIT (fechas y si son hábiles `[VERIFICAR texto oficial de la Circular 0034/2026]`) | PESV |
| 10.º día hábil de ene-2027 | Acumulado anual Formulario 2 (vigilados Supertransporte) | PESV |
| Feb-abr 2027 | ICA anual Bogotá (26-feb-2027, Res. SDH-000195/2025 vía Siempre al Día `[VERIFICAR]`), Régimen Simple (abr) | Calendario tributario |
| 1-abr-2027 | Entra en vigencia la reforma pensional | Pensiones (observar) |
| May-jul 2027 | Autoevaluación SG-SST en SGRL (plazo 31-jul) | SST |
| Ago-2027 | Formulario 1 SISI-PESV; temporada de renta | PESV, impuestos |

## 4. Secuencia propuesta (fuente única de las fases)

Mes 1 del modelo = mes de constitución de la S.A.S. (supuesto: nov-2026). En el modelo base del dossier, el abogado junior entra en el mes 19 (≈ may-2028); este análisis recomienda adelantar esa decisión al cierre de la Fase 3 si la demanda supera la capacidad dos meses seguidos.

| Fase | Meses | Producto (Code) | Práctica (Brian) | Meta de salida |
|---|---|---|---|---|
| **0 · Fundación** | oct-dic 2026 | E0 cobro + Postgres/RLS · E1 núcleo de cuentas personales · **E3 PESV con reporte MinTrabajo** | Constituir S.A.S. · landing y diagnóstico **manual** de defensa DIAN | 3 pilotos SST/PESV · 3 casos DIAN pagos |
| **1 · Motor B2C** | ene-mar 2027 | E2 motor de plazos y documentos · **E4 peticiones y tutelas** (salud + petición) · E5 calendario tributario | Atender tutelas complejas derivadas | 500 usuarios registrados · primeras suscripciones de seguimiento |
| **2 · Herramientas del abogado** | abr-jun 2027 | E6 consola del abogado sobre **Firma App portada (E13)** (conflictos, expediente, cupo) · Cerebro C2-C4 (líneas y estrategias con Radar) · E14 penal (triaje, querella guiada, alertas, módulo "evento grave" en SST) · E7 defensa DIAN en app (lector, conciliador, simulador) · E8 centrales de riesgo (especificar antes de abril) | Campaña autoevaluación SST con retainer | Valor/hora del abogado > $180.000 |
| **3 · Laboral e insolvencia** | jul-dic 2027 | E9 laboral (calculadora + derivación con control de conflictos) · E10 insolvencia | Abrir cuota litis laboral solo si hay capacidad o abogado asociado | Decisión de contratar o asociar abogado |
| **4 · Tránsito** | 2028, o antes si hay abogado asociado | E11 accidentes (guía, pruebas, plazos y calculadora gratis; calculadora premium sin recomendación; sin cuota litis hasta tener abogado asociado) · E12 fotomultas | Cuota litis de accidentes solo con abogado asociado | Primer caso de tránsito sin queja disciplinaria |

Detalle de épicas en `06-backlog-claude-code.md`.
