# 02 — FLI / FLS

Ce domaine transforme une analyse financière en décision de prêt défendable. Il tranche l'admissibilité, fixe le prix du risque, vérifie la conformité à la politique d'investissement et produit le dossier soumis au comité d'investissement commun.

La règle d'or du domaine : **aucun paramètre de politique ne se cite de mémoire**. Chaque plafond, chaque taux, chaque ratio et chaque seuil de délégation provient du document en vigueur, à la version en vigueur. Le référentiel `data/parametres-politique.csv` tient la liste de ces paramètres et leur statut de validation ; tant qu'un paramètre porte le statut `A_VALIDER`, aucun chiffre qui en dépend ne peut être présenté comme définitif.

## Vue d'ensemble

| Module | ID | Produit | Dépend de |
|---|---|---|---|
| admissibilite | P1 | Verdict d'admissibilité motivé et dépenses admissibles retenues | Aucun |
| tarification | P2 | Taux, terme, amortissement, congé de capital et frais | F3, F4, P1 |
| conformite-politique | P3 | Grille de conformité point par point et dérogations demandées | F2, P1, P2 |
| preparation-CIC | P4 | Note d'investissement, conditions de décaissement, projet de résolution | F1 à F4, P1 à P3 |

L'ordre n'est pas négociable et il est contre-intuitif pour qui vient du secteur bancaire.

P1 vient en premier, avant toute analyse financière. Un dossier non admissible ne doit jamais consommer d'heures d'analyse : le verdict d'admissibilité est un filtre, pas une formalité de fin de parcours. Rendre ce verdict tôt protège le temps du conseiller et évite de créer chez le promoteur une attente que la politique ne permet pas de satisfaire.

P2 vient après la cotation de risque produite en F4, jamais avant. Tarifer avant de coter, c'est fixer un prix puis chercher les arguments qui le justifient — l'inverse exact du travail attendu. La séquence correcte est : je comprends le risque, je le cote, puis la grille me donne le prix.

P3 vient après le montage et la tarification parce qu'il vérifie leur produit combiné : c'est le montage tarifé qui doit être conforme, pas le montage seul. P3 est aussi le module qui détermine le niveau d'instance décisionnelle et donc à quelle table le dossier sera présenté.

P4 assemble et n'analyse plus. Toute analyse nouvelle qui apparaîtrait à l'étape de rédaction est le signe qu'un module amont a été escamoté ; il faut y retourner plutôt que de l'improviser dans la note.

## P1 — admissibilite

**Objectif.** Trancher, avant toute analyse, si l'entreprise, le projet et les dépenses sont admissibles aux fonds visés et sur le territoire desservi.

**Entrées requises.**

- Description de l'entreprise, de son établissement principal et de ses établissements secondaires
- Code SCIAN et description réelle des activités, qui ne coïncident pas toujours
- Nature du projet et ventilation préliminaire des dépenses
- Stade de développement : démarrage, croissance, consolidation, relève, redressement
- Liste des aides publiques déjà reçues, demandées ou en cours d'instruction
- Structure de propriété et liens avec d'autres entreprises

### Méthode

#### 1. Vérifier le territoire d'opération et le lieu de l'établissement visé

Le paramètre `TERRITOIRE_ADMISSIBLE` définit le territoire desservi. La question n'est pas où se trouve le siège social inscrit au registre des entreprises, mais où se déroulera l'activité financée et où seront créés ou maintenus les emplois. Une entreprise dont le siège est ailleurs mais qui ouvre un établissement sur le territoire peut être admissible ; une entreprise dont le siège est sur le territoire mais qui investit ailleurs ne l'est généralement pas. Demandez l'adresse civique de l'établissement visé et confrontez-la à un document indépendant : bail, offre d'achat, compte de taxes, permis municipal. Un dossier où l'établissement visé n'est pas encore choisi se traite en admissibilité conditionnelle, avec la localisation comme condition à lever.

#### 2. Confirmer la forme juridique et l'immatriculation

Vérifiez l'existence légale au registre des entreprises : dénomination exacte, numéro d'entreprise, statut, date d'immatriculation, administrateurs et actionnaires déclarés. Une immatriculation en défaut de déclaration de mise à jour est un signal de gestion à noter. Confirmez que la forme juridique correspond à ce que la politique permet de financer : société par actions, société de personnes, coopérative, entreprise individuelle, organisme à but non lucratif — toutes ne sont pas admissibles à tous les fonds. Notez la date de fin d'exercice, qui déterminera quels états financiers vous pourrez obtenir.

#### 3. Valider le secteur d'activité contre les exclusions

Le paramètre `SECTEURS_EXCLUS` porte la liste des secteurs et activités exclus. Cette liste se reprend intégralement du document en vigueur : elle ne se reconstitue ni de mémoire, ni par analogie avec un autre fonds, ni par déduction logique. Deux pièges reviennent constamment. Le premier est l'entreprise à activités multiples dont une seule est exclue : il faut alors déterminer si le projet financé porte sur l'activité exclue et si la politique raisonne par entreprise ou par projet. Le second est le décalage entre le code SCIAN déclaré et l'activité réelle ; c'est l'activité réelle qui gouverne.

#### 4. Qualifier chaque dépense du projet

Reprenez le projet poste par poste et attribuez à chacun un statut : admissible, non admissible, admissible sous condition. Le paramètre `DEPENSES_ADMISSIBLES` porte la règle applicable. Les postes qui exigent systématiquement une vérification sont les taxes récupérables, qui ne sont normalement pas admissibles ; la main-d'œuvre interne capitalisée ; les dépenses payées à une partie liée ; les véhicules ; le fonds de roulement ; et les frais professionnels. Cette qualification produit le montant de dépenses admissibles qui servira ensuite de base au calcul du cumul des aides et parfois au calcul du montant maximal du prêt.

#### 5. Vérifier le cumul des aides publiques

Recensez toutes les aides publiques touchant le même projet, tous paliers confondus, y compris celles obtenues d'un autre organisme sans que le promoteur les considère comme des aides : crédits d'impôt, subventions salariales, garanties de prêt, prêts à conditions avantageuses. Le plafond applicable est le paramètre `CUMUL_MAX_AIDES`, et lorsque plusieurs programmes se superposent, c'est la règle la plus contraignante qui gouverne. Le calcul se fait sur les dépenses admissibles et non sur le coût total du projet — l'erreur inverse est fréquente et fait passer un dossier non conforme pour conforme.

#### 6. Vérifier les exclusions de nature

Certaines opérations sont exclues quel que soit le secteur. Le refinancement d'une dette existante est généralement exclu, y compris lorsqu'il se présente sous la forme d'un rachat d'équipement déjà financé. Les dépenses engagées avant le dépôt de la demande sont normalement inadmissibles : demandez les dates des bons de commande, des dépôts et des contrats signés, pas seulement les dates de facture. Les transferts entre parties liées appellent une vigilance particulière, notamment dans les dossiers de relève où l'acheteur et le vendeur appartiennent à la même famille. Confirmez chacune de ces règles dans le document en vigueur plutôt que de les tenir pour acquises.

#### 7. Rendre un verdict tranché

Le module se conclut par l'une de trois réponses, jamais par une nuance. Admissible : le dossier passe à l'analyse. Admissible sous réserve : le dossier passe à l'analyse, avec la liste écrite des réserves à lever et le moment où elles doivent l'être. Non admissible : le dossier s'arrête, avec le motif précis et la référence à la disposition applicable. Dans ce dernier cas, le conseiller informe le promoteur rapidement et, lorsque c'est possible, l'oriente vers un autre guichet — c'est la partie du travail qui préserve la relation malgré le refus.

### Sorties

- Verdict d'admissibilité motivé, daté et versé au dossier
- Montant des dépenses admissibles retenues
- Liste des réserves à lever et échéance de chacune
- Motif de refus et disposition applicable, le cas échéant

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Analyser le dossier avant de statuer sur l'admissibilité | Des heures d'analyse investies dans un dossier qui ne peut pas être financé, et une attente créée chez le promoteur | P1 est la première étape de PL1 ; aucune analyse financière n'est ouverte sans verdict versé au dossier |
| Présumer d'un plafond de cumul sans le vérifier | Dossier non conforme découvert après la décision, aide à rembourser | Contrôle C18 : tout paramètre au statut `A_VALIDER` est signalé avant présentation |
| Accepter des dépenses engagées avant le dépôt | Inadmissibilité partielle du projet, montant de prêt à réviser à la baisse | Demander les dates de bons de commande et de dépôts, pas les dates de facture |
| Retenir le code SCIAN déclaré plutôt que l'activité réelle | Secteur exclu non détecté | Décrire l'activité en une phrase et la confronter à la liste d'exclusions |
| Traiter une entreprise à activités multiples comme un tout | Financement indirect d'une activité exclue | Déterminer si la politique raisonne par entreprise ou par projet, et documenter la réponse |
| Oublier une aide obtenue d'un autre palier | Dépassement du plafond de cumul | Faire signer au promoteur une déclaration des aides reçues et demandées |

## P2 — tarification

**Objectif.** Fixer le taux, le terme, l'amortissement et les frais du prêt en fonction du risque coté et de la grille en vigueur.

**Entrées requises.**

- Cotation de risque produite en F4, avec ses mitigants et ses risques résiduels
- Ratio de couverture du service de la dette par scénario, produit en F3
- Garanties offertes, leur rang et leur valeur de réalisation estimée
- Grille de tarification en vigueur et taux de référence courant
- Durée de vie utile des actifs financés

### Méthode

#### 1. Partir du taux de référence en vigueur

Le paramètre `TAUX_REFERENCE` porte le taux de base et l'indice auquel il est rattaché. Notez la date de constatation : un taux de référence indexé change entre le moment de l'analyse et celui du décaissement, et l'offre doit préciser si le taux est fixé à l'acceptation ou au décaissement. Cette précision, souvent négligée à l'étape de l'analyse, devient une source de litige quand les taux bougent entre les deux dates.

#### 2. Ajouter la prime de risque correspondant à la cote

Le paramètre `GRILLE_PRIME_RISQUE` établit la correspondance entre la cote produite en F4 et la prime applicable. La prime se lit dans la grille ; elle ne se négocie pas au cas par cas, sans quoi la grille perd sa fonction de traitement équitable entre promoteurs. Si le conseiller estime que la cote ne reflète pas le risque réel, la correction se fait en révisant la cotation en F4, avec les motifs écrits, et non en ajustant discrètement la prime.

#### 3. Ajuster selon le rang de sûreté et la qualité des garanties

Un prêt en second rang derrière une institution bancaire ne porte pas le même risque de perte qu'un prêt en premier rang, même à cote de risque égale, parce que la probabilité de défaut est la même mais la perte en cas de défaut ne l'est pas. Documentez la valeur de réalisation estimée des garanties, pas leur valeur comptable ni leur valeur d'assurance. Le paramètre `GARANTIES_EXIGEES` porte les exigences minimales selon le montant, incluant la question du cautionnement personnel des promoteurs et de son étendue.

#### 4. Fixer le terme et l'amortissement selon la durée de vie des actifs

Les paramètres `TERME_MAX` et `AMORTISSEMENT_MAX` portent les maximums permis. Le principe qui gouverne au-delà du maximum permis est simple : l'amortissement ne doit jamais excéder la durée de vie utile de l'actif financé, même quand la politique le permettrait. Amortir un équipement sur une période plus longue que sa vie utile revient à garantir que l'entreprise paiera encore un actif qu'elle devra déjà remplacer. Pour un financement mixte — bâtiment, équipement et fonds de roulement dans un même prêt —, l'amortissement se pondère selon la composition, ou le financement se scinde en tranches.

#### 5. Déterminer le congé de capital requis

Le paramètre `CONGE_CAPITAL_MAX` porte le maximum permis, mais le congé accordé doit être justifié par la courbe de trésorerie produite en F3, pas simplement permis par la politique. Un congé se justifie quand le projet comporte une période de montée en régime pendant laquelle les flux ne sont pas encore au rendez-vous : construction, mise en service d'équipement, développement de marché. Il ne se justifie pas pour compenser une capacité de remboursement insuffisante en régime permanent — dans ce cas, c'est le montant du prêt qui doit être revu, pas son échéancier. Rappelez-vous que le congé augmente le total des intérêts payés par l'emprunteur.

#### 6. Appliquer les frais prévus

Le paramètre `FRAIS_OUVERTURE` porte les frais d'ouverture et d'analyse. Précisez s'ils sont capitalisables au prêt ou exigibles au décaissement, parce que la réponse change le montant décaissé et donc le montant disponible pour le projet. Les frais capitalisés augmentent aussi la base sur laquelle courent les intérêts.

#### 7. Recalculer la couverture avec la tarification finale

C'est l'étape que l'on saute quand le temps manque, et c'est celle qui produit les erreurs les plus embarrassantes en séance. Le ratio de couverture calculé en F3 l'a été avec une hypothèse de taux ; si le taux final diffère, le ratio change. Reprenez le calcul avec le taux, le terme, l'amortissement et le congé effectivement recommandés, et vérifiez que le résultat respecte toujours le paramètre `RCD_MINIMAL`. Le contrôle C08 rend cette vérification obligatoire et bloquante.

### Sorties

- Taux proposé et décomposition entre taux de référence, prime de risque et ajustements
- Terme, amortissement et congé de capital recommandés
- Frais applicables et modalité de perception
- Confirmation écrite que le ratio de couverture demeure conforme après tarification

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Fixer le taux avant d'avoir coté le risque | Prix décidé puis justifié après coup, traitement inéquitable entre promoteurs | La séquence PL1 place P2 après F4 ; la cote doit exister et être datée |
| Amortir au-delà de la vie utile de l'actif | L'entreprise paie encore un actif à remplacer, et la garantie s'est évaporée | Comparer l'amortissement proposé à la durée de vie utile documentée |
| Accorder un congé de capital non justifié par les flux | Report d'un problème de capacité de remboursement, coût d'intérêt accru | Le congé doit s'appuyer sur la courbe de trésorerie de F3, pièce à l'appui |
| Ne pas revalider la couverture après tarification | Ratio présenté au comité qui ne correspond pas à la recommandation | Contrôle C08, bloquant |
| Négocier la prime hors grille | La grille perd sa fonction, le précédent devient la règle | Toute correction passe par une révision motivée de la cote en F4 |
| Omettre de préciser la date de fixation du taux | Litige au décaissement quand les taux ont bougé | L'offre précise si le taux est fixé à l'acceptation ou au décaissement |

## P3 — conformite-politique

**Objectif.** Vérifier ligne par ligne que le montage projeté respecte la politique d'investissement en vigueur avant présentation au comité.

**Entrées requises.**

- Montage financier complet produit en F2
- Tarification recommandée produite en P2
- Politique d'investissement en vigueur, dans sa version applicable à la date de la demande
- État des engagements existants envers l'entreprise et envers toutes les entités de son groupe
- État du portefeuille à la date de la demande, pour les limites de concentration

### Méthode

#### 1. Vérifier les plafonds par entreprise et par groupe lié

Les paramètres `PLAFOND_ENTREPRISE_FLI`, `PLAFOND_ENTREPRISE_FLS` et `PLAFOND_GROUPE_LIE` portent les montants maximaux. Deux vérifications distinctes sont nécessaires. La première porte sur le dossier courant. La seconde porte sur le cumul : le plafond s'applique-t-il par dossier ou par entreprise cumulée dans le temps, et sur quelle période ? Recensez les engagements existants, y compris les prêts en cours de remboursement et les engagements autorisés mais non encore décaissés. Pour le groupe lié, la définition du lien se lit dans la politique et repose généralement sur le contrôle, non sur la simple présence d'un actionnaire commun.

#### 2. Vérifier le ratio de participation entre les fonds

Le paramètre `RATIO_FLI_FLS` détermine si les fonds doivent intervenir en parts fixes ou si la répartition est discrétionnaire. Ce paramètre découle en partie de l'entente avec le bailleur du fonds de solidarité et peut différer de la politique locale : en cas de divergence apparente, c'est l'entente la plus contraignante qui s'applique, et la divergence elle-même mérite d'être signalée à la direction.

#### 3. Valider la mise de fonds minimale et sa forme

Les paramètres `MISE_FONDS_MIN` et `FORMES_MISE_FONDS` portent l'exigence et les formes reconnues. La question de forme est celle qui fait le plus souvent basculer un dossier : une subvention est rarement reconnue comme mise de fonds, un apport en nature exige une évaluation indépendante, et un bilan de départ constitué de biens déjà détenus n'a pas la même valeur d'engagement qu'un apport en argent frais. Vérifiez également la provenance des fonds : une mise de fonds elle-même empruntée personnellement par le promoteur change son profil de risque, puisqu'elle crée un service de dette hors du bilan de l'entreprise.

#### 4. Contrôler les limites de concentration

Les paramètres `CONCENTRATION_SECTEUR` et `CONCENTRATION_DOSSIER` portent les limites du portefeuille. Ces contrôles se font contre l'état du portefeuille à la date de la demande, jamais contre un état historique ou contre le dernier rapport trimestriel s'il n'est plus à jour. La limite par dossier en pourcentage du fonds est la contrainte la plus souvent oubliée pour un gros dossier dans un fonds de taille modeste ; elle peut rendre non conforme un dossier par ailleurs excellent, et il vaut mieux le découvrir à l'analyse qu'en séance.

#### 5. Vérifier le niveau d'autorisation requis

Le paramètre `SEUIL_DELEGATION` détermine l'instance décisionnelle. Ne présumez jamais d'une délégation : vérifiez à la fois la politique et les résolutions en vigueur, parce qu'une délégation peut avoir été modifiée par résolution sans que la politique ait été rééditée. Le cumul compte également ici : un nouveau prêt modeste à une entreprise déjà financée peut faire franchir le seuil au niveau du groupe.

#### 6. Contrôler les règles de garanties et de cautionnement

Le paramètre `GARANTIES_EXIGEES` porte les exigences. Vérifiez que les garanties proposées existent réellement et ne sont pas déjà grevées : une hypothèque mobilière de premier rang promise sur un équipement déjà donné en garantie à une autre institution n'est pas une garantie. Le cautionnement personnel appelle une attention particulière quant à son étendue, à sa durée et au nombre de cautions.

#### 7. Documenter toute dérogation demandée

Une dérogation n'est pas une faute ; une dérogation implicite en est une. Lorsque le montage s'écarte de la politique, la note doit le nommer explicitement, indiquer la disposition concernée, l'ampleur de l'écart, le motif et les mesures compensatoires. Le contrôle C25 rend cette documentation bloquante. Un comité qui découvre une dérogation en séance perd confiance dans l'ensemble du dossier, y compris dans ses parties irréprochables.

### Sorties

- Grille de conformité point par point, chaque ligne portant son statut et sa référence
- Liste des dérogations demandées, avec motif et mesures compensatoires
- Niveau d'autorisation requis et instance visée
- Version de la politique utilisée pour la vérification

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Citer un plafond de mémoire | Dossier présenté comme conforme alors qu'il ne l'est pas | Contrôle C18 : les paramètres proviennent du document en vigueur |
| Oublier le cumul avec les engagements existants du groupe | Dépassement de plafond découvert après la décision | Recenser les engagements de toutes les entités liées avant de conclure |
| Présumer d'une délégation d'autorisation | Décision rendue par la mauvaise instance, validité de la décision fragilisée | Vérifier la politique et les résolutions en vigueur, les deux |
| Contrôler la concentration contre un état de portefeuille périmé | Limite franchie sans que personne ne le voie | Utiliser l'état du portefeuille à la date de la demande |
| Passer une dérogation sous silence | Perte de confiance du comité dans l'ensemble du dossier | Contrôle C25, bloquant |
| Accepter une garantie déjà grevée | Sûreté sans valeur au moment où elle servirait | Vérifier les inscriptions au registre des droits personnels et réels mobiliers |

## P4 — preparation-CIC

**Objectif.** Produire le dossier complet et défendable soumis au comité d'investissement commun, incluant la recommandation et ses conditions.

**Entrées requises.**

- Ensemble des livrables amont : F1 à F4 et P1 à P3, tous datés et versionnés
- Pièces justificatives du dossier, avec leur registre
- Profil des promoteurs et de l'équipe de direction
- Échéancier du projet et date de décaissement souhaitée

### Méthode

#### 1. Rédiger selon la structure normalisée

La note suit toujours le même ordre : entreprise, promoteurs, projet, montage, analyse financière, risques, recommandation. Cette constance n'est pas une contrainte bureaucratique — elle permet aux membres du comité de trouver l'information au même endroit d'un dossier à l'autre et de comparer des dossiers entre eux. Un comité qui doit chercher lit moins bien.

#### 2. Placer la recommandation et le montant en tête

Le lecteur doit connaître la demande dès les premières lignes : quel montant, de quel fonds, à quelles conditions principales, pour quel projet. Le raisonnement vient ensuite. Enterrer la recommandation en fin de note force chaque membre à lire dix pages avant de savoir de quoi il est question, et c'est le meilleur moyen d'obtenir une discussion désordonnée. Le contrôle C23 rend cette exigence bloquante.

#### 3. Rattacher chaque chiffre à sa source

Tout chiffre présenté dans la note existe ailleurs dans le dossier, dans une pièce identifiable. Le module Q3 produit le registre des sources qui établit ce lien. Un chiffre qui n'existe que dans la note est un chiffre orphelin : soit il provient d'un calcul non documenté, soit il a été modifié quelque part sans que l'origine suive. Les deux cas sont bloquants.

#### 4. Formuler les conditions préalables de façon vérifiable

Une condition de décaissement doit nommer trois choses : la pièce attendue, la personne ou la fonction qui constatera sa réalisation, et le moment où cette constatation doit intervenir. « Obtenir une preuve de mise de fonds satisfaisante » n'est pas une condition, parce que personne ne sait ce qui est satisfaisant ni qui en juge. « Recevoir un relevé bancaire au nom de l'entreprise démontrant un dépôt d'au moins X dollars, constaté par le conseiller au dossier avant le décaissement » en est une. Le contrôle C24 rend cette précision bloquante.

#### 5. Rédiger les engagements pour la durée du prêt

Distinguez les engagements de faire — transmettre les états financiers annuels dans un délai donné, maintenir une couverture d'assurance, informer de tout changement de contrôle — et les engagements de ne pas faire — ne pas consentir de nouvelle sûreté sans autorisation, ne pas verser de dividende au-delà d'un seuil, ne pas disposer des actifs financés. Chaque engagement doit être vérifiable au suivi, faute de quoi il ne sera jamais vérifié.

#### 6. Préparer la résolution et déclarer les pièces manquantes

Le projet de résolution reprend le montant, le fonds, les modalités et les conditions dans un texte que le comité peut adopter tel quel. La liste des pièces manquantes se déclare ouvertement : un comité peut décider avec des pièces manquantes s'il sait lesquelles et si elles sont converties en conditions, mais il ne peut pas décider s'il croit le dossier complet alors qu'il ne l'est pas.

#### 7. Soumettre au préflight avant dépôt

Le dossier passe par Q1, Q2, Q3 puis Q4 avant l'envoi de l'ordre du jour. Le préflight porte sur la version exactement destinée au dépôt : contrôler une version puis en déposer une autre annule la valeur du contrôle, ce que vérifie le contrôle C07.

### Sorties

- Note d'investissement complète, structurée et datée
- Conditions préalables au décaissement, vérifiables et datables
- Engagements de faire et de ne pas faire
- Projet de résolution
- Liste déclarée des pièces manquantes
- Registre de préflight avec statut de sortie

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Conditions formulées de façon invérifiable | Conditions jamais constatées, décaissement sur un dossier incomplet | Contrôle C24, bloquant : pièce, responsable et moment nommés |
| Recommandation noyée en fin de note | Discussion désordonnée en séance, décision mal cadrée | Contrôle C23, bloquant |
| Chiffres de la note divergents des annexes | Perte de crédibilité de l'ensemble du dossier | Contrôle C04, bloquant |
| Pièces manquantes non déclarées | Le comité décide en croyant le dossier complet | Liste des pièces manquantes obligatoire dans la note |
| Analyser encore à l'étape de rédaction | Analyse improvisée, non contrôlée, insérée dans un livrable final | Toute analyse nouvelle renvoie au module amont concerné |
| Contrôler une version et en déposer une autre | Le registre de contrôle ne prouve rien | Contrôle C07, bloquant |

## Le mur des paramètres

Ce domaine repose sur vingt-deux paramètres de politique recensés dans `data/parametres-politique.csv`. À la livraison du système, tous portent le statut `A_VALIDER` et la valeur `À_RENSEIGNER`. C'est délibéré : le système ne prétend pas connaître la politique d'investissement de l'organisation, et un système qui inventerait ces valeurs serait plus dangereux qu'utile.

La mise en service du domaine 02 consiste donc à ouvrir la politique en vigueur et à remplir ce fichier, paramètre par paramètre, en renseignant quatre colonnes : la valeur, la source précise, la date de validation et le statut, qui passe alors à `VALIDE`.

Tant qu'un paramètre demeure `A_VALIDER`, trois mécanismes se déclenchent automatiquement. La commande `route` signale les paramètres non validés que la séquence recommandée va mobiliser. La commande `preflight` les liste dans sa section dédiée. Le contrôle C18 rend bloquante la présentation de tout chiffre qui en dépend sans signalement explicite au lecteur.

Cette discipline a un coût réel au démarrage et une valeur qui apparaît à la première mise à jour de la politique : il suffit alors de mettre à jour le fichier et de repasser les dossiers en cours au contrôle, plutôt que de chercher dans les notes déjà rédigées lesquelles reposaient sur l'ancienne version.

## Conditions préalables au décaissement : formulation

Les conditions sont la partie du dossier qui survit le plus longtemps : elles seront relues par une autre personne, souvent des mois plus tard, au moment du décaissement. Elles doivent donc se suffire à elles-mêmes.

Une condition bien formulée répond à quatre questions. Quelle pièce est attendue, décrite assez précisément pour être reconnue sans ambiguïté. Quel seuil ou quel contenu cette pièce doit démontrer. Qui constate sa réalisation. À quel moment la constatation doit intervenir — avant le décaissement, avant le premier versement, dans les trente jours suivants.

Les familles de conditions qui reviennent dans la plupart des dossiers sont la confirmation des autres sources de financement, la preuve de mise de fonds, les inscriptions de sûretés, les couvertures d'assurance avec l'organisme désigné comme créancier, les permis et autorisations, les baux et titres de propriété, et les documents corporatifs incluant les résolutions d'emprunt.

Les conditions se distinguent des engagements : la condition se réalise une fois, avant le décaissement, et se referme ; l'engagement dure toute la vie du prêt et se vérifie au suivi. Confondre les deux produit des dossiers où l'on attend indéfiniment la réalisation d'une condition qui était en réalité un engagement continu.

## Passage au domaine suivant

Le domaine 02 remet à 05-PRODUCTION une note d'investissement complète et validée, à partir de laquelle R2 produit le sommaire exécutif et R3 le support de présentation. La production ne réanalyse rien : si un chiffre nouveau apparaît à l'étape de mise en forme, il doit repasser par Q1 et Q3.

Il remet à 06-QA l'ensemble du dossier pour la chaîne complète Q1, Q3, Q2 puis Q4. Le passage est conditionnel : un dossier dont le verdict d'admissibilité n'est pas versé, dont la grille de conformité est incomplète, ou dont les conditions ne sont pas formulées de façon vérifiable ne franchit pas le préflight.

Il remet enfin au suivi post-décision les engagements de faire et de ne pas faire, qui deviennent la matière du suivi de portefeuille. Un engagement qui n'est pas repris dans l'outil de suivi au moment du décaissement ne sera jamais vérifié.
