# Copilote BCM

**Assistant conversationnel francophone pour la réalisation du bilan comparatif des médicaments (BCM)** — conçu pour les infirmières et infirmiers du Québec.

> ⚠️ **Cadre d'utilisation.** Le Copilote BCM est une aide cognitive et documentaire. Il ne pose aucun acte clinique, ne recommande aucun traitement et ne remplace ni le jugement professionnel ni la procédure locale. Chaque rapport doit être vérifié et validé par un professionnel avant transcription au dossier. **Aucun renseignement identificatoire** (nom, numéro d'assurance maladie, date de naissance complète, adresse) ne doit être saisi.

## Ce que c'est

Le BCM — l'établissement du meilleur schéma thérapeutique possible (MSTP) et sa documentation — est exigeant, normé et sujet aux omissions. Le Copilote BCM le transforme en conversation : l'infirmière parle naturellement (« Madame prend du Tylenol quand elle a mal au dos, du Jardiance le matin et son conjoint prépare le pilulier »), l'assistant structure, repère ce qui manque et ne pose que les questions utiles.

Ses quatre forces :

1. **Intelligence contextuelle** — il retient l'âge, l'autonomie, la provenance, le secteur, le rôle du professionnel et les médicaments déjà documentés : aucune question redondante.
2. **Entrevue naturelle** — pas de « langage informatique », pas de formulaire : la conversation fait le travail.
3. **Radar de sécurité documentaire** — anticoagulants, insulines, prises hebdomadaires, injections semestrielles, opioïdes, PRN, MVL, PSN : surveillés en silence, rappelés seulement quand c'est pertinent pour ce patient.
4. **Indice de complétude** — un pourcentage et, surtout, un **niveau de confiance documentaire** (Élevé / Modéré / À consolider) justifié en une phrase, qui pointe où une vérification supplémentaire serait utile — sans jamais remplacer le jugement clinique.

## Structure du projet

```
assistant-bcm/
├── README.md                        ← vous êtes ici
├── prompt/
│   └── instructions-systeme.md      # Le prompt système (< 8 000 caractères, portable partout)
├── connaissances/
│   ├── entrevue-bcm.md              # Déroulement, formulations, adaptations par contexte, mode intégration
│   ├── radar-securite.md            # 10 fiches de vigilance documentaire par classe
│   └── gabarit-documentation.md     # Gabarit du rapport, indice de complétude, exemple complet
└── docs/                            # Dossier professionnel (présentable à une organisation de santé)
    ├── 01-vision.md                 # Problème, solution, objectifs mesurables
    ├── 02-architecture-fonctionnelle.md
    ├── 03-regles-metier.md          # Règles numérotées, auditables
    ├── 04-cas-utilisation.md        # 6 cas, dont un dialogue complet
    ├── 05-limites-ia.md             # Ce que l'outil n'est pas, risques et mitigations
    ├── 06-gouvernance.md            # Rôles, cycle de vie, incidents, déploiement par étapes
    ├── 07-confidentialite.md        # Zéro identifiant par conception, Loi 25, ÉFVP
    └── 08-evolution.md              # Feuille de route v1.x → v2 → v3
```

## Déploiement en 5 minutes

### ChatGPT (GPT personnalisé)

1. Créer un GPT personnalisé ;
2. Coller le contenu intégral de `prompt/instructions-systeme.md` dans le champ **Instructions** (le fichier fait moins de 8 000 caractères — il entre au complet) ;
3. Joindre les **trois fichiers** de `connaissances/` comme fichiers de connaissances ;
4. **Désactiver** toutes les capacités (navigation web, génération d'images, exécution de code) ;
5. Vérifier les paramètres de confidentialité du compte : entraînement sur les données **désactivé** (voir `docs/07-confidentialite.md`).

### Claude (Projet)

1. Créer un projet ;
2. Coller `prompt/instructions-systeme.md` dans les **instructions du projet** ;
3. Ajouter les trois fichiers de `connaissances/` aux **connaissances du projet**.

### Amorces de conversation suggérées

- « Nouveau BCM — admission »
- « Nouveau BCM express — urgence »
- « Reprendre un BCM en cours » *(coller le rapport partiel)*
- « Guide-moi pas à pas, c'est mon premier BCM » *(mode intégration)*

## Aperçu express

> **Infirmière :** Patiente de 78 ans, arrive du domicile. Madame prend du Tylenol quand elle a mal au dos, du Jardiance le matin et son conjoint prépare le pilulier.
>
> **Copilote :** C'est noté — empagliflozine (Jardiance) le matin (teneur à préciser), acétaminophène (Tylenol) au besoin pour douleur lombaire (dose et fréquence réelle à préciser), et le conjoint prépare le pilulier. Trois précisions : le Jardiance, 10 ou 25 mg ? Le Tylenol, quelle teneur et combien de fois par semaine réellement ? Le pilulier — fait maison ou Dispill de la pharmacie ?

Le dialogue complet et cinq autres cas : `docs/04-cas-utilisation.md`.

## Le critère de réussite

Qu'à la fin d'un BCM, l'infirmière puisse dire :

> « Je n'ai pas eu à réfléchir à la procédure. J'ai simplement suivi la conversation. J'avais confiance de ne rien oublier. »

## Statut

| | |
|---|---|
| Version | 1.0.0 |
| Date | 2026-08-05 |
| Étape de déploiement | 1 — usage individuel encadré (voir `docs/06-gouvernance.md`) |
| Prochaine étape | Mesure de départ des indicateurs, puis pilote restreint |
