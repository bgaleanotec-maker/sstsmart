# Unit economics y métricas

---

## 1. CAC por canal

Estimaciones para el mercado colombiano de SaaS B2B pyme. **Todos son [E]** — mídelos desde el primer mes y reemplázalos por datos reales.

| Canal | CAC estimado | Ciclo | Volumen posible | Comentario |
|---|---:|---|---|---|
| **Canal de consultores** | **$400.000 – $900.000** | 3–6 semanas | Bajo (5–10 al año) | **El mejor CAC del plan.** Un consultor trae 5–40 empresas |
| **Referidos de clientes** | $200.000 – $500.000 | 2–4 semanas | Bajo al inicio, crece | El más barato. Exige producto que la gente quiera recomendar |
| **SEO y contenido** | $600.000 – $1.500.000 | 4–8 semanas | Medio-alto, crece con el tiempo | **La ventana mayo–julio concentra la mitad del tráfico del año** |
| **Gremios (Fenalco, ACOPI, cámaras)** | $800.000 – $2.000.000 | 2–4 meses | Medio, por lotes | Requiere convenio; alta credibilidad |
| **Google Ads** | $1.200.000 – $2.500.000 | 2–6 semanas | Alto, con presupuesto | Palabras clave caras en la ventana estacional |
| **Venta saliente (outbound)** | $2.000.000 – $4.000.000 | 2–4 meses | Bajo por persona | Solo para Corporativo y PESV, donde el ticket lo justifica |

**Recomendación de asignación de esfuerzo:**

| Etapa | Prioridad |
|---|---|
| Meses 1–6 | Referidos + red personal + 2 consultores piloto |
| Meses 7–12 | **Canal de consultores** + SEO de fondo |
| Meses 13–18 | SEO maduro + gremios + Ads en la ventana estacional |
| Meses 19–24 | Todo lo anterior + outbound para Corporativo y PESV |

---

## 2. LTV por segmento

$$LTV = ARPA \times Margen\ bruto \times \frac{1}{Churn\ mensual}$$

Con margen bruto del **80%** (SaaS puro; el retainer jurídico tiene margen menor porque consume horas de abogado):

| Segmento | ARPA | Churn mensual | Vida media | **LTV** |
|---|---:|---:|---:|---:|
| Esencial | $149.000 | 3,0% | 33 meses | **$3.960.000** |
| Profesional | $349.000 | 2,0% | 50 meses | **$13.960.000** |
| Profesional + PESV + Legal | $838.000 | 1,2% | 83 meses | **$55.600.000** |
| Corporativo | $749.000 | 1,0% | 100 meses | **$59.920.000** |
| **Canal (10 empresas)** | $786.000 | **0,8%** | **125 meses** | **$78.600.000** |

> **Dos conclusiones que deberían dirigir todo el esfuerzo comercial:**
>
> 1. **El canal tiene el mejor LTV y el mejor CAC simultáneamente.** No es un empate: gana en las dos dimensiones. Un consultor con 20 empresas migradas tiene un costo de cambio altísimo — volver a Excel le cuesta semanas de trabajo.
> 2. **Un cliente con add-ons vale 4 veces un cliente sin ellos** ($55,6M contra $13,96M), y no solo por el ARPA: el churn cae de 2,0% a 1,2% porque el costo de cambio sube con cada módulo activo.

---

## 3. Ratios

| Segmento | LTV | CAC | **LTV/CAC** | **Payback** |
|---|---:|---:|---:|---:|
| Esencial | $3,96M | $1,20M | **3,3×** | 10 meses |
| Profesional | $13,96M | $1,20M | **11,6×** | 4,3 meses |
| Profesional + add-ons | $55,60M | $1,50M | **37,1×** | 2,2 meses |
| Corporativo | $59,92M | $3,00M | **20,0×** | 5,0 meses |
| **Canal** | $78,60M | $0,70M | **112×** | **1,1 meses** |

**Referencias de la industria:** LTV/CAC ≥ 3× es sano · ≥ 5× es excelente · payback < 12 meses es sano, < 6 meses es excelente.

> **El Esencial está en el límite.** Con LTV/CAC de 3,3× y payback de 10 meses, solo tiene sentido como **puerta de entrada** hacia el Profesional y los add-ons, no como producto final. Si al mes 12 más del 50% de los clientes de Esencial sigue en Esencial, o subes su precio, o le quitas funcionalidad para forzar el salto, o dejas de venderlo.

---

## 4. Márgenes

| Línea | Margen bruto | Por qué |
|---|---:|---|
| Suscripción SaaS | **~85%** | Infraestructura + pasarela + soporte |
| Add-on PESV | **~85%** | Mismo software |
| Retainer Legal Básico | **~60%** | 2 consultas/mes consumen horas de abogado |
| Retainer Legal Plus | **~50%** | 6 consultas |
| Retainer Legal Defensa | **~35%** | Consultas ilimitadas + acompañamiento presencial |
| Servicios por proyecto | **~45%** | Intensivos en horas |
| **Mezcla al mes 24** | **~76%** | |

> **La regla del retainer:** el margen depende enteramente de la **biblioteca de respuestas**. Con las 50 consultas más frecuentes resueltas por plantilla que el abogado adapta y firma, Legal Básico se sostiene en 60%. Sin ella, cada consulta es trabajo desde cero y el margen se desploma. **Construye la biblioteca antes de vender el décimo retainer, no después.**

---

## 5. Tablero de KPIs

### 5.1 Semanal

| Métrica | Umbral de alarma |
|---|---|
| Nuevos registros de prueba | <5/semana en el mes 6+ |
| Conversión de prueba a pago | <15% |
| Demos o llamadas agendadas | <3/semana |
| Tickets de soporte abiertos >48 h | >5 |

### 5.2 Mensual

| Métrica | Objetivo m12 | Objetivo m24 | Alarma |
|---|---|---|---|
| **MRR** | $12,5M | $29,7M | −20% del plan por 2 meses |
| MRR nuevo | $1,2M | $1,5M | — |
| MRR de expansión (upsell) | $200.000 | $600.000 | <10% del MRR nuevo |
| MRR perdido (churn) | <$250.000 | <$450.000 | >3% del MRR |
| **Cuentas activas** | 32 | 64 | — |
| **ARPA** | $390.000 | $461.329 | <$350.000 |
| **Churn mensual de logos** | <2,0% | <1,5% | >2,5% |
| **Churn de ingresos (neto)** | <1,5% | **negativo** | positivo por 3 meses |
| **Attach PESV** | 15% | 23% | <10% |
| **Attach jurídico** | 15% | 23% | <10% |
| CAC combinado | <$1,2M | <$1,5M | >$2M |
| Payback | <6 meses | <5 meses | >12 meses |
| Utilidad operativa | $7,2M | $9,2M | negativa 2 meses |
| Caja disponible | >3 meses de costos | >6 meses | <2 meses |

**El objetivo más ambicioso de la lista: churn de ingresos neto negativo al mes 24.** Significa que la expansión (upsells y add-ons) supera lo que se pierde por cancelaciones — es decir, que el negocio crece aunque no entre un cliente nuevo. Es lo que separa un SaaS bueno de uno mediocre, y en este modelo se consigue con add-ons y con el crecimiento del número de empresas dentro de cada cuenta de canal.

### 5.3 De producto

| Métrica | Por qué importa |
|---|---|
| Empresas con autoevaluación Res. 0312 completada | **Predictor #1 de retención.** El cliente que la completó tiene un activo que no quiere perder |
| Documentos cargados por empresa | Costo de cambio |
| Usuarios activos semanales por cuenta | Si solo entra una persona, el cliente es frágil |
| Reportes de condiciones inseguras/mes | Adopción real en piso de planta |
| Consultas jurídicas por cuenta con retainer | Control del margen del retainer |
| Empresas por cuenta de canal | Salud del canal (objetivo: 8) |
| Alertas normativas abiertas / total enviadas | Si nadie las abre, la matriz legal no está entregando valor percibido |

---

## 6. Señales de alarma temprana

| Señal | Qué significa | Qué hacer |
|---|---|---|
| Churn del Esencial >4% | El plan no entrega valor suficiente | Subir funcionalidad o descontinuarlo |
| Attach de add-ons <10% al mes 12 | El momento o el mensaje de la oferta está mal | Mover la oferta al mes 2–3 de uso; probar bundle |
| ARPA en caída sostenida | Descuentos fuera de control o mix hacia Esencial | Revisar la política de descuentos |
| CAC creciente con conversión estable | El canal se está saturando | Diversificar antes de que se agote |
| Consultas del retainer por encima del cupo, sistemáticamente | El precio está mal calibrado | Ajustar cupo o precio **antes** de escalar el plan |
| Servicios >35% del ingreso al mes 18 | Te estás convirtiendo en consultora | Rechazar proyectos que no dejen algo reutilizable |
| Un solo cliente >15% del MRR | Riesgo de concentración | Diversificar antes de que se vaya |
| Usuarios activos por cuenta = 1 | El cliente no adoptó, solo compró | Campaña de activación; es churn diferido |

---

## 7. Qué medir desde el primer día

No esperes a tener 20 clientes para instrumentar. Con **PostHog en plan gratuito** (1M eventos/mes) alcanza de sobra:

1. **Embudo de registro:** landing → registro → onboarding completado → primer documento cargado → primer pago.
2. **Time to value:** cuánto tarda una cuenta nueva en completar su primera autoevaluación. Si son más de 7 días, el onboarding está roto.
3. **Origen de cada cuenta**, con UTM, para calcular CAC por canal de verdad y no por intuición.
4. **Eventos de add-on:** quién ve la oferta, quién la abre, quién convierte.
5. **Grabaciones de sesión** de los primeros 20 clientes. Es la información cualitativa más barata y más valiosa que vas a conseguir: vas a ver exactamente dónde se traban.
