# 04 — Cas d'utilisation

Six cas couvrant les situations types. Le CU-01 inclut un dialogue complet ; il sert aussi de cas de démonstration et de test de non-régression (voir `06-gouvernance.md`).

---

## CU-01 — BCM d'admission, personne âgée venant du domicile

**Acteur :** infirmière d'une unité de médecine.
**Contexte :** patiente de 78 ans admise depuis l'urgence ; conjoint présent ; liste de pharmacie disponible.
**Préconditions :** aucune — l'infirmière ouvre l'assistant et parle.

**Déroulement (dialogue) :**

> **Infirmière :** Nouveau BCM. Patiente de 78 ans, arrive du domicile, admise en médecine. Madame prend du Tylenol quand elle a mal au dos, du Jardiance le matin et son conjoint prépare le pilulier.
>
> **Copilote :** C'est noté. Voici ce que j'ai déjà structuré :
> - **empagliflozine (Jardiance)** — 1 fois par jour le matin — *teneur à préciser*
> - **acétaminophène (Tylenol)** — au besoin, douleur lombaire — *dose et fréquence réelle à préciser*
> - **Gestion :** le conjoint prépare le pilulier → aide requise pour la médication.
>
> Trois précisions, puis on continue :
> 1. Le Jardiance : 10 ou 25 mg ?
> 2. Le Tylenol : quelle teneur, et dans une semaine normale, elle en prend combien de fois ?
> 3. Le pilulier : préparé maison par le conjoint, ou Dispill de la pharmacie ?
>
> **Infirmière :** Jardiance 10. Tylenol 500, à peu près 3 comprimés par semaine. Pilulier maison.
>
> **Copilote :** Parfait, tout est intégré. Avez-vous une source objective sous la main — liste de pharmacie, DSQ, ou les contenants ?
>
> **Infirmière :** J'ai la liste de la pharmacie, datée de la semaine passée.
>
> **Copilote :** Excellent. Quand vous êtes prête, lisez-moi ce qui s'y trouve ; je comparerai avec ce qu'on a et je ne relèverai que les écarts.

*(…collecte des réguliers, PRN, MVL/PSN, balayage des formes oubliées — le copilote repère à la validation croisée des gouttes de latanoprost absentes de l'entrevue, et un clopidogrel servi il y a 4 mois que le conjoint dit cessé…)*

> **Copilote :** État des lieux : **complétude 90 %**, niveau de confiance documentaire **Modéré** — sources concordantes, sauf le clopidogrel à confirmer avec le prescripteur ; le DSQ n'a pas été consulté. Il ne reste que les allergies. Des allergies ou réactions à des médicaments ?

**Résultat :** rapport final conforme au gabarit (voir l'exemple complet dans `gabarit-documentation.md`), avec divergence consignée et éléments à valider.
**Valeur démontrée :** entrevue naturelle, zéro question redondante, omission (gouttes) attrapée par la validation croisée, divergence documentée sans être tranchée.

---

## CU-02 — Urgence, patient confus, proche au téléphone

**Acteur :** infirmière d'urgence.
**Contexte :** homme de 84 ans, désorienté ; fille jointe par téléphone ; aucune liste disponible pour l'instant.

**Déroulement (résumé) :** l'infirmière signale « patient confus, mode express ». Le copilote bascule : priorité aux classes de vigilance (anticoagulants, insulines, opioïdes, immunosuppresseurs), aux dernières prises et aux allergies, questions adressées à la fille. Il consigne « déclarations du patient non fiables ; source principale : proche aidant » et recommande de joindre la pharmacie dès que possible.

**Résultat :** BCM partiel honnête — complétude affichée (p. ex. 60 %), confiance **À consolider**, liste claire de ce qui reste à faire, prêt à reprendre.
**Valeur démontrée :** le mode express priorise sans sacrifier la traçabilité ; l'indice dit la vérité au lieu de donner une fausse assurance.

---

## CU-03 — Validation croisée DSQ + liste de pharmacie

**Acteur :** infirmière clinicienne.
**Contexte :** patient bon historien ; DSQ consulté et liste de pharmacie disponibles.

**Déroulement (résumé) :** collecte standard, puis parcours élément par élément des deux sources. Le copilote rappelle que le DSQ montre le **servi**, pas le **pris** ; chaque écart devient une question (« le DSQ montre du pantoprazole servi il y a deux mois — le prend-il encore ? ») ou une divergence consignée.

**Résultat :** confiance documentaire **Élevé** — deux sources objectives concordantes, dernières prises documentées.
**Valeur démontrée :** la validation croisée outillée devient rapide et systématique.

---

## CU-04 — Transfert de CHSLD

**Acteur :** infirmière d'unité recevant un transfert.
**Contexte :** FADM du CHSLD jointe au transfert.

**Déroulement (résumé) :** le copilote traite la FADM comme source de référence pour les réguliers, et concentre l'entrevue sur ce qui n'y figure pas : PRN réellement utilisés, MVL, PSN, timbres et injections espacées, allergies confirmées.

**Résultat :** BCM complet sans redite de la FADM.
**Valeur démontrée :** l'adaptation à la provenance élimine le travail inutile.

---

## CU-05 — Nouvelle infirmière en mode intégration

**Acteur :** candidate à l'exercice de la profession, en préceptorat.

**Déroulement (résumé) :** « Guide-moi, c'est mon premier BCM seule. » Le déroulement est identique, mais le copilote glisse des capsules brèves : pourquoi la réaction allergique se décrit, pourquoi le DSQ ne suffit pas, pourquoi le jour du méthotrexate est vital. Deux phrases maximum par capsule, jamais bloquantes.

**Résultat :** BCM conforme + apprentissage en contexte réel.
**Valeur démontrée :** l'objectif d'intégration des nouvelles infirmières est servi par le même outil, sans mode d'emploi séparé.

---

## CU-06 — Reprise d'un BCM interrompu

**Acteur :** infirmière rappelée ailleurs pendant la collecte.

**Déroulement (résumé) :** avant de partir, elle demande « donne-moi l'état ». Le copilote produit le rapport partiel. Au retour (même session ou nouvelle), elle colle le rapport ; le copilote résume l'état en deux lignes (« 6 médicaments documentés ; il reste PRN, allergies, validation croisée ») et poursuit exactement au point d'arrêt, sans une seule question déjà répondue.

**Résultat :** aucune perte, aucune redite.
**Valeur démontrée :** l'outil épouse la réalité des interruptions constantes sur les unités.
