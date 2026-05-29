"""Génère un jeu de prêts FLI/FLS/PAUPME fictif mais réaliste pour le MVP.

Sortie : examples/portfolio_simulator/data/prets.csv

Remplace ce fichier par tes vraies données quand tu les auras (mêmes en-têtes).
"""
from __future__ import annotations
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)  # reproductible

OUT = Path(__file__).parent / "data" / "prets.csv"

FONDS_MIX = [
    ("FLI", 0.45, (50_000, 250_000), (5.5, 9.0), (36, 84)),
    ("FLS", 0.30, (75_000, 300_000), (6.0, 8.5), (48, 84)),
    ("PAUPME", 0.25, (10_000, 50_000), (3.0, 3.0), (36, 60)),
]
SECTEURS = [
    "Manufacturier", "Services professionnels", "Commerce de détail",
    "Restauration", "Technologies", "Construction", "Tourisme",
    "Agroalimentaire", "Transport", "Santé",
]
STATUT_WEIGHTS = [("Actif", 0.78), ("Remboursé", 0.15), ("Radié", 0.04), ("En défaut", 0.03)]

def weighted_choice(pairs):
    r, cum = random.random(), 0.0
    for val, w in pairs:
        cum += w
        if r <= cum:
            return val
    return pairs[-1][0]

def pick_fonds():
    r, cum = random.random(), 0.0
    for row in FONDS_MIX:
        cum += row[1]
        if r <= cum:
            return row
    return FONDS_MIX[-1]

def gen_pret(i: int) -> dict:
    fonds, _, (cmin, cmax), (tmin, tmax), (dmin, dmax) = pick_fonds()
    capital = round(random.uniform(cmin, cmax), -3)  # arrondi au 1000$
    taux = round(random.uniform(tmin, tmax), 2)
    duree = random.choice(range(dmin, dmax + 1, 6))
    decaiss = date(2021, 1, 1) + timedelta(days=random.randint(0, 1700))
    statut = weighted_choice(STATUT_WEIGHTS)
    # PAUPME = moratoire COVID plus long
    moratoire = random.choice([12, 18, 24]) if fonds == "PAUPME" else random.choice([0, 0, 0, 6, 12])
    return {
        "id_pret": f"P-{decaiss.year}-{i:04d}",
        "fonds": fonds,
        "entreprise": f"Entreprise {chr(65 + (i % 26))}{i:03d} inc.",
        "secteur": random.choice(SECTEURS),
        "date_decaissement": decaiss.isoformat(),
        "capital_initial": capital,
        "taux_interet": taux,
        "duree_mois": duree,
        "mois_moratoire": moratoire,
        "frequence": "Mensuelle",
        "jour_prelevement": random.choice([1, 8, 15, 15, 15, 20, 22, 25]),  # biais vers le 15
        "statut": statut,
    }

def main(n: int = 60) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = [gen_pret(i + 1) for i in range(n)]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    total = sum(r["capital_initial"] for r in rows)
    print(f"✓ {n} prêts générés → {OUT}")
    print(f"  Capital déployé total (fictif) : {total:,.0f} $")
    by_fonds = {}
    for r in rows:
        by_fonds.setdefault(r["fonds"], 0)
        by_fonds[r["fonds"]] += r["capital_initial"]
    for fonds, montant in by_fonds.items():
        print(f"  {fonds:<8} : {montant:>12,.0f} $  ({montant/total*100:>4.1f} %)")

if __name__ == "__main__":
    main()
