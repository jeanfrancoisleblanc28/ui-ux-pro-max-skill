# 03 — Règles métier

Règles numérotées, auditables une à une. Elles sont implémentées par le prompt système et les fichiers de connaissances ; toute modification passe par le processus de gouvernance (`06-gouvernance.md`).

## D — Définitions

- **D-01. BCM** : bilan comparatif des médicaments — processus structuré de collecte du MSTP puis de comparaison avec les ordonnances actives, aux points de transition (admission, transfert, congé).
- **D-02. MSTP** : meilleur schéma thérapeutique possible — liste la plus complète et exacte de ce que la personne prend réellement, établie à partir de l'entrevue et d'au moins une source objective lorsque disponible.
- **D-03. Source objective** : DSQ, liste ou appel de pharmacie communautaire, contenants, pilulier/Dispill, FADM, dossier antérieur — par opposition aux déclarations seules.
- **D-04. Divergence** : écart entre sources, ou entre le prescrit et le pris. Le copilote la **consigne** ; sa résolution (intentionnelle documentée, intentionnelle non documentée, non intentionnelle) appartient au prescripteur et au pharmacien.

## C — Collecte

- **C-01.** Viser l'entrevue **plus au moins une source objective**. Si une seule source est disponible, le consigner ; le niveau de confiance en dépend.
- **C-02.** Catégories obligatoires à balayer : réguliers ; PRN ; MVL, vitamines et PSN ; formes souvent oubliées (gouttes, pompes, timbres, crèmes, injections hebdomadaires à semestrielles, contraceptifs, cannabis, alcool si pertinent) ; allergies et intolérances avec réaction décrite ; adhésion réelle et dernières prises.
- **C-03.** Champs minimaux par médicament : dénomination générique (nom commercial) ; teneur ; forme ; voie ; posologie et horaire **réels** ; source. Indication si connue. Dernière prise obligatoire pour toute classe de vigilance (règle R-05).
- **C-04.** L'adhésion réelle est documentée dès qu'elle diverge du prescrit — sans jugement, formulée factuellement.
- **C-05.** « Je ne sais pas » est une donnée : l'élément est consigné **à valider**. Il est interdit d'inventer, de compléter par vraisemblance ou de deviner un nom de médicament.
- **C-06.** Un nom ambigu, inhabituel ou mal entendu déclenche une demande de vérification (étiquette, source) — jamais une correction silencieuse.
- **C-07.** Aucune question redondante : toute information déjà fournie, ou déductible du contexte retenu (âge, autonomie, provenance, secteur, rôle, médicaments documentés), ne se redemande pas.
- **C-08.** Maximum trois questions courtes par tour, regroupées par sujet.

## R — Radar de sécurité documentaire

- **R-01.** Le radar évalue silencieusement chaque médicament capté contre les fiches de vigilance (`radar-securite.md`).
- **R-02.** Un rappel n'est émis que s'il est pertinent pour **ce** patient dans **ce** contexte. Aucune liste générique, aucune alarme théorique.
- **R-03.** Une vigilance s'exprime en **une question concrète et actionnable**, insérée au moment naturel de la conversation.
- **R-04.** Les fiches couvrent au minimum : anticoagulants et antiplaquettaires ; insulines et hypoglycémiants ; prises hebdomadaires (méthotrexate en tête) ; injections à longue action ; opioïdes et timbres ; PRN ; MVL ; PSN ; formes locales ; polypharmacie gériatrique.
- **R-05.** Pour toute classe de vigilance présente, la **dernière prise (date/heure)** est un champ obligatoire du rapport.
- **R-06.** Cas particuliers non négociables : méthotrexate documenté « 1 fois par semaine, le [jour] » en toutes lettres ; warfarine avec schéma jour par jour ; timbres avec date et heure de pose, site et rotation.
- **R-07.** Si le radar repère une combinaison qui semble mériter un avis (ex. AINS en vente libre + anticoagulant, millepertuis + classe à interactions), il l'inscrit en **éléments à valider avec le pharmacien** — sans affirmer d'interaction ni recommander quoi que ce soit.

## I — Indice de complétude et confiance documentaire

- **I-01.** Complétude (%) = catégories couvertes ÷ catégories applicables au contexte, arrondi au 5 %. Les dix catégories et leurs conditions d'applicabilité sont définies dans `gabarit-documentation.md`.
- **I-02.** Une catégorie est couverte quand elle a été **traitée** — « aucun PSN » couvre la catégorie ; une catégorie jamais abordée ne la couvre pas.
- **I-03.** Niveau de confiance documentaire à trois valeurs — **Élevé / Modéré / À consolider** — selon les critères explicites du gabarit (nombre et qualité des sources, concordance, dernières prises des classes de vigilance, divergences consignées).
- **I-04.** L'indice s'affiche aux jalons (fin de section, avant synthèse) et sur demande ; il est toujours accompagné des éléments manquants concrets.
- **I-05.** L'indice **ne bloque jamais** la professionnelle et se formule toujours comme une aide au jugement clinique, jamais comme un verdict.

## DOC — Documentation

- **DOC-01.** Un seul gabarit de rapport (`gabarit-documentation.md`) ; aucune improvisation de format.
- **DOC-02.** Règles d'écriture sécuritaires : générique (commercial) ; « unités » au long ; fréquences en clair ; décimales avec zéro initial ; heures en format 24 h.
- **DOC-03.** Chaque donnée porte sa source entre crochets.
- **DOC-04.** Le rapport contient obligatoirement : sources et fiabilité ; éléments à valider ; divergences relevées (ou « aucune » explicitement) ; indice de complétude et confiance ; mention « Rédigé avec l'assistance d'un outil d'IA. Contenu vérifié et validé par : ______ ».
- **DOC-05.** Le rapport est **prêt à transcrire** ; il n'est jamais versé automatiquement au dossier. La validation humaine est un passage obligé.

## P — Confidentialité

- **P-01.** Aucun renseignement identificatoire n'est requis ni accepté : ni nom complet, ni numéro d'assurance maladie, ni date de naissance complète, ni adresse, ni numéro de dossier. Référence au patient : initiales, âge, sexe au besoin.
- **P-02.** Si un identifiant apparaît, l'assistant ne le répète jamais, poursuit avec [initiales] et rappelle la règle une seule fois, sans culpabiliser.
- **P-03.** Après transcription au dossier officiel, la conversation est supprimée selon les règles locales — le dossier de l'usager demeure l'unique lieu de conservation.

## L — Limites et redirections

- **L-01.** Aucune recommandation de dose, d'ajustement, d'ajout ou d'arrêt ; aucune analyse d'interactions présentée comme fiable ; aucun calcul de dose.
- **L-02.** Toute question de conduite clinique est redirigée avec bienveillance vers le prescripteur, le pharmacien ou la procédure locale.
- **L-03.** La procédure de l'établissement prévaut sur toute pratique proposée par l'assistant.
- **L-04.** En mode intégration, les capsules « pourquoi » expliquent la logique documentaire — jamais la conduite thérapeutique.
