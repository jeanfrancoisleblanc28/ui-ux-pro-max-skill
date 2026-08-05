# 06 — Gouvernance

## Rôles et responsabilités

| Rôle | Responsabilité | Titulaire (v1) |
|---|---|---|
| **Propriétaire du produit** | Vision, arbitrages, feuille de route, versionnage, publication | Porteur du projet |
| **Répondante clinique (soins infirmiers)** | Validation du déroulement d'entrevue, des formulations, de l'adéquation terrain ; premier retour d'expérience | Infirmière utilisatrice pilote |
| **Répondant pharmacie** | Revue des fiches du radar (`radar-securite.md`) : justesse, exemples, pièges ; revue des règles d'écriture sécuritaires | À recruter (pharmacien communautaire ou d'établissement) |
| **Responsable confidentialité** | Application de `07-confidentialite.md`, choix et paramétrage des plateformes | Porteur du projet (v1) |
| **Utilisatrices et utilisateurs** | Usage conforme, validation des rapports, signalement des incidents | Chaque professionnel |

Une même personne peut cumuler des rôles en v1 ; les rôles, eux, ne disparaissent pas.

## Cycle de vie du prompt et des connaissances

1. **Proposition** de modification (nouvelle formulation, fiche radar enrichie, règle ajustée) — consignée par écrit avec sa motivation ;
2. **Revue clinique** : répondante soins infirmiers pour l'entrevue, répondant pharmacie pour le radar et les règles d'écriture ;
3. **Banc d'essai** : rejouer les six cas d'utilisation (`04-cas-utilisation.md`) sur la version candidate — le CU-01 au complet, les autres en abrégé ; vérifier qu'aucun comportement attendu ne régresse (questions redondantes, rappels non pertinents, format du rapport, indice) ;
4. **Publication** : mise à jour simultanée du prompt et des connaissances sur les plateformes de déploiement ;
5. **Journal** : entrée datée au journal des versions (dépôt git — chaque changement est un commit relu).

**Versionnage sémantique :** MAJEUR (changement de comportement ou de cadre), MINEUR (nouvelle capacité ou fiche), CORRECTIF (formulation, coquille). La version figure dans le README.

## Gestion des incidents

**Est un incident :** une information inventée ou déformée par l'assistant ; une recommandation clinique (même implicite) ; un rappel radar non pertinent répétitif ; une question redondante systématique ; la répétition d'un renseignement identificatoire ; un rapport non conforme au gabarit.

| Étape | Détail |
|---|---|
| Signalement | Canal simple et unique (courriel ou formulaire) ; capture de l'échange anonymisée |
| Tri | Gravité A (contenu clinique erroné ou fuite) — correction avant toute nouvelle utilisation ; gravité B (comportement hors cadre) — correction à la prochaine version ; gravité C (irritant) — backlog |
| Correction | Modification du prompt ou des connaissances via le cycle de vie ci-dessus |
| Registre | Chaque incident, sa gravité, sa correction et sa date sont consignés |

## Formation des utilisatrices

Avant la première utilisation : une capsule de 15 minutes couvrant — ce que l'outil fait et ne fait pas ; la règle « zéro identifiant » avec démonstration ; la validation obligatoire du rapport ; le canal de signalement. Le mode intégration de l'outil complète la formation, il ne la remplace pas.

## Évaluation continue

- Mesure de départ puis suivi des indicateurs de `01-vision.md` (temps, omissions détectées, conformité au gabarit, confiance des nouvelles infirmières, charge perçue) ;
- Sondage court auprès des utilisatrices à fréquence fixe pendant le pilote ;
- Revue trimestrielle : incidents, indicateurs, backlog, décision d'évolution.

## Déploiement par étapes

| Étape | Portée | Condition de passage |
|---|---|---|
| 1. Usage individuel encadré | Une utilisatrice (l'infirmière du projet), cas réels, validation systématique | Banc d'essai v1 réussi + formation faite |
| 2. Pilote restreint | 2 ou 3 collègues volontaires, même encadrement | Étape 1 stable, incidents A = 0 sur la période |
| 3. Présentation à une organisation (CIUSSS) | Dossier complet : ce dépôt + résultats du pilote | Indicateurs mesurés, gouvernance rodée, avis de conformité locale (`07-confidentialite.md`) |

À l'étape 3, la gouvernance décrite ici a vocation à être **transférée** à l'organisation (direction des soins infirmiers, pharmacie, DPO/RPRP, direction des ressources informationnelles) — ce document sert alors de proposition de départ, pas de structure définitive.
