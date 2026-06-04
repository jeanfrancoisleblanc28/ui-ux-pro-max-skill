# Simulateur de portefeuille FLI / FLS / PAUPME

MVP d'un tableau de bord de pilotage pour un portefeuille de prêts d'investissement
(FLI = Fonds local d'investissement, FLS = Fonds local de solidarité,
PAUPME = Programme d'aide d'urgence aux PME).

## Ce qu'il fait

- **KPI portefeuille** : capital déployé, capital restant dû (CRD), nb prêts actifs, défauts, top exposition
- **Projection 6-60 mois** des perceptions (capital + intérêts) par fonds
- **Mix par fonds** et **concentration sectorielle**
- **Stress test** : appliquer un taux de défaut additionnel pour évaluer l'impact
- **Top 10 expositions** par CRD

## Lancer

```bash
pip install streamlit pandas plotly
# 1. Générer un jeu de données factices (60 prêts)
python3 examples/portfolio_simulator/generate_fake_data.py
# 2. Lancer le tableau de bord
streamlit run examples/portfolio_simulator/portfolio_simulator.py
```

## Brancher tes vraies données

Remplace `data/prets.csv` par tes vraies données avec les mêmes en-têtes :

| Champ | Type | Description |
|---|---|---|
| `id_pret` | texte | Identifiant unique (ex. `P-2023-014`) |
| `fonds` | `FLI` \| `FLS` \| `PAUPME` | Source de financement |
| `entreprise` | texte | Bénéficiaire |
| `secteur` | texte | Secteur d'activité |
| `date_decaissement` | `YYYY-MM-DD` | Date de mise en vigueur |
| `capital_initial` | nombre | Montant prêté ($) |
| `taux_interet` | nombre | Taux annuel (%) |
| `duree_mois` | entier | Durée d'amortissement totale |
| `mois_moratoire` | entier | Période sans capital (0 si aucun) |
| `frequence` | texte | `Mensuelle` (seul supporté pour l'instant) |
| `jour_prelevement` | entier | Jour du mois (1-28) |
| `statut` | `Actif` \| `Remboursé` \| `Radié` \| `En défaut` | État courant |

## Limitations du MVP

- **Pas de capitalisation des intérêts** pendant le moratoire (à raffiner si pertinent)
- **Stress défaut linéaire** : applique un facteur de réduction uniforme sur toutes les
  perceptions futures. Une modélisation par cohorte/secteur serait plus précise.
- **Pas de vieillissement réel** (30/60/90j+) — basé sur le statut déclaré seulement.
  Pour l'ajouter, il faut brancher le fichier historique des PPA et comparer
  perceptions attendues vs réelles.
- **Fréquence hebdo non supportée** (à ajouter si nécessaire).

## Prochaines étapes possibles

- Ajout d'un onglet "Validation modèle" qui compare projection vs historique réel
- Calcul de provisions selon la grille interne par fonds
- Projection du "capital disponible pour redéploiement" intégrant les remboursements
- Export PDF/Excel pour rapports CA
