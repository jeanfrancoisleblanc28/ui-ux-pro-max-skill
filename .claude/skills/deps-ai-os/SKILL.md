---
name: deps-ai-os
description: "Système d'exploitation de travail du DÉPS (Développement Économique Pierre-De Saurel) : oriente une demande vers le bon parcours d'analyse et impose la chaîne de contrôle avant remise. Couvre 22 modules en 6 domaines — financement (analyse financière, montage, capacité de remboursement, analyse de risque), FLI/FLS (admissibilité, tarification, conformité à la politique, préparation CIC), évaluation d'entreprise (normalisation du BAIIA, multiples, actualisation des flux, rapport), développement économique (programmes et subventions, analyse sectorielle, intelligence territoriale), production (design ui-ux-pro-max, rapport exécutif, présentation au CA) et assurance qualité (contrôle des calculs, nomenclature, validation des sources, préflight final). Déclencher pour : dossier de financement, demande de prêt, note CIC, comité d'investissement, admissibilité, tarification, ratio de couverture du service de la dette, montage financier, évaluation d'entreprise, combien vaut cette entreprise, BAIIA normalisé, subvention, cumul des aides, veille territoriale, retombées économiques, rapport au conseil d'administration, contrôle qualité d'un livrable, contre-analyse, préflight avant envoi."
---

# DÉPS AI Operating System

Système d'exploitation de travail pour les dossiers de financement, d'évaluation et de développement économique. Il ne remplace pas le jugement professionnel : il impose un ordre d'exécution, rend chaque chiffre traçable et bloque la sortie d'un livrable qui n'a pas passé ses contrôles.

## Quand l'utiliser

Utilisez ce système dès qu'une demande porte sur un dossier de financement, une évaluation d'entreprise, un montage avec des aides publiques, une analyse territoriale, ou la vérification d'un livrable avant remise.

Ne l'utilisez pas pour une question factuelle isolée — un taux, une définition, une date. Répondez directement.

## Premier réflexe : router la demande

N'improvisez jamais la séquence de travail. Lancez :

```bash
python3 .claude/skills/deps-ai-os/scripts/deps.py route "<la demande, dans les mots de l'utilisateur>"
```

La commande retourne le parcours ou le module recommandé, la séquence complète d'exécution, et surtout la liste des paramètres de politique non validés que cette séquence va mobiliser. Exécutez ensuite les modules dans l'ordre donné, sans en sauter.

## L'organigramme

```
DÉPS AI OPERATING SYSTEM
│
├── 01 — FINANCEMENT
│   ├── F1  analyse-financiere
│   ├── F2  montage-financier
│   ├── F3  capacite-remboursement
│   └── F4  analyse-risque
│
├── 02 — FLI / FLS
│   ├── P1  admissibilite
│   ├── P2  tarification
│   ├── P3  conformite-politique
│   └── P4  preparation-CIC
│
├── 03 — ÉVALUATION
│   ├── E1  normalisation-BAIIA
│   ├── E2  multiples
│   ├── E3  DCF
│   └── E4  rapport-evaluation
│
├── 04 — DÉVELOPPEMENT ÉCONOMIQUE
│   ├── D1  programmes-subventions
│   ├── D2  analyse-sectorielle
│   └── D3  intelligence-territoriale
│
├── 05 — PRODUCTION
│   ├── R1  ui-ux-pro-max
│   ├── R2  rapport-executif
│   └── R3  presentation-CA
│
└── 06 — QA
    ├── Q1  controle-calculs
    ├── Q2  nomenclature
    ├── Q3  validation-sources
    └── Q4  preflight-final
```

## Les parcours pré-câblés

| Parcours | Pour | Séquence |
|---|---|---|
| `dossier-cic` | Dossier de financement complet jusqu'au comité | P1 → F1 → F3 → F4 → P3 → P2 → F2 → P4 → QA |
| `evaluation-entreprise` | Combien vaut l'entreprise | E1 → E2 → E3 → E4 → QA |
| `diagnostic-express` | Portrait rapide, triage, pré-analyse | F1 → F3 → D2 → R2 → QA |
| `veille-territoriale` | Lecture stratégique du territoire | D3 → D2 → D1 → R2 → QA |
| `presentation-decision` | Mettre en scène un livrable validé | R2 → R3 → R1 → QA |
| `recherche-financement` | Cartographier les sources et monter le financement | P1 → D1 → F2 → F3 → QA |
| `controle-qualite` | Vérifier un livrable déjà rédigé, même écrit à la main | Q1 → Q3 → Q2 → Q4 |
| `contre-analyse` | Second regard qui recalcule avant de commenter | Q1 → F4 → F3 → Q3 → Q4 |

## Règles non négociables

**L'admissibilité se tranche en premier.** Un dossier non admissible ne consomme jamais d'analyse financière. P1 précède F1 dans `dossier-cic`, et ce n'est pas un détail d'ordonnancement.

**La tarification suit la cotation du risque.** P2 vient après F4, jamais avant. Fixer le prix puis chercher les arguments qui le justifient est l'inverse du travail attendu.

**Aucun paramètre de politique ne se cite de mémoire.** Les plafonds, taux, ratios entre fonds, mises de fonds minimales et seuils de délégation vivent dans `data/parametres-politique.csv`. Tant qu'un paramètre porte le statut `A_VALIDER`, aucun chiffre qui en dépend ne peut être présenté comme définitif. Voir « Mise en service » ci-dessous.

**Aucun chiffre orphelin.** Tout chiffre présenté est rattaché à une pièce source datée, dont le niveau d'assurance est déclaré : audité, examen, avis au lecteur, interne, déclaré par le promoteur, estimé.

**Rien ne sort sans préflight.** Tous les parcours se referment sur Q4, qui rend un statut daté : PRÊT, PRÊT SOUS RÉSERVE ou BLOQUÉ. Un livrable sans statut n'est pas remis.

**La production ne réanalyse rien.** Si un chiffre nouveau apparaît au moment de mettre en forme, il repasse par Q1 et Q3.

## Mise en service

À la livraison, les 22 paramètres de politique portent la valeur `À_RENSEIGNER` et le statut `A_VALIDER`. C'est délibéré : le système ne prétend pas connaître la politique d'investissement de l'organisation, et un système qui inventerait ces valeurs serait plus dangereux qu'utile.

Première étape avant tout usage réel :

```bash
python3 .claude/skills/deps-ai-os/scripts/deps.py params --statut A_VALIDER
```

Ouvrez la politique d'investissement en vigueur et remplissez, pour chaque paramètre, la valeur, la source précise et la date de validation, puis passez le statut à `VALIDE`. Le fichier à éditer est `src/deps-ai-os/data/parametres-politique.csv`.

Tant que ce travail n'est pas fait, le système reste utilisable : il signale simplement, à chaque routage et à chaque préflight, quels chiffres demeurent provisoires.

## Commandes

| Besoin | Commande |
|---|---|
| Orienter une demande | `deps.py route "<demande>"` |
| Fiche complète d'un module | `deps.py module F3` |
| Lister les parcours | `deps.py pipeline` |
| Détail d'un parcours | `deps.py pipeline dossier-cic` |
| Paramètres de politique | `deps.py params [--fonds FLI] [--statut A_VALIDER] [--module P3]` |
| Formules normalisées | `deps.py formule [<recherche>] [--module F3]` |
| Contrôles qualité | `deps.py qa [--module Q1] [--bloquants]` |
| Liste à cocher avant remise | `deps.py preflight --type NOTE-CIC` |
| Conventions de nommage | `deps.py nomenclature [--type NOTE-CIC]` |
| Intégrité du référentiel | `deps.py doctor` |

Toutes les commandes acceptent `--json` pour un traitement programmatique.

## Doctrine détaillée

Chaque domaine a son document de référence, à lire avant d'exécuter ses modules pour la première fois :

- `references/01-financement.md`
- `references/02-fli-fls.md`
- `references/03-evaluation.md`
- `references/04-developpement-economique.md`
- `references/05-production.md`
- `references/06-qa.md`

## Bases de connaissances

| Fichier | Contenu |
|---|---|
| `data/modules.csv` | Les 22 modules : objectif, entrées, méthode en étapes, sorties, dépendances, portes QA, pièges |
| `data/pipelines.csv` | Les 8 parcours pré-câblés et leur point de contrôle humain |
| `data/formules.csv` | 24 formules normalisées avec termes, interprétation, seuils indicatifs et pièges |
| `data/parametres-politique.csv` | Les 22 paramètres de politique et leur statut de validation |
| `data/controles-qa.csv` | Les 28 contrôles qualité, dont 19 bloquants |
| `data/nomenclature.csv` | Conventions de nommage et de versionnage des livrables |

## Articulation avec ui-ux-pro-max

Le module R1 est le pont vers le moteur de design de ce dépôt. Quand un livrable doit devenir un artefact visuel — tableau de bord, calculateur, présentation, rapport mis en page —, R1 interroge `src/ui-ux-pro-max/scripts/search.py` pour obtenir le système de design, puis applique par-dessus l'identité visuelle institutionnelle en vigueur. Le détail est dans `references/05-production.md`.

## Ce que le système ne fait pas

Il ne juge pas si une recommandation est bonne : un dossier peut passer les 28 contrôles et recommander un mauvais prêt. Pour challenger le fond, utilisez le parcours `contre-analyse`, qui recalcule avant de commenter.

Il ne connaît pas la politique d'investissement de l'organisation tant que `parametres-politique.csv` n'a pas été rempli.

Il ne remplace pas la lecture des pièces au dossier.
