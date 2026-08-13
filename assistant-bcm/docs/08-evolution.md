# 08 — Possibilités d'évolution

## Feuille de route

### v1.x — Raffinements terrain (horizon : pendant le pilote)

Nourris par l'usage réel et le canal d'incidents :

- formulations d'entrevue affinées selon les retours de la ou des utilisatrices ;
- fiches radar enrichies et revues par le répondant pharmacie ;
- déclinaisons sectorielles supplémentaires du guide d'entrevue (périopératoire approfondi, pédiatrie, santé mentale, congé — le BCM de départ avec conciliation des changements) ;
- amorces de conversation additionnelles (préparation d'un appel à la pharmacie communautaire, liste de questions à poser au prescripteur pour les divergences).

**Condition :** aucune — c'est le cycle de vie normal (`06-gouvernance.md`).

### v2 — Application dédiée (horizon : après un pilote concluant)

Un produit logiciel mince autour du même cœur :

- interface hybride : conversation + panneau structuré du MSTP en construction (les deux toujours synchronisés) ;
- export PDF du rapport, mise en page dossier ;
- **lecture d'étiquettes et de listes par photo**, avec anonymisation locale avant tout traitement (le nom ne quitte jamais l'appareil) ;
- **dictée vocale mains libres** pour l'entrevue au chevet ;
- indice de complétude calculé par code (déterministe à 100 %) plutôt qu'estimé par le modèle ;
- gabarits paramétrables par établissement (le gabarit v1 devient un profil par défaut).

**Conditions :** financement du développement ; revue de la posture réglementaire (l'OCR et la dictée restent documentaires — toute dérive vers l'analyse clinique déclencherait l'évaluation LIM/SaMD, voir `05-limites-ia.md`) ; ÉFVP si des photos ou de la voix entrent en jeu.

### v3 — Intégration institutionnelle (horizon : avec une organisation partenaire)

- authentification organisationnelle et journalisation des accès ;
- intégration en lecture aux sources officielles (DSQ, DME) pour pré-remplir la validation croisée — l'entrevue demeure le cœur ;
- versement **assisté** (jamais automatique) du rapport validé au dossier ;
- tableau de bord qualité anonymisé : complétude moyenne, catégories les plus souvent manquantes, divergences les plus fréquentes — de l'amélioration continue pour l'organisation, pas de la surveillance individuelle ;
- gouvernance transférée à l'organisation (`06-gouvernance.md`, étape 3).

**Conditions :** entente organisationnelle, ÉFVP complète, architecture d'hébergement conforme, comité incluant soins infirmiers, pharmacie, RPRP et ressources informationnelles.

## Pistes évaluées et volontairement non retenues

| Piste | Décision | Motif |
|---|---|---|
| Détection d'interactions médicamenteuses par l'assistant | **Non** | Hors du cadre « aide documentaire » ; fiabilité insuffisante d'un modèle de langage seul ; ferait basculer le produit en instrument médical. Le rôle reste : consigner et orienter vers le pharmacien. |
| Conservation d'un historique de BCM dans l'outil | **Non** | Le dossier de l'usager est l'unique lieu de conservation ; tout historique parallèle serait un passif de confidentialité. |
| Appel automatisé à la pharmacie par un agent | **Pas en v1-v2** | Intérêt réel, mais prématuré : enjeux d'identité, de consentement et de responsabilité non résolus. |
| Score de « qualité de l'infirmière » | **Non, jamais** | L'indice mesure la documentation d'un BCM, pas les personnes. Toute dérive vers l'évaluation individuelle détruirait l'adoption et la confiance. |

## Vision à long terme

Le pari méthodologique du projet dépasse le BCM : **un cadre reproductible** — entrevue naturelle + mémoire contextuelle + radar spécialisé + indice de complétude explicable + gabarit unique + gouvernance — applicable à d'autres collectes structurées en soins : évaluation initiale, suivi de plaies, histoire de chute, préparation au congé. Si le Copilote BCM fait ses preuves, il devient le premier d'une famille d'assistants documentaires cliniques francophones, et ce dépôt en est le modèle de référence : chaque assistant naît avec sa vision, ses règles métier, ses limites, sa gouvernance et sa confidentialité — pas seulement avec un prompt.
