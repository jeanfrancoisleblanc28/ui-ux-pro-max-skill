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

# --------------------------------------------------------------------------
# CALIBRATION AVEC PERCEPTIONS RÉELLES (modèle V2 : signatures + batch)
# --------------------------------------------------------------------------
st.markdown("---")
st.subheader("📊 Calibration avec perceptions réelles (modèle V2)")
st.caption("Charge un CSV de perceptions historiques (colonnes : `Date`, `Montant`) — "
           "le modèle détecte signatures récurrentes + batch mensuel et projette 12 mois.")

up = st.file_uploader("Perceptions historiques (CSV)", type=["csv", "tsv"],
                       help="Format attendu : 2 colonnes Date + Montant. Séparateur tab ou virgule auto-détecté.")

if up is not None:
    try:
        sample = up.read(2048).decode("utf-8", errors="replace")
        up.seek(0)
        sep = "\t" if sample.count("\t") > sample.count(",") else ","
        per = pd.read_csv(up, sep=sep)
        # Normalise colonnes
        colmap = {}
        for c in per.columns:
            cl = c.lower()
            if "date" in cl or "cree" in cl: colmap[c] = "Date"
            elif "mont" in cl or "amount" in cl: colmap[c] = "Montant"
        per = per.rename(columns=colmap)
        per["Montant"] = per["Montant"].astype(str).str.replace(",", ".", regex=False).astype(float)
        per["Date"] = pd.to_datetime(per["Date"])
        per["Jour"] = per["Date"].dt.day
        per["MontantArr"] = per["Montant"].round(2)
        per = per.sort_values("Date").reset_index(drop=True)

        ref_d = per["Date"].max()
        total_hist = per["Montant"].sum()
        mensuel_moy = per.groupby(per["Date"].dt.to_period("M"))["Montant"].sum().mean()

        c1, c2, c3 = st.columns(3)
        c1.metric("Période couverte", f"{(ref_d - per['Date'].min()).days // 30} mois")
        c2.metric("Total historique", f"{total_hist:,.0f} $")
        c3.metric("Moyenne mensuelle", f"{mensuel_moy:,.0f} $")

        # Détection signatures actives (hors batch jour 13-17)
        hors = per[~per["Jour"].between(13, 17)].copy()
        sig = hors.groupby(["MontantArr", "Jour"]).agg(
            n=("Date", "count"), derniere=("Date", "max")
        ).reset_index()
        sig = sig[sig["n"] >= 3]
        sig = sig[(ref_d - sig["derniere"]).dt.days <= 60]

        def _freq(g):
            if len(g) < 2: return np.nan
            return g["Date"].sort_values().diff().dt.days.dropna().mean()
        fr = hors.groupby(["MontantArr", "Jour"]).apply(_freq, include_groups=False).rename("freq")
        sig = sig.merge(fr, on=["MontantArr", "Jour"], how="left")

        # Tendance du batch mensuel
        batch = per[per["Jour"].between(13, 17)].groupby(
            per[per["Jour"].between(13, 17)]["Date"].dt.to_period("M")
        )["Montant"].sum()
        if len(batch) >= 3:
            slope, intercept = np.polyfit(range(len(batch)), batch.values, 1)
        else:
            slope, intercept = 0.0, float(batch.mean() if len(batch) else 0)

        # Projection 12 mois V2
        from datetime import timedelta as _td
        proj_rows = []
        for _, s in sig.iterrows():
            if pd.isna(s["freq"]): continue
            nxt = s["derniere"]
            while nxt < ref_d + _td(days=365):
                nxt = nxt + _td(days=int(s["freq"]))
                if ref_d < nxt <= ref_d + _td(days=365):
                    proj_rows.append({"date": nxt, "montant": s["MontantArr"], "source": "signature"})
        i_last = len(batch) - 1 if len(batch) else 0
        for m in range(1, 13):
            d = (ref_d.replace(day=1) + pd.DateOffset(months=m)).replace(day=15)
            proj_rows.append({"date": d, "montant": max(0, slope * (i_last + m) + intercept),
                              "source": "batch"})

        proj_real = pd.DataFrame(proj_rows)
        proj_real["mois"] = proj_real["date"].dt.to_period("M")
        proj_mens = proj_real.groupby(["mois", "source"])["montant"].sum().unstack(fill_value=0)
        proj_mens["total"] = proj_mens.sum(axis=1)
        total_v2 = proj_mens["total"].sum()

        st.markdown(f"**{len(sig)} signatures actives** détectées + "
                    f"batch mensuel moyen **{batch.mean():,.0f} $/mois** "
                    f"(tendance {slope:+,.0f} $/mois)")

        # Comparaison avec projection portefeuille synthétique
        proj_synth_12 = ech[ech["mois"] < pd.Timestamp(ref_date) + pd.DateOffset(months=12)]["total"].sum() if not ech.empty else 0
        c4, c5, c6 = st.columns(3)
        c4.metric("Projection V2 réelle (12m)", f"{total_v2:,.0f} $")
        c5.metric("Projection synthétique (12m)", f"{proj_synth_12:,.0f} $")
        ecart = (proj_synth_12 / total_v2 - 1) * 100 if total_v2 else 0
        c6.metric("Calibration", f"{ecart:+.1f} %",
                  help="Écart de la projection portefeuille vs réalité observée. "
                       "Proche de 0 = portefeuille bien calibré.")

        # Graphique projection V2
        proj_disp = proj_mens.reset_index()
        proj_disp["mois"] = proj_disp["mois"].astype(str)
        fig_v2 = go.Figure()
        if "signature" in proj_disp.columns:
            fig_v2.add_trace(go.Bar(x=proj_disp["mois"], y=proj_disp["signature"],
                                     name="Signatures récurrentes", marker_color=OK))
        if "batch" in proj_disp.columns:
            fig_v2.add_trace(go.Bar(x=proj_disp["mois"], y=proj_disp["batch"],
                                     name="Batch mensuel (tendance)", marker_color=PRIMARY))
        fig_v2.update_layout(barmode="stack", height=320,
                              yaxis_title="Perception ($)",
                              margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_v2, width='stretch')

        if len(batch) >= 6:
            recent_batch = batch.iloc[-3:].mean()
            ancien_batch = batch.iloc[:-3].mean()
            if recent_batch < ancien_batch * 0.9:
                st.warning(f"⚠️ Changement de régime détecté sur le batch — "
                           f"moyenne 3 derniers mois ({recent_batch:,.0f}$) "
                           f"vs historique ({ancien_batch:,.0f}$) "
                           f"= **{(recent_batch/ancien_batch-1)*100:+.1f}%**")

    except Exception as e:
        st.error(f"Impossible de parser le CSV : {e}")
        st.caption("Format attendu : colonnes `Date` et `Montant`, séparateur tab ou virgule.")
