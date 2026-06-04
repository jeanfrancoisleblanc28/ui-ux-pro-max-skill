import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Simulateur Stratégique CPA & BFR", layout="wide")

# Couleurs corporatives (Palette Executive)
PRIMARY = "#24135D"   # Indigo
SECONDARY = "#0057B8" # Bleu
ACCENT = "#00AEC7"    # Cyan
ALERT = "#E26D5C"     # Corail pour les alertes de liquidité

st.markdown(f"""
    <style>
    .main-title {{ color: {PRIMARY}; font-size: 28px; font-weight: bold; margin-bottom: 20px; }}
    .section-title {{ color: {SECONDARY}; font-size: 20px; font-weight: bold; margin-top: 15px; }}
    .kpi-card {{ background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid {ACCENT}; }}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Simulateur de Pilotage Financier & Optimisation du BFR</div>', unsafe_allow_html=True)
st.caption("Outil de discussion stratégique CPA : Analyse de l'impact combiné de la rentabilité et du cycle d'exploitation sur les liquidités.")

# 2. DONNÉES DE BASE (SITUATION ACTUELLE - PME)
@st.cache_data
def load_base_data():
    return {
        "rev_base": 2500000, "vol_base": 50000, "prix_base": 50.0,
        "cmv_pct": 0.45, "salaires_base": 600000, "loyer_base": 80000,
        "frais_fixes_base": 300000, "frais_var_pct": 0.05,
        # Variables de fonds de roulement actuelles
        "dso_base": 45,  # Délai clients (jours)
        "dio_base": 60,  # Rotation stocks (jours)
        "dpo_base": 30,  # Délai fournisseurs (jours)
        "dette_existante": 450000, "service_dette_actuel": 75000
    }

base = load_base_data()

# 3. SIDEBAR : LEVIERS ET SCÉNARIOS
with st.sidebar:
    st.markdown(f"<h2 style='color:{PRIMARY};'>Configuration</h2>", unsafe_allow_html=True)

    scen_type = st.selectbox("Scénario Prédéfini", ["Actuel", "Optimisation Cash", "Crise de Croissance", "Personnalisé"])

    # Configuration des scénarios types
    if scen_type == "Actuel":
        c_p, c_v, c_mb, c_f = 0.0, 0.0, 0.0, 0.0
        c_dso, c_dio, c_dpo = base["dso_base"], base["dio_base"], base["dpo_base"]
    elif scen_type == "Optimisation Cash":
        c_p, c_v, c_mb, c_f = 2.0, 0.0, 1.0, -2.0
        c_dso, c_dio, c_dpo = 35, 45, 45  # On accélère les encaissements et ralentit les décaissements
    elif scen_type == "Crise de Croissance":
        c_p, c_v, c_mb, c_f = -5.0, 25.0, -2.0, 10.0  # Forte hausse volume, baisse prix, hausse frais
        c_dso, c_dio, c_dpo = 55, 75, 25  # Détérioration forte des cycles opérationnels
    else:
        c_p, c_v, c_mb, c_f = 0.0, 0.0, 0.0, 0.0
        c_dso, c_dio, c_dpo = base["dso_base"], base["dio_base"], base["dpo_base"]

    st.markdown("**📊 Leviers Commerciaux & Prix**")
    p_var = st.slider("Variation Prix (%)", -15.0, 15.0, c_p, step=0.5)
    v_var = st.slider("Variation Volume (%)", -20.0, 30.0, c_v, step=1.0)

    st.markdown("**⚙️ Leviers Opérationnels**")
    mb_var = st.slider("Optimisation Marge Brute (%)", -5.0, 10.0, c_mb, step=0.5)
    ff_var = st.slider("Variation Frais Fixes (%)", -15.0, 15.0, c_f, step=1.0)

    st.markdown("**⏳ Gestion du Cycle de Caisse (Jours)**")
    dso = st.slider("Délai Clients (DSO)", 10, 90, int(c_dso), step=1)
    dio = st.slider("Rotation des Stocks (DIO)", 10, 120, int(c_dio), step=1)
    dpo = st.slider("Délai Fournisseurs (DPO)", 10, 90, int(c_dpo), step=1)

    st.markdown("**🏦 Structure de Financement**")
    nouveau_pret = st.number_input("Nouveau Prêt ($)", min_value=0, value=0, step=25000)
    taux_int = st.slider("Taux d'intérêt (%)", 4.0, 12.0, 7.5, step=0.25)
    amortissement = st.slider("Durée (années)", 1, 15, 5)

# 4. MOTEUR DE CALCUL FINANCIER ENRICHI (P&L + BFR)
def run_model(p_v, v_v, mb_v, ff_v, n_p, t_i, am, current_dso, current_dio, current_dpo):
    # Projections du compte de résultat
    prix_proj = base["prix_base"] * (1 + p_v / 100)
    vol_proj = base["vol_base"] * (1 + v_v / 100)
    rev_proj = prix_proj * vol_proj

    cmv_pct_ajuste = base["cmv_pct"] - (mb_v / 100)
    cmv_proj = rev_proj * cmv_pct_ajuste
    marge_brute = rev_proj - cmv_proj

    frais_fixes = (base["loyer_base"] + base["frais_fixes_base"] + base["salaires_base"]) * (1 + ff_v / 100)
    frais_var = rev_proj * base["frais_var_pct"]

    baiia = marge_brute - (frais_fixes + frais_var)

    # Dette
    if n_p > 0:
        r = (t_i / 100)
        nouvel_amort = n_p * (r / (1 - (1 + r)**(-am))) if r > 0 else n_p / am
    else:
        nouvel_amort = 0
    tot_service_dette = base["service_dette_actuel"] + nouvel_amort
    dscr = baiia / tot_service_dette if tot_service_dette > 0 else 0
    seuil_rentabilite = frais_fixes / (1 - cmv_pct_ajuste) if cmv_pct_ajuste < 1 else float("inf")

    # --- CALCULS COMPLÉMENTAIRES DU BFR ---
    # Comptes clients = (Revenus / 365) * DSO
    comptes_clients = (rev_proj / 365) * current_dso
    # Stocks = (Coût des ventes / 365) * DIO
    stocks = (cmv_proj / 365) * current_dio
    # Comptes fournisseurs = (Coût des ventes + Frais variables) / 365 * DPO
    comptes_fournisseurs = ((cmv_proj + frais_var) / 365) * current_dpo

    # BFR Opérationnel Total
    bfr_total = comptes_clients + stocks - comptes_fournisseurs
    cycle_conversion_cash = current_dso + current_dio - current_dpo

    # Estimation de l'impact net sur les liquidités de l'année (Modèle simplifié de Flux de Trésorerie)
    # Cash généré = BAIIA - Service de la dette - Variation du BFR
    return {
        "Revenus": rev_proj, "Marge Brute": marge_brute, "BAIIA": baiia,
        "DSCR": dscr, "SR": seuil_rentabilite, "Service Dette": tot_service_dette,
        "BFR": bfr_total, "CCC": cycle_conversion_cash, "Clients": comptes_clients,
        "Stocks": stocks, "Fournisseurs": comptes_fournisseurs
    }

# Calcul des deux scénarios
actuel = run_model(0, 0, 0, 0, 0, 7.5, 5, base["dso_base"], base["dio_base"], base["dpo_base"])
simule = run_model(p_var, v_var, mb_var, ff_var, nouveau_pret, taux_int, amortissement, dso, dio, dpo)

# 5. AFFICHAGE DES RÉSULTATS (KPI CARDS)
col1, col2, col3, col4 = st.columns(4)

with col1:
    var_rev = ((simule["Revenus"] - actuel["Revenus"]) / actuel["Revenus"]) * 100 if actuel["Revenus"] else 0
    st.markdown(f"""<div class='kpi-card'><b>Chiffre d'affaires</b><br>
    <span style='font-size:22px;font-weight:bold;'>{simule["Revenus"]:,.0f} $</span><br>
    <span style='color:{"green" if var_rev >= 0 else "red"};'>{var_rev:+.1f}% vs Actuel</span></div>""", unsafe_allow_html=True)

with col2:
    var_baiia = simule["BAIIA"] - actuel["BAIIA"]
    st.markdown(f"""<div class='kpi-card'><b>BAIIA (EBITDA)</b><br>
    <span style='font-size:22px;font-weight:bold;'>{simule["BAIIA"]:,.0f} $</span><br>
    <span style='color:{"green" if var_baiia >= 0 else "red"};'>{var_baiia:+,.0f} $</span></div>""", unsafe_allow_html=True)

with col3:
    var_bfr = simule["BFR"] - actuel["BFR"]
    # Une hausse du BFR détruit des liquidités (donc rouge si positif)
    color_bfr = "red" if var_bfr > 0 else "green"
    st.markdown(f"""<div class='kpi-card'><b>Besoin en Fonds de Roulement</b><br>
    <span style='font-size:22px;font-weight:bold;'>{simule["BFR"]:,.0f} $</span><br>
    <span style='color:{color_bfr};'>Variation: {var_bfr:+,.0f} $</span></div>""", unsafe_allow_html=True)

with col4:
    # Trésorerie d'exploitation théorique libérée ou immobilisée sur la période
    cash_flow_effet = (simule["BAIIA"] - simule["Service Dette"]) - (simule["BFR"] - actuel["BFR"])
    color_cash = "green" if cash_flow_effet >= 0 else "red"
    st.markdown(f"""<div class='kpi-card' style='border-left-color:{color_cash};'><b>Impact Net sur Liquidités</b><br>
    <span style='font-size:22px;font-weight:bold;color:{color_cash};'>{cash_flow_effet:,.0f} $</span><br>
    <span>BAIIA - Serv. Dette - ΔBFR</span></div>""", unsafe_allow_html=True)

# 6. GRAPHIQUES INTERACTIFS
st.markdown('---')
g1, g2 = st.columns(2)

with g1:
    st.markdown('<div class="section-title">Analyse Comparative du BFR Opérationnel ($)</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Situation Actuelle', x=['Comptes Clients', 'Stocks', 'Fournisseurs'], y=[actuel["Clients"], actuel["Stocks"], -actuel["Fournisseurs"]], marker_color=PRIMARY))
    fig.add_trace(go.Bar(name='Scénario Simulé', x=['Comptes Clients', 'Stocks', 'Fournisseurs'], y=[simule["Clients"], simule["Stocks"], -simule["Fournisseurs"]], marker_color=ACCENT))
    fig.update_layout(barmode='group', height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Les fournisseurs agissent comme financement (valeur négative).")

with g2:
    st.markdown('<div class="section-title">Cycle de Conversion de l\'Encaisse (Jours)</div>', unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name='Cycle (Jours)', x=['Actuel', 'Simulé'], y=[actuel["CCC"], simule["CCC"]], marker_color=[SECONDARY, ALERT if simule["CCC"] > actuel["CCC"] else "green"]))
    fig2.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig2, use_container_width=True)

# 7. SYNTHÈSE STRATÉGIQUE CPA
st.markdown('---')
st.markdown('<div class="section-title">Analyse Conseil & Stratégie de Trésorerie</div>', unsafe_allow_html=True)

c_left, c_right = st.columns(2)
with c_left:
    st.markdown("### 🔍 Diagnostic du Fonds de Roulement")
    st.write(f"Le **Cycle de Conversion de l'Encaisse (CCC)** passe de **{actuel['CCC']} jours** à **{simule['CCC']} jours**.")
    if simule["CCC"] > actuel["CCC"]:
        st.error(f"⚠️ **Alerte d'asphyxie financière** : Le cycle s'allonge de {simule['CCC'] - actuel['CCC']} jours. Même si l'entreprise est rentable sur papier, elle immobilise **{var_bfr:,.0f} $** additionnels dans ses opérations, ce qui dégrade directement son compte de banque.")
    elif simule["CCC"] < actuel["CCC"]:
        st.success(f"🎉 **Optimisation de l'encaisse** : La réduction du cycle libère **{abs(var_bfr):,.0f} $** en liquidités directes, augmentant l'autofinancement disponible sans recours à de la dette externe.")
    else:
        st.write("Le cycle d'exploitation est stable. Les variations de liquidité dépendent uniquement de la rentabilité opérationnelle (BAIIA).")

with c_right:
    st.markdown("### 💡 Recommandations du CPA (Plan d'Action)")
    points = []
    if dso > 40:
        points.append(f"**Comptes clients ({dso} jours)** : Mettre en place une politique d'affacturage, des incitatifs au paiement rapide (ex: 2/10 net 30) ou durcir le suivi des comptes en souffrance.")
    if dio > 50:
        points.append(f"**Gestion des stocks ({dio} jours)** : Réduire les volumes de commande, identifier les désuétudes ou adopter une approche de gestion juste-à-temps pour libérer les capitaux.")
    if dpo < 35:
        points.append(f"**Fournisseurs ({dpo} jours)** : Négocier des extensions de termes de paiement auprès des partenaires clés pour maximiser le crédit commercial gratuit.")

    if points:
        for p in points:
            st.info(p)
    else:
        st.success("Excellente maîtrise opérationnelle des composantes du fonds de roulement.")
