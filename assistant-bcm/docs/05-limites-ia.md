# 05 — Limites de l'IA

Ce document dit franchement ce que l'outil **n'est pas**, ce qu'il peut mal faire, et comment ces risques sont mitigés. C'est la pièce que tout comité clinique lira en premier — elle est écrite pour ça.

## Positionnement

Le Copilote BCM est une **aide cognitive et documentaire**. Il ne diagnostique pas, ne traite pas, ne recommande pas, ne surveille pas de paramètre clinique. Il structure une collecte d'information menée par un professionnel qui demeure l'unique auteur et responsable du contenu versé au dossier.

**Prudence réglementaire :** dans sa forme v1 (aide à la documentation, sans fonction de décision clinique), l'outil est conçu pour rester hors du périmètre des instruments médicaux. Toute évolution qui ajouterait une fonction d'analyse clinique (ex. détection d'interactions présentée comme fiable) devrait faire l'objet d'une évaluation au regard du cadre de Santé Canada sur les logiciels à titre d'instruments médicaux (LIM/SaMD) **avant** développement. Cette frontière est volontaire et gouvernée (`06-gouvernance.md`).

## Limites intrinsèques et mitigations

| Limite | Risque concret | Mitigation en place |
|---|---|---|
| **Hallucination** : un modèle de langage peut produire un nom, une teneur ou une « correction » plausible mais fausse | Un médicament mal identifié se rend au dossier | Règles C-05 et C-06 : interdiction d'inventer et de corriger silencieusement ; tout nom ambigu → vérification à l'étiquette ou à la source ; validation humaine obligatoire (DOC-05) |
| **Connaissances datées** : nouveaux médicaments, retraits du marché, changements de pratique postérieurs à l'entraînement | Fiche de vigilance incomplète ou désuète | Le radar documente, il ne décide pas ; les fiches sont révisables par le répondant pharmacie sans toucher au reste (architecture déclarative) |
| **Aucun accès aux systèmes** : pas de DSQ, pas de DME, pas de dossier | L'outil ne « sait » que ce qu'on lui dit | Assumé par conception ; le rapport trace explicitement quelles sources ont été consultées et lesquelles manquent |
| **Pas d'analyse d'interactions fiable** | Fausse réassurance si l'outil se prononçait | Interdiction absolue (L-01, R-07) : les combinaisons préoccupantes deviennent des « éléments à valider avec le pharmacien », jamais des verdicts |
| **Variabilité** : deux sessions identiques peuvent formuler différemment | Hétérogénéité résiduelle | Gabarit unique et règles d'écriture fermes (DOC-01 à DOC-04) ; banc d'essai de non-régression à chaque version |
| **Excès de confiance de l'utilisatrice** : « l'outil l'a dit » | Transfert indu de responsabilité | Mention IA obligatoire, champ de validation nommée, formulation systématique de l'indice comme aide au jugement (I-05) ; formation initiale (`06-gouvernance.md`) |
| **Fuite de renseignements personnels** par inadvertance | Donnée identificatoire dans un système externe | Conception « zéro identifiant » (P-01, P-02), paramètres de plateforme, suppression post-transcription (`07-confidentialite.md`) |

## Ce que l'assistant refuse de faire

- Recommander, ajuster, débuter ou cesser un traitement ; proposer une dose ; faire un calcul de dose.
- Se prononcer sur une interaction, une contre-indication ou la conduite à tenir.
- Poursuivre un échange contenant des renseignements identificatoires sans appliquer la règle P-02.
- Transcrire quoi que ce soit au dossier — il n'en a ni la capacité ni le droit.
- Se substituer à la procédure locale : en cas d'écart, il s'efface.

## Responsabilité professionnelle

L'infirmière ou l'infirmier demeure responsable de l'évaluation, de la collecte et de la documentation, conformément à son champ d'exercice et à ses obligations déontologiques. Concrètement :

1. **Relire intégralement** le rapport avant transcription — jamais de copier-coller aveugle ;
2. **Valider** les éléments marqués « à valider » selon le jugement clinique et la procédure ;
3. **Signer** la validation (le champ est prévu au gabarit) ;
4. **Signaler** toute erreur de l'assistant via le canal de gouvernance — chaque signalement améliore l'outil.

L'outil retient le rôle du professionnel pour adapter le niveau de détail de la conversation ; il ne statue jamais sur les champs d'exercice — cette question relève de l'établissement et des ordres professionnels.

## Conditions d'utilisation sécuritaire (résumé opposable)

- Formation courte préalable (attentes, limites, confidentialité) ;
- Zéro renseignement identificatoire, toujours ;
- Validation humaine systématique avant transcription ;
- Suppression de la conversation après transcription ;
- Procédure locale > copilote, en tout temps.
