# Spec — Reporting financier par fonds (FLI / FLS / PAUPME)

> Cahier des charges du Outil de reporting financier consommant les exports
> d'Acomba (3 dossiers) pour produire états consolidés, PDF CA, dashboard
> direction et templates bailleurs.
>
> **Statut :** Brouillon — à valider avant développement
> **Auteur :** session de travail collaborative
> **Version :** 0.1

---

## 1. Contexte & objectifs

L'organisme gère **trois fonds d'investissement distincts**, comptabilisés dans
**trois dossiers Acomba séparés** :

| Fonds | Bailleur principal | Reddition de comptes |
|---|---|---|
| **FLI** — Fonds local d'investissement | MEI / municipalité | Rapport annuel CLD |
| **FLS** — Fonds local de solidarité | Fonds locaux de solidarité FTQ | Reddition annuelle FTQ |
| **PAUPME** — Programme d'aide d'urgence aux PME | MEI (programme COVID) | Reddition selon cadre PAUPME |

### Douleur actuelle
Produire les états financiers **consolidés et comparatifs** demande une
ventilation Excel manuelle à chaque période — exposée aux erreurs et coûteuse
en temps de la contrôleuse / direction.

### Objectifs SMART
1. **Réduire de >80%** le temps de production du rapport mensuel/trimestriel
   au CA (de ~1 jour à <2h)
2. **Éliminer** les retraitements Excel manuels après les exports Acomba
3. **Uniformiser** la présentation des 3 fonds dans un format unique
4. Produire les **templates bailleurs** (FTQ, MEI) sans ressaisie

---

## 2. Architecture

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Acomba FLI  │  │ Acomba FLS  │  │ Acomba PAUP │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │export csv      │export csv      │export csv
       └────────────────┼────────────────┘
                        ▼
       ┌──────────────────────────────────┐
       │  account_mapping.csv             │ ← config :
       │  (numéros source → normalisés)   │   plan harmonisé
       └────────────────┬─────────────────┘
                        ▼
       ┌──────────────────────────────────┐
       │  CORE                            │
       │  • Loader (3 CSV → DataFrame)    │
       │  • Mapper (harmonisation)        │
       │  • Aggregator (bilan, résultats) │
       │  • Comparator (vs N-1, budget)   │
       └────────────────┬─────────────────┘
                        ▼
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌─────────┐   ┌──────────────┐   ┌──────────────┐
   │ PDF CA  │   │ Dashboard    │   │ Templates    │
   │ (Wkhtml)│   │ Streamlit    │   │ bailleurs    │
   └─────────┘   └──────────────┘   └──────────────┘
```

### Stack technique proposée
- **Python 3.11+**, `pandas`, `pydantic` (validation des entrées)
- **Streamlit** + `plotly` pour le dashboard (cohérent avec PR #2 et #3)
- **WeasyPrint** ou **ReportLab** pour les PDF (WeasyPrint = HTML→PDF, plus simple)
- **openpyxl** pour les templates Excel bailleurs

---

## 3. Entrées (formats attendus)

### 3.1 Exports Acomba — un par fonds

**Fichier `balance_<fonds>_<YYYYMM>.csv`** (un par dossier, par période)

Acomba peut exporter la balance des comptes en CSV. Format minimal attendu :

```csv
no_compte;description;debit;credit;solde
1000;Encaisse - Compte courant;125450,32;0;125450,32
1100;Comptes à recevoir;0;0;0
1200;Placements - Prêts FLI capital;0;0;2847500,00
1210;Provision pour pertes - FLI;0;320000,00;-320000,00
4100;Intérêts gagnés sur prêts;0;187432,15;-187432,15
6100;Frais d'administration;25000,00;0;25000,00
...
```

| Champ | Type | Description |
|---|---|---|
| `no_compte` | texte | Numéro de compte tel qu'au plan comptable du dossier |
| `description` | texte | Libellé du compte |
| `debit` | nombre | Cumul débits de la période (ou de l'exercice — à confirmer) |
| `credit` | nombre | Cumul crédits |
| `solde` | nombre | Solde de fin de période (signé selon nature) |

**À valider :**
- ☐ Format exact de l'export Acomba (séparateur, décimale, encodage UTF-8/Latin-1)
- ☐ Cumul depuis début d'exercice ou seulement la période ?
- ☐ Gérer les comptes auxiliaires (clients, fournisseurs) — agrégat ou détail ?

### 3.2 Fichier de mapping `account_mapping.csv`

Vu que les plans comptables sont **similaires mais avec variations**, on harmonise
via une table de correspondance.

```csv
fonds;no_compte_source;no_compte_norm;categorie;sous_categorie
FLI;1000;1000;ACTIF;Encaisse
FLI;1200;1200;ACTIF;Prêts (capital)
FLS;1000;1000;ACTIF;Encaisse
FLS;1250;1200;ACTIF;Prêts (capital)
FLS;1255;1210;ACTIF;Prêts (provision)
PAUPME;1000;1000;ACTIF;Encaisse
PAUPME;1300;1200;ACTIF;Prêts (capital)
...
```

| Champ | Description |
|---|---|
| `fonds` | FLI / FLS / PAUPME |
| `no_compte_source` | Numéro tel qu'utilisé dans le dossier Acomba du fonds |
| `no_compte_norm` | Numéro de compte cible dans le plan normalisé |
| `categorie` | `ACTIF` / `PASSIF` / `AVOIR` / `REVENU` / `DEPENSE` |
| `sous_categorie` | Regroupement pour l'état (ex. `Encaisse`, `Prêts (capital)`) |

### 3.3 Données contextuelles (optionnelles, pour enrichir)

- `budget_<fonds>_<exercice>.csv` — budget par compte normalisé pour comparatif
- `prets.csv` (réutilise PR #3) — pour rapprochement portefeuille ↔ comptable

---

## 4. Calculs & règles d'agrégation

### 4.1 Bilan par fonds + consolidé
- Somme par catégorie/sous-catégorie après mapping
- **Pas d'élimination inter-fonds** dans un premier temps (les 3 fonds sont
  juridiquement séparés, pas de transactions intra-groupe attendues — **à valider**)

### 4.2 État des résultats par fonds + consolidé
- Idem, par sous-catégorie de revenus / dépenses
- Présentation comparative N vs N-1 vs Budget

### 4.3 Ratios par fonds
- **Rendement** : Intérêts gagnés / Capital moyen prêté
- **Provision pour pertes / Capital outstanding** (%)
- **Frais d'administration / Revenus** (%)
- **Capital disponible** : Encaisse + placements liquides / Capital total

### 4.4 Comparatifs inter-fonds
- Tableau côte-à-côte des 3 fonds + colonne consolidée
- Indicateurs relatifs (taille du fonds, performance)

---

## 5. Livrables détaillés

### 5.1 PDF formaté pour le CA

**Structure cible (5-8 pages) :**
1. Page couverture : nom organisme, période, date production
2. Résumé exécutif (1 page) : KPIs principaux par fonds + consolidé
3. Bilan consolidé + détail par fonds (tableau côte-à-côte)
4. État des résultats consolidé + détail par fonds
5. Tableau de bord ratios (1 page)
6. Notes / commentaires de la direction (zone libre)

**Mise en page :** A4 portrait, en-tête organisme, pagination, signatures.

**Décisions à prendre :**
- ☐ Logo & en-tête : tu fournis ou on utilise un placeholder ?
- ☐ Politique de couleur : la palette indigo/cyan utilisée dans PR #2 et #3 ou différente ?

### 5.2 Dashboard Streamlit

**Pages :**
- **Vue d'ensemble** : KPIs des 3 fonds + tendances
- **Bilan** : tableau interactif avec filtre période + fonds
- **Résultats** : idem + comparatif vs budget
- **Ratios** : visualisation des ratios sur 12 mois roulants
- **Détail compte** : drill-down sur un compte normalisé spécifique

**Filtres globaux :** période, fonds (multi), comparaison (N-1, Budget, aucune)

### 5.3 Templates bailleurs

**FLS — FTQ** (à valider format exact requis)
- Rapport annuel des activités d'investissement
- Détail des prêts décaissés / remboursés / radiés
- États financiers du fonds dans gabarit FTQ

**FLI — MEI / municipalité**
- Reddition annuelle de la CLD
- Stats d'investissement par secteur, par région

**PAUPME — MEI**
- Reddition selon cadre PAUPME (probablement échéance unique fin programme)

**⚠️ Action requise :** récupérer les **templates exigés** par chaque bailleur
(souvent disponibles sur leur portail ou dans la convention de gestion) pour qu'on
puisse les remplir programmatiquement plutôt que reproduire de mémoire.

---

## 6. Plan d'implémentation par phases

### Phase 1 — Foundation (~3-5 jours)
- [ ] Structure de projet `examples/fund_financial_reporter/`
- [ ] Générateur de données factices (3 balances + mapping) pour MVP
- [ ] Loader + Mapper + agrégateur de base
- [ ] Tests unitaires sur les calculs (mensualités déjà couvertes côté PR #3)

### Phase 2 — Dashboard Streamlit (~3-5 jours)
- [ ] Page Vue d'ensemble + KPIs
- [ ] Page Bilan
- [ ] Page Résultats
- [ ] Page Ratios + Page Drill-down

### Phase 3 — PDF CA (~3-4 jours)
- [ ] Template HTML pour WeasyPrint
- [ ] Génération automatique avec données réelles
- [ ] Validation visuelle (le CA reconnaît son rapport actuel)

### Phase 4 — Templates bailleurs (~variable, dépend des formats récupérés)
- [ ] FTQ
- [ ] MEI / CLD
- [ ] PAUPME

### Phase 5 — Mise en production (~1-2 jours)
- [ ] Procédure d'export mensuel depuis Acomba (3 fichiers)
- [ ] Documentation utilisateur (contrôleuse / DG)
- [ ] Formation rapide (~1h)

---

## 7. Données factices pour MVP

Le générateur produira :
- **3 fichiers `balance_*.csv`** simulant 24 mois d'historique pour chaque fonds
- Plan comptable proche du réel d'un CLD (encaisse, prêts, provisions, intérêts,
  frais d'administration, contributions)
- **`account_mapping.csv`** avec quelques variations entre fonds pour démontrer
  le mécanisme de mapping

---

## 8. Hors scope du MVP

- Saisie / écriture vers Acomba (Option A — voir conversation)
- Rapprochement bancaire automatique (chantier séparé)
- Conformité fiscale / production de T4A intérêts aux emprunteurs
- Authentification / multi-utilisateur (utilisation locale par la contrôleuse)
- Cloud / SaaS (livré comme outil local)

---

## 9. Risques & questions ouvertes

| # | Risque / Question | Mitigation |
|---|---|---|
| 1 | Format d'export Acomba pas standard entre éditions | Loader avec adapter par version (Acomba X vs Linko) |
| 2 | Templates bailleurs non documentés publiquement | Récupérer auprès des contacts FTQ / MEI |
| 3 | Plan comptable change dans le temps | Mapping versionné avec dates effectives |
| 4 | Volumétrie écritures trop grande pour CSV | Utiliser balance pas grand livre pour les états |
| 5 | Présentation officielle vs interne diffère | Profils de présentation paramétrables |

---

## 10. Décisions à figer avant Phase 1

- [ ] **Logo / en-tête organisme** — fourniture par le client
- [ ] **Palette graphique** : reprend PR #2/#3 ou personnalisée ?
- [ ] **Templates bailleurs** — accès aux formats officiels ?
- [ ] **Plan comptable normalisé** : on part du FLI ou on définit un plan greenfield ?
- [ ] **Export Acomba** — fréquence (mensuelle / trimestrielle), responsable
- [ ] **Données réelles anonymisées** disponibles pour calibrage ?
