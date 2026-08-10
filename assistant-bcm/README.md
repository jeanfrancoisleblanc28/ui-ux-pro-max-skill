# Copilote BCM

**Un assistant conversationnel en français pour aider une infirmière à réaliser ses bilans comparatifs des médicaments (BCM) — sans avoir à penser à la procédure.**

Ce projet existe pour une raison simple : aider une infirmière bien réelle dans son quotidien. Pas une démonstration, pas un produit — un outil qu'on installe une fois, qu'on lui remet avec une page de guide, et qui fait qu'à la fin d'un BCM elle peut dire :

> « Je n'ai pas eu à réfléchir à la procédure. J'ai simplement suivi la conversation. J'avais confiance de ne rien oublier. »

> ⚠️ **Cadre d'utilisation.** Le Copilote BCM est une aide à la collecte et à la documentation. Il ne recommande aucun traitement et ne remplace ni le jugement professionnel ni la procédure de l'établissement. Chaque rapport est relu et validé par l'infirmière avant transcription au dossier. **Aucun renseignement identificatoire** (nom, numéro d'assurance maladie, date de naissance complète, adresse) ne doit être saisi — l'outil est conçu pour fonctionner sans.

## Installation

**Rien ne s'installe sur un ordinateur.** L'assistant vit dans un compte ChatGPT : une fois configuré, elle le retrouve sur n'importe quel appareil — ordinateur, tablette, téléphone — simplement en se connectant.

La marche à suivre ci-dessous crée le GPT **dans votre compte** et le lui partage par lien privé. C'est la meilleure façon de faire pour une raison précise : quand vous améliorerez le prompt après ses premiers vrais BCM, elle profitera de la mise à jour instantanément, sans que vous ayez à retoucher quoi que ce soit chez elle. Et ses conversations restent dans son compte à elle — vous n'y avez pas accès, ce qui est exactement ce qu'on veut.

**Ce qu'il faut avant de commencer :** un abonnement ChatGPT payant sur votre compte (nécessaire pour créer un GPT personnalisé). Elle pourra l'utiliser avec un compte gratuit, mais les limites du gratuit risquent de couper un BCM en plein milieu ; pour un usage régulier au travail, un abonnement de son côté est le petit investissement qui rend l'outil fiable.

### Étape 1 — Créer le GPT (chez vous, 5 minutes)

1. Dans ChatGPT, ouvrez **Mes GPT → Créer un GPT**, puis l'onglet **Configurer** ;
2. Donnez-lui un nom clair — « Copilote BCM » — et une description courte ;
3. Collez le contenu intégral de `prompt/instructions-systeme.md` dans le champ **Instructions**. Le fichier fait moins de 8 000 caractères : il entre au complet, sans coupure ;
4. Dans **Connaissances**, téléversez les **trois fichiers** du dossier `connaissances/` : `entrevue-bcm.md`, `radar-securite.md`, `gabarit-documentation.md` ;
5. Dans **Fonctionnalités**, **décochez tout** — navigation web, génération d'images, interpréteur de code. L'assistant n'en a besoin d'aucune, et chaque capacité inutile est une source d'erreur en moins.

### Étape 2 — Partager le lien privé (chez vous, 1 minute)

Cliquez sur **Créer / Enregistrer**, puis choisissez **« Toute personne disposant du lien »**. Ne le publiez pas au magasin public de GPT. Copiez le lien et envoyez-le-lui.

### Étape 3 — Chez elle (10 minutes, une seule fois)

1. Elle se connecte à **son** compte ChatGPT et ouvre votre lien ;
2. Elle démarre une conversation : le GPT s'ajoute automatiquement à sa liste. Elle peut l'**épingler** pour le garder en haut ;
3. Dans les réglages de **son** compte — *Paramètres → Contrôles des données* — **désactivez l'amélioration du modèle pour tous** (l'entraînement sur ses conversations). C'est le réglage qui compte le plus ;
4. Sur son ordinateur : ajoutez un **favori** dans le navigateur, ou un raccourci sur le bureau, pour qu'elle y arrive en un clic. Sur son téléphone : l'application ChatGPT, avec l'assistant épinglé.

### Étape 4 — Le premier essai, ensemble

Remettez-lui **`GUIDE-UTILISATION.md`** — une seule page, écrite pour elle, à imprimer et garder près du clavier. Puis faites **un premier BCM fictif ensemble**, avant un vrai patient : le dialogue de `docs/04-cas-utilisation.md` fait un bon scénario. Dix minutes qui enlèvent toute la nervosité de la première vraie fois.

### Plus tard : améliorer l'assistant

Vous modifiez le GPT depuis votre compte (Instructions ou fichiers de connaissances), vous enregistrez — c'est tout. Elle utilise la nouvelle version dès sa prochaine conversation, sans rien faire de son côté. C'est précisément pour ça qu'on l'a monté chez vous.

### Variante — Claude (Projet)

Si vous préférez Claude : il n'y a pas de partage simple de projet entre comptes personnels, il faut donc créer le Projet **directement dans son compte à elle** (chez elle, en visio avec partage d'écran, ou depuis votre ordinateur en navigation privée — vous vous déconnectez après). Collez `prompt/instructions-systeme.md` dans les instructions du projet, ajoutez les trois fichiers de `connaissances/` aux connaissances du projet. Les mises à jour futures exigeront de refaire ce détour à chaque fois.

## Les trois règles qui la protègent

1. **Jamais de nom de patient.** Initiales et âge seulement — jamais de nom, de numéro d'assurance maladie ni de date de naissance. L'assistant le rappelle lui-même si ça arrive.
2. **Elle relit et valide tout** avant de transcrire au dossier. L'assistant aide à documenter ; il ne décide de rien.
3. **On supprime la conversation** une fois le rapport transcrit au dossier.

## Comment elle s'en sert (aperçu)

> **Infirmière :** Patiente de 78 ans, arrive du domicile. Madame prend du Tylenol quand elle a mal au dos, du Jardiance le matin et son conjoint prépare le pilulier.
>
> **Copilote :** C'est noté — empagliflozine (Jardiance) le matin (teneur à préciser), acétaminophène (Tylenol) au besoin pour douleur lombaire (dose et fréquence réelle à préciser), et le conjoint prépare le pilulier. Trois précisions : le Jardiance, 10 ou 25 mg ? Le Tylenol, quelle teneur et combien de fois par semaine réellement ? Le pilulier — fait maison ou Dispill de la pharmacie ?

Elle peut aussi : reprendre un BCM interrompu (en collant le rapport partiel), demander le « mode express » à l'urgence, ou dire « guide-moi pas à pas » pour recevoir de courtes explications en chemin.

À la fin, l'assistant produit un rapport uniforme avec un **indice de complétude** et un **niveau de confiance documentaire** (Élevé / Modéré / À consolider) qui pointe où une vérification supplémentaire serait utile — sans jamais remplacer son jugement.

## Ce qu'il y a dans ce dossier

```
assistant-bcm/
├── README.md                        ← vous êtes ici
├── GUIDE-UTILISATION.md             # La page à lui remettre
├── prompt/
│   └── instructions-systeme.md      # Le cerveau de l'assistant (à coller dans les instructions)
├── connaissances/                   # Les 3 fichiers à joindre à l'assistant
│   ├── entrevue-bcm.md              #   déroulement de l'entrevue, formulations, contextes
│   ├── radar-securite.md            #   vigilances par classe de médicaments
│   └── gabarit-documentation.md     #   gabarit du rapport, indice de complétude, exemple
└── docs/                            # Documentation de référence — pas nécessaire pour utiliser
                                     # l'assistant (fonctionnement détaillé, limites de l'IA,
                                     # confidentialité, et le reste si un jour on en a besoin)
```

Deux documents de référence valent la lecture même pour un usage personnel : `docs/05-limites-ia.md` (ce que l'outil ne sait pas faire) et `docs/07-confidentialite.md` (pourquoi la règle « jamais de nom » la protège).

## Statut

Version 1.0 — août 2026. Prêt à être essayé sur de vrais BCM, avec relecture et validation systématiques.
