# 01 — FINANCEMENT

Ce domaine produit le socle chiffré de toute décision de prêt du DÉPS : le portrait financier réel de l'entreprise, le montage du tour de financement, la démonstration de la capacité de remboursement et la cotation structurée du risque. Tout ce qui est présenté au comité d'investissement commun, tarifé ou déclaré conforme repose sur ces quatre livrables et sur rien d'autre.

La règle d'or du domaine tient en deux exigences indissociables. Aucun chiffre ne circule sans sa source, sa date et son niveau d'assurance ; et aucune conclusion de capacité de remboursement ne s'appuie sur le bénéfice comptable, mais toujours sur les flux de trésorerie. Les paramètres de politique — plafonds, taux, ratios entre fonds, mise de fonds minimale, seuils de délégation — ne sont jamais reconstitués de mémoire : ils proviennent de `data/parametres-politique.csv` et de la politique d'investissement en vigueur, et tout paramètre encore au statut A_VALIDER doit être signalé comme tel dans le livrable plutôt que remplacé par une valeur présumée.

## Vue d'ensemble

| Module | ID | Produit | Dépend de |
|---|---|---|---|
| analyse-financiere | F1 | Tableau des 3 exercices retraités, grille de ratios avec repères sectoriels, signaux d'alerte cotés, questions ouvertes au promoteur | Aucun module du domaine ; l'admissibilité P1 est tranchée en amont du pipeline |
| montage-financier | F2 | Tableau Sources et Emplois balancé, structure de sûretés par rang, échéancier de décaissement, conditions inter-prêteurs | F1, P1 |
| capacite-remboursement | F3 | Ratio de couverture par exercice et par scénario, seuil de rupture, besoin de marge de crédit, recommandation de terme et de congé de capital | F1, F2 |
| analyse-risque | F4 | Matrice de risque cotée, risques résiduels, conditions de décaissement proposées, engagements, garanties requises | F1, F3, D2 |

L'ordre logique du domaine est F1, puis F2, puis F3, puis F4, et cet ordre n'est pas une convention de présentation : chaque module consomme littéralement les sorties du précédent. F1 établit la base normalisée sans laquelle le levier de F2 et le flux disponible de F3 ne veulent rien dire. F2 fixe le coût de projet et l'ensemble des dettes projetées, faute de quoi F3 calculerait une couverture sur un service de la dette incomplet. F3 produit la mesure de solidité que F4 traduit en risques cotés, en conditions et en garanties.

Dans le pipeline complet de dossier CIC, le montage F2 se travaille toutefois en deux passes : une version de travail suffisante pour alimenter F3, puis une version finale reprise après la tarification P2, puisque le taux, le terme et le congé de capital modifient le service de la dette et donc l'équilibre du montage. Un dossier jugé non admissible en P1 ne doit jamais consommer d'analyse financière : le verdict d'admissibilité précède l'ouverture du domaine 01. Les quatre modules partagent les mêmes portes de sortie, les contrôles Q1 (recalcul indépendant) et Q3 (validation des sources), qui doivent être passés et consignés avant tout usage aval des livrables.

## F1 — analyse-financiere

**Objectif.** Établir le portrait financier réel de l'entreprise sur trois exercices et dégager la trajectoire, la structure et les signaux d'alerte avant toute recommandation. F1 ne juge pas le projet : il établit d'où part l'entreprise.

**Entrées requises.**
- États financiers de trois exercices complets, de préférence issus d'une mission d'examen ou d'un audit, avec les notes complémentaires et non uniquement les états sommaires.
- Balance de vérification récente, pour rapprocher les états intérimaires et repérer les écritures de régularisation non encore passées.
- États intérimaires de l'exercice en cours, accompagnés de la période comparative correspondante de l'exercice précédent.
- Liste de l'âge des comptes clients et des comptes fournisseurs à une date récente, en tranches de 30, 60 et 90 jours et plus.
- Conventions entre actionnaires, incluant les clauses de retrait, de rachat et de postposition des avances.
- Contrats de dette existants : offres de financement, conventions de prêt, contrats de crédit-bail, marges autorisées et utilisées, engagements financiers en vigueur.
- Détail de la rémunération et des retraits des actionnaires sur la période analysée.
- Organigramme des entités liées et, le cas échéant, états financiers des sociétés de gestion ou immobilières associées.

### Méthode

#### 1. Qualifier la source et noter le niveau d'assurance

Le premier geste consiste à identifier précisément le niveau d'assurance des états financiers : audit, mission d'examen, avis au lecteur ou états produits à l'interne. Ce niveau ne sert pas à décorer la note ; il détermine le degré de scepticisme à appliquer et il devra être déclaré au registre des sources exigé par Q3. Un avis au lecteur ne comporte aucune assurance : les soldes n'ont fait l'objet d'aucune vérification, et un chiffre issu d'une compilation ne doit jamais être qualifié de vérifié dans un livrable.

Lisez également la lettre du professionnel comptable et les notes complémentaires : une réserve, une note de continuité d'exploitation ou un changement de cabinet en cours de période sont des informations de premier ordre. Notez la date de fin d'exercice et vérifiez qu'elle n'a pas changé, ainsi que l'identité exacte de l'entité présentée — société opérante seule, société de gestion, ou états consolidés. Un travail bâclé se reconnaît à ceci : il analyse trois séries de chiffres sans jamais dire d'où elles viennent ni ce qu'elles couvrent.

#### 2. Reconstituer les trois exercices en colonnes comparables

Montez un tableau unique où les trois exercices apparaissent côte à côte, poste par poste, dans une nomenclature stable que vous imposez vous-même plutôt que de recopier la présentation variable du comptable. Le risque principal est la comparabilité : un exercice de transition de neuf ou de quinze mois ne se compare pas à un exercice de douze mois et doit être annualisé ou écarté avec mention explicite. Retraitez les changements de méthode comptable, les reclassements entre coût des ventes et frais généraux, et les changements de méthode d'évaluation des stocks, sans quoi la tendance des marges que vous lirez sera un artefact de présentation.

Vérifiez le chaînage du bilan : le bénéfice net de l'exercice doit se retrouver dans la variation des bénéfices non répartis, aux dividendes et redressements près. Isolez dès cette étape les postes qui gouvernent la lecture du dossier — avances d'actionnaires, soldes de prix de vente, comptes à recevoir de parties liées, actifs incorporels et écarts d'acquisition. Un bon retraitement se voit à ce qu'il documente chaque écart entre le chiffre publié et le chiffre retenu, sur une ligne dédiée, avec sa source.

#### 3. Calculer les ratios de liquidité, structure, rentabilité et cycle d'exploitation

Produisez la grille complète pour les trois exercices, et non pour le dernier seulement : liquidité (fonds de roulement, ratio du fonds de roulement, liquidité immédiate), structure (dette portant intérêt sur BAIIA normalisé, passif total sur avoir), rentabilité (marge brute, marge d'exploitation, seuil de rentabilité) et cycle d'exploitation (délai de recouvrement des clients, délai d'écoulement des stocks, délai de paiement des fournisseurs, cycle de conversion de trésorerie). Chaque ratio doit être accompagné d'une définition écrite de son numérateur et de son dénominateur, parce que deux analystes qui n'utilisent pas la même définition de la dette ne produisent pas le même levier.

Retirez la portion à court terme de la dette à long terme du calcul du fonds de roulement seulement si vous le déclarez, et tenez la convention constante sur les trois exercices. Les seuils indicatifs figurant au tableau des formules sont des repères de marché, jamais des seuils de politique du DÉPS : présentez-les comme tels. Un ratio sans repère de comparaison est un chiffre inutile ; à défaut de repère sectoriel documenté et daté, comparez au moins l'entreprise à elle-même dans le temps et dites-le explicitement.

#### 4. Analyser la tendance et non le point

L'objet de F1 est une trajectoire, pas une photographie. Pour chaque poste significatif, présentez la variation en dollars et en pourcentage entre les exercices, puis interprétez le sens du mouvement plutôt que son ampleur seule. Une hausse de 18 % des ventes accompagnée d'une baisse de 4 points de marge brute et d'un allongement de 22 jours du délai de recouvrement raconte une croissance achetée par des concessions de prix et de conditions, ce qu'aucun des trois chiffres ne dit isolément.

Cherchez systématiquement les divergences entre postes qui devraient évoluer ensemble : ventes et comptes clients, ventes et stocks, masse salariale et volume produit, immobilisations et amortissement. Un poste stable au dollar près sur trois exercices est presque toujours une estimation reconduite plutôt qu'une mesure, et mérite une question écrite. Distinguez enfin ce qui relève d'un effet de volume, d'un effet de prix et d'un effet de mixte : trois causes qui appellent trois conclusions différentes sur la pérennité de la performance.

#### 5. Décomposer la marge brute et les charges fixes contre variables

Reconstituez la marge brute et vérifiez d'abord que la ventilation entre coût des ventes et frais généraux est identique d'un exercice à l'autre ; sinon, retraitez avant de comparer. Décomposez ensuite la structure de coûts en charges fixes, variables et semi-variables, en résistant à la tentation de classer en fixe tout ce qui ne bouge pas d'un exercice à l'autre. Une charge semi-variable mal classée fausse à la fois le seuil de rentabilité et tous les scénarios de tension de F3 ; ce classement se documente ligne par ligne du grand livre pour les postes matériels, et non par intuition.

Calculez le seuil de rentabilité et exprimez la distance entre les ventes réelles et ce seuil en pourcentage : c'est le coussin d'exploitation, et c'est l'un des trois ou quatre chiffres que le comité retiendra. Vérifiez la sensibilité de la structure : dans une entreprise à fortes charges fixes, un recul de revenus de 10 % peut effacer la totalité du bénéfice, et ce constat doit être écrit noir sur blanc plutôt que laissé au lecteur. Le travail est complet lorsque l'on peut répondre sans recalculer à la question « à partir de quel niveau de ventes l'entreprise perd-elle de l'argent ».

#### 6. Rapprocher le bénéfice net et l'encaisse

Une entreprise rentable au sommaire des résultats peut être en détresse de trésorerie, et c'est précisément ce que ce rapprochement met au jour. Partez du bénéfice net, ajoutez l'amortissement, retirez la variation du fonds de roulement hors trésorerie, retirez les investissements, ajoutez le financement net obtenu, et vérifiez que le résultat correspond à la variation réelle de l'encaisse au bilan. Lorsque le bénéfice se convertit mal en trésorerie sur plusieurs exercices, cherchez la cause du côté des comptes clients qui s'allongent, des stocks qui gonflent, d'un chantier en cours non facturé ou d'une croissance qui consomme mécaniquement du fonds de roulement.

Mesurez le taux de conversion sur trois exercices plutôt que sur un seul, un exercice isolé pouvant refléter un simple décalage de facturation. Vérifiez au passage l'utilisation moyenne de la marge de crédit et non seulement son solde à la date de clôture : un solde nul au dernier jour de l'exercice peut masquer une marge saturée onze mois sur douze. C'est ce rapprochement qui alimente directement le flux disponible au service de la dette calculé en F3 ; le bâcler ici revient à fabriquer un ratio de couverture flatteur plus loin.

#### 7. Lever les drapeaux rouges et formuler les questions au promoteur

Terminez par une liste de signaux d'alerte cotés, chacun formulé en une phrase factuelle, avec sa source, son ampleur chiffrée et son degré de gravité. Les signaux qui reviennent le plus souvent : avoir des actionnaires négatif, avances d'actionnaires non postposées traitées comme de l'équité, concentration de la clientèle, comptes clients de plus de 90 jours sans provision, stocks croissant plus vite que les ventes, comptes gouvernementaux en retard, retraits d'actionnaires supérieurs au bénéfice, et engagements financiers déjà en défaut technique auprès d'un autre prêteur.

Cotez chaque signal plutôt que de les empiler à plat, sinon le lecteur ne saura pas lesquels commandent une condition et lesquels relèvent du bruit. Chaque signal non expliqué par le dossier doit produire une question écrite et datée au promoteur, jamais une hypothèse comblée par l'analyste. Un dossier sans aucun signal d'alerte est un dossier mal lu ou une entreprise exceptionnelle : dans les deux cas, il faut le dire explicitement plutôt que de laisser la section vide.

### Sorties

- Tableau des trois exercices retraités, avec la ligne de rapprochement entre chiffres publiés et chiffres retenus.
- Grille de ratios sur trois exercices, avec repères sectoriels lorsqu'ils sont documentés, datés et sourcés.
- Décomposition de la structure de coûts et seuil de rentabilité avec le coussin d'exploitation exprimé en pourcentage.
- Rapprochement du bénéfice et de l'encaisse sur la période, avec l'utilisation moyenne de la marge de crédit.
- Liste des signaux d'alerte cotés, chacun rattaché à sa pièce source.
- Questions ouvertes au promoteur, numérotées et datées.
- Niveau d'assurance déclaré pour chaque source financière utilisée.

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Comparer des exercices de durée inégale | La tendance lue est un artefact de calendrier ; croissance ou décroissance fictive | Vérifier la durée de chaque exercice au premier tableau ; annualiser ou écarter avec mention explicite |
| Utiliser le BAIIA non normalisé comme mesure de performance | Le levier et la capacité de remboursement sont faussés par la rémunération du propriétaire | Exiger le tableau de normalisation avant toute lecture de rentabilité, chaque ajustement portant sa source |
| Confondre bénéfice et liquidité | Une entreprise en tension de trésorerie est présentée comme saine | Produire le rapprochement bénéfice-encaisse sur les trois exercices et l'utilisation moyenne de la marge |
| Ignorer les avances d'actionnaires et les soldes de prix de vente | L'endettement réel est sous-déclaré et le rang des sûretés est mal établi en F2 | Recenser toutes les dettes envers des parties liées et vérifier l'existence d'une convention de postposition signée |
| Lire un ratio de fin d'exercice choisi au creux du cycle | La liquidité apparente ne reflète pas la réalité des douze mois | Recouper avec les états intérimaires et l'utilisation mensuelle de la marge de crédit |
| Accepter la ventilation du comptable sans la retraiter | Les marges des trois exercices ne sont pas comparables entre elles | Reclasser dans une nomenclature stable imposée par l'analyste et documenter chaque reclassement |

### Formules mobilisées

| Clé | Formule | Seuil indicatif |
|---|---|---|
| RATIO_FDR | Ratio = Actif à court terme / Passif à court terme | ≥ 1,25 ; ≥ 1,50 en secteur saisonnier (indicatif) |
| FDR | FDR = Actif à court terme - Passif à court terme | Positif et croissant avec le chiffre d'affaires (indicatif) |
| LIQ_IMM | Ratio = (Encaisse + Comptes clients) / Passif à court terme | ≥ 1,00 pour une entreprise de services ; ≥ 0,80 en distribution (indicatif) |
| DETTE_BAIIA | Levier = Dette portant intérêt totale / BAIIA normalisé | ≤ 3,0 x pour une PME manufacturière ; ≤ 4,0 x avec actifs tangibles importants (indicatif) |
| DETTE_AVOIR | Ratio = Passif total / Avoir des actionnaires | ≤ 3,0 selon le secteur ; à interpréter avec l'intensité capitalistique (indicatif) |
| MARGE_BRUTE | Marge = (Ventes - Coût des ventes) / Ventes | Comparer au repère sectoriel plutôt qu'à un seuil absolu (indicatif) |
| SEUIL_RENT | Seuil = Charges fixes / Taux de marge sur coûts variables | Aucun seuil ; mesure du coussin d'exploitation |
| CYCLE_CONV | Cycle = DSO + DIO - DPO | Comparer au repère sectoriel (indicatif) |
| DSO | DSO = (Comptes clients / Ventes à crédit) x 365 | Comparer aux conditions de vente accordées (indicatif) |
| BAIIA_NORM | BAIIA normalisé = BAIIA publié ± ajustements de normalisation | Aucun seuil ; chaque ajustement doit porter sa source |

Tous les seuils de cette table proviennent de `data/formules.csv` et y portent le statut indicatif : ce sont des repères de marché servant à situer l'entreprise, jamais des exigences de la politique d'investissement du DÉPS. Lorsqu'un ratio s'écarte du repère, la question à poser est celle de la cause et non celle de la conformité.

## F2 — montage-financier

**Objectif.** Structurer le tour de financement complet du projet — coût total, sources, rangs de sûretés et effet de levier — de façon bancable et conforme aux politiques. F2 doit permettre à un tiers de reconstituer, au dollar près, d'où vient chaque dollar et où il va.

**Entrées requises.**
- Coût de projet ventilé poste par poste et documenté : soumissions, offres d'achat, devis, contrats, évaluations d'immeubles ou d'équipements.
- Mise de fonds disponible, avec sa provenance vérifiable : relevés bancaires, lettre d'engagement, produit d'une vente d'actif, apport en nature évalué de façon indépendante.
- Lettres d'intérêt ou offres de financement des autres prêteurs, avec leurs conditions, leurs sûretés demandées et leur date de validité.
- Programmes, subventions et crédits d'impôt visés, avec le statut réel de chaque demande : non déposée, déposée, en analyse, confirmée par écrit.
- Inventaire des garanties disponibles et de celles déjà grevées, avec les rangs existants aux registres publics applicables.
- Verdict d'admissibilité de P1 et liste des dépenses admissibles retenues.
- Portrait financier F1, notamment le cycle de conversion de trésorerie et le BAIIA normalisé.
- Échéancier de réalisation du projet et calendrier des engagements contractuels déjà pris.

### Méthode

#### 1. Établir le tableau Sources et Emplois qui balance au dollar près

Le tableau Sources et Emplois est la colonne vertébrale du montage : à gauche, tous les emplois, c'est-à-dire le coût total du projet ; à droite, toutes les sources, c'est-à-dire tous les financements. L'équilibre exigé est strict et sans tolérance : un écart, même de quelques centaines de dollars, signale un poste oublié ou un double emploi, jamais une simple imprécision. Ce contrôle porte le statut bloquant au registre des formules, ce qui signifie qu'un dossier qui ne balance pas ne franchit pas la porte de sortie du module.

Ne faites jamais balancer artificiellement le tableau avec un poste « divers » ou « autres » : un tel poste est le symptôme d'un montage incomplet, pas sa solution. Présentez le tableau avec les montants et les pourcentages du coût total, car c'est cette colonne de pourcentages qui rend immédiatement lisibles la mise de fonds, le levier public et la part assumée par chaque prêteur. Le contrôle Q1 refera ce calcul de façon indépendante, et tout écart détecté est renvoyé à la source plutôt que corrigé dans le livrable.

#### 2. Valider chaque poste du coût de projet par une pièce

Chaque ligne des emplois doit renvoyer à une pièce nommée et datée : une soumission avec sa date de validité, une offre d'achat acceptée, un devis d'ingénieur, une évaluation agréée. Un montant fourni verbalement par le promoteur ou estimé par l'analyste demeure une estimation et doit être identifié comme telle dans la colonne des sources. Vérifiez la date de validité des soumissions : une soumission d'équipement vieille de plusieurs mois, dans un contexte de variation des coûts ou des taux de change, ne soutient plus le montant qu'elle porte.

Portez une attention particulière au traitement des taxes : les taxes récupérables ne font pas partie du coût de projet financé, et les inclure gonfle artificiellement le besoin de financement et la mise de fonds requise. Vérifiez enfin que les postes correspondent aux dépenses jugées admissibles en P1, un poste admissible au financement bancaire pouvant être exclu des dépenses admissibles du fonds. Un travail rigoureux se reconnaît à ce que chaque dollar du coût de projet porte le nom du document qui le justifie.

#### 3. Vérifier la mise de fonds minimale exigée et sa nature

La mise de fonds se mesure comme la part des promoteurs dans le coût total du projet, mais l'enjeu réel est sa nature autant que son montant. Le taux exigé est un paramètre de politique (`MISE_FONDS_MIN`, à valider contre la politique en vigueur) et ne doit jamais être cité de mémoire ni repris d'un dossier antérieur. Les formes d'apport reconnues sont elles aussi un paramètre de politique (`FORMES_MISE_FONDS`, à valider) : une subvention, un apport en nature, un bilan de départ ou une avance d'actionnaire ne sont pas automatiquement admis comme mise de fonds, et ce point est un motif fréquent de refus tardif.

Un apport en nature doit être évalué de façon indépendante et non à la valeur déclarée par le promoteur, et la provenance des liquidités doit être documentée. Vérifiez que la mise de fonds est effectivement disponible à la date prévue du décaissement et non conditionnelle à la vente d'un actif encore à vendre. Lorsque la mise de fonds provient d'un emprunt personnel du promoteur, l'effet de levier réel du groupe est supérieur à celui que montre le montage, et ce constat doit apparaître au dossier.

#### 4. Attribuer chaque source à son rang de sûreté

Dressez la liste des sûretés demandées par chaque prêteur — sur quel actif, en quel rang — et confrontez-la aux charges déjà inscrites. Le double comptage d'une même garantie est le défaut classique : deux prêteurs qui croient tous deux détenir une première charge sur le même équipement produisent un conflit qui n'apparaîtra qu'au moment de la réalisation. Vérifiez l'existence des charges antérieures aux registres publics plutôt que de vous fier à la déclaration du promoteur, et recensez les crédits-bails, qui laissent la propriété au bailleur et retirent l'actif de l'assiette de garantie.

Lorsque plusieurs prêteurs interviennent, identifiez dès cette étape les conditions inter-prêteurs à négocier : partage de rang, convention de subordination, priorité sur les comptes clients et les stocks, mécanisme applicable en cas de défaut. Les exigences de garanties et de cautionnement applicables aux fonds relèvent de la politique (`GARANTIES_EXIGEES`, à valider contre la politique en vigueur) et doivent être reprises telles quelles, y compris pour ce qui touche le cautionnement personnel des promoteurs et son étendue. Un montage qui ne dit pas qui prend quoi en garantie, et en quel rang, n'est pas terminé.

#### 5. Tester l'effet de levier

Une fois les sources arrêtées, mesurez l'endettement projeté après réalisation du projet et non l'endettement historique : c'est le bilan d'après qui doit tenir. Calculez le levier comme la dette portant intérêt totale sur le BAIIA normalisé, en incluant les crédits-bails et en excluant les avances d'actionnaires uniquement lorsqu'une convention de postposition signée existe. Calculez également le ratio du passif total sur l'avoir des actionnaires, en gardant à l'esprit qu'un avoir négatif rend ce ratio ininterprétable et qu'il faut alors l'écrire plutôt qu'afficher un nombre dépourvu de sens.

Les repères de 3,0 x et de 4,0 x issus du registre des formules sont indicatifs et sectoriels, et ne constituent pas des limites de politique du DÉPS. Lorsque le levier projeté dépasse nettement le repère, le montage doit être retravaillé — davantage de capitaux propres, étalement des investissements, apport en subvention confirmée — plutôt que défendu par des hypothèses de croissance. Ce test demeure un test de structure : il ne remplace pas le test de flux de F3, et l'un peut passer pendant que l'autre échoue.

#### 6. Réserver un fonds de roulement et une contingence explicites

Le fonds de roulement de démarrage et la contingence sont les deux postes les plus souvent absents des montages, et les deux causes les plus fréquentes de retour en défaut dans les douze premiers mois. Le fonds de roulement se calcule à partir du cycle de conversion de trésorerie établi en F1 et du niveau d'activité projeté : plus le cycle est long et la croissance rapide, plus le besoin est élevé. La contingence n'est pas une politesse : pour tout projet de construction, d'aménagement ou d'installation d'équipement, elle doit figurer explicitement au coût de projet, à un pourcentage justifié par la nature et la complexité des travaux.

Ces deux postes se placent du côté des emplois, ce qui augmente le coût total et donc la mise de fonds requise en dollars — c'est précisément pour cette raison qu'ils sont escamotés, et précisément pour cette raison qu'il faut les exiger. Une contingence non utilisée se retourne en réduction du financement au décaissement final ; un fonds de roulement absent se retourne en marge de crédit saturée et en défaut. Documentez le calcul des deux plutôt que de retenir un pourcentage sans justification écrite.

#### 7. Séquencer les décaissements selon l'avancement du projet

Le montage n'est complet qu'accompagné d'un échéancier précisant quand chaque source entre et contre quelle preuve d'avancement. La règle de séquence est que la mise de fonds des promoteurs se décaisse en premier ou au prorata, jamais en dernier : un promoteur qui n'a rien engagé n'a rien à perdre. Rattachez chaque tranche à une pièce vérifiable — facture acquittée, certificat d'avancement, confirmation écrite de la subvention, preuve de prise de possession — et non à une date de calendrier.

Alignez la séquence sur les conditions des autres prêteurs, faute de quoi deux financements peuvent s'attendre mutuellement et bloquer le projet. Prévoyez la retenue applicable aux travaux de construction et le moment de sa libération. Rappelez enfin que le délai de validité de l'offre de financement est un paramètre de politique (`DELAI_VALIDITE_OFFRE`, à valider contre la politique en vigueur) et qu'il fixe la date limite de réalisation des conditions préalables au décaissement.

### Sorties

- Tableau Sources et Emplois balancé, avec la colonne des pourcentages du coût total et la colonne des pièces justificatives.
- Coût total du projet ventilé, incluant fonds de roulement de démarrage et contingence explicites.
- Structure de sûretés par actif, par prêteur et par rang, confrontée aux charges existantes.
- Échéancier de décaissement rattaché à des preuves d'avancement vérifiables.
- Liste des conditions inter-prêteurs à négocier.
- Taux de mise de fonds calculé, avec la nature de chaque apport.
- Statut écrit de chaque source : confirmée, en analyse, non déposée.
- Levier projeté après réalisation du projet, calculé sur le bilan d'après.

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Sources et emplois qui ne balancent pas | Un poste est oublié ou compté deux fois ; tout le montage aval est faux | Contrôle bloquant : écart de zéro exigé, revérifié indépendamment par Q1 |
| Contingence absente | Le premier imprévu de chantier se finance par la marge de crédit ou ne se finance pas | Exiger une ligne de contingence chiffrée et justifiée pour tout projet de construction ou d'aménagement |
| Fonds de roulement de démarrage oublié | Trésorerie négative dès les premiers mois malgré un projet réalisé | Calculer le besoin à partir du cycle de conversion de F1 et l'inscrire aux emplois |
| Subvention comptabilisée avant confirmation écrite | Le montage s'effondre si l'aide est refusée ou réduite | N'inscrire au scénario de base que les aides confirmées par écrit ; les autres en scénario seulement |
| Double comptage d'une même garantie | Conflit de rang découvert au moment de la réalisation, perte de la sûreté | Vérifier les charges existantes aux registres publics et dresser la matrice actif-prêteur-rang |
| Taxes récupérables incluses au coût de projet | Besoin de financement et mise de fonds requise surévalués | Valider le traitement fiscal poste par poste avec les pièces justificatives |

### Formules mobilisées

| Clé | Formule | Seuil indicatif |
|---|---|---|
| SOURCES_EMPLOIS | Somme des sources = Somme des emplois | Écart de zéro exigé (statut bloquant) |
| COUT_TOTAL_PROJET | Coût total = Immobilisations + Améliorations locatives + Équipements + Stocks de départ + Fonds de roulement + Frais professionnels + Contingence | Contingence prévue pour tout projet de construction ou d'aménagement (indicatif) |
| MISE_FONDS | Taux = Mise de fonds / Coût total du projet | Selon la politique en vigueur (paramètre `MISE_FONDS_MIN`, statut A_VALIDER) |
| DETTE_BAIIA | Levier = Dette portant intérêt totale / BAIIA normalisé | ≤ 3,0 x pour une PME manufacturière ; ≤ 4,0 x avec actifs tangibles importants (indicatif) |
| DETTE_AVOIR | Ratio = Passif total / Avoir des actionnaires | ≤ 3,0 selon le secteur ; à interpréter avec l'intensité capitalistique (indicatif) |
| FDR | FDR = Actif à court terme - Passif à court terme | Positif et croissant avec le chiffre d'affaires (indicatif) |

Deux statuts cohabitent dans cette table et ne se traitent pas de la même façon. L'équilibre Sources et Emplois est bloquant : il n'admet aucune tolérance et suspend la sortie du module. Le taux de mise de fonds renvoie à un paramètre de politique au statut A_VALIDER : il se calcule toujours, mais son appréciation exige la politique en vigueur, jamais une valeur de mémoire.

## F3 — capacite-remboursement

**Objectif.** Démontrer par les flux de trésorerie que l'entreprise peut servir la dette projetée, et mesurer la marge de sécurité avant défaut. F3 répond à la seule question qui compte pour un prêteur : l'entreprise pourra-t-elle payer, et à partir de quel écart cessera-t-elle de pouvoir payer.

**Entrées requises.**
- Prévisionnel de trésorerie mensuel sur 12 à 24 mois, bâti sur les encaissements et décaissements réels et non sur le résultat comptable réparti en douze.
- États prévisionnels sur 2 à 3 ans, accompagnés de la liste écrite des hypothèses de volume, de prix, de marge et de charges.
- Échéanciers de toutes les dettes existantes et projetées : prêts à terme, marges, crédits-bails, prêts de parties liées, soldes de prix de vente, ententes de paiement fiscales.
- Retraits prévus des actionnaires : salaires, bonis, dividendes, remboursements d'avances, avantages.
- Programme d'investissements de maintien nécessaire au maintien de la capacité de production actuelle, distinct des investissements de croissance du projet.
- Tableau de normalisation du BAIIA, chaque ajustement portant sa source.
- Montage F2 arrêté, avec le service de la dette qui en découle.
- Historique de saisonnalité et d'utilisation de la marge de crédit établi en F1.

### Méthode

#### 1. Reconstituer le flux de trésorerie disponible au service de la dette

Partez du BAIIA normalisé et retirez successivement les impôts payés en trésorerie, les investissements de maintien, la variation du fonds de roulement et les retraits des actionnaires. Chacune de ces déductions est régulièrement escamotée, et chacune gonfle le ratio de couverture lorsqu'elle l'est. Les investissements de maintien ne sont pas les investissements de croissance : ce sont les dépenses nécessaires pour que l'entreprise continue de produire au niveau actuel, et une PME manufacturière qui déclare aucun investissement de maintien sur trois ans est en train de décapitaliser son parc d'équipements.

La variation du fonds de roulement est le poste le plus sous-estimé en phase de croissance : une entreprise qui croît de 25 % immobilise mécaniquement du capital dans ses comptes clients et ses stocks, et cet argent n'est pas disponible pour payer les prêteurs. Les retraits d'actionnaires jugés discrétionnaires ne peuvent être retirés du calcul que s'il existe un engagement écrit de limitation, sans quoi ils constituent une sortie de fonds réelle. Le calcul doit être présenté ligne par ligne, chaque déduction étant visible, plutôt que résumé en un nombre unique que personne ne peut vérifier.

#### 2. Additionner le service total de la dette

Le service de la dette est la somme du capital et des intérêts de toutes les dettes de l'exercice, sans exception. L'oubli le plus fréquent est le crédit-bail, souvent traité comme une charge d'exploitation alors qu'il constitue un financement d'actif dont les versements grèvent la trésorerie exactement comme un prêt. Doivent aussi y figurer les intérêts sur la marge de crédit selon son utilisation moyenne, les remboursements de prêts de parties liées non postposés, les soldes de prix de vente en cours de remboursement et les ententes de paiement fiscales.

Additionnez la dette existante et la dette projetée : le ratio se calcule sur la situation d'après-projet, jamais sur celle d'avant. Prenez le service tel qu'il tombe dans chaque exercice, en tenant compte des versements ballons, des congés de capital qui se terminent et des versements progressifs en cours de terme. Un service de la dette sous-déclaré produit un ratio de couverture dépourvu de valeur, et c'est une erreur que le contrôle Q1 est explicitement chargé de détecter.

#### 3. Calculer le ratio de couverture du service de la dette par exercice

Le ratio se calcule en divisant le flux disponible par le service total, et il se présente pour chaque exercice de l'horizon, jamais pour la seule première année. Le repère de marché documenté est de 1,25 ou plus pour une PME établie et de 1,35 ou plus en démarrage ou en secteur cyclique ; ces valeurs sont indicatives. Le seuil minimal exigé par le DÉPS, s'il en existe un, est un paramètre de politique (`RCD_MINIMAL`, à valider contre la politique en vigueur) : en son absence, présentez explicitement le repère du marché comme un repère et non comme une exigence institutionnelle.

À 1,00, l'entreprise paie ses versements sans aucune marge ; sous 1,00, elle puise dans ses réserves ou dans sa marge de crédit, ce qui n'est pas un remboursement mais un report. Ne calculez jamais la couverture sur le bénéfice net : celui-ci est net de l'amortissement, qui n'est pas une sortie de fonds, et brut des remboursements de capital, qui en sont une. Présentez le ratio avec deux décimales au maximum et rappelez sur quelle définition de flux il est bâti.

#### 4. Appliquer les scénarios : base, prudent, tension

Un ratio calculé sur un scénario unique n'est qu'une hypothèse bien présentée. Le scénario de base reprend les hypothèses du promoteur telles quelles ; le scénario prudent corrige celles que l'historique de F1 ne soutient pas ; le scénario de tension applique un choc défendable et documenté sur les variables les plus sensibles, généralement le volume, le prix de vente ou le coût des intrants. Choisissez les variables du choc à partir de la structure de coûts établie en F1 : dans une entreprise à fortes charges fixes, c'est le volume qui fait mal ; dans une entreprise à forte composante de matières, c'est le prix des intrants.

Chaque scénario produit son propre ratio de couverture par exercice, les trois séries étant présentées côte à côte dans un même tableau. Le scénario prudent n'est pas une décoration : c'est celui sur lequel la recommandation devrait s'appuyer lorsque les hypothèses du promoteur s'écartent nettement de son historique. Documentez le pourcentage de choc appliqué et sa justification, sans quoi le scénario de tension devient un exercice arbitraire que le comité ne pourra pas apprécier.

#### 5. Calculer le seuil de rupture

Le seuil de rupture exprime en pourcentage la baisse des flux disponibles qui ramène le ratio de couverture à 1,00 ; c'est la mesure la plus directe de la marge de sécurité et l'un des chiffres les plus utiles à présenter au comité. Le calcul porte sur les flux et non sur les revenus, distinction essentielle parce que les charges fixes amplifient l'effet d'une baisse de revenus. Une entreprise dont les flux peuvent reculer de 20 % avant rupture peut n'absorber qu'une baisse de revenus bien moindre si son levier d'exploitation est élevé ; les deux chiffres se présentent ensemble, avec la mention explicite de ce qui est mesuré.

Traduisez ensuite le seuil en langage d'exploitation : la perte de tel client, la baisse de tel prix, la hausse de tel intrant. Ce chiffre alimente directement la cotation du risque financier en F4. Un seuil de rupture faible ne bloque pas nécessairement un dossier, mais il commande des conditions et des engagements plus serrés, et il doit être énoncé franchement plutôt que dilué dans le texte.

#### 6. Vérifier la trésorerie plancher mensuelle et le besoin de marge de crédit

Le ratio annuel peut être conforme pendant que l'entreprise manque de liquidités au troisième mois. Reprenez le prévisionnel mensuel, cumulez le solde de trésorerie mois par mois et identifiez le creux : c'est ce plancher, et non la moyenne, qui détermine le besoin de marge de crédit. Vérifiez que la marge autorisée existante couvre ce creux avec une réserve, et que la base d'emprunt de la marge — comptes clients admissibles et stocks selon les règles du prêteur — soutient effectivement le tirage nécessaire au moment où il est requis.

Tenez compte de la saisonnalité réelle établie en F1 : ignorer la saisonnalité en ne regardant que l'annuel est le piège le plus commun du module. Vérifiez également le décalage entre les décaissements du projet et l'entrée des subventions, qui arrivent souvent après la réalisation des dépenses et créent un besoin de financement intérimaire. Concluez par un besoin de marge chiffré et daté, plutôt que par une mention générale de suffisance.

#### 7. Conclure sur le terme, l'amortissement et le congé de capital requis

La conclusion de F3 n'est pas un verdict binaire mais une recommandation de structure de remboursement. L'amortissement doit correspondre à la durée de vie utile de l'actif financé : amortir un équipement sur une durée supérieure à sa vie utile revient à financer son remplacement avec la dette du précédent. Les durées maximales de terme et d'amortissement sont des paramètres de politique (`TERME_MAX` et `AMORTISSEMENT_MAX`, à valider contre la politique en vigueur), et le fait qu'une durée soit permise ne signifie pas qu'elle soit indiquée.

Le congé de capital se justifie par la courbe de trésorerie et par elle seule : lorsque le prévisionnel montre un creux au démarrage suivi d'une remontée, le congé a un sens ; lorsqu'il sert à faire passer un ratio de couverture autrement insuffisant, il déplace le problème vers l'exercice suivant. Sa durée maximale est également un paramètre de politique (`CONGE_CAPITAL_MAX`, à valider). Rappelez enfin qu'un congé de capital augmente le total des intérêts payés et donc le coût effectif de l'emprunt, ce que la tarification P2 devra intégrer, et que la couverture devra être recalculée une fois la tarification arrêtée.

### Sorties

- Tableau du flux de trésorerie disponible au service de la dette, présenté ligne par ligne, par exercice.
- Service de la dette total par exercice, toutes sources incluses, existant et projeté.
- Ratio de couverture par exercice et par scénario : base, prudent, tension.
- Hypothèses de choc retenues pour le scénario de tension, avec leur justification.
- Seuil de rupture exprimé en pourcentage des flux, et sa traduction en langage d'exploitation.
- Besoin de marge de crédit chiffré et daté, établi à partir du creux de trésorerie mensuel.
- Recommandation de terme, d'amortissement et de congé de capital, justifiée par la courbe de trésorerie.

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Oublier les investissements de maintien | Le flux disponible est surévalué et l'entreprise décapitalise son parc d'actifs | Exiger le programme d'investissements de maintien et retenir l'amortissement historique comme repère minimal |
| Omettre les retraits des actionnaires | Une sortie de fonds réelle est absente du calcul de couverture | Recenser salaires, bonis, dividendes et remboursements d'avances ; ne les exclure que contre engagement écrit de limitation |
| Utiliser le BAIIA publié plutôt que normalisé | La rentabilité récurrente est faussée par la rémunération du propriétaire et les éléments non récurrents | Exiger le tableau de normalisation avec la source de chaque ajustement |
| Calculer la couverture sur le bénéfice net | Le ratio ne mesure plus rien : l'amortissement et le capital y sont mal traités | Contrôle Q1 : vérifier que le numérateur est bien le flux disponible et non le bénéfice |
| Ignorer la saisonnalité en ne regardant que l'annuel | Un ratio annuel conforme masque une rupture de trésorerie en cours d'exercice | Analyser le prévisionnel mensuel et présenter le creux de trésorerie |
| Omettre le crédit-bail du service de la dette | Le service est sous-déclaré et le ratio de couverture surévalué | Recenser tous les contrats de location-acquisition et les ajouter au service |

### Formules mobilisées

| Clé | Formule | Seuil indicatif |
|---|---|---|
| RCD | RCD = FTDSD / SDT | ≥ 1,25 pour une PME établie ; ≥ 1,35 en démarrage ou en secteur cyclique (indicatif) |
| FTDSD | FTDSD = BAIIA normalisé - impôts en trésorerie - investissements de maintien - variation du fonds de roulement - retraits des actionnaires | Aucun seuil |
| SEUIL_RUPT | Baisse tolérée = (FTDSD - SDT) / FTDSD | Aucun seuil ; mesure directe de la marge de sécurité |
| BAIIA_NORM | BAIIA normalisé = BAIIA publié ± ajustements de normalisation | Aucun seuil ; chaque ajustement doit porter sa source |
| SEUIL_RENT | Seuil = Charges fixes / Taux de marge sur coûts variables | Aucun seuil ; distance entre le seuil et les ventes réelles égale au coussin d'exploitation |
| CYCLE_CONV | Cycle = DSO + DIO - DPO | Comparer au repère sectoriel (indicatif) |

Le repère de 1,25 et celui de 1,35 sont des repères de marché consignés dans `data/formules.csv` au statut indicatif. Le seuil exigible par le DÉPS relève du paramètre `RCD_MINIMAL`, encore au statut A_VALIDER : tant qu'il n'est pas renseigné, un livrable ne peut affirmer qu'un ratio est conforme à la politique, seulement qu'il se situe au-dessus ou au-dessous du repère du marché.

## F4 — analyse-risque

**Objectif.** Identifier, coter et atténuer les risques du dossier de façon structurée, et traduire chaque risque résiduel en condition de financement. F4 est le module qui transforme une inquiétude d'analyste en clause opposable.

**Entrées requises.**
- Analyse financière F1 et capacité de remboursement F3 complétées, avec leurs signaux d'alerte et leur seuil de rupture.
- Profil des promoteurs : parcours, expérience du secteur, historique de crédit, autres entreprises détenues, engagements personnels existants.
- Structure de l'actionnariat, convention entre actionnaires, mécanisme de résolution des différends et clauses de retrait.
- Contexte sectoriel et concurrentiel issu de l'analyse sectorielle D2, avec ses repères de performance et ses vents contraires.
- Contrats et dépendances clés : contrats clients, ententes de distribution, baux, licences, fournisseurs uniques.
- Couverture d'assurance en vigueur : biens, responsabilité, interruption des affaires, assurance des personnes clés.
- Autorisations, permis et certificats requis pour le projet, avec leur statut.
- Historique de litiges, de réclamations et de conformité environnementale des lieux visés.

### Méthode

#### 1. Balayer les cinq catégories de risque

Le balayage est systématique et couvre cinq catégories : marché, opérationnel, financier, promoteur et gouvernance, conformité et environnement. La méthode par catégories existe précisément pour empêcher l'analyste de ne voir que les risques qui l'inquiètent spontanément : un analyste de formation comptable trouvera les risques financiers et manquera les risques opérationnels, et inversement. Aucune catégorie ne peut rester vide sans une phrase expliquant pourquoi.

Le risque de marché couvre la demande, la concurrence, la concentration de la clientèle, la substitution et le cycle sectoriel. Le risque opérationnel couvre la capacité de production, la main-d'oeuvre disponible, la chaîne d'approvisionnement, les équipements critiques et la dépendance à un site unique. Le risque financier reprend les constats de F1 et F3 : levier, liquidité, seuil de rupture, qualité des comptes clients. Le risque promoteur et gouvernance couvre l'expérience, la relève, la dépendance à une personne clé, la mésentente potentielle entre actionnaires et la qualité de l'information de gestion. Le risque de conformité et d'environnement couvre les autorisations requises, la contamination potentielle d'un terrain, les normes applicables et les litiges en cours.

#### 2. Coter chaque risque en probabilité et en impact

Chaque risque identifié reçoit deux cotes distinctes : la probabilité qu'il se matérialise et l'impact qu'il aurait sur la capacité de remboursement s'il se matérialisait. La séparation des deux dimensions est ce qui rend la matrice utile : un risque très probable et de faible impact n'appelle pas le même traitement qu'un risque peu probable et fatal. Utilisez une échelle courte et stable d'un dossier à l'autre, et écrivez le critère qui distingue chaque niveau plutôt que de coter à l'instinct.

Le défaut le plus fréquent consiste à coter tous les risques comme moyens : une matrice uniformément moyenne ne hiérarchise rien et ne guide aucune décision. Obligez-vous à identifier explicitement les deux ou trois risques les plus élevés du dossier et à les nommer comme tels dans la note. Lorsque c'est possible, ancrez l'impact dans un chiffre issu de F3 : la perte du principal client fait passer le ratio de couverture de tel niveau à tel autre, formulation infiniment plus utile qu'une cote abstraite.

#### 3. Documenter le mitigant existant et son efficacité réelle

Pour chaque risque, décrivez ce qui existe déjà pour l'atténuer, puis évaluez si cela fonctionne réellement. Un mitigant est une mesure en place, vérifiable et opposable : un contrat signé, une police d'assurance en vigueur avec sa couverture et sa franchise, une seconde source d'approvisionnement déjà qualifiée, une réserve de trésorerie constituée. Ce qui n'est pas un mitigant : une intention, un projet de diversification, une confiance dans le promoteur, une déclaration verbale.

Le mitigant doit être proportionné au risque qu'il couvre : une assurance sur la personne clé dont le montant ne couvre qu'une fraction du solde du prêt atténue partiellement, pas totalement. Vérifiez aussi l'exécutabilité réelle : un contrat client de trois ans résiliable sur préavis de trente jours n'est pas un contrat de trois ans. Confondre un mitigant et un voeu pieux est l'erreur qui coûte le plus cher au portefeuille, parce qu'elle produit des dossiers qui paraissent couverts et ne le sont pas.

#### 4. Isoler le risque résiduel après mitigant

Le risque résiduel est ce qui subsiste une fois le mitigant appliqué, et c'est la seule colonne qui compte pour la décision. Présentez-la explicitement plutôt que de laisser le lecteur soustraire lui-même le mitigant du risque initial. Un risque élevé fortement atténué peut devenir acceptable ; un risque moyen sans mitigant réel reste entier et peut peser davantage sur la décision.

Recotez le résiduel avec la même échelle que le risque brut, de façon que la matrice se lise en trois colonnes cohérentes : brut, mitigant, résiduel. Vérifiez la corrélation entre risques : plusieurs risques individuellement moyens qui se déclenchent ensemble à la faveur d'un même événement — un ralentissement sectoriel frappant simultanément le volume, le prix et le délai de recouvrement — produisent un impact combiné supérieur à leur somme apparente. C'est cette lecture combinée qui doit être rapprochée du seuil de rupture calculé en F3.

#### 5. Traduire chaque risque résiduel significatif en condition, garantie ou engagement

C'est ici que F4 devient utile plutôt que descriptif. Chaque risque résiduel significatif doit produire une contrepartie concrète : une condition préalable au décaissement, une garantie additionnelle, un engagement de faire ou de ne pas faire pendant la durée du prêt. La règle de rédaction est la vérifiabilité : une condition doit pouvoir être constatée par une pièce, à une date, par une personne autre que son rédacteur. « Obtenir une assurance de tel montant sur telle personne, cédée au prêteur, avant le premier décaissement » est une condition ; « s'assurer d'une couverture adéquate » n'en est pas une.

Les engagements de faire portent typiquement sur la remise périodique d'états financiers, le maintien d'un ratio, l'avis en cas d'événement majeur ; les engagements de ne pas faire portent sur les retraits d'actionnaires, les investissements majeurs, l'endettement additionnel, la disposition d'actifs et le changement de contrôle. Les exigences de garanties applicables relèvent de la politique (`GARANTIES_EXIGEES`, à valider contre la politique en vigueur) et ne s'improvisent pas au cas par cas. Ces conditions et engagements sont transmis tels quels à P4 pour la rédaction de la note au comité.

#### 6. Nommer explicitement les risques non atténuables assumés par le prêteur

Certains risques ne peuvent être ni éliminés ni raisonnablement atténués : un cycle sectoriel, une dépendance structurelle à un client unique dans un marché qui n'en compte que quelques-uns, la santé d'un promoteur unique dans une entreprise bâtie autour de lui. La doctrine du DÉPS est de les nommer, pas de les diluer. Écrivez-les dans une section distincte de la note, en une phrase chacun, avec l'effet estimé sur la capacité de remboursement si le risque se matérialisait.

Cette transparence remplit deux fonctions : elle permet au comité de décider en connaissance de cause plutôt que de découvrir le risque au premier défaut, et elle protège l'organisation en documentant que la décision a été prise les yeux ouverts. Un dossier peut être recommandé avec des risques non atténuables assumés ; il ne peut pas être recommandé avec des risques non atténuables passés sous silence. La cotation globale qui ressort de F4 alimente directement la prime de risque appliquée en tarification, selon la grille en vigueur (`GRILLE_PRIME_RISQUE`, à valider), et le taux ne doit jamais être fixé avant que cette cotation soit arrêtée.

### Sorties

- Matrice de risque cotée en trois colonnes : risque brut, mitigant et son efficacité, risque résiduel.
- Liste des risques résiduels significatifs, chacun rattaché à sa contrepartie.
- Conditions préalables au décaissement proposées, formulées de façon vérifiable et datable.
- Engagements de faire et de ne pas faire pendant la durée du prêt.
- Garanties requises, par actif et par rang, cohérentes avec la structure de sûretés de F2.
- Liste explicite des risques non atténuables assumés, avec leur effet estimé sur la capacité de remboursement.
- Cotation globale du dossier, transmise à la tarification P2.

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Lister des risques sans mitigant ni conséquence | La section devient descriptive et n'influence aucune condition du prêt | Exiger que chaque ligne porte un mitigant, un résiduel et une contrepartie, ou la mention explicite de leur absence |
| Coter tous les risques comme moyens | Aucune hiérarchie ; le comité ignore ce qui menace réellement le dossier | Imposer la désignation nominale des deux ou trois risques les plus élevés et ancrer l'impact dans un chiffre de F3 |
| Confondre mitigant et voeu pieux | Le dossier paraît couvert alors qu'il ne l'est pas ; perte constatée au premier défaut | N'accepter comme mitigant qu'une mesure en place, vérifiable par pièce et opposable |
| Omettre le risque de dépendance au propriétaire ou à un client unique | Le risque le plus fréquent en PME est absent de l'analyse | Vérifier systématiquement la concentration de la clientèle et la dépendance aux personnes clés dans toutes les catégories |
| Rédiger des conditions invérifiables | Les conditions ne peuvent être constatées au décaissement et deviennent inopérantes | Test de rédaction : pièce attendue, date limite, personne qui constate |
| Fixer la tarification avant la cotation | La prime de risque ne correspond plus au risque réel du dossier | Séquence imposée : F4 avant P2 ; le pipeline de dossier CIC place un contrôle humain après F4 |

### Formules mobilisées

| Clé | Formule | Seuil indicatif |
|---|---|---|
| SEUIL_RUPT | Baisse tolérée = (FTDSD - SDT) / FTDSD | Aucun seuil ; mesure directe de la marge de sécurité |

F4 mobilise peu de formules propres : sa matière première est constituée des ratios déjà calculés en F1 et en F3. Le seuil de rupture est la seule formule qui lui soit directement rattachée dans `data/formules.csv`, parce qu'il fournit l'ancrage chiffré de l'impact des risques identifiés. Chaque cote d'impact devrait, dans la mesure du possible, être exprimée en variation du ratio de couverture ou en consommation de la marge de sécurité, plutôt qu'en qualificatif seul.

## Questions au promoteur

Ces questions se posent lorsque le domaine 01 révèle une zone d'ombre. Elles se transmettent par écrit, se datent, et leurs réponses se versent au dossier comme pièces sources plutôt que d'être intégrées de mémoire à l'analyse.

**Qualité et périmètre de l'information financière**

1. Qui produit vos états financiers, à quel niveau de mission, et le mandat a-t-il changé au cours des trois derniers exercices ?
2. Existe-t-il d'autres entités liées — société de gestion, société immobilière, entreprise détenue par un actionnaire — dont les résultats influencent ceux de l'entreprise présentée ?
3. Y a-t-il eu des changements de méthode comptable, de fin d'exercice ou de ventilation entre coût des ventes et frais généraux au cours de la période analysée ?

**Rentabilité et structure de coûts**

4. Comment expliquez-vous l'évolution de votre marge brute sur les trois derniers exercices : effet de volume, de prix, de mixte de produits ou de coût des intrants ?
5. Quelles charges de votre structure sont réellement fixes à court terme, et lesquelles pourriez-vous comprimer si les ventes reculaient sensiblement ?
6. Quels éléments de vos résultats considérez-vous comme non récurrents, et quelle pièce permet de les documenter ?

**Trésorerie et fonds de roulement**

7. Quel est le solde moyen utilisé de votre marge de crédit au cours des douze derniers mois, et à quel moment de l'année atteignez-vous votre creux de trésorerie ?
8. Quelle part de vos comptes clients dépasse 90 jours, et quelles sommes sont en litige ou en recouvrement ?
9. Vos stocks comprennent-ils des articles à rotation lente ou désuets, et à quelle valeur sont-ils portés au bilan ?
10. Quels comptes gouvernementaux — taxes, retenues à la source, acomptes — accusent un retard ou font l'objet d'une entente de paiement ?

**Projet, coût et sources**

11. Chaque poste de votre coût de projet est-il appuyé par une soumission, un devis ou une offre en vigueur avec sa date de validité, et avez-vous prévu une contingence ainsi qu'un fonds de roulement de démarrage chiffrés ?
12. D'où proviennent les liquidités de votre mise de fonds, et une partie provient-elle d'un emprunt personnel ou de la vente d'un actif encore à réaliser ?
13. Quel est le statut écrit réel de chaque subvention ou crédit d'impôt inscrit au montage : non déposé, déposé, en analyse ou confirmé ?

**Dettes, garanties et engagements**

14. Pouvez-vous fournir la liste complète de vos financements — incluant les crédits-bails, les prêts d'actionnaires et les soldes de prix de vente — avec leurs échéanciers, et indiquer quels actifs sont déjà grevés d'une charge, en faveur de qui et en quel rang ?
15. Vos ententes de financement existantes comportent-elles des engagements financiers, et l'un d'eux est-il actuellement en défaut, même technique ?

**Promoteurs, gouvernance et dépendances**

16. Quelle part de votre chiffre d'affaires provient de votre principal client, et quelle serait la conséquence immédiate de sa perte ?
17. Qui pourrait diriger l'entreprise pendant une absence prolongée de la personne clé, et quelles assurances sont en vigueur sur cette personne ?
18. Quels retraits — salaires, bonis, dividendes, remboursements d'avances — prévoyez-vous effectuer au cours des vingt-quatre prochains mois, et seriez-vous disposé à les encadrer par un engagement écrit ?

## Passage au domaine suivant

Le domaine 01 remet au domaine 02-FLI-FLS quatre livrables dont dépend toute la suite : le tableau Sources et Emplois balancé et la structure de sûretés de F2, qui alimentent la vérification de conformité P3 et la finalisation du montage ; la cotation de risque de F4, sans laquelle la prime de risque de la tarification P2 ne peut être établie ; le ratio de couverture, le seuil de rupture et la courbe de trésorerie de F3, qui justifient le terme, l'amortissement et le congé de capital ; et les conditions, engagements et garanties de F4, qui deviennent les conditions préalables au décaissement rédigées en P4. Il remet au domaine 03-ÉVALUATION le portrait retraité de F1, base à partir de laquelle la normalisation du BAIIA en E1 identifie les ajustements de rémunération, de loyer avec partie liée et d'éléments non récurrents.

Le passage n'est autorisé qu'à trois conditions. Les contrôles Q1 et Q3 sont passés et consignés, c'est-à-dire que les chiffres porteurs ont été recalculés de façon indépendante et que chaque chiffre est rattaché à une source datée et de niveau déclaré. Aucun chiffre orphelin ne subsiste dans les livrables. Tout paramètre de politique encore au statut A_VALIDER qui alimente un chiffre présenté est signalé comme tel plutôt que remplacé par une valeur présumée. Enfin, la boucle de retour est explicite : lorsque la tarification arrêtée en P2 modifie le service de la dette, F2 et F3 doivent être repris avec les valeurs finales et le ratio de couverture recalculé avant que le dossier ne soit soumis au comité.
