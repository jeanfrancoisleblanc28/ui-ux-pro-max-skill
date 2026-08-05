# 01 — Vision

## Résumé exécutif

Le **Copilote BCM** est un assistant conversationnel francophone qui accompagne les infirmières et infirmiers du Québec dans la réalisation du **bilan comparatif des médicaments (BCM)** : la collecte du meilleur schéma thérapeutique possible (MSTP) et sa documentation uniforme. Il transforme un processus exigeant, normé et sujet aux omissions en une conversation naturelle — l'infirmière raconte, l'assistant structure, repère ce qui manque et ne pose que les questions utiles.

L'ambition n'est pas de fabriquer « un bon GPT », mais **le meilleur assistant conversationnel francophone pour la réalisation d'un BCM** — conçu en croisant cinq regards : analyste de processus, pharmacien, infirmière clinicienne, architecte logiciel et spécialiste UX.

## Le problème

Le BCM est une pratique organisationnelle requise (Agrément Canada) et un maillon reconnu de la sécurité médicamenteuse : l'OMS, avec son initiative *Medication Without Harm*, identifie les transitions de soins comme un moment à haut risque d'erreurs médicamenteuses. Sur le terrain :

- le BCM est **chronophage** et entre en compétition avec le reste de la charge de travail ;
- le **risque d'omission** est structurel : gouttes, pompes, timbres, injections espacées, PRN, médicaments en vente libre (MVL) et produits de santé naturels (PSN) échappent au pilulier comme à la mémoire ;
- la **collecte varie d'une personne à l'autre**, et la documentation qui en résulte aussi ;
- les **nouvelles infirmières** doivent intérioriser une procédure dense tout en apprenant le reste ;
- la **charge cognitive** est élevée : mener l'entrevue, se rappeler la procédure, structurer et documenter, en même temps.

## La solution

Un copilote conversationnel spécialisé, disponible pendant l'entrevue ou immédiatement après, qui repose sur quatre capacités signatures :

1. **Intelligence contextuelle** — il retient l'âge, l'autonomie, la provenance, le secteur, le rôle du professionnel et les médicaments déjà documentés ; il ne pose jamais une question redondante.
2. **Entrevue naturelle** — l'infirmière n'a pas besoin de « parler informatique » : « Madame prend du Tylenol quand elle a mal au dos, du Jardiance le matin et son conjoint prépare le pilulier » suffit ; le copilote structure et ne demande que ce qui manque.
3. **Radar de sécurité documentaire** — il surveille silencieusement les classes à risque (anticoagulants, insulines, hebdomadaires, injections semestrielles, opioïdes, PRN, MVL, PSN) et ne rappelle que ce qui est réellement pertinent pour ce patient.
4. **Indice de complétude** — un pourcentage, mais surtout un **niveau de confiance documentaire** (Élevé / Modéré / À consolider) justifié en une phrase, qui pointe où une vérification supplémentaire serait utile. Il éclaire le jugement clinique ; il ne le remplace jamais.

## Objectifs mesurables

| # | Objectif | Indicateur proposé | Méthode de mesure (pilote) |
|---|---|---|---|
| 1 | Réduire le temps consacré au BCM | Durée moyenne d'un BCM complet | Auto-chronométrage avant / avec copilote |
| 2 | Réduire le risque d'omission | Éléments ajoutés lors de la contre-vérification (pharmacien ou pairs) | Revue d'un échantillon de BCM |
| 3 | Standardiser la collecte | % des BCM couvrant toutes les catégories applicables | Lecture des rapports produits |
| 4 | Faciliter l'intégration des nouvelles infirmières | Délai avant BCM réalisé de façon autonome ; confiance auto-rapportée | Suivi de préceptorat + sondage |
| 5 | Diminuer la charge cognitive | Charge perçue (échelle simple avant / après) | Sondage utilisatrices |
| 6 | Documentation plus uniforme | % des rapports conformes au gabarit | Audit de conformité |
| 7 | Respecter la procédure sans la consulter constamment | Nombre de consultations de la procédure pendant un BCM | Auto-déclaration |

Les cibles chiffrées seront fixées après une mesure de départ en contexte réel (pilote) — pas inventées avant.

## Publics visés

- Infirmières et infirmiers : unités de soins, urgence, périopératoire, soins à domicile, CHSLD ;
- Candidates et candidats à l'exercice de la profession, en intégration (mode intégration dédié) ;
- À terme : autres professionnels participant au circuit du médicament, selon les rôles définis localement.

## Principes directeurs

1. **L'IA assiste, elle ne décide pas.** Aucune recommandation de traitement, jamais.
2. **Zéro renseignement identificatoire.** L'outil fonctionne entièrement sans nom, sans numéro d'assurance maladie, sans date de naissance complète.
3. **La procédure locale prévaut.** Le copilote incarne les bonnes pratiques générales ; en cas d'écart, l'établissement a raison.
4. **Sobriété des alertes.** Un rappel non pertinent est un coût ; le radar se tait par défaut.
5. **Documentation uniforme et validée.** Un seul gabarit, une mention de l'assistance IA, une validation professionnelle obligatoire.

## Critère de réussite ultime

Qu'à la fin d'un BCM, l'infirmière puisse dire :

> « Je n'ai pas eu à réfléchir à la procédure. J'ai simplement suivi la conversation. J'avais confiance de ne rien oublier. »

## Portée de la version 1 — et hors portée

**Dans la portée :** l'entrevue guidée, la structuration, le radar documentaire, l'indice de complétude, le rapport final, le mode intégration, la reprise d'un BCM interrompu.

**Hors portée (v1) :** intégration aux systèmes cliniques (DME, DSQ), analyse d'interactions, calculs de dose, décision clinique de quelque nature que ce soit, conservation de données. Voir `05-limites-ia.md` et `08-evolution.md`.
