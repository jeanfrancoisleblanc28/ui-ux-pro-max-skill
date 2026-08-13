# Gabarit de documentation BCM

> Fichier de connaissances du Copilote BCM. Définit le format unique du rapport final,
> les règles de rédaction, la méthode de calcul de l'indice de complétude et du niveau
> de confiance documentaire, puis un exemple complet.

## Règles de rédaction

1. **Dénomination générique d'abord**, nom commercial entre parenthèses : « empagliflozine (Jardiance) ».
2. **Unités écrites au long** : « 12 unités », jamais « 12 U ».
3. **Fréquences en clair** : « 1 fois par jour, le matin », « 1 fois par semaine, le vendredi » — pas d'abréviations ambiguës.
4. **Décimales avec zéro initial** : 0,5 mg — jamais ,5 mg.
5. **Heures en format 24 h** : 08 h, 17 h 30.
6. **Chaque donnée porte sa source** : [patient], [proche aidant], [liste de pharmacie], [DSQ], [contenants], [pilulier], [FADM], [dossier antérieur].
7. **Ce qui n'est pas su est écrit comme tel** : « à valider », jamais un blanc, jamais une invention.
8. **Aucun renseignement identificatoire** : initiales, âge, sexe au besoin — rien d'autre.

---

## Structure du rapport

```markdown
# Bilan comparatif des médicaments — MSTP
**Patient :** [initiales], [âge] ans — **Contexte :** [provenance → secteur]
**Gestion des médicaments :** [qui prépare / qui administre / pilulier ?]
**Réalisé par :** [rôle] — **Date :** [date]

## Sources consultées
| Source | Consultée | Remarque sur la fiabilité |
|---|---|---|
| Entrevue patient | Oui/Non | [bon historien / récit incertain / …] |
| Proche aidant | Oui/Non | [présent / téléphone / …] |
| Liste de pharmacie / DSQ | Oui/Non | [date de la liste] |
| Contenants / pilulier / FADM | Oui/Non | [détail] |

## Médicaments
| # | Médicament (générique — commercial) | Teneur | Forme | Voie | Posologie et horaire réels | Dernière prise | Indication (si connue) | Source | Notes / adhésion |
|---|---|---|---|---|---|---|---|---|---|

*(sections : réguliers — PRN — MVL / PSN — formes particulières et injections espacées)*

## Allergies et intolérances
| Substance | Réaction décrite | Source |
|---|---|---|

## Points de vigilance documentés
- [rappels du radar qui se sont appliqués et ce qui a été documenté en conséquence]

## Éléments à valider
- [liste priorisée de ce qui manque ou repose sur une source unique]

## Divergences relevées entre les sources — à clarifier (prescripteur / pharmacien)
- [source A indique X ; source B indique Y]

## Indice de complétude
**Complétude : X %** ([n] catégories couvertes sur [m] applicables)
**Niveau de confiance documentaire : [Élevé / Modéré / À consolider]** — [justification en une phrase]

---
*Rédigé avec l'assistance d'un outil d'IA. Contenu vérifié et validé par : ______________*
*À transcrire au dossier selon la procédure locale. Cet indice éclaire le jugement clinique ; il ne le remplace pas.*
```

---

## Indice de complétude — méthode de calcul

### Les dix catégories

| # | Catégorie | Applicable… |
|---|---|---|
| 1 | Contexte patient (âge, provenance, secteur, autonomie, gestion) | toujours |
| 2 | Sources : entrevue + au moins une source objective consultée | toujours *(objective : si disponible)* |
| 3 | Médicaments réguliers, champs complets | toujours |
| 4 | PRN et fréquence réelle | toujours |
| 5 | MVL, vitamines, PSN passés en revue | toujours |
| 6 | Formes souvent oubliées balayées (gouttes, pompes, timbres, crèmes, injections espacées) | toujours |
| 7 | Allergies et intolérances, réaction décrite | toujours |
| 8 | Dernières prises documentées pour toute classe de vigilance présente | si classe de vigilance présente |
| 9 | Validation croisée entre les sources | si au moins deux sources |
| 10 | Divergences relevées consignées (ou « aucune » écrit explicitement) | si validation croisée faite |

### Calcul

- **Complétude (%) = catégories couvertes ÷ catégories applicables**, arrondi au 5 % le plus proche.
- Une catégorie est « couverte » quand elle a été **traitée**, même si la réponse est « aucun » (ex. : « aucun PSN » est une catégorie couverte ; une catégorie jamais abordée ne l'est pas).
- En mode express (urgence), l'indice reste calculé sur toutes les catégories applicables : il montre honnêtement ce qui reste à faire — c'est sa fonction.

### Niveau de confiance documentaire

| Niveau | Critères (tous ceux qui s'appliquent) |
|---|---|
| **Élevé** | Au moins deux sources indépendantes dont une objective, concordantes pour l'essentiel ; toutes les catégories applicables couvertes ; dernières prises documentées pour chaque classe de vigilance présente ; aucune divergence non consignée. |
| **Modéré** | Une seule source fiable, ou déclarations du patient seules alors qu'il est bon historien ; ou quelques éléments secondaires à valider ; rien de critique en suspens. |
| **À consolider** | Sources contradictoires non résolues ; patient au récit incertain sans source objective ni proche joint ; catégorie entière non couverte ; ou classe de vigilance sans dernière prise documentée. |

**Formulations types :**
- « Niveau de confiance documentaire : Élevé — entrevue et liste de pharmacie concordantes, dernières prises documentées. »
- « Niveau de confiance documentaire : Modéré — certaines informations reposent uniquement sur les déclarations du patient et méritent une validation complémentaire. »
- « Niveau de confiance documentaire : À consolider — récit incertain, aucune source objective encore consultée ; la liste de pharmacie changerait beaucoup la donne. »

L'indice **ne bloque jamais** l'infirmière et **ne remplace pas** le jugement clinique : il pointe où une vérification supplémentaire serait la plus utile.

---

## Exemple complet

# Bilan comparatif des médicaments — MSTP
**Patiente :** M. T., 78 ans — **Contexte :** domicile (avec conjoint) → unité de médecine
**Gestion des médicaments :** le conjoint prépare un pilulier hebdomadaire maison ; il administre matin et soir
**Réalisé par :** infirmière — **Date :** 2026-08-05

## Sources consultées
| Source | Consultée | Remarque sur la fiabilité |
|---|---|---|
| Entrevue patiente | Oui | Bonne historienne, cohérente |
| Proche aidant (conjoint) | Oui | Présent, gère la médication |
| Liste de pharmacie | Oui | Liste datée de la semaine dernière |
| DSQ | Non | À consulter si accès disponible |

## Médicaments
| # | Médicament (générique — commercial) | Teneur | Forme | Voie | Posologie et horaire réels | Dernière prise | Indication (si connue) | Source | Notes / adhésion |
|---|---|---|---|---|---|---|---|---|---|
| 1 | empagliflozine (Jardiance) | 10 mg | comprimé | orale | 1 fois par jour, le matin | ce matin 08 h | diabète type 2 | [conjoint] + [liste] | dans le pilulier |
| 2 | amlodipine (Norvasc) | 5 mg | comprimé | orale | 1 fois par jour, le matin | ce matin 08 h | hypertension | [conjoint] + [liste] | dans le pilulier |
| 3 | atorvastatine (Lipitor) | 20 mg | comprimé | orale | 1 fois par jour, au coucher | hier 22 h | cholestérol | [liste] | dans le pilulier |
| 4 | latanoprost (Xalatan) | 0,005 % | gouttes | ophtalmique | 1 goutte chaque œil, au coucher | hier 22 h | glaucome | [liste], confirmé [patiente] | **hors pilulier** — repérée à la validation croisée |
| 5 | acétaminophène (Tylenol) | 500 mg | comprimé | orale | 1 à 2 comprimés au besoin, douleur lombaire — réellement environ 3 comprimés par semaine | avant-hier | douleur lombaire | [patiente] | MVL, hors pilulier |
| 6 | cholécalciférol (vitamine D) | 1 000 unités | comprimé | orale | 1 fois par jour, le matin | ce matin 08 h | — | [conjoint] | MVL, dans le pilulier |

## Allergies et intolérances
| Substance | Réaction décrite | Source |
|---|---|---|
| pénicilline | éruption cutanée dans l'enfance | [patiente] |

## Points de vigilance documentés
- Gouttes ophtalmiques hors pilulier : documentées après balayage des formes oubliées, confirmées par la patiente.
- Fréquence réelle du PRN documentée (environ 3 comprimés par semaine).

## Éléments à valider
- DSQ non consulté — à faire si l'accès est disponible.
- Aucun produit de santé naturel déclaré ; question posée avec exemples, réponse « non » des deux répondants.

## Divergences relevées entre les sources — à clarifier (prescripteur / pharmacien)
- La liste de pharmacie montre du **clopidogrel (Plavix) 75 mg** servi il y a 4 mois ; le conjoint rapporte un arrêt « demandé par le cardiologue ». Arrêt non documenté au dossier disponible — **à confirmer avec le prescripteur avant toute conclusion**.

## Indice de complétude
**Complétude : 90 %** (9 catégories couvertes sur 10 — DSQ non consulté, la validation croisée repose sur la seule liste de pharmacie)
**Niveau de confiance documentaire : Modéré** — sources concordantes sauf une divergence consignée (clopidogrel) ; la confirmation du prescripteur et le DSQ permettraient de passer à Élevé.

---
*Rédigé avec l'assistance d'un outil d'IA. Contenu vérifié et validé par : ______________*
*À transcrire au dossier selon la procédure locale. Cet indice éclaire le jugement clinique ; il ne le remplace pas.*
