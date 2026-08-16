# 03 — ÉVALUATION

Le domaine 03 produit une opinion de valeur défendable sur une entreprise privée québécoise : un BAIIA normalisé documenté ligne par ligne, une valeur d'entreprise établie par deux approches indépendantes, un passage explicite à la valeur des actions, et un rapport d'évaluation qui déclare sa date, sa portée et ses hypothèses limitatives. Il sert les contextes où la valeur devient un intrant de décision et non un exercice théorique : transfert d'entreprise, relève familiale ou interne, acquisition financée par prêt, prise de participation. La règle d'or est que la normalisation gouverne tout le reste : une erreur dans le BAIIA normalisé se multiplie mécaniquement par le multiple en E2 et se capitalise à perpétuité en E3. Son corollaire est que l'on conclut sur une fourchette rattachée à une date d'évaluation précise, jamais sur un point présenté au dollar près.

## Vue d'ensemble

| Module | ID | Produit | Dépend de |
|---|---|---|---|
| normalisation-BAIIA | E1 | Tableau de normalisation ligne par ligne avec source, BAIIA normalisé par exercice, BAIIA normalisé retenu et sa justification | F1 (analyse financière) |
| multiples | E2 | Fourchette de multiples justifiée, valeur d'entreprise, passage détaillé à la valeur des actions, fourchette de valeur des actions | E1 |
| DCF | E3 | Valeur d'entreprise actualisée, décomposition du taux d'actualisation, table de sensibilité, poids de la valeur terminale, réconciliation avec l'approche de marché | E1, E2 |
| rapport-evaluation | E4 | Rapport structuré, fourchette de valeur conclue, hypothèses limitatives, annexes de calcul | E1, E2, E3 |

La chaîne de dépendance et les barrières de contrôle applicables se lisent ainsi.

| Module | Amont | Aval | Barrières QA |
|---|---|---|---|
| E1 | F1 | E2, E3, E4 | Q1, Q3 |
| E2 | E1 | E3, E4 | Q1, Q3 |
| E3 | E1, E2 | E4 | Q1, Q3 |
| E4 | E1, E2, E3 | R2, R3 | Q1, Q2, Q3, Q4 |

L'ordre d'exécution n'est pas une convention de présentation : c'est une chaîne de dépendance arithmétique. E1 produit la mesure de rentabilité récurrente et transférable sur laquelle E2 applique un multiple et dont E3 tire le point de départ de ses flux de trésorerie disponibles ; tout ajustement de normalisation modifié en cours de route oblige à reprendre E2 et E3, sans exception. Le point de contrôle humain se situe donc à la sortie de E1 : le BAIIA normalisé retenu doit être validé et signé avant qu'un seul multiple ne soit appliqué. E2 précède E3 parce que la fourchette de multiples observée sur le marché fournit le test de vraisemblance du multiple de sortie implicite du modèle d'actualisation, et non l'inverse. E4 ne calcule rien de neuf : il réconcilie, pondère, déclare la portée et ferme le dossier. Les modules E1 à E3 passent les barrières Q1 (contrôle des calculs) et Q3 (validation des sources) ; E4 passe en plus Q2 (nomenclature) et Q4 (préflight final) parce qu'il constitue le livrable remis.

## E1 — normalisation-BAIIA

**Objectif.** Reconstituer le BAIIA réellement récurrent et transférable de l'entreprise, c'est-à-dire la rentabilité qu'un acquéreur raisonnable pourrait s'attendre à retrouver après la transaction, indépendamment des choix de rémunération et des arrangements privés du propriétaire actuel. Ce BAIIA normalisé est la base de toute évaluation par les multiples et le point de départ des flux de trésorerie disponibles du modèle d'actualisation.

**Entrées requises.**

- États financiers de 3 à 5 exercices, avec mention du niveau d'assurance de chacun (audit, mission d'examen, avis au lecteur, compilation interne).
- Grand livre ou détail des comptes de charges sensibles : rémunération, honoraires professionnels, déplacements, représentation, véhicules, loyers, assurances, entretien.
- Contrats de location et ententes de services avec des parties liées, y compris les baux immobiliers détenus par une société de gestion du propriétaire.
- Détail complet de la rémunération des actionnaires : salaires, primes, dividendes, avantages imposables, cotisations, régimes.
- Liste des éléments non récurrents identifiés par la direction, avec les pièces qui les appuient.
- Organigramme de l'actionnariat et des sociétés liées, et convention entre actionnaires si elle existe.
- Balance de vérification récente et états intérimaires pour vérifier la coupure et la continuité des ajustements.

### Méthode

#### 1. Partir du bénéfice avant impôts publié et remonter au BAIIA publié

On ne commence jamais la normalisation à partir d'un chiffre reconstitué : on part du bénéfice avant impôts tel que publié aux états financiers, puis on remonte au BAIIA publié en réintégrant les intérêts et frais financiers, l'amortissement des immobilisations et l'amortissement des actifs incorporels. Chaque ligne de cette remontée doit se rattacher à un poste identifiable de l'état des résultats ou d'une note aux états financiers, de sorte qu'un lecteur externe puisse refaire le pont en sens inverse.

On isole tout de suite les charges financières incluses dans d'autres postes, notamment les frais de crédit-bail comptabilisés en frais d'exploitation et les frais bancaires liés à l'affacturage. Lorsque plusieurs entités du groupe participent à l'exploitation, on établit le périmètre exact évalué avant d'additionner quoi que ce soit, et on documente les transactions intersociétés à éliminer. Le résultat de cette étape est un BAIIA publié par exercice, sans aucun jugement encore appliqué, qui servira de ligne de départ vérifiable du tableau de normalisation.

#### 2. Normaliser la rémunération des actionnaires actifs au salaire de marché du poste

Dans une PME privée, la rémunération des actionnaires actifs reflète une planification fiscale et non le coût de la fonction : elle doit être remplacée par le coût de marché du poste réellement occupé. On décrit d'abord la fonction exercée (direction générale, direction des ventes, supervision de production) et le temps réellement consacré, puis on retient une échelle salariale appuyée par une source documentée au dossier : enquête de rémunération sectorielle, échelle publiée, offre d'emploi comparable, avis d'un cabinet spécialisé.

L'ajustement porte sur la rémunération globale, charges sociales et avantages compris, et non sur le seul salaire de base. Le même traitement s'applique en sens inverse aux membres de la famille rémunérés sans contribution réelle à l'exploitation : leur rémunération est retirée. Il faut aussi vérifier si le repreneur devra embaucher pour remplacer une fonction que le cédant assumait gratuitement ou en surplus ; ce coût additionnel est une charge normative à ajouter, pas un ajustement à la hausse à omettre. Un ajustement de rémunération sans source citée est indéfendable et sera rejeté au contrôle Q3.

#### 3. Ramener les loyers avec parties liées à la valeur locative de marché

Lorsque l'immeuble d'exploitation appartient au propriétaire ou à une société liée, le loyer inscrit aux résultats est un choix de répartition du bénéfice entre deux poches du même actionnaire. On le remplace par la valeur locative de marché, appuyée par une source : rapport d'un évaluateur agréé, baux comparables du secteur, avis écrit d'un courtier immobilier commercial, rôle d'évaluation avec méthode de conversion déclarée. On précise la structure du bail normalisé (net, semi-brut, brut) parce que la charge normative diffère selon que les taxes, les assurances et l'entretien sont ou non à la charge du locataire.

Le sens de l'ajustement doit être appliqué avec rigueur : un loyer inférieur au marché gonfle artificiellement le BAIIA et exige un ajustement à la baisse, ce qui est le cas le plus souvent passé sous silence. Il faut également déclarer si l'immeuble est inclus ou exclu du périmètre de la transaction envisagée, puisque cela change à la fois la charge normative et la nature des actifs hors exploitation traités en E2. Les ententes de services avec parties liées — gestion, comptabilité, transport — se traitent selon la même logique.

#### 4. Retirer les dépenses personnelles et non liées à l'exploitation

On extrait du grand livre les charges qui financent le train de vie du propriétaire plutôt que l'exploitation : véhicules personnels, voyages sans lien d'affaires, cotisations à des clubs, honoraires de planification patrimoniale, assurances vie détenues au bénéfice de l'actionnaire, dépenses de résidence. Chaque retrait doit être appuyé par une pièce ou par un extrait de grand livre annexé, et non par une déclaration verbale du propriétaire.

La prudence commande de ne retirer que la portion clairement personnelle d'une charge mixte : un véhicule utilisé à la fois pour la livraison et pour l'usage privé se répartit selon un pourcentage justifié, jamais retiré en totalité. Il faut aussi vérifier la symétrie : un revenu personnel encaissé dans l'entreprise, comme un loyer résidentiel ou une commission d'un tiers, doit être retiré au même titre. Ces ajustements sont les plus contestés en négociation parce qu'ils augmentent la valeur ; ils doivent donc être les mieux documentés du tableau. Un ajustement dont la pièce justificative n'est pas au dossier ne figure pas au BAIIA normalisé retenu, il figure au plus dans une note de sensibilité.

#### 5. Retirer les éléments non récurrents des deux côtés (gains et pertes)

La normalisation des éléments non récurrents n'est légitime que si elle s'applique dans les deux sens : on retire aussi bien un gain exceptionnel sur disposition d'actif, une indemnité d'assurance ou une aide gouvernementale ponctuelle qu'une perte sur créance exceptionnelle, un litige réglé ou un coût de démarrage d'usine. Le test à appliquer est celui de la répétition attendue : un élément est non récurrent s'il est improbable qu'il se reproduise dans un horizon prévisible, et non simplement parce qu'il est inhabituel ou qu'il déplaît.

Les mauvaises créances, les réparations d'équipement et les frais de recrutement sont récurrents par nature dans une PME, même si leur montant varie d'un exercice à l'autre ; on les lisse plutôt que de les retirer. On documente pour chaque élément le montant, l'exercice touché, le compte visé, la pièce d'appui et le motif du caractère non récurrent. Les aides publiques reçues pendant une période exceptionnelle exigent une attention particulière : elles doivent être retirées du BAIIA normalisé si elles ne se reproduiront pas, et leur retrait doit être signalé explicitement dans la note de synthèse parce qu'il modifie sensiblement la trajectoire apparente.

#### 6. Corriger les changements de méthode comptable et les erreurs de coupure

Trois à cinq exercices ne sont comparables que si les méthodes le sont : on vérifie la constance de la méthode d'évaluation des stocks, du seuil de capitalisation des immobilisations, du traitement des contrats de location, de la comptabilisation des produits sur contrats de longue durée et de la ventilation entre coût des ventes et frais généraux. Tout changement repéré est retraité rétrospectivement sur les exercices antérieurs, ou à défaut, signalé comme limite de comparabilité dans le tableau.

Les erreurs de coupure sont fréquentes dans les dossiers à faible niveau d'assurance : produits comptabilisés à la facturation plutôt qu'à la livraison, charges reportées à l'exercice suivant, stocks non ajustés au dénombrement, travaux en cours absents du bilan. Un exercice de durée inégale — période de transition à la suite d'un changement de fin d'exercice — n'est jamais comparé tel quel : il est annualisé avec mention explicite, ou écarté. On note aussi le niveau d'assurance de chaque exercice, puisqu'un exercice compilé sans assurance ne porte pas le même poids qu'un exercice audité au moment de la pondération.

#### 7. Pondérer les exercices selon leur représentativité et documenter chaque ajustement avec sa source

Le BAIIA normalisé retenu n'est pas une moyenne automatique : c'est un choix motivé entre le dernier exercice, une moyenne simple, une moyenne pondérée en faveur des exercices récents ou une année normative reconstruite. La justification s'appuie sur des faits vérifiables : stabilité ou volatilité du chiffre d'affaires, changement structurel de la clientèle, ajout de capacité de production, perte d'un contrat important, cycle sectoriel. Lorsqu'un exercice est écarté ou fortement décoté, le motif est écrit dans le tableau, jamais laissé implicite.

Le tableau de normalisation final présente une ligne par ajustement, avec l'exercice touché, le montant, le compte visé, la source d'appui, le nom de la personne qui a fourni la pièce et la date. On note pour mémoire que les ajustements de normalisation sont établis avant impôts : leur effet fiscal ne se répercute pas sur le BAIIA lui-même, mais il se répercute sur les flux de trésorerie disponibles calculés en E3 et sur la charge d'impôts en trésorerie utilisée en aval. Le livrable de E1 se termine par une phrase de conclusion qui nomme le BAIIA normalisé retenu, la méthode de pondération et les deux ou trois ajustements les plus déterminants.

### Sorties

- Tableau de normalisation ligne par ligne, avec pour chaque ajustement l'exercice, le montant, le compte, la source d'appui et son statut de vérification.
- BAIIA normalisé par exercice sur l'ensemble de la période analysée, réconcilié au BAIIA publié.
- BAIIA normalisé retenu, sa méthode de pondération et sa justification écrite.
- Liste des ajustements écartés faute de pièce, conservée pour la sensibilité et la négociation.
- Note sur les limites de comparabilité entre exercices et sur le niveau d'assurance de chacun.

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Normaliser à la hausse seulement | Le BAIIA normalisé devient un plaidoyer de vendeur ; la valeur est surestimée et le rapport perd sa crédibilité dès la première contre-analyse | Exiger un décompte des ajustements par sens ; tout tableau ne comportant aucun ajustement à la baisse est retourné pour révision |
| Utiliser un salaire de marché non appuyé par une source | L'ajustement le plus lourd du tableau repose sur une opinion ; il est écarté en négociation et la valeur s'effondre | Q3 : chaque ajustement de rémunération porte une source nommée et datée, sinon il est retiré du BAIIA retenu |
| Traiter un élément récurrent comme non récurrent | La rentabilité récurrente est gonflée et l'erreur est multipliée par le multiple en E2, puis capitalisée à perpétuité en E3 | Appliquer le test de répétition attendue et vérifier la présence du même type d'élément dans les autres exercices |
| Oublier l'effet fiscal des ajustements | Les flux de trésorerie disponibles de E3 sont établis sur une charge d'impôts incohérente avec le BAIIA normalisé | Réconcilier explicitement la charge d'impôts en trésorerie avec le BAIIA normalisé avant de transmettre à E3 |
| Pondérer les exercices sans justification | La conclusion de valeur devient arbitraire et impossible à défendre devant un tiers | Écrire le motif de pondération dans le tableau et le rattacher à un fait vérifiable du dossier |
| Évaluer un périmètre flou entre entités liées | Double comptage de produits ou de charges entre la société d'exploitation et la société de gestion | Déclarer le périmètre évalué en tête de tableau et éliminer les opérations intersociétés avant normalisation |

### Formules mobilisées

| Clé | Formule | Note |
|---|---|---|
| BAIIA_NORM | BAIIA normalisé = BAIIA publié ± ajustements de normalisation | Ajustements typiques : rémunération des actionnaires ramenée au marché ; loyer avec partie liée ramené au marché ; éléments non récurrents retirés ; dépenses personnelles retirées. Mesure de la rentabilité récurrente et transférable, indépendante des choix de rémunération du propriétaire actuel. Aucun seuil (sans objet). Pièges : normaliser uniquement à la hausse ; retirer des éléments récurrents en les qualifiant d'exceptionnels ; oublier de documenter la source du salaire de marché. |

## E2 — multiples

**Objectif.** Établir la valeur par l'approche de marché en appliquant un multiple justifié au BAIIA normalisé retenu, puis passer rigoureusement de la valeur d'entreprise à la valeur des actions. Cette approche fournit la lecture que fera le marché de l'entreprise et sert de test de vraisemblance à l'approche par actualisation.

**Entrées requises.**

- BAIIA normalisé retenu de E1, avec sa justification et son tableau d'appui.
- Données sectorielles et transactions comparables, chacune avec sa source, sa date et son périmètre.
- Dette nette à la date d'évaluation : dette portant intérêt détaillée par prêteur, encaisse et encaisse excédentaire distinguées.
- Fonds de roulement normatif du secteur ou de l'entreprise, et fonds de roulement réel à la date d'évaluation.
- Liste des actifs et passifs hors exploitation, avec leur valeur et la pièce qui l'appuie.
- Portrait de la concentration de la clientèle, de la dépendance au propriétaire et de la profondeur de l'équipe de direction.

### Méthode

#### 1. Choisir la base de multiple appropriée et justifier le choix

Le multiple s'applique à une base de rentabilité, et le choix de cette base n'est pas neutre. Le multiple du BAIIA est le repère dominant pour une PME parce qu'il neutralise la structure de financement et les politiques d'amortissement, mais il devient trompeur pour une entreprise à forte intensité capitalistique dont les investissements de maintien sont élevés : dans ce cas, le multiple du BAII rend mieux compte de la charge réelle du capital. Le multiple des revenus n'est retenu que lorsque la rentabilité est nulle, négative ou trop volatile pour être significative, et il doit alors être présenté comme un repère grossier et non comme une conclusion.

La base retenue doit être cohérente avec celle qui a servi à construire les comparables : appliquer un multiple observé sur des transactions établies en fonction du BAIIA à un BAII produit une erreur de plusieurs ordres de grandeur. On déclare explicitement la base retenue, le motif du choix et la raison pour laquelle les autres bases ont été écartées.

#### 2. Constituer l'échantillon de comparables et documenter chaque source

Chaque multiple utilisé doit provenir d'une source identifiable et datée versée au dossier : base de données de transactions privées, rapport sectoriel publié, transaction récente dans le même secteur dont les modalités sont connues, ou avis écrit d'un professionnel de l'évaluation. Un multiple avancé de mémoire, entendu en réunion ou repris d'un dossier antérieur sans revalidation n'a aucune valeur probante et doit être traité comme un chiffre orphelin par Q3.

Pour chaque comparable retenu, on consigne la date de la transaction, la taille de l'entreprise visée, son secteur précis, sa situation géographique, la nature de la transaction (majoritaire ou minoritaire, actions ou actifs) et le périmètre inclus dans le prix. Les transactions portant sur des sociétés cotées ou sur des entreprises d'une tout autre échelle sont conservées à titre de borne supérieure seulement, avec la mention de leur non-comparabilité directe. On documente aussi les comparables écartés et le motif de leur exclusion, parce que la sélection d'un échantillon est en soi un jugement susceptible d'être contesté. La règle de conduite est simple : le rapport ne contient aucun multiple dont on ne peut pas nommer la source au dossier.

#### 3. Retenir une fourchette de multiples plutôt qu'un point

Un multiple ponctuel donne une fausse impression de précision et masque la dispersion réelle des transactions observées. On retient une fourchette bornée par des observations documentées, puis on justifie le positionnement de l'entreprise à l'intérieur de cette fourchette au moyen de critères qualitatifs vérifiables : croissance, marge par rapport au secteur, récurrence des revenus, qualité du carnet de commandes, profondeur de l'équipe, état des actifs, position concurrentielle. Le positionnement s'écrit sous forme d'argumentaire, pas sous forme de pondération arbitraire.

Lorsque la dispersion de l'échantillon est très large, il faut se demander si l'échantillon mélange des réalités différentes et resserrer les critères de sélection plutôt qu'élargir la conclusion. La fourchette retenue et son point de positionnement sont énoncés avant tout calcul, de sorte que le résultat ne soit pas construit à rebours d'une valeur souhaitée par une partie.

#### 4. Ajuster pour la taille, la liquidité, la dépendance au propriétaire et la concentration de la clientèle

Une PME privée ne se transige pas au même multiple qu'une entreprise plus grande ou cotée : les écarts s'expliquent par la taille, l'absence de marché liquide pour les titres, la profondeur limitée de la direction et la concentration des risques. Chaque décote ou prime appliquée doit être nommée, motivée et appuyée par une source ou par un raisonnement écrit rattaché aux faits du dossier ; aucune décote ne s'applique par convention ni par habitude. La dépendance au propriétaire est l'ajustement le plus déterminant en contexte de transfert et de relève : si les relations clients, les compétences techniques ou les décisions d'approvisionnement reposent sur une seule personne qui quittera, une part de la rentabilité normalisée n'est tout simplement pas transférable. La concentration de la clientèle s'apprécie avec la part du premier client et des cinq premiers clients, l'ancienneté des relations et l'existence de contrats écrits.

On évite le double comptage : un facteur de risque déjà pris en compte en réduisant le multiple retenu à l'intérieur de la fourchette ne doit pas être facturé une deuxième fois sous forme de décote distincte. Les ajustements retenus sont présentés dans un tableau qui montre le passage du multiple de départ au multiple appliqué.

#### 5. Calculer la valeur d'entreprise sur la fourchette

La valeur d'entreprise s'obtient en appliquant la fourchette de multiples au BAIIA normalisé retenu, ce qui donne une borne inférieure et une borne supérieure, jamais une seule valeur. On présente le calcul de façon transparente pour qu'un tiers puisse le refaire : BAIIA normalisé retenu, multiple bas, multiple haut, valeur d'entreprise correspondante. Si l'on retient plusieurs bases de BAIIA normalisé — dernier exercice et moyenne pondérée, par exemple — on présente les combinaisons dans une grille plutôt que d'en choisir une sans le dire.

À cette étape, la valeur obtenue est la valeur de l'ensemble de l'exploitation, avant toute considération de financement : c'est ce que vaut l'entreprise, pas ce que reçoivent ses actionnaires. Cette distinction doit être rappelée explicitement dans le texte, parce que sa confusion est la source d'erreur la plus fréquente en évaluation de PME.

#### 6. Déduire la dette nette et ajuster l'écart de fonds de roulement par rapport au normatif

Le passage de la valeur d'entreprise à la valeur des actions commence par la déduction de la dette nette à la date d'évaluation : dette bancaire, prêts des fonds locaux, crédit-bail, avances portant intérêt, moins l'encaisse excédentaire. La qualification de l'encaisse est décisive : seule la portion qui excède les besoins d'exploitation est excédentaire, le reste finance le cycle et n'est pas distribuable. On traite explicitement les avances d'actionnaires selon qu'elles sont ou non postposées et selon qu'elles seront remboursées ou converties à la clôture.

Vient ensuite l'écart de fonds de roulement : on compare le fonds de roulement réel à la date d'évaluation au fonds de roulement normatif nécessaire pour faire tourner l'entreprise à son niveau d'activité, et l'écart s'ajoute ou se retranche. Le fonds de roulement normatif s'établit à partir du cycle de conversion observé sur plusieurs exercices et non à partir d'un solde de fin d'exercice choisi au creux du cycle, particulièrement en secteur saisonnier. Cet ajustement est régulièrement oublié dans les dossiers de PME et il peut représenter une part significative de l'écart entre le prix annoncé et le prix réellement encaissé.

#### 7. Ajouter les actifs hors exploitation et conclure sur une fourchette de valeur des actions

On ajoute enfin les actifs qui ne servent pas à l'exploitation et qui n'ont donc pas contribué au BAIIA normalisé : placements, immeuble excédentaire, terrain non utilisé, véhicules récréatifs, polices d'assurance ayant une valeur de rachat, créances non liées à l'exploitation. Chaque actif hors exploitation est évalué séparément, à sa valeur nette de l'impôt latent le cas échéant, et appuyé par une pièce. Les passifs hors exploitation subissent le même traitement en sens inverse.

La conclusion de E2 est une fourchette de valeur des actions, présentée avec le tableau de passage complet allant de la valeur d'entreprise à la valeur des actions, ligne par ligne. On rappelle en note que cette fourchette suppose une transaction en actions ; une transaction en actifs modifie le périmètre, la fiscalité et souvent le prix, et exige un traitement distinct. La fourchette et le tableau de passage sont transmis à E3 pour la réconciliation et à E4 pour la pondération finale.

### Sorties

- Fourchette de multiples justifiée, avec le tableau des comparables retenus et leur source datée.
- Tableau du passage du multiple de départ au multiple appliqué, décote par décote et prime par prime.
- Valeur d'entreprise calculée aux bornes de la fourchette.
- Tableau de passage détaillé de la valeur d'entreprise à la valeur des actions.
- Fourchette de valeur des actions selon l'approche de marché.
- Liste des actifs et passifs hors exploitation évalués séparément avec leurs pièces d'appui.

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Appliquer un multiple de grandes entreprises à une PME | Surévaluation systématique ; la conclusion ne résiste pas à la première offre réelle du marché | Documenter la taille de chaque comparable et exiger une justification écrite de toute borne tirée de sociétés d'une autre échelle |
| Oublier la décote de dépendance au propriétaire | Une part non transférable de la rentabilité est vendue comme si elle l'était, en contexte de transfert ou de relève | Documenter la dépendance au propriétaire et rendre l'ajustement explicite ou écrire pourquoi il ne s'applique pas |
| Confondre valeur d'entreprise et valeur des actions | Le prix annoncé aux parties ne correspond pas à ce qui sera encaissé ; le montage de financement est faussé | Q1 : le tableau de passage doit apparaître intégralement, aucune valeur d'actions ne peut être présentée sans lui |
| Ignorer l'écart de fonds de roulement | Le vendeur livre une entreprise sous-capitalisée ou le prix ne reflète pas le fonds de roulement effectivement transféré | Établir le fonds de roulement normatif sur plusieurs exercices et le comparer au solde à la date d'évaluation |
| Présenter un point au lieu d'une fourchette | Fausse précision ; la négociation s'ancre sur un chiffre que l'analyse ne soutient pas | Refuser toute conclusion ponctuelle en E2 ; la fourchette est la forme obligatoire de la sortie |
| Retenir un multiple sans source au dossier | Chiffre orphelin ; l'ensemble de l'approche de marché devient indéfendable | Q3 : chaque multiple porte une source nommée et datée, à défaut il est retiré |

### Formules mobilisées

| Clé | Formule | Note |
|---|---|---|
| VE | VE = BAIIA normalisé retenu x Multiple retenu | Multiple issu de transactions comparables ou de repères sectoriels, ajusté pour la taille et le risque spécifique. Valeur de l'ensemble de l'exploitation, avant de tenir compte du financement. Aucun seuil (sans objet). Pièges : appliquer un multiple de sociétés cotées à une PME sans décote ; retenir un multiple ponctuel plutôt qu'une fourchette. |
| VA_ACTIONS | Valeur des actions = VE - Dette nette + Écart de fonds de roulement + Actifs hors exploitation | Dette nette = dette portant intérêt - encaisse excédentaire ; écart de fonds de roulement = FDR réel - FDR normatif du secteur. Ce que reçoivent les actionnaires une fois les prêteurs remboursés et le fonds de roulement normalisé. Aucun seuil (sans objet). Pièges : oublier l'écart de fonds de roulement ; traiter toute l'encaisse comme excédentaire alors qu'une partie est nécessaire à l'exploitation. |

## E3 — DCF

**Objectif.** Établir la valeur par l'actualisation des flux de trésorerie disponibles futurs, en rendant explicites les hypothèses de croissance, de marge et d'investissement qui la soutiennent, puis réconcilier ce résultat avec l'approche de marché. Cette approche est la seule qui rende visible la mécanique de création de valeur et qui permette de tester la sensibilité de la conclusion.

**Entrées requises.**

- Prévisionnel détaillé sur 3 à 5 ans, avec les hypothèses documentées ligne par ligne et leur auteur identifié.
- Investissements de maintien et investissements de croissance distingués, avec l'échéancier et les pièces d'appui.
- Variation prévue du fonds de roulement, cohérente avec le cycle de conversion observé et avec le fonds de roulement normatif de E2.
- Structure de capital cible et coût de la dette courant, distincts de la structure comptable actuelle.
- Taux sans risque et primes de marché observés à la date d'évaluation, avec leur source.
- Taux d'imposition effectif applicable à l'entité, incluant le traitement des déductions et crédits récurrents.
- BAIIA normalisé de E1 et fourchette de multiples de E2 pour le test de vraisemblance de la valeur terminale.

### Méthode

#### 1. Construire le flux de trésorerie disponible par exercice de l'horizon explicite

Le flux de trésorerie disponible se construit à partir du BAIIA normalisé de l'exercice projeté, duquel on retranche les impôts en trésorerie, les investissements de maintien nécessaires pour préserver la capacité de production, les investissements de croissance requis par le plan, et la variation du fonds de roulement engendrée par l'activité. La distinction entre investissements de maintien et de croissance est structurante : un modèle qui projette une croissance des ventes sans les investissements et le fonds de roulement qui la rendent possible produit une valeur fictive. La variation du fonds de roulement doit suivre la logique du cycle de conversion réel de l'entreprise, ce qui signifie qu'une croissance rapide consomme de la trésorerie même lorsque la rentabilité progresse.

L'horizon explicite doit être suffisamment long pour que la dernière année projetée représente un régime stabilisé, faute de quoi la valeur terminale sera assise sur une année atypique. On présente les flux en dollars nominaux, ce qui impose un taux d'actualisation nominal, et cette cohérence est vérifiée explicitement.

#### 2. Documenter chaque hypothèse de croissance et de marge et la confronter à l'historique

Chaque hypothèse du prévisionnel est écrite, chiffrée et rattachée à une source : carnet de commandes signé, contrat pluriannuel, capacité de production installée, embauche prévue, prix négocié avec un fournisseur. Ces hypothèses sont ensuite confrontées à la performance historique retraitée produite par E1 et par l'analyse financière amont : une croissance ou une marge projetée qui n'a jamais été atteinte doit être expliquée par un fait nouveau vérifiable, pas par une intention.

Le profil en crosse de hockey — plusieurs années de stagnation suivies d'une envolée soudaine — est le signal d'alerte le plus courant et doit être soit documenté, soit corrigé. On teste également la cohérence interne du prévisionnel : la masse salariale suit-elle le volume, la marge brute tient-elle compte de la pression sur les intrants, les frais de vente accompagnent-ils la croissance annoncée. Lorsque le prévisionnel provient de la direction, on le déclare comme tel et on documente les modifications apportées par l'évaluateur ainsi que leur motif. Un scénario prudent est produit en parallèle du scénario de base, parce que la conclusion de valeur ne doit jamais reposer sur le seul scénario le plus favorable.

#### 3. Établir le taux d'actualisation

Le coût moyen pondéré du capital se construit en deux temps : le coût des fonds propres, puis la pondération avec le coût de la dette après impôts à la structure de capital cible. Le coût des fonds propres se décompose en taux sans risque, prime de risque du marché multipliée par le bêta, prime de taille et prime spécifique, chaque terme portant sa source et sa date d'observation. Le bêta emprunté à un échantillon sectoriel doit être déleveragé de la structure de capital des sociétés de l'échantillon, puis releveragé à la structure cible de l'entreprise évaluée ; utiliser un bêta publié tel quel introduit une erreur de levier silencieuse.

La prime spécifique couvre les risques propres non captés ailleurs — dépendance au propriétaire, concentration de la clientèle, absence de relève, fragilité d'un approvisionnement — et chaque composante doit être nommée et motivée par écrit plutôt qu'empilée globalement. La pondération entre dette et fonds propres se fait aux valeurs cibles et non aux valeurs comptables actuelles, sinon une entreprise temporairement surendettée se voit attribuer un taux d'actualisation artificiellement bas. On vérifie enfin qu'aucun risque n'est compté deux fois, une fois dans le taux et une fois dans les flux, ce qui est le défaut classique des modèles construits sur un scénario déjà prudent.

#### 4. Calculer la valeur terminale par croissance perpétuelle et par multiple de sortie, et comparer les deux

La valeur terminale se calcule d'abord par croissance perpétuelle, à partir du flux de trésorerie disponible de l'année terminale, en retenant un taux de croissance qui doit demeurer inférieur à la croissance nominale de l'économie à long terme, ce seuil étant indicatif mais structurant. Un taux de croissance perpétuelle qui s'approche du coût moyen pondéré du capital fait exploser le dénominateur et produit une valeur dénuée de sens : ce contrôle se fait avant toute présentation. On calcule ensuite une seconde valeur terminale par multiple de sortie appliqué au BAIIA normalisé de l'année terminale, en utilisant la fourchette de multiples documentée en E2.

La comparaison des deux méthodes est le test de vraisemblance central du modèle : si la croissance perpétuelle retenue implique un multiple de sortie très supérieur à ce que le marché paie réellement pour ce type d'entreprise, le modèle est incohérent et doit être corrigé. On vérifie enfin que l'année terminale est représentative d'un régime durable, notamment que les investissements de maintien y sont au moins égaux à l'amortissement et que le fonds de roulement y croît au même rythme que l'activité.

#### 5. Actualiser les flux et la valeur terminale

Les flux de l'horizon explicite et la valeur terminale sont ramenés à la date d'évaluation au coût moyen pondéré du capital, en déclarant la convention d'actualisation retenue — fin de période ou milieu de période — et en l'appliquant uniformément. La date d'évaluation est le point d'ancrage : si des flux ont déjà été réalisés entre la fin du dernier exercice et cette date, le traitement de la période intercalaire est explicité.

Le résultat de l'actualisation est la valeur d'entreprise, à laquelle on applique ensuite le même passage à la valeur des actions qu'en E2 : déduction de la dette nette, ajustement de l'écart de fonds de roulement par rapport au normatif, addition des actifs hors exploitation. Ce passage doit être strictement identique à celui de l'approche de marché, sur les mêmes soldes et à la même date, sinon la comparaison entre les deux approches est faussée dès le départ. Toute divergence de traitement entre les deux approches doit être signalée et justifiée dans la réconciliation.

#### 6. Mesurer le poids de la valeur terminale dans la valeur totale

On calcule systématiquement la part de la valeur d'entreprise attribuable à la valeur terminale actualisée, et on la présente dans le rapport. Ce ratio indique à quel point la conclusion repose sur l'après-horizon plutôt que sur le prévisionnel détaillé qui a été documenté et contesté. À titre indicatif, au-delà de 75 % le résultat devient très sensible aux hypothèses terminales, et le rapport doit alors le signaler explicitement plutôt que de présenter le modèle comme robuste.

Un poids élevé n'invalide pas le modèle, mais il déplace le débat : la discussion doit alors porter sur le taux de croissance perpétuelle, sur le multiple de sortie implicite et sur la représentativité de l'année terminale, et non sur le détail des trois premières années. Lorsque ce poids est élevé, on renforce le test de vraisemblance par multiple de sortie et on élargit la table de sensibilité. Ne pas calculer ce poids et présenter néanmoins le modèle d'actualisation comme solide est une faute de méthode relevée en contrôle.

#### 7. Produire l'analyse de sensibilité croisée et réconcilier avec E2

La conclusion de l'approche par actualisation se présente sous forme de table de sensibilité croisée faisant varier le taux d'actualisation et le taux de croissance perpétuelle autour des valeurs retenues, ce qui transforme un point unique en surface de valeurs plausibles. On complète par une sensibilité aux deux hypothèses d'exploitation les plus déterminantes du dossier, généralement la marge brute et le volume, afin de montrer où se joue réellement la valeur.

Les résultats sont ensuite confrontés à la fourchette produite par l'approche de marché en E2 : on compare les valeurs d'entreprise entre elles, jamais une valeur d'entreprise à une valeur d'actions. On calcule le multiple implicite du modèle d'actualisation, c'est-à-dire la valeur d'entreprise obtenue divisée par le BAIIA normalisé retenu, et on le situe dans la fourchette de multiples documentée en E2. Cette confrontation est la véritable sortie de E3 : elle identifie l'origine de tout écart entre les deux approches et prépare la pondération de E4.

### Sorties

- Flux de trésorerie disponible par exercice de l'horizon explicite, avec ses hypothèses sourcées.
- Décomposition complète du taux d'actualisation, terme par terme, avec la date d'observation de chaque paramètre.
- Valeur terminale calculée selon les deux méthodes, avec la comparaison et le motif de la méthode retenue.
- Valeur d'entreprise actualisée et passage à la valeur des actions sur les mêmes soldes qu'en E2.
- Poids de la valeur terminale dans la valeur d'entreprise totale.
- Table de sensibilité croisée taux et croissance, plus la sensibilité aux hypothèses d'exploitation clés.
- Multiple implicite du modèle et note de réconciliation avec l'approche de marché.

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Valeur terminale qui représente une part démesurée de la valeur | La conclusion repose sur l'après-horizon et non sur le prévisionnel documenté ; la robustesse annoncée est illusoire | Calculer et publier le poids de la valeur terminale ; au-delà du repère indicatif de 75 %, le signaler et renforcer le test par multiple de sortie |
| Croissance perpétuelle supérieure à la croissance de l'économie | L'entreprise finit mathématiquement par dépasser son marché ; la valeur devient absurde | Contrôler que le taux retenu demeure inférieur à la croissance nominale de l'économie, seuil indicatif mais bloquant en pratique |
| Prévisionnel en crosse de hockey non justifié | Valeur assise sur une performance jamais atteinte ; l'écart avec l'approche de marché devient inexplicable | Confronter chaque hypothèse à l'historique retraité de E1 et exiger un fait nouveau vérifiable pour toute rupture de trajectoire |
| Incohérence entre flux nominaux et taux réel | Erreur systématique d'un ordre de grandeur sur la conclusion, invisible à la lecture | Déclarer la convention retenue en tête de modèle et vérifier la cohérence flux et taux au contrôle Q1 |
| Bêta emprunté sans ajustement de structure | Le risque financier de l'échantillon est importé au lieu de celui de l'entreprise évaluée | Déleverager le bêta de l'échantillon puis le releverager à la structure cible, et documenter les deux étapes |
| Double comptage du risque dans les flux et dans le taux | Sous-évaluation systématique ; le scénario prudent est pénalisé deux fois | Choisir explicitement où le risque est traité et l'écrire dans la note méthodologique |

### Formules mobilisées

| Clé | Formule | Note |
|---|---|---|
| WACC | WACC = Ke x (E / (D+E)) + Kd x (1 - t) x (D / (D+E)) | Ke = coût des fonds propres ; Kd = coût de la dette avant impôts ; t = taux d'imposition effectif ; D et E aux valeurs cibles et non comptables. Taux d'actualisation reflétant le coût de toutes les sources de financement à la structure cible. Aucun seuil (sans objet). Pièges : utiliser la structure de capital comptable actuelle plutôt que la structure cible ; oublier l'économie d'impôt sur les intérêts ; mélanger un taux nominal avec des flux réels. |
| KE | Ke = Rf + Bêta x PRM + Prime de taille + Prime spécifique | Rf = taux sans risque ; PRM = prime de risque du marché ; prime de taille et prime spécifique documentées pour la PME visée. Rendement exigé par un actionnaire compte tenu du risque assumé. Aucun seuil (sans objet). Pièges : emprunter un bêta sectoriel sans le déleverager puis le releverager à la structure cible ; empiler des primes sans justification écrite. |
| VT_GORDON | VT = FTD de l'année terminale x (1 + g) / (WACC - g) | g = taux de croissance perpétuelle ; doit demeurer inférieur à la croissance nominale de l'économie à long terme. Valeur de tous les flux au-delà de l'horizon explicite. Seuil indicatif : g inférieur à la croissance nominale de l'économie. Pièges : retenir un g proche du WACC qui fait exploser la valeur ; asseoir la valeur terminale sur une année d'exploitation non représentative ; laisser la valeur terminale dominer la valeur totale sans le signaler. |
| POIDS_VT | Poids = VT actualisée / Valeur d'entreprise totale | VT actualisée = valeur terminale ramenée à la date d'évaluation. Indique à quel point la conclusion repose sur l'après-horizon plutôt que sur le prévisionnel détaillé. Seuil indicatif : au-delà de 75 % le résultat devient très sensible aux hypothèses terminales. Piège : ne pas calculer ce poids et présenter le modèle d'actualisation comme robuste alors qu'il repose presque entièrement sur la valeur terminale. |
| VA_ACTIONS | Valeur des actions = VE - Dette nette + Écart de fonds de roulement + Actifs hors exploitation | Passage appliqué à la valeur d'entreprise actualisée, sur les mêmes soldes et à la même date qu'en E2, faute de quoi la comparaison entre les deux approches est faussée. Aucun seuil (sans objet). |

## E4 — rapport-evaluation

**Objectif.** Produire le rapport d'évaluation qui déclare sa date, sa définition de valeur et sa portée, réconcilie les approches retenues, pondère explicitement et conclut sur une fourchette assortie de ses hypothèses limitatives. E4 ne recalcule rien : il assemble, justifie, encadre juridiquement et ferme le dossier.

**Entrées requises.**

- Résultats complets et validés de E1, E2 et E3, avec leurs tableaux d'appui.
- Lettre de mandat précisant le client, l'usage prévu, la définition de valeur demandée et le niveau de portée convenu.
- Date d'évaluation retenue et motif de son choix.
- Inventaire des restrictions d'accès à l'information et des documents demandés mais non obtenus.
- Description de l'entreprise, de son actionnariat, de son historique et du contexte de la transaction envisagée.
- Registre des sources produit par Q3 et registre des contrôles arithmétiques produit par Q1.

### Méthode

#### 1. Déclarer la date d'évaluation, la définition de valeur retenue et la portée du mandat

Le rapport s'ouvre sur trois déclarations sans lesquelles aucune conclusion n'est utilisable. La date d'évaluation fixe le moment auquel la valeur est établie et à laquelle tous les soldes de bilan, les paramètres de marché et les faits connus se rapportent ; un événement postérieur ne peut être intégré sans changer la date. La définition de valeur retenue est énoncée textuellement : la juste valeur marchande s'entend du prix le plus élevé, exprimé en argent, qu'un bien obtiendrait sur un marché libre et sans entrave entre des parties bien informées, prudentes et sans lien de dépendance, ni l'une ni l'autre n'étant contrainte de transiger. Si le mandat vise plutôt une valeur pour un acquéreur stratégique identifié, une valeur de liquidation ou une valeur aux fins d'une clause de convention entre actionnaires, cela est déclaré explicitement, car la conclusion diffère.

La portée du mandat est décrite dans les mêmes termes que dans la lettre de mandat : nature du travail effectué, étendue des vérifications faites et non faites, documents consultés. Une conclusion de valeur produite sans déclaration de portée n'est pas un livrable remettable.

#### 2. Décrire l'entreprise et le contexte de l'évaluation

Le rapport présente l'entreprise de façon factuelle : raison sociale exacte, forme juridique, date de constitution, actionnariat et répartition des droits de vote, activités, marchés desservis, effectif, installations, principaux clients et fournisseurs, actifs clés. Il expose ensuite le contexte de l'évaluation, parce que ce contexte conditionne la lecture de la conclusion : transfert à un membre de la famille, rachat par la direction, acquisition par un tiers financée par emprunt, entrée ou sortie d'un actionnaire, prise de participation.

On décrit également la structure envisagée de la transaction — vente d'actions ou d'actifs, périmètre inclus, sort de l'immeuble et des actifs hors exploitation — puisque la conclusion s'y rattache. Cette section contient les faits, jamais les arguments : les qualités et les fragilités de l'entreprise appartiennent à l'analyse et aux ajustements, pas au portrait descriptif. Les informations sensibles sur les personnes sont limitées à ce qui est nécessaire à la compréhension du dossier.

#### 3. Présenter les approches retenues et écartées avec motifs

Le rapport nomme les approches d'évaluation considérées — approche de marché, approche de rendement, approche fondée sur les actifs — et motive celles qui sont retenues comme celles qui sont écartées. Une approche fondée sur la valeur des actifs nets réajustés est pertinente pour une entreprise dont la rentabilité ne justifie pas une valeur supérieure à ses actifs, pour une société de portefeuille ou pour un scénario de liquidation ; l'écarter est un choix qui doit être écrit, en particulier lorsque la rentabilité est faible. On explique pourquoi l'approche de marché et l'approche de rendement ont été menées en parallèle : elles s'éclairent mutuellement, l'une reflétant ce que le marché paie et l'autre ce que l'entreprise peut générer.

Les limites de chaque approche dans le dossier concerné sont énoncées : qualité de l'échantillon de comparables, fiabilité du prévisionnel, sensibilité aux hypothèses terminales. Cette section est celle qu'un contre-expert lira en premier ; elle doit tenir seule.

#### 4. Réconcilier les résultats des approches et pondérer explicitement

La réconciliation confronte les fourchettes obtenues par les deux approches sur une base strictement comparable — valeur d'entreprise contre valeur d'entreprise, puis valeur des actions contre valeur des actions — et explique l'origine de l'écart plutôt que de le contourner. La pondération accordée à chaque approche est chiffrée et justifiée par la qualité relative des intrants : profondeur et pertinence de l'échantillon de comparables d'un côté, fiabilité du prévisionnel et poids de la valeur terminale de l'autre. Une pondération présentée sans motif est une faute de méthode ; une pondération égale par défaut en est une autre lorsqu'elle masque une différence évidente de qualité des intrants.

Lorsque les deux approches convergent, la convergence elle-même devient un élément de confort qui doit être souligné. Lorsqu'elles divergent fortement, la divergence non résolue est déclarée et le rapport élargit la fourchette conclue plutôt que de choisir arbitrairement un camp.

#### 5. Conclure sur une fourchette et un point médian si requis

La conclusion prend la forme d'une fourchette de valeur des actions à la date d'évaluation, exprimée avec un arrondi que la précision des intrants supporte réellement. Une valeur présentée au dollar près sur la base d'un multiple retenu à l'intérieur d'une fourchette et d'un prévisionnel produit par la direction constitue un faux précis, immédiatement relevé au contrôle.

Un point médian n'est produit que si le mandat l'exige, par exemple pour l'exercice d'une clause d'une convention entre actionnaires, et il est alors accompagné de la mention qu'il ne représente pas une valeur plus certaine que le reste de la fourchette. La conclusion rappelle la définition de valeur retenue, la date d'évaluation et le périmètre visé, de sorte qu'elle demeure interprétable si elle est extraite du rapport. Elle renvoie enfin aux hypothèses limitatives, qui en font partie intégrante et ne peuvent en être détachées.

#### 6. Énoncer les hypothèses limitatives et les restrictions

Les hypothèses limitatives encadrent la portée juridique et pratique de la conclusion : elles précisent ce qui a été présumé, ce qui n'a pas été vérifié, qui peut utiliser le rapport et à quelles fins. Elles ne sont pas une clause de style : elles doivent refléter le travail réellement effectué dans ce dossier précis, ce qui suppose de les adapter et non de les recopier d'un rapport antérieur.

Toute restriction d'accès à l'information est nommée : document demandé et non obtenu, période non couverte, entité liée non consultée, direction non rencontrée. Lorsqu'une restriction touche un élément déterminant de la conclusion, elle est signalée à la fois dans les hypothèses limitatives et dans le corps du rapport, à l'endroit où elle produit son effet. La clause d'usage restreint est indispensable : elle nomme le destinataire, l'usage prévu et l'interdiction de diffusion à un tiers sans autorisation écrite.

#### 7. Annexer les tableaux de calcul et les sources

Les annexes rendent le rapport reproductible : tableau de normalisation de E1 ligne par ligne, tableau des comparables et de leurs sources, tableau de passage de la valeur d'entreprise à la valeur des actions, flux de trésorerie disponible par exercice, décomposition du taux d'actualisation, table de sensibilité, registre des sources produit par Q3. Chaque annexe est numérotée et appelée dans le corps du texte à l'endroit où elle appuie une affirmation.

Les chiffres du corps du rapport et ceux des annexes doivent être strictement identiques ; tout écart, même d'arrondi, est corrigé à la source avant remise. Le rapport porte une identification de version claire et ne contient aucune mention de travail résiduelle, conformément au contrôle de nomenclature. Le dossier complet est ensuite soumis au préflight final, qui rend le statut de sortie.

### Sorties

- Rapport d'évaluation structuré, avec déclaration de date, de définition de valeur et de portée.
- Section de réconciliation des approches avec pondération motivée.
- Fourchette de valeur des actions conclue à la date d'évaluation, et point médian si le mandat l'exige.
- Hypothèses limitatives et restrictions adaptées au dossier.
- Annexes de calcul numérotées et registre des sources.
- Statut de sortie du préflight final et liste des blocages résiduels le cas échéant.

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Conclure sans déclarer la portée | Le lecteur attribue au rapport un niveau d'assurance qu'il n'a pas ; la responsabilité professionnelle devient indéfendable | Q4 : aucun rapport ne sort sans les trois déclarations d'ouverture, date, définition de valeur et portée |
| Pondérer les approches sans justification | La conclusion devient arbitraire et s'effondre au premier contre-interrogatoire | Exiger un motif chiffré rattaché à la qualité relative des intrants de chaque approche |
| Présenter une valeur au dollar près | Faux précis ; la fausse précision décrédibilise l'ensemble du travail | Q1 : arrondir à la précision que les intrants supportent et refuser toute décimale non soutenue |
| Omettre les restrictions d'information | Une limite déterminante reste invisible pour le lecteur qui prend la décision | Tenir l'inventaire des documents demandés et non obtenus, et le reporter dans le rapport |
| Réutiliser une évaluation à une date différente sans mise à jour | Les soldes de bilan, les paramètres de marché et les faits ont changé ; la conclusion ne vaut plus | Interdire toute réutilisation sans mise à jour formelle et sans nouvelle date d'évaluation |
| Chiffres du corps divergents de ceux des annexes | Perte de confiance immédiate et remise en cause de tout le dossier | Q1 et Q4 : contrôle de cohérence inter-documents avant remise, sur la version effectivement remise |

### Formules mobilisées

E4 ne comporte aucune formule propre : il reprend et présente celles des modules amont. Les formules ci-dessous sont reproduites en annexe du rapport, telles qu'appliquées, avec leurs termes.

| Clé | Formule | Note |
|---|---|---|
| BAIIA_NORM | BAIIA normalisé = BAIIA publié ± ajustements de normalisation | Reproduite en annexe avec le tableau de normalisation ligne par ligne et la source de chaque ajustement. |
| VE | VE = BAIIA normalisé retenu x Multiple retenu | Reproduite avec la fourchette de multiples, l'échantillon de comparables et la source datée de chacun. |
| VA_ACTIONS | Valeur des actions = VE - Dette nette + Écart de fonds de roulement + Actifs hors exploitation | Reproduite deux fois, une fois pour l'approche de marché et une fois pour l'approche de rendement, sur les mêmes soldes et à la même date. |
| WACC | WACC = Ke x (E / (D+E)) + Kd x (1 - t) x (D / (D+E)) | Reproduite avec la structure de capital cible retenue et la date d'observation des paramètres. |
| KE | Ke = Rf + Bêta x PRM + Prime de taille + Prime spécifique | Reproduite terme par terme, chaque prime portant sa justification écrite. |
| VT_GORDON | VT = FTD de l'année terminale x (1 + g) / (WACC - g) | Reproduite avec le taux de croissance perpétuelle retenu et la comparaison avec la valeur terminale par multiple de sortie. |
| POIDS_VT | Poids = VT actualisée / Valeur d'entreprise totale | Reproduite et commentée ; au-delà du repère indicatif de 75 %, la sensibilité aux hypothèses terminales est signalée dans le corps du rapport. |

## Réconciliation des approches

La réconciliation est le moment où l'évaluation cesse d'être un calcul pour devenir une opinion défendable. Elle commence par une mise en comparabilité stricte : on confronte la valeur d'entreprise de l'approche de marché à la valeur d'entreprise de l'approche de rendement, sur le même périmètre, à la même date d'évaluation et avec le même traitement de la dette nette, du fonds de roulement normatif et des actifs hors exploitation. Toute divergence de traitement entre les deux passages à la valeur des actions doit être éliminée avant de commenter l'écart, faute de quoi on interprète une différence de méthode comme une différence de valeur.

Le premier outil de réconciliation est le multiple implicite : on divise la valeur d'entreprise obtenue par actualisation par le BAIIA normalisé retenu, et on situe le résultat dans la fourchette de multiples documentée en E2. Si le multiple implicite tombe à l'intérieur de la fourchette, les deux approches se confirment et la conclusion se resserre. S'il se situe nettement au-dessus, le prévisionnel ou les hypothèses terminales sont plus optimistes que ce que le marché paie ; s'il se situe nettement en dessous, soit le prévisionnel est excessivement prudent, soit l'échantillon de comparables ne reflète pas la réalité de l'entreprise évaluée.

Devant une divergence forte, on ne choisit pas : on cherche d'abord l'erreur. Les causes récurrentes sont peu nombreuses et se vérifient dans l'ordre suivant avant toute interprétation.

| Ordre | Cause à vérifier | Correction |
|---|---|---|
| 1 | Le BAIIA normalisé retenu en E2 diffère du BAIIA de la première année projetée en E3 sans motif écrit | Aligner les deux ou écrire le motif de l'écart dans la note méthodologique |
| 2 | Le prévisionnel projette une croissance ou une marge que l'historique retraité de E1 ne soutient pas | Documenter le fait nouveau vérifiable ou ramener la projection à la trajectoire observée |
| 3 | La valeur terminale domine la valeur d'entreprise et impose un multiple de sortie que le marché ne pratique pas | Recalculer la valeur terminale par multiple de sortie et corriger le taux de croissance perpétuelle |
| 4 | L'échantillon de comparables mélange des tailles, des sous-secteurs ou des natures de transaction incompatibles | Resserrer les critères de sélection et reconstituer la fourchette |
| 5 | Une décote de dépendance au propriétaire est appliquée dans une approche et oubliée dans l'autre | Appliquer le facteur de risque une seule fois et au même endroit dans les deux approches |
| 6 | Un actif ou un passif hors exploitation est compté d'un seul côté | Reprendre le même inventaire hors exploitation dans les deux passages à la valeur des actions |
| 7 | La dette nette ou le fonds de roulement n'est pas arrêté à la même date dans les deux approches | Figer une seule date d'arrêté, celle de l'évaluation, et refaire les deux passages |

Ce n'est qu'une fois ces vérifications faites que la divergence résiduelle devient interprétable : elle exprime alors une différence réelle entre ce que le marché paie aujourd'hui pour ce type d'entreprise et ce que celle-ci peut générer selon son plan. Cette différence se commente, elle ne se dissout pas dans une moyenne.

La pondération se justifie par la qualité relative des intrants et par le contexte du mandat, jamais par une convention. On accorde plus de poids à l'approche de marché lorsque l'échantillon de comparables est profond, récent et véritablement comparable, et lorsque le prévisionnel est faible, tardif ou entièrement produit par une partie intéressée. On accorde plus de poids à l'approche de rendement lorsque le prévisionnel est solide, appuyé par des contrats et cohérent avec l'historique, lorsque l'entreprise entre dans une phase de transformation que les comparables historiques ne captent pas, ou lorsque les comparables disponibles sont rares ou de taille très différente.

Le contexte du mandat module également la pondération. En transfert d'entreprise et en relève, la dépendance au propriétaire et la transférabilité de la rentabilité pèsent lourd, ce qui renforce le poids de l'approche de marché ajustée pour ce facteur. En acquisition financée par prêt, l'approche de rendement porte une valeur informationnelle supplémentaire parce que les mêmes flux serviront à démontrer la capacité de remboursement en aval, et une incohérence entre l'évaluation et le prévisionnel de service de la dette serait immédiatement relevée. En prise de participation minoritaire, la question de l'absence de contrôle et de la liquidité des titres s'ajoute et doit être traitée explicitement plutôt que noyée dans la pondération. Le poids accordé à chaque approche et son motif sont écrits en toutes lettres dans le rapport.

La conclusion prend la forme d'une fourchette et non d'un point pour trois raisons cumulatives. D'abord, chaque intrant est lui-même une fourchette : le multiple observé varie d'une transaction à l'autre, le taux d'actualisation dépend de primes estimées, le prévisionnel est une projection. Ensuite, la juste valeur marchande décrit un prix théorique entre parties hypothétiques, alors que le prix réel d'une transaction dépendra de la négociation, des modalités de paiement, de la balance de prix de vente, des clauses d'ajustement et de la fiscalité des parties. Enfin, une fourchette est plus utile qu'un point pour la décision qu'elle sert : elle indique où se situe la zone de discussion raisonnable et à partir de quel niveau un prix devient difficile à justifier. La largeur de la fourchette est elle-même un message : une fourchette étroite signale des intrants convergents et bien documentés, une fourchette large signale une incertitude réelle qu'il serait malhonnête de dissimuler.

## Hypothèses limitatives types

Les énoncés suivants sont rédigés pour être insérés tels quels dans un rapport d'évaluation, après adaptation aux faits du dossier. Ils ne remplacent pas un examen des restrictions propres au mandat.

- La présente évaluation est établie en date du [date d'évaluation] et ne tient compte d'aucun événement, fait ou condition survenu après cette date, même s'il a été porté à notre connaissance par la suite ; toute utilisation de la conclusion à une autre date exigerait une mise à jour du présent rapport.
- La conclusion de valeur repose sur l'information financière et opérationnelle fournie par la direction et par les représentants de l'entreprise ; cette information n'a fait l'objet d'aucun audit, d'aucun examen ni d'aucune procédure de vérification de notre part, et nous n'exprimons aucune opinion d'audit ou d'examen à son égard.
- Le mandat qui nous a été confié est d'une portée limitée et convenue avec le client ; il ne constitue ni une vérification diligente, ni un examen exhaustif des livres et registres, ni une recherche de fraude ou d'irrégularité, et il ne saurait être interprété comme tel.
- Aucune vérification diligente juridique, fiscale, environnementale, technique ou immobilière n'a été effectuée dans le cadre du mandat ; nous avons présumé l'absence de passif éventuel, de litige, de contamination ou de non-conformité qui ne nous aurait pas été déclaré par écrit.
- Nous avons présumé que les titres de propriété sont valides et cessibles, que les actifs sont libres de toute charge autre que celles qui nous ont été déclarées, et que l'entreprise détient les permis, licences et autorisations nécessaires à la poursuite de ses activités.
- L'entreprise a été évaluée sur une base de continuité d'exploitation ; la conclusion serait différente dans une hypothèse de liquidation, de cessation d'activité ou de vente forcée.
- La conclusion suppose une transaction hypothétique entre des parties bien informées, prudentes et sans lien de dépendance, dont aucune n'est contrainte de transiger ; elle ne tient compte d'aucune synergie propre à un acquéreur stratégique déterminé, à moins que le mandat ne l'exige expressément et que cela ne soit indiqué.
- Les projections financières utilisées ont été préparées par la direction et retenues avec les modifications décrites au rapport ; les résultats réels différeront des projections et les écarts peuvent être importants, sans que cela remette rétroactivement en cause la conclusion à la date d'évaluation.
- Les paramètres de marché utilisés dans l'établissement du taux d'actualisation ont été observés à la date d'évaluation ; une variation de ces paramètres modifierait la conclusion et exigerait une mise à jour du rapport.
- La conclusion est présentée sous forme de fourchette ; aucune valeur située à l'intérieur de cette fourchette ne doit être extraite, citée isolément ou présentée comme un prix de transaction, et la fourchette ne peut être dissociée des hypothèses limitatives qui en font partie intégrante.
- Le présent rapport est destiné exclusivement à [destinataire] aux fins de [usage prévu] ; il ne peut être utilisé, cité, reproduit ni communiqué à un tiers, en tout ou en partie, sans notre autorisation écrite préalable, et nous n'assumons aucune responsabilité envers tout tiers qui en prendrait connaissance ou s'en prévaudrait.
- Notre rémunération pour ce mandat n'est aucunement liée à la conclusion de valeur ni à la réalisation de la transaction envisagée ; les documents suivants ont été demandés et n'ont pas été obtenus : [liste des restrictions d'accès à l'information], et leur absence limite la portée des travaux dans la mesure décrite au rapport.

## Passage au domaine suivant

L'évaluation remet à 05-PRODUCTION un contenu déjà arrêté : la fourchette de valeur conclue, le tableau de passage à la valeur des actions, la pondération motivée des approches et les hypothèses limitatives. Le module de rapport exécutif condense ce contenu en plaçant la fourchette et sa date en première ligne, suivies des trois à cinq chiffres qui la portent — BAIIA normalisé retenu, fourchette de multiples, taux d'actualisation, poids de la valeur terminale — sans jamais réécrire la conclusion. Le module de présentation met en scène ce même livrable validé pour une instance décisionnelle, avec la mention obligatoire de la date d'évaluation et de la portée sur la diapositive de conclusion. Aucune donnée nouvelle n'apparaît en production : tout chiffre qui surgirait à cette étape doit repasser par le contrôle des calculs et la validation des sources avant d'être présenté.

À 06-QA, l'évaluation soumet ses calculs au recalcul indépendant et ses chiffres à la traçabilité complète. Le contrôle des calculs recalcule le BAIIA normalisé, la valeur d'entreprise, le passage à la valeur des actions et le poids de la valeur terminale sans reprendre les formules du modèle d'origine, et vérifie la cohérence d'un même chiffre entre le corps du rapport, les annexes et le sommaire. La validation des sources exige qu'aucun multiple, aucune prime et aucun salaire de marché ne demeure orphelin, et qualifie le niveau de chaque source. La nomenclature et le préflight final ferment la chaîne : version identifiée, raison sociale exacte, annexes annoncées présentes, conclusion explicite en tête, et statut de sortie rendu avant toute remise.
