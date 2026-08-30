# -*- coding: utf-8 -*-
"""
Modelo financiero SST Smart — ruta a $30.000.000 COP/mes.

Uso:
    python scripts/modelo_financiero.py            # tabla mes a mes (escenario base)
    python scripts/modelo_financiero.py --esc      # comparación de los tres escenarios

Documentación: docs/05-monetizacion/02-modelo-financiero-30M.md
Todos los supuestos están arriba, en constantes. Cámbialos y vuelve a correr.
"""
import sys

# --- Supuestos de precio (COP/mes) -----------------------------------------
PRECIOS = {
    "esencial":     149_000,
    "profesional":  349_000,
    "corporativo":  749_000,
    "canal":        590_000,   # hasta 10 empresas
    "canal_extra":   49_000,   # empresa adicional dentro de una cuenta canal
    "pesv_prom":    299_000,   # promedio ponderado basico/estandar/avanzado
    "legal_prom":   400_000,   # promedio ponderado Basico/Plus/Defensa
}

# --- Altas netas por mes (escenario base, 24 meses) ------------------------
ALTAS = {
    "esencial":    [1,1,1,2,2,2, 2,2,2,2,2,2, 2,2,2,2,2,2, 1,1,1,1,1,1],
    "profesional": [0,0,1,1,1,1, 1,1,1,1,1,1, 1,1,1,2,2,2, 2,2,2,2,2,2],
    "corporativo": [0,0,0,0,0,0, 0,0,0,0,0,1, 0,0,1,0,0,0, 0,1,0,0,0,0],
    "canal":       [0,0,0,0,1,0, 0,1,0,0,1,0, 0,1,0,0,1,0, 0,1,0,0,0,0],
}

CHURN_MENSUAL = 0.020   # 2,0% mensual de logos (24% anual)
USD = 4_100             # TRM de trabajo
PASARELA = 0.0315       # Wompi 2,65% + $700 + IVA, efectivo


def run(mult=1.0, churn=CHURN_MENSUAL):
    """Devuelve una lista de dicts, uno por mes."""
    base = {k: 0.0 for k in ALTAS}
    filas = []
    for m in range(24):
        for k in ALTAS:
            base[k] = base[k] * (1 - churn) + ALTAS[k][m] * mult

        cuentas_directas = base["esencial"] + base["profesional"] + base["corporativo"]
        cuentas_total = cuentas_directas + base["canal"]
        emp_por_consultor = 4 + min(4, m // 6)   # el consultor migra su cartera

        mrr_saas = (
            base["esencial"]    * PRECIOS["esencial"]
            + base["profesional"] * PRECIOS["profesional"]
            + base["corporativo"] * PRECIOS["corporativo"]
            + base["canal"]       * PRECIOS["canal"]
            + base["canal"] * emp_por_consultor * PRECIOS["canal_extra"]
        )

        attach_pesv  = 0.10 + 0.13 * min(1, m / 20)
        attach_legal = 0.08 + 0.15 * min(1, m / 20)
        mrr_pesv  = cuentas_directas * attach_pesv  * PRECIOS["pesv_prom"]
        mrr_legal = cuentas_directas * attach_legal * PRECIOS["legal_prom"]
        mrr = mrr_saas + mrr_pesv + mrr_legal

        # servicios por proyecto (implementaciones, disenos PESV, auditorias)
        servicios = min(6_500_000, 2_000_000 + 220_000 * m) * mult

        filas.append(dict(
            mes=m + 1, cuentas=cuentas_total,
            mrr_saas=mrr_saas, mrr_pesv=mrr_pesv, mrr_legal=mrr_legal,
            mrr=mrr, servicios=servicios, total=mrr + servicios,
        ))
    return filas


def costos(idx_mes, cuentas, ingreso):
    """Costos del mes. idx_mes es 0-based."""
    if cuentas < 15:
        infra = 40 * USD
    elif cuentas < 60:
        infra = 160 * USD
    else:
        infra = 700 * USD

    herramientas = 350_000 if idx_mes < 12 else 900_000
    contable = 700_000 if idx_mes < 6 else 1_300_000      # 2 sociedades desde el mes 6
    marketing = 800_000 if idx_mes < 11 else 2_000_000

    nomina = 0
    if idx_mes >= 6:  nomina += 4_900_000   # desarrollador semi-senior
    if idx_mes >= 12: nomina += 4_600_000   # comercial
    if idx_mes >= 17: nomina += 4_200_000   # soporte / CS
    if idx_mes >= 19: nomina += 5_100_000   # abogado junior (retainer)

    return infra + herramientas + contable + marketing + nomina + ingreso * PASARELA


def cop(x):
    return f"{round(x):,}".replace(",", ".")


def tabla():
    print("| Mes | Cuentas | MRR SaaS | MRR PESV | MRR Legal | MRR total | Servicios | Ingreso | Costos | Utilidad |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    acum = 0
    for r in run():
        c = costos(r["mes"] - 1, r["cuentas"], r["total"])
        acum += r["total"] - c
        print(f"| {r['mes']} | {r['cuentas']:.0f} | {cop(r['mrr_saas'])} | {cop(r['mrr_pesv'])} "
              f"| {cop(r['mrr_legal'])} | {cop(r['mrr'])} | {cop(r['servicios'])} "
              f"| {cop(r['total'])} | {cop(c)} | {cop(r['total'] - c)} |")
    f = run()[-1]
    print(f"\nMes 24 — MRR {cop(f['mrr'])} · ingreso {cop(f['total'])} · ARR {cop(f['mrr']*12)}")
    print(f"          cuentas {f['cuentas']:.0f} · ARPA {cop(f['mrr']/f['cuentas'])} · utilidad acumulada {cop(acum)}")


def escenarios():
    for nombre, (mult, churn) in {
        "Conservador": (0.70, 0.030),
        "Base":        (1.00, 0.020),
        "Agresivo":    (1.35, 0.015),
    }.items():
        r = run(mult, churn)
        m12, m18, m24 = r[11], r[17], r[23]
        cruce_mrr = next((x["mes"] for x in r if x["mrr"] >= 30_000_000), None)
        cruce_tot = next((x["mes"] for x in r if x["total"] >= 30_000_000), None)
        print(f"{nombre:12} | MRR m12 {cop(m12['mrr']):>12} | m18 {cop(m18['mrr']):>12} "
              f"| m24 {cop(m24['mrr']):>12} | cuentas m24 {m24['cuentas']:.0f}")
        print(f"{'':12} | ingreso m24 {cop(m24['total']):>12} | ARR {cop(m24['mrr']*12):>12} "
              f"| ingreso>=30M mes {cruce_tot or '>24'} | MRR>=30M mes {cruce_mrr or '>24'}\n")


if __name__ == "__main__":
    escenarios() if "--esc" in sys.argv else tabla()
