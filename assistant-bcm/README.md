# Copilote BCM

**Un assistant conversationnel en français pour aider une infirmière à réaliser ses bilans comparatifs des médicaments (BCM) — sans avoir à penser à la procédure.**

Ce projet existe pour une raison simple : aider une infirmière bien réelle dans son quotidien. Pas une démonstration, pas un produit — un outil qu'on installe une fois, qu'on lui remet avec une page de guide, et qui fait qu'à la fin d'un BCM elle peut dire :

> « Je n'ai pas eu à réfléchir à la procédure. J'ai simplement suivi la conversation. J'avais confiance de ne rien oublier. »

> ⚠️ **Cadre d'utilisation.** Le Copilote BCM est une aide à la collecte et à la documentation. Il ne recommande aucun traitement et ne remplace ni le jugement professionnel ni la procédure de l'établissement. Chaque rapport est relu et validé par l'infirmière avant transcription au dossier. **Aucun renseignement identificatoire** (nom, numéro d'assurance maladie, date de naissance complète, adresse) ne doit être saisi — l'outil est conçu pour fonctionner sans.

## Installer l'assistant (5 minutes, à faire une fois)

Faites l'installation **depuis son compte à elle**, pour qu'elle retrouve l'assistant dans sa liste à chaque fois.

### Option A — ChatGPT (GPT personnalisé)

1. Créer un GPT personnalisé ;
2. Coller le contenu intégral de `prompt/instructions-systeme.md` dans le champ **Instructions** (le fichier fait moins de 8 000 caractères — il entre au complet) ;
3. Joindre les **trois fichiers** de `connaissances/` comme fichiers de connaissances ;
4. **Désactiver** toutes les capacités (navigation web, génération d'images, exécution de code) ;
5. Dans les réglages du compte, **désactiver l'entraînement sur les données** et garder le GPT privé (« Seulement moi »).

### Option B — Claude (Projet)

1. Créer un projet ;
2. Coller `prompt/instructions-systeme.md` dans les **instructions du projet** ;
3. Ajouter les trois fichiers de `connaissances/` aux **connaissances du projet**.

### Ensuite

- Remettez-lui **`GUIDE-UTILISATION.md`** — une seule page, écrite pour elle, imprimable ;
- Faites un premier BCM fictif ensemble (le dialogue de `docs/04-cas-utilisation.md` peut servir de scénario) pour qu'elle voie comment ça se passe avant un vrai patient.

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
