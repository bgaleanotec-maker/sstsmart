"""Modelo de la plataforma multivertical + la práctica jurídica de Brian.

Responde tres preguntas con supuestos explícitos (todos [E] = estimación, ajustables):
  1. ¿Cuánto vale una hora de abogado en cada línea de servicio?
  2. Con la capacidad real de horas, ¿qué parte de la demanda se atiende y cuánto deja?
  3. ¿Cuánto aporta cada entidad (S.A.S. y abogado) en devengado y en caja?

Uso (desde la raíz del repo):
    python plataforma/modelo/modelo_plataforma.py              # 60 h/mes de abogado
    python plataforma/modelo/modelo_plataforma.py --horas 160  # con un abogado de tiempo completo

Convenciones:
- Mes 1 = mes de constitución de la S.A.S. (supuesto: nov-2026) → mes 12 ≈ oct-2027, mes 24 ≈ oct-2028.
- El modelo SaaS B2B (SST + PESV) es el de docs/05-monetizacion/02-modelo-financiero-30M.md
  (scripts/modelo_financiero.py). Aquí se le RESTA el retainer, porque el retainer lo factura
  el abogado y consume sus horas.
- Precios B2C con IVA incluido (regla 11 de producto): el ingreso de la S.A.S. es precio / 1,19
  menos la comisión de pasarela.
- Las horas de cuota litis se cuentan completas por caso nuevo: es un proxy de estado
  estacionario (líneas abiertas hace más de ~15 meses). Al abrir la línea, la carga real es menor
  y la caja es cero durante el rezago.
- Asignación de horas: primero los compromisos contractuales recurrentes (retainer), luego las
  líneas de mayor valor esperado por hora (no en proporción).
- Sin dependencias externas.
"""
from __future__ import annotations

import argparse

IVA = 0.19
COMISION_PASARELA = 0.0315
TOPE_NO_RESPONSABLE_IVA_ANUAL = 3_500 * 52_374  # 3.500 UVT 2026 (art. 437 par. 3 ET)

# ---------------------------------------------------------------------------
# Práctica jurídica (factura el abogado persona natural)
# ---------------------------------------------------------------------------
LINEAS_ABOGADO = {
    "defensa_dian": dict(nombre="Defensa DIAN (70% requerimiento ordinario / 30% especial o recurso)",
                         ticket=0.7 * 550_000 + 0.3 * 2_500_000, horas=0.7 * 4 + 0.3 * 14,
                         p_exito=1.0, rezago=0),
    "tutela_compleja": dict(nombre="Tutela compleja: impugnación, desacato difícil, pensión (fijo)",
                            ticket=400_000, horas=2.5, p_exito=1.0, rezago=0),
    "retainer_b2b": dict(nombre="Retainer jurídico SST/PESV (por cliente-mes)",
                         ticket=400_000, horas=3.0, p_exito=1.0, rezago=0),
    "laboral_cuota_litis": dict(nombre="Laboral trabajador, cuota litis 25% sobre $15M recuperados",
                                ticket=0.25 * 15_000_000, horas=25, p_exito=0.6, rezago=15),
    "accidente_cuota_litis": dict(nombre="Accidente de tránsito RC, cuota litis 25% sobre $25M",
                                  ticket=0.25 * 25_000_000, horas=30, p_exito=0.6, rezago=12),
}

# Demanda: casos NUEVOS por mes (clientes activos, para el retainer) [E].
# Cuota litis: laboral solo desde la Fase 3 y sujeta a capacidad; accidentes sin cuota litis
# hasta tener abogado asociado (03-priorizacion §4).
DEMANDA_ABOGADO = {
    12: dict(defensa_dian=6, tutela_compleja=8, retainer_b2b=7, laboral_cuota_litis=0, accidente_cuota_litis=0),
    24: dict(defensa_dian=10, tutela_compleja=15, retainer_b2b=15, laboral_cuota_litis=3, accidente_cuota_litis=0),
}

# ---------------------------------------------------------------------------
# Capa B2C de la S.A.S. — herramientas automáticas, SIN análisis del caso concreto
# (precio con IVA, unidades o suscripciones activas por mes) [E]
# ---------------------------------------------------------------------------
PRODUCTOS_SAS = {
    "tutela_premium": ("Tutela/petición premium: chequeo automático de soportes, citas de la biblioteca y paquete de radicación", 49_900),
    "seguimiento": ("Suscripción de seguimiento de plazos y desacato", 19_900),
    "calendario_trib": ("Calendario tributario + alertas por NIT", 29_900),
    "informe_dian": ("Informe automático de un acto DIAN: tipo, vencimiento y sanción simulada (sin recomendación)", 49_000),
    "calculadora_accidente": ("Calculadora premium de accidente: topes SOAT y rangos (sin recomendación)", 79_000),
}
ESCENARIO_SAS = {
    12: dict(tutela_premium=80, seguimiento=60, calendario_trib=30, informe_dian=25, calculadora_accidente=0),
    24: dict(tutela_premium=250, seguimiento=250, calendario_trib=150, informe_dian=80, calculadora_accidente=30),
}

# Totales del modelo SaaS base (escenario base) y el retainer que incluyen
SAAS_BASE = {12: 16_910_000, 24: 36_194_280}
RETAINER_EN_BASE = {12: 7 * 400_000, 24: 5_481_840}


def cop(x: float) -> str:
    return f"${x:,.0f}".replace(",", ".")


def neto_sas(precio_con_iva: float) -> float:
    return precio_con_iva / (1 + IVA) * (1 - COMISION_PASARELA)


def valor_hora(k: str) -> float:
    l = LINEAS_ABOGADO[k]
    return l["ticket"] * l["p_exito"] / l["horas"]


def asignar(mes: int, horas_disp: float) -> dict:
    """Retainer primero (es un compromiso mensual ya vendido); luego por valor/hora."""
    restantes, atendidos = horas_disp, {}
    orden = ["retainer_b2b"] + sorted((k for k in LINEAS_ABOGADO if k != "retainer_b2b"),
                                      key=valor_hora, reverse=True)
    for k in orden:
        demanda = DEMANDA_ABOGADO[mes].get(k, 0)
        posibles = int(restantes // LINEAS_ABOGADO[k]["horas"])
        n = min(demanda, max(posibles, 0))
        atendidos[k] = n
        restantes -= n * LINEAS_ABOGADO[k]["horas"]
    return atendidos


def resumen_abogado(casos: dict) -> tuple[float, float, float]:
    horas = sum(LINEAS_ABOGADO[k]["horas"] * n for k, n in casos.items())
    devengado = sum(LINEAS_ABOGADO[k]["ticket"] * LINEAS_ABOGADO[k]["p_exito"] * n for k, n in casos.items())
    caja = sum(LINEAS_ABOGADO[k]["ticket"] * n for k, n in casos.items() if LINEAS_ABOGADO[k]["rezago"] == 0)
    return horas, devengado, caja


def main(horas_disp: float):
    print("## 1. Valor esperado por hora de abogado\n")
    print("| Línea | Ticket | Horas/caso | P(cobro) | Rezago (meses) | Valor esperado/hora |")
    print("|---|---:|---:|---:|---:|---:|")
    for k in sorted(LINEAS_ABOGADO, key=valor_hora, reverse=True):
        l = LINEAS_ABOGADO[k]
        print(f"| {l['nombre']} | {cop(l['ticket'])} | {l['horas']:.1f} | {l['p_exito']:.0%} | {l['rezago']} | {cop(valor_hora(k))} |")

    print(f"\n## 2. Demanda vs. capacidad ({horas_disp:.0f} h/mes; retainer primero, luego por valor/hora)\n")
    print("| Corte | Horas que pide la demanda | Horas usadas | Casos no atendidos | Abogado devengado | Abogado en caja | Anualizado vs. tope IVA (3.500 UVT) |")
    print("|---|---:|---:|---|---:|---:|---|")
    atendidos_por_mes = {}
    for mes in (12, 24):
        h_dem, _, _ = resumen_abogado(DEMANDA_ABOGADO[mes])
        at = asignar(mes, horas_disp)
        atendidos_por_mes[mes] = at
        h_us, dev, caja = resumen_abogado(at)
        faltan = {k: DEMANDA_ABOGADO[mes][k] - at[k] for k in at if DEMANDA_ABOGADO[mes][k] - at[k] > 0}
        faltan_txt = ", ".join(f"{k}: {v}" for k, v in faltan.items()) or "ninguno"
        anual = caja * 12
        iva_txt = "supera" if anual > TOPE_NO_RESPONSABLE_IVA_ANUAL else "por debajo"
        print(f"| Mes {mes} | {h_dem:.0f} | {h_us:.0f} | {faltan_txt} | {cop(dev)} | {cop(caja)} | {cop(anual)} ({iva_txt}) |")

    print("\n## 3. Consolidado por entidad\n")
    print("| Corte | S.A.S.: SaaS B2B sin retainer | S.A.S.: capa B2C neta (sin IVA ni pasarela) | **S.A.S. total** | Abogado en caja (incluye retainer) | Abogado devengado | **Grupo en caja** | Grupo devengado |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    for mes in (12, 24):
        saas = SAAS_BASE[mes] - RETAINER_EN_BASE[mes]
        b2c = sum(neto_sas(PRODUCTOS_SAS[k][1]) * n for k, n in ESCENARIO_SAS[mes].items())
        _, dev, caja = resumen_abogado(atendidos_por_mes[mes])
        print(f"| Mes {mes} | {cop(saas)} | {cop(b2c)} | **{cop(saas + b2c)}** | {cop(caja)} | {cop(dev)} | **{cop(saas + b2c + caja)}** | {cop(saas + b2c + dev)} |")

    print("\n## 4. Unidades necesarias para $5M/mes netos en la S.A.S.\n")
    print("| Producto | Precio con IVA | Neto por unidad | Unidades para $5M |")
    print("|---|---:|---:|---:|")
    for k, (nombre, precio) in PRODUCTOS_SAS.items():
        n = neto_sas(precio)
        print(f"| {nombre} | {cop(precio)} | {cop(n)} | {5_000_000 / n:,.0f} |")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--horas", type=float, default=60, help="horas/mes que el abogado dedica a la práctica")
    main(ap.parse_args().horas)
