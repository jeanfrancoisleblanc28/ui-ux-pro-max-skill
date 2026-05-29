"""Simulateur de portefeuille FLI / FLS / PAUPME — MVP.

Charge data/prets.csv et calcule : capital restant dû, échéancier projeté,
mix par fonds/secteur, scénarios de stress (défauts, taux).

Lancer :  streamlit run examples/portfolio_simulator/portfolio_simulator.py
"""
from __future__ import annotations
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parent / "data" / "prets.csv"

# Palette
PRIMARY, SECONDARY, ACCENT, ALERT, OK = "#24135D", "#0057B8", "#00AEC7", "#E26D5C", "#2EA86F"
FONDS_COLORS = {"FLI": PRIMARY, "FLS": SECONDARY, "PAUPME": ACCENT}

st.set_page_config(page_title="Portefeuille FLI/FLS/PAUPME", layout="wide")

# --------------------------------------------------------------------------
# CALCULS
# --------------------------------------------------------------------------
def mensualite(p: float, taux_annuel: float, n_mois: int) -> float:
    if n_mois <= 0:
        return 0.0
    r = taux_annuel / 100 / 12
    if r == 0:
        return p / n_mois
    return p * r / (1 - (1 + r) ** -n_mois)

def crd(p: float, taux_annuel: float, duree: int, mois_ecoules: int, moratoire: int = 0) -> float:
    """Capital restant dû. Pendant le moratoire, le capital ne baisse pas (intérêts capitalisés ignorés ici)."""
    mois_amort = max(0, mois_ecoules - moratoire)
    n = max(0, duree - moratoire)
    if mois_amort >= n:
        return 0.0
    if n == 0:
        return p
    r = taux_annuel / 100 / 12
    if r == 0:
        return max(0.0, p * (1 - mois_amort / n))
    m = mensualite(p, taux_annuel, n)
    # CRD après k paiements = M * (1 - (1+r)^-(n-k)) / r
    return m * (1 - (1 + r) ** -(n - mois_amort)) / r

def echeancier_pret(row: pd.Series, horizon_mois: int, ref: date) -> pd.DataFrame:
    """Retourne les flux mensuels (capital + intérêts) attendus pour ce prêt."""
    if row["statut"] in ("Remboursé", "Radié"):
        return pd.DataFrame()
    p = float(row["capital_initial"])
    taux = float(row["taux_interet"])
    duree = int(row["duree_mois"])
    moratoire = int(row["mois_moratoire"])
    decaiss = pd.to_datetime(row["date_decaissement"]).date()
    mois_depuis_decaiss = (ref.year - decaiss.year) * 12 + (ref.month - decaiss.month)
    n_amort = max(1, duree - moratoire)
    m = mensualite(p, taux, n_amort)
    r = taux / 100 / 12
    rows = []
    for h in range(horizon_mois):
        mois_idx = mois_depuis_decaiss + h
        # Avant le moratoire : seulement intérêts (optionnel — ici on ignore aussi)
        if mois_idx < moratoire:
            interets = 0.0
            capital = 0.0
        else:
            mois_amort = mois_idx - moratoire
            if mois_amort >= n_amort:
                interets = capital = 0.0
            else:
                crd_avant = m * (1 - (1 + r) ** -(n_amort - mois_amort)) / r if r else p * (1 - mois_amort / n_amort)
                interets = crd_avant * r
                capital = m - interets
        annee = ref.year + (ref.month + h - 1) // 12
        mois = (ref.month + h - 1) % 12 + 1
        rows.append({
            "id_pret": row["id_pret"], "fonds": row["fonds"],
            "mois": pd.Timestamp(year=annee, month=mois, day=1),
            "capital": capital, "interets": interets, "total": capital + interets,
        })
    return pd.DataFrame(rows)

def appliquer_defaut(df_ech: pd.DataFrame, taux_defaut_pct: float) -> pd.DataFrame:
    """Réduit linéairement les perceptions attendues du taux de défaut additionnel."""
    if taux_defaut_pct <= 0:
        return df_ech
    facteur = 1 - taux_defaut_pct / 100
    out = df_ech.copy()
    out[["capital", "interets", "total"]] *= facteur
    return out

# --------------------------------------------------------------------------
# CHARGEMENT
# --------------------------------------------------------------------------
@st.cache_data
def load_prets(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["date_decaissement"])

if not DATA.exists():
    st.error(f"Fichier introuvable : {DATA}\n\nLance d'abord : `python3 examples/portfolio_simulator/generate_fake_data.py`")
    st.stop()

prets = load_prets(DATA)

# --------------------------------------------------------------------------
# SIDEBAR
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"<h2 style='color:{PRIMARY};'>Paramètres</h2>", unsafe_allow_html=True)

    ref_date = st.date_input("Date d'évaluation", value=date(2026, 5, 31))
    horizon = st.slider("Horizon de projection (mois)", 6, 60, 24, step=6)

    st.markdown("**Filtres**")
    fonds_sel = st.multiselect("Fonds", ["FLI", "FLS", "PAUPME"], default=["FLI", "FLS", "PAUPME"])
    secteurs_dispo = sorted(prets["secteur"].unique())
    secteurs_sel = st.multiselect("Secteurs", secteurs_dispo, default=secteurs_dispo)

    st.markdown("**Stress tests**")
    taux_defaut_add = st.slider("Défauts additionnels (%)", 0.0, 30.0, 0.0, step=0.5,
                                 help="Réduction linéaire des perceptions attendues")
    inclure_defaut = st.checkbox("Inclure prêts 'En défaut' dans la projection", value=False)

# Filtre
mask = prets["fonds"].isin(fonds_sel) & prets["secteur"].isin(secteurs_sel)
if not inclure_defaut:
    mask &= prets["statut"] != "En défaut"
df = prets[mask].copy()

# --------------------------------------------------------------------------
# CRD par prêt
# --------------------------------------------------------------------------
def calc_crd_row(r):
    if r["statut"] in ("Remboursé", "Radié"):
        return 0.0
    decaiss = r["date_decaissement"].date()
    mois_ecoules = (ref_date.year - decaiss.year) * 12 + (ref_date.month - decaiss.month)
    return crd(r["capital_initial"], r["taux_interet"], r["duree_mois"], mois_ecoules, r["mois_moratoire"])

df["crd"] = df.apply(calc_crd_row, axis=1)

# --------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------
st.markdown(f"<h1 style='color:{PRIMARY};margin-bottom:0;'>Portefeuille FLI / FLS / PAUPME</h1>", unsafe_allow_html=True)
st.caption(f"Évaluation au {ref_date:%d %B %Y} — données : `{DATA.name}`")

# --------------------------------------------------------------------------
# KPI cards
# --------------------------------------------------------------------------
k1, k2, k3, k4, k5 = st.columns(5)
total_deploye = df["capital_initial"].sum()
total_crd = df["crd"].sum()
nb_actifs = (df["statut"] == "Actif").sum()
nb_defauts = (df["statut"] == "En défaut").sum()
expo_max = df["crd"].max() if not df.empty else 0
concentration = expo_max / total_crd * 100 if total_crd else 0

k1.metric("Capital déployé", f"{total_deploye:,.0f} $")
k2.metric("Capital restant dû", f"{total_crd:,.0f} $", f"{total_crd/total_deploye*100:.0f} % déployé" if total_deploye else "—")
k3.metric("Prêts actifs", f"{nb_actifs}", f"{len(df)} au total")
k4.metric("Prêts en défaut", f"{nb_defauts}", f"{nb_defauts/len(df)*100:.1f} %" if len(df) else "—")
k5.metric("Top exposition", f"{expo_max:,.0f} $", f"{concentration:.1f} % du CRD")

st.markdown("---")

# --------------------------------------------------------------------------
# Échéancier projeté
# --------------------------------------------------------------------------
ech_parts = [echeancier_pret(r, horizon, ref_date) for _, r in df.iterrows() if r["statut"] not in ("Remboursé", "Radié")]
ech = pd.concat(ech_parts, ignore_index=True) if ech_parts else pd.DataFrame(columns=["mois", "fonds", "capital", "interets", "total"])
ech = appliquer_defaut(ech, taux_defaut_add)

c1, c2 = st.columns([2, 1])
with c1:
    st.subheader("Projection des perceptions")
    if ech.empty:
        st.info("Aucune perception projetée — vérifie les filtres.")
    else:
        agg = ech.groupby(["mois", "fonds"]).agg(total=("total", "sum")).reset_index()
        fig = px.bar(agg, x="mois", y="total", color="fonds",
                     color_discrete_map=FONDS_COLORS,
                     labels={"total": "Perception ($)", "mois": ""})
        fig.update_layout(height=380, legend_title="", margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, width='stretch')
        proj_12 = ech[ech["mois"] < pd.Timestamp(ref_date) + pd.DateOffset(months=12)]["total"].sum()
        st.caption(f"Perception projetée sur les 12 prochains mois : **{proj_12:,.0f} $** "
                   f"({'avec' if taux_defaut_add else 'sans'} stress défauts)")

with c2:
    st.subheader("Mix par fonds (CRD)")
    by_fonds = df.groupby("fonds")["crd"].sum().reset_index()
    fig2 = px.pie(by_fonds, values="crd", names="fonds", hole=0.55,
                  color="fonds", color_discrete_map=FONDS_COLORS)
    fig2.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), showlegend=True)
    st.plotly_chart(fig2, width='stretch')

# --------------------------------------------------------------------------
# Vieillissement (basé sur statut — sera enrichi avec perceptions réelles)
# --------------------------------------------------------------------------
st.markdown("---")
c3, c4 = st.columns(2)
with c3:
    st.subheader("Répartition par statut")
    par_statut = df.groupby("statut").agg(nb=("id_pret", "count"), crd=("crd", "sum")).reset_index()
    fig3 = go.Figure()
    color_map = {"Actif": OK, "Remboursé": ACCENT, "Radié": "#777", "En défaut": ALERT}
    fig3.add_trace(go.Bar(x=par_statut["statut"], y=par_statut["crd"],
                          marker_color=[color_map.get(s, "#999") for s in par_statut["statut"]],
                          text=[f"{n} prêts" for n in par_statut["nb"]], textposition="outside"))
    fig3.update_layout(height=320, yaxis_title="CRD ($)", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig3, width='stretch')

with c4:
    st.subheader("Concentration sectorielle")
    by_sect = df.groupby("secteur")["crd"].sum().sort_values(ascending=True).reset_index()
    fig4 = px.bar(by_sect, x="crd", y="secteur", orientation="h",
                  labels={"crd": "CRD ($)", "secteur": ""})
    fig4.update_traces(marker_color=SECONDARY)
    fig4.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig4, width='stretch')

# --------------------------------------------------------------------------
# Top expositions
# --------------------------------------------------------------------------
st.markdown("---")
st.subheader("Top 10 expositions (CRD)")
top = df.sort_values("crd", ascending=False).head(10)[
    ["id_pret", "fonds", "entreprise", "secteur", "capital_initial", "crd", "statut"]
].rename(columns={"capital_initial": "Capital initial", "crd": "CRD"})
st.dataframe(top.style.format({"Capital initial": "{:,.0f} $", "CRD": "{:,.0f} $"}),
             width='stretch', hide_index=True)

with st.expander("⚠️ Données fictives — pour MVP de démonstration"):
    st.markdown(
        "Ce simulateur utilise un fichier `data/prets.csv` généré par "
        "`generate_fake_data.py`. Remplace-le par tes vraies données (mêmes en-têtes) "
        "pour analyser le portefeuille réel. La modélisation du moratoire est "
        "simplifiée (intérêts non capitalisés). Le vieillissement basé sur les retards "
        "réels sera ajouté quand le fichier historique des perceptions sera branché."
    )
