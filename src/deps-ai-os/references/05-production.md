# 05 — PRODUCTION

Le domaine 05 transforme un contenu analytique déjà validé en artefacts remis: un artefact visuel ou interactif (R1), un sommaire exécutif d'une page (R2) et un support de présentation calibré pour une décision en séance (R3). Ces trois modules constituent la couche de mise en forme du système: ils changent la forme, la densité et le support du message, jamais le fond.

La règle d'or du domaine est absolue: la production ne réanalyse rien. Toute donnée nouvelle, tout chiffre recalculé ou toute nuance apparue pendant la mise en forme doit repartir vers son module analytique d'origine, puis repasser par le contrôle des calculs (Q1) et la validation des sources (Q3) avant de réintégrer un artefact.

## Vue d'ensemble

| Module | ID | Produit | Dépend de |
|---|---|---|---|
| ui-ux-pro-max | R1 | Artefact visuel ou interactif autonome, système de design appliqué, contrôles d'accessibilité passés | P4, E4, R2 |
| rapport-executif | R2 | Sommaire exécutif d'une page: verdict, chiffres porteurs, demande explicite | F1, F3, F4, P4, E4, D3 |
| presentation-CA | R3 | Support de présentation, déroulé chronométré, annexes de réponse aux questions attendues | P4, E4, R2, D3 |

R2 précède presque toujours R3 et R1 pour une raison structurelle: la condensation en une page force à trancher ce qui porte réellement la décision. Tant que le verdict n'est pas formulé en une phrase et que les trois à cinq chiffres porteurs ne sont pas arrêtés, un support de présentation n'a pas de fil décisionnel à suivre et un artefact visuel n'a pas de message à servir. Faire l'inverse — monter les diapositives ou le tableau de bord d'abord — produit invariablement un support descriptif qui expose le dossier au lieu de demander une décision.

R1 intervient ensuite, soit pour habiller le sommaire de R2 en artefact remis, soit pour fournir à R3 ses visuels lisibles à distance; c'est pourquoi R1 figure en aval de R2 et en amont de R3 dans le pipeline de présentation. Les trois modules convergent vers la même barrière de sortie: aucun d'eux ne remet quoi que ce soit sans le préflight final Q4.

## R1 — ui-ux-pro-max

**Objectif.** Produire l'artefact visuel ou interactif du livrable en s'appuyant sur le moteur de design du dépôt et sur l'identité visuelle du DÉPS. Le module traduit un contenu validé en tableau de bord, calculateur, outil interactif, visualisation ou mise en page, sans jamais modifier le contenu qu'il met en forme.

**Entrées requises.**

- Contenu validé du livrable, dont chaque chiffre est déjà rattaché à sa source par le registre de Q3.
- Type d'artefact visé: tableau de bord, calculateur, diagnostic interactif, rapport paginé, visualisation isolée.
- Contraintes de diffusion: consultation à l'écran, projection en séance, export PDF, impression, envoi par courriel.
- Identité visuelle institutionnelle applicable, telle qu'elle figure au guide de marque en vigueur de l'organisation.
- Auditoire et contexte d'usage: consultation individuelle, présentation animée, remise à un partenaire externe.
- Contraintes techniques du destinataire: poste sans accès au réseau, restriction de format, taille maximale de fichier.
- Système de design déjà persisté pour le dossier, le cas échéant, afin d'éviter une régénération inutile.

### Méthode

#### 1. Interroger le moteur de design du dépôt pour le type de produit visé

Le point de départ n'est pas une intuition esthétique, c'est une interrogation du moteur de design du dépôt, exécutée depuis la racine de celui-ci. La commande de base est `python3 src/ui-ux-pro-max/scripts/search.py "<query>" [--domain <domain>] [--stack <stack>] [-n <max_results>] [--json]`. Pour cadrer le type de produit visé, on interroge le domaine `product`, par exemple `python3 src/ui-ux-pro-max/scripts/search.py "financial dashboard" --domain product`. La requête décrit le produit dans les termes du moteur, en anglais, puisque les bases de connaissances sont rédigées ainsi.

Si le domaine est omis, le script le détecte à partir de la requête; en contexte institutionnel, on le nomme malgré tout explicitement pour que le résultat soit reproductible d'une session à l'autre. On consigne la requête, le domaine interrogé et le type de produit retenu au registre de production, car ils serviront de fil conducteur à toutes les interrogations suivantes. Une requête mal cadrée à cette étape se propage dans tout l'artefact et coûte beaucoup plus cher à corriger à la fin qu'au début.

#### 2. Générer ou récupérer le système de design

Plutôt que d'enchaîner des interrogations isolées, le moteur produit un système complet en une passe avec `python3 src/ui-ux-pro-max/scripts/search.py "<query>" --design-system [-p "Project Name"] [--format ascii|markdown]`. Ce mode lance des recherches parallèles sur les domaines `product`, `style`, `color`, `landing` et `typography`, applique les règles de raisonnement du moteur et retourne un système unique: patron, style, couleurs, typographie, effets et anti-patrons. Pour un dossier appelé à produire plusieurs artefacts, on persiste ce système avec `python3 src/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"`, ce qui écrit la source de vérité dans `design-system/<project-slug>/MASTER.md`.

Un artefact qui doit s'écarter du système commun reçoit sa propre surcouche avec `python3 src/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"`, écrite dans `design-system/<project-slug>/pages/<page>.md`; la surcouche de page a préséance sur le fichier maître au moment de la consultation. Avant de régénérer quoi que ce soit, on vérifie qu'un système n'existe pas déjà pour le dossier: reprendre le système persisté prime toujours sur une nouvelle génération. Ce patron maître et surcouches évite la dérive visuelle entre un tableau de bord de portefeuille, une fiche de dossier et un rapport de reddition produits à des semaines d'intervalle. Le système généré demeure un point de départ générique et n'est jamais le rendu final.

#### 3. Appliquer l'identité visuelle institutionnelle par-dessus les jetons génériques

Le moteur produit des jetons génériques: palette, échelle typographique, rayons, ombres et espacements. Ces jetons ne sont pas l'identité du DÉPS et ne doivent jamais être présentés comme tels. L'identité visuelle institutionnelle en vigueur s'applique par-dessus les jetons génériques produits par le moteur, et elle doit être tirée du guide de marque de l'organisation, jamais reconstituée de mémoire, déduite d'un artefact antérieur ou approchée par ressemblance. Concrètement, on substitue les valeurs de marque aux jetons génériques correspondants — couleurs officielles, familles typographiques officielles, logotype et ses zones de protection, règles d'usage du bloc-marque — en conservant la structure du système généré, qui demeure utile pour la hiérarchie, les états et les espacements.

Lorsqu'une valeur de marque n'est pas disponible ou n'a pas été confirmée, elle est traitée comme un paramètre à valider: l'artefact ne sort pas avec une valeur inventée, il sort avec un marqueur explicite et la mention que la valeur reste à confirmer auprès du guide de marque. Toute couleur, toute police et tout code de nuancier figurant dans un artefact remis doit pouvoir être rattaché au guide en vigueur, exactement comme un chiffre doit pouvoir être rattaché à sa pièce source. Cette exigence vaut aussi pour les couleurs de séries de graphiques, trop souvent laissées au choix par défaut de la bibliothèque et jamais vérifiées.

#### 4. Choisir les visualisations selon le message analytique et non selon l'esthétique

Chaque visualisation répond à une question précise et à une seule. On formule d'abord le message en une phrase — une évolution, une composition, une comparaison, une distribution, une relation, un écart à un seuil — puis on choisit la forme qui sert ce message. Le domaine `chart` documente les types de graphiques, les bibliothèques et les notes d'accessibilité: `python3 src/ui-ux-pro-max/scripts/search.py "debt service coverage over time" --domain chart`.

Les artefacts financiers du DÉPS obéissent à quelques constantes: un ratio de couverture se lit dans le temps et par scénario, une structure de sources et emplois se lit en composition qui balance, une concentration de portefeuille se lit en part du total, un écart à un seuil se lit avec le seuil tracé. Le titre du graphique énonce la conclusion et non la variable représentée. Un graphique qui ne changerait rien à la décision est retiré plutôt que décoré, et un tableau demeure préférable lorsque le lecteur doit lire des valeurs exactes.

#### 5. Vérifier l'accessibilité: contraste, navigation clavier, tailles de cible

L'accessibilité se vérifie pendant la construction et non à la remise. Le contraste du texte sur son fond est mesuré et consigné, y compris pour les libellés d'axes, les légendes, les notes de tableau, les états désactivés et le texte posé sur un aplat de couleur de marque. Tous les éléments interactifs — champs de calculateur, onglets, filtres, boutons d'export — sont atteignables et actionnables au clavier seul, dans un ordre de tabulation qui suit l'ordre de lecture, avec un indicateur de focus visible en tout temps. Les cibles tactiles respectent une surface minimale et un espacement suffisant pour un usage sur tablette, en réunion comme en visite d'entreprise.

Le moteur fournit les règles applicables par les domaines `ux` et `web`, par exemple `python3 src/ui-ux-pro-max/scripts/search.py "keyboard navigation focus" --domain web`. Aucune information n'est portée par la couleur seule: un état de risque, un dépassement de seuil ou un écart défavorable est aussi marqué par un libellé, une forme ou une valeur. Les contrôles effectués sont consignés au registre de production, faute de quoi ils sont réputés ne pas avoir eu lieu.

#### 6. Vérifier le rendu en impression et en mode sombre le cas échéant

Un artefact du DÉPS finit régulièrement imprimé, souvent en noir et blanc, et parfois consulté dans un environnement en mode sombre. Le rendu s'éprouve dans ces deux conditions avant la remise, jamais après une plainte. À l'impression, on vérifie que les couleurs se distinguent encore en nuances de gris, que les fonds foncés ne consomment pas l'encre inutilement, que les tableaux ne se coupent pas au milieu d'une ligne et que les en-têtes de colonnes se répètent sur chaque page.

En mode sombre, on vérifie que la palette institutionnelle demeure conforme au guide de marque, que le contraste reste au-dessus du seuil dans les deux thèmes et qu'aucune couleur n'est définie uniquement dans l'un d'eux. Lorsque l'artefact n'est pas destiné au mode sombre, on l'assume explicitement en fixant les couleurs plutôt que de laisser l'environnement du lecteur décider du rendu. Le contrôle se conclut par un essai réel: une page imprimée et un aperçu dans chaque thème pris en charge.

#### 7. Livrer un artefact autonome sans dépendance réseau non maîtrisée

Un artefact remis doit s'ouvrir et fonctionner sans accès au réseau, sur un poste dont on ne maîtrise pas la configuration, y compris dans une salle de conseil à la connexion instable. Les styles, les scripts, les polices et les images sont intégrés au fichier remis; les appels vers des services externes de graphiques, de polices ou d'icônes sont éliminés ou remplacés par une ressource intégrée. Le domaine `icons` documente les bibliothèques et leurs modes d'importation: `python3 src/ui-ux-pro-max/scripts/search.py "status indicator icons" --domain icons`.

Cette autonomie a aussi une dimension de confidentialité: un artefact de dossier de financement ne doit émettre aucune requête vers un tiers au moment de son ouverture. On vérifie l'autonomie en ouvrant le fichier avec le réseau désactivé et en confirmant que rien n'est manquant ni dégradé. L'artefact est ensuite nommé selon les conventions de Q2, puis soumis au préflight Q4 avant toute diffusion.

### Pont vers le moteur de design du dépôt

Ce dépôt est le moteur de design. R1 est le point de jonction entre le système DÉPS et ce moteur: chaque besoin de l'artefact correspond à un domaine interrogeable, et chaque interrogation se fait avec la commande du dépôt, exécutée depuis la racine de celui-ci.

Le tableau ci-dessous associe les besoins courants d'un livrable du DÉPS aux domaines du moteur. Les requêtes données sont des exemples: elles se réécrivent selon le dossier, mais le domaine, lui, se choisit selon le besoin et non selon l'habitude.

| Besoin du livrable | Domaine à interroger | Commande |
|---|---|---|
| Cadrer le type de produit (tableau de bord de portefeuille, calculateur, fiche de dossier) | `product` | `python3 src/ui-ux-pro-max/scripts/search.py "financial dashboard" --domain product` |
| Arrêter le registre visuel et ses mots-clés CSS | `style` | `python3 src/ui-ux-pro-max/scripts/search.py "institutional minimal report" --domain style` |
| Obtenir la palette de jetons de couleur à surcharger par la marque | `color` | `python3 src/ui-ux-pro-max/scripts/search.py "fintech dashboard palette" --domain color` |
| Établir l'échelle et les appariements typographiques | `typography` | `python3 src/ui-ux-pro-max/scripts/search.py "corporate report typography" --domain typography` |
| Choisir le type de graphique qui sert le message analytique | `chart` | `python3 src/ui-ux-pro-max/scripts/search.py "debt service coverage over time" --domain chart` |
| Structurer une page publique de programme ou d'appel à projets | `landing` | `python3 src/ui-ux-pro-max/scripts/search.py "program landing page structure" --domain landing` |
| Contrôler l'ergonomie et écarter les anti-patrons | `ux` | `python3 src/ui-ux-pro-max/scripts/search.py "data table usability" --domain ux` |
| Sélectionner un jeu d'icônes et son mode d'importation | `icons` | `python3 src/ui-ux-pro-max/scripts/search.py "status indicator icons" --domain icons` |
| Appliquer les règles d'interface web (ARIA, focus, formulaires) | `web` | `python3 src/ui-ux-pro-max/scripts/search.py "keyboard navigation focus" --domain web` |

Pour un artefact bâti sur React ou Next.js, le domaine `react` complète ces interrogations avec les règles de performance du moteur: `python3 src/ui-ux-pro-max/scripts/search.py "chart rendering performance" --domain react`. Lorsque la technologie de l'artefact est arrêtée, le mode par pile fournit les règles propres à cette pile avec `python3 src/ui-ux-pro-max/scripts/search.py "<query>" --stack <stack>`, les piles disponibles incluant notamment `html-tailwind`, `react`, `nextjs` et `shadcn`.

Le nombre de résultats se règle avec `-n <max_results>` et la sortie machine s'obtient avec `--json` lorsqu'on souhaite consigner l'interrogation au dossier sous une forme réutilisable. Lorsque plusieurs artefacts découlent du même dossier, le mode `--design-system --persist` remplace avantageusement la répétition des interrogations domaine par domaine.

Lorsqu'une interrogation ne retourne rien de pertinent, on ne comble pas le vide par une invention: on reformule la requête dans le vocabulaire du moteur, on élargit le nombre de résultats, puis on change de domaine si le besoin a été mal qualifié. Si le moteur demeure muet sur un besoin réel, la décision de conception est prise explicitement, documentée au registre de production et signalée au préflight comme un choix non appuyé par le moteur.

Une mise en garde clôt ce pont: les résultats du moteur sont des recommandations génériques, calibrées pour des produits numériques en général. Ils précèdent l'application de l'identité visuelle institutionnelle du DÉPS, ils ne la remplacent jamais, et aucun jeton générique ne doit subsister dans un artefact remis là où une valeur de marque existe au guide en vigueur.

### Sorties

- Artefact visuel ou interactif autonome, ouvrable hors ligne, nommé selon les conventions de Q2.
- Système de design appliqué et consigné, y compris la persistance dans `design-system/<project-slug>/MASTER.md` lorsque le dossier produit plusieurs artefacts.
- Surcouches de page consignées dans `design-system/<project-slug>/pages/<page>.md` pour les artefacts qui s'écartent du système commun.
- Registre des interrogations du moteur: requête, domaine, date et résultat retenu.
- Relevé des contrôles d'accessibilité passés: contraste mesuré, parcours clavier éprouvé, tailles de cible vérifiées.
- Preuves de rendu: aperçu imprimé en noir et blanc et, le cas échéant, aperçu dans chaque thème pris en charge.
- Attestation d'autonomie: résultat de l'ouverture du fichier avec le réseau désactivé.
- Liste des valeurs de marque restées à confirmer auprès du guide de marque, le cas échéant.
- Liste des décisions de conception prises sans appui du moteur, signalées au préflight.

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Choisir un graphique pour son apparence plutôt que pour son message | Le lecteur voit une image sans comprendre la décision à prendre; le support devient décoratif | Exiger que chaque visualisation soit précédée de sa phrase-message et que son titre énonce la conclusion |
| Texte sous le seuil de contraste | Une partie de l'auditoire ne lit pas l'information, en séance comme à l'écran; risque de non-conformité | Mesurer le contraste de chaque combinaison texte-fond, y compris légendes, axes et texte sur aplat de marque |
| Artefact dépendant d'une ressource externe | L'artefact se dégrade ou échoue en salle sans réseau et peut émettre des requêtes vers des tiers | Ouvrir le fichier avec le réseau désactivé avant la remise et confirmer qu'aucun appel externe ne subsiste |
| Palette ou typographie hors identité institutionnelle | Le livrable ne se reconnaît pas comme un document de l'organisation et la marque se dilue | Rattacher chaque couleur et chaque police au guide de marque en vigueur; traiter toute valeur non confirmée comme paramètre à valider |
| Réanalyser ou recalculer pendant la mise en forme | Les chiffres de l'artefact divergent du dossier validé et la remise est bloquée au préflight | Renvoyer toute donnée nouvelle vers son module analytique, puis vers Q1 et Q3, avant de la réintégrer |
| Repartir d'un artefact antérieur plutôt que du système de design | La dérive visuelle s'installe et les erreurs de l'artefact précédent se propagent au dossier suivant | Consulter le système persisté ou le régénérer avant chaque nouvel artefact du dossier |

## R2 — rapport-executif

**Objectif.** Condenser une analyse complète en une page de décision, avec le verdict d'abord, les chiffres porteurs ensuite et le développement après. Le sommaire ne résume pas le dossier: il en extrait ce qui change la décision et écarte tout le reste.

**Entrées requises.**

- Analyse complète validée, provenant selon le cas de F1, F3, F4, P4, E4 ou D3.
- Décision précise demandée: approuver, refuser, reporter, autoriser une dérogation, mandater une suite.
- Auditoire visé et son niveau de connaissance du dossier, qui détermine ce qui peut être présumé connu.
- Contraintes de format: page unique, canal de diffusion, présence ou non d'annexes accessibles au lecteur.
- Registre des sources de Q3, qui permet de rattacher chaque chiffre du sommaire à sa pièce justificative.
- Échéance de la décision, qui conditionne la formulation de la demande finale.
- Positions déjà exprimées par l'instance sur des dossiers comparables, lorsqu'elles sont connues.
- Identification du dossier et mention de version à porter en tête du document.

### Méthode

#### 1. Formuler le verdict en une phrase et le placer en première ligne

Le verdict est écrit avant tout le reste et occupe la première ligne du document. Il tient en une phrase et contient trois éléments: la position prise, l'objet précis et la condition majeure s'il y en a une. Une formulation acceptable nomme le montant, le fonds visé et la réserve principale; une formulation inacceptable annonce que le dossier présente des éléments intéressants.

Le verdict s'écrit à la voix active et sans conditionnel de précaution: si la position n'est pas tenable, c'est le verdict qui doit changer, non sa formulation. Un lecteur qui ne lirait que cette ligne doit savoir ce qu'on lui demande et quelle réponse est recommandée. Si la phrase dépasse deux lignes à l'écran, c'est généralement que la position n'est pas encore arrêtée.

#### 2. Sélectionner les trois à cinq chiffres qui portent la décision

Un sommaire d'une page ne peut pas porter plus de cinq chiffres sans que le lecteur cesse de les hiérarchiser. On retient ceux dont la variation ferait basculer la recommandation: typiquement le montant demandé, le ratio de couverture du service de la dette, le levier, la mise de fonds et le seuil de rupture. Chaque chiffre est présenté avec son unité, sa période et sa base — normalisée ou publiée, prévisionnelle ou historique — parce qu'un chiffre sans base est ininterprétable.

Les décimales se limitent à ce que la donnée d'entrée supporte réellement, un faux précis affaiblissant la crédibilité de l'ensemble. Les chiffres écartés ne sont pas perdus: ils demeurent au dossier complet, où ils restent consultables et sourcés. La sélection se justifie en une ligne interne au dossier, ce qui facilite la reprise du sommaire lors d'une mise à jour.

#### 3. Écrire le raisonnement en trois blocs maximum

Le raisonnement explique comment on passe des chiffres au verdict, en trois blocs au plus. Une structure éprouvée pour un dossier de financement traite successivement la solidité de l'entreprise, la capacité de servir la dette projetée, puis la solidité du montage et des garanties. Chaque bloc porte un intertitre qui énonce sa conclusion et tient en trois à cinq phrases.

Aucun bloc ne réexpose la méthode d'analyse: le lecteur ne veut pas savoir comment le ratio a été calculé, il veut savoir ce qu'il indique. Les renvois vers les sections du dossier complet remplacent les développements. Si un quatrième bloc s'impose, c'est généralement le signe que le sommaire tente de faire le travail du dossier.

#### 4. Nommer explicitement ce qui pourrait faire échouer la recommandation

Un sommaire qui ne présente que les arguments favorables se fait démonter en séance. On nomme donc en clair les deux ou trois éléments susceptibles de faire échouer la recommandation: dépendance à un client unique, hypothèse de croissance non appuyée, aide publique non confirmée par écrit, dépendance au propriétaire, saisonnalité mal couverte. Chaque élément est suivi de son atténuation réelle, ou de la mention qu'il est assumé sans atténuation.

Cette section protège la crédibilité de l'analyste: elle démontre que les objections ont été anticipées plutôt que subies. Elle prépare aussi les diapositives d'annexe de R3, qui répondront aux mêmes objections. Un risque nommé sans conséquence ni traitement n'est pas un risque nommé, c'est une précaution rhétorique.

#### 5. Terminer par la demande précise faite au lecteur

Le sommaire se termine par ce que l'on attend du lecteur, formulé de manière actionnable et datée. La demande précise l'instance sollicitée, l'acte attendu — adopter une résolution, autoriser une dérogation, mandater une vérification complémentaire — et l'échéance qui rend la décision utile. Lorsque plusieurs options sont ouvertes, elles sont énumérées avec leur conséquence respective, sans que cela dilue la recommandation.

Un sommaire qui s'achève sur une synthèse au lieu d'une demande laisse le lecteur sans prise et provoque un report. La demande doit être cohérente avec le verdict de la première ligne: toute divergence entre les deux signale un sommaire non abouti.

#### 6. Retirer tout contenu qui ne change pas la décision

La dernière passe de rédaction est soustractive. Chaque phrase est testée: si sa suppression ne change ni la décision ni la compréhension du risque, elle sort. Sortent en priorité l'historique détaillé de l'entreprise, la description des méthodes, les rappels de contexte connus de l'auditoire, les précautions de langage et les répétitions d'un bloc à l'autre.

La contrainte d'une page n'est pas une contrainte typographique que l'on satisfait en réduisant les marges ou le corps du texte: c'est une contrainte de sélection. Un sommaire qui ne tient qu'en réduisant la taille de police n'est pas un sommaire d'une page, c'est un dossier compressé. La densité visuelle du document doit rester compatible avec une lecture complète en cinq minutes.

#### 7. Vérifier que chaque chiffre du sommaire correspond au dossier complet

Le contrôle final rapproche un à un les chiffres du sommaire et ceux du dossier: même valeur, même période, même base, même arrondi. Cette vérification se fait chiffre par chiffre et non par relecture d'ensemble, parce que la divergence typique naît d'une mise à jour du dossier postérieure à la rédaction du sommaire. Toute divergence se corrige à la source, jamais dans le sommaire seul, sans quoi l'écart réapparaîtra à la version suivante.

Le sommaire est ensuite soumis aux contrôles Q1, Q2 et Q3, puis au préflight Q4, comme l'exige la chaîne de passages du domaine 06. Un sommaire dont un seul chiffre diverge du dossier discrédite l'ensemble du travail analytique qui le précède.

### Gabarit du sommaire exécutif d'une page

Le sommaire suit un ordre de blocs fixe, conçu pour qu'un lecteur pressé s'arrête à n'importe quelle ligne en ayant déjà l'essentiel. L'ordre n'est pas négociable: il porte à lui seul la moitié de l'efficacité du document.

**Bloc 1 — Verdict.** Première ligne du document, une phrase, deux lignes à l'écran au maximum. Il contient la position prise, l'objet, le montant et la condition majeure. Il ne contient jamais de mise en contexte, de rappel historique, de conditionnel de précaution ni de renvoi à une section ultérieure.

**Bloc 2 — Chiffres porteurs.** Trois à cinq chiffres, présentés en liste ou en bandeau, chacun sur une ligne avec son libellé, son unité, sa période et sa base. Il contient uniquement les chiffres dont la variation ferait basculer la recommandation. Il ne contient jamais de tableau complet, de série historique, de chiffre décoratif ni de décimale que la donnée d'entrée ne supporte pas.

**Bloc 3 — Raisonnement.** Trois blocs au maximum, de trois à cinq phrases chacun, chaque bloc coiffé d'un intertitre qui énonce sa conclusion. Il contient le lien explicite entre les chiffres porteurs et le verdict. Il ne contient jamais l'exposé des méthodes de calcul, la reprise du dossier complet ni de répétition d'un bloc à l'autre.

**Bloc 4 — Ce qui pourrait faire échouer la recommandation.** Deux à trois éléments, d'une à deux phrases chacun, chaque élément suivi de son atténuation ou de la mention qu'il est assumé. Il contient les objections anticipées et les fragilités réelles du dossier. Il ne contient jamais de risque générique sans conséquence, de mitigant non documenté ni de formulation qui minimise l'exposition.

**Bloc 5 — Demande au lecteur.** Deux à quatre lignes, en clôture du document. Il contient l'instance sollicitée, l'acte attendu, l'échéance et, s'il y a lieu, les options ouvertes avec leur conséquence. Il ne contient jamais de synthèse répétant le verdict, de remerciements, de formule d'ouverture vague ni de demande implicite laissée à l'interprétation.

L'ensemble tient sur une page à densité de lecture normale, sans réduction du corps de texte ni des marges. Les renvois vers le dossier complet remplacent tout développement, et chaque chiffre du sommaire demeure rattachable à sa pièce source par le registre de Q3.

Un dernier contrôle de forme s'impose avant la remise: le document doit rester lisible à l'impression en noir et blanc, puisqu'un sommaire exécutif circule presque toujours sur papier en séance.

Le document porte enfin, en en-tête ou en pied de page, l'identification du dossier, la date et la mention de version. Un sommaire exécutif se détache facilement de son dossier: sans ces trois marqueurs, une version périmée peut circuler et servir de base à une décision.

### Sorties

- Sommaire exécutif d'une page, structuré selon le gabarit ci-dessus.
- Verdict formulé en une phrase et placé en première ligne.
- Ensemble des trois à cinq chiffres porteurs, avec unité, période et base.
- Liste des éléments pouvant faire échouer la recommandation, chacun avec son atténuation ou la mention qu'il est assumé.
- Demande explicite adressée au lecteur, avec instance sollicitée, acte attendu et échéance.
- Table de correspondance interne entre chaque chiffre du sommaire et sa source au dossier.
- Justification en une ligne de la sélection des chiffres porteurs, conservée au dossier de travail.
- Version imprimable éprouvée en noir et blanc.
- Identification du dossier, date et mention de version portées en en-tête ou en pied de page.

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Enterrer le verdict en conclusion | Le lecteur pressé n'atteint jamais la position recommandée et arbitre sans elle | Imposer le verdict en première ligne et vérifier qu'il est lisible sans défilement |
| Recopier le dossier au lieu de le condenser | Le sommaire perd sa fonction de tri et le lecteur retombe dans le détail | Appliquer la passe soustractive: toute phrase qui ne change pas la décision est retirée |
| Chiffres du sommaire qui divergent du dossier | La crédibilité de toute l'analyse est atteinte et le préflight bloque la remise | Rapprocher chaque chiffre un à un avec sa source et corriger à la source, jamais dans le sommaire seul |
| Omettre la demande faite au lecteur | La séance se termine sans décision et le dossier revient à l'ordre du jour suivant | Vérifier que la dernière ligne nomme l'instance, l'acte attendu et l'échéance |
| Présenter le risque sans son atténuation | Les objections surgissent en séance et paraissent non anticipées | Exiger que chaque fragilité nommée soit suivie de son traitement ou de la mention qu'elle est assumée |
| Tenir la page en réduisant le corps de texte | Le document devient illisible en réunion et à l'impression | Contrôler la densité à taille de lecture normale, marges et corps de texte inchangés |

## R3 — presentation-CA

**Objectif.** Monter le support de présentation destiné au conseil d'administration, au comité d'investissement commun ou aux partenaires, calibré pour qu'une décision soit prise en séance dans le temps alloué. Le support met en scène un livrable déjà validé; il ne produit aucune analyse nouvelle.

**Entrées requises.**

- Livrable analytique validé, généralement la note de P4, le rapport d'évaluation de E4 ou le sommaire de R2.
- Durée exactement allouée en séance, en précisant si la période de questions y est incluse.
- Composition de l'auditoire: administrateurs, membres du comité, représentants des bailleurs, élus.
- Décision recherchée et libellé pressenti du projet de résolution.
- Historique des questions déjà posées par cette instance sur des dossiers comparables.
- Conditions matérielles de la séance: taille de la salle, matériel de projection, remise ou non d'une version papier.
- Identité visuelle institutionnelle applicable, tirée du guide de marque en vigueur de l'organisation.
- Ordre du jour de la séance, qui situe le dossier parmi les autres points et confirme la plage réelle.

### Méthode

#### 1. Établir le fil décisionnel: ce qui est demandé et pourquoi maintenant

Avant la première diapositive, on écrit en une phrase ce que l'instance doit décider et pourquoi la décision se prend à cette séance plutôt qu'à la suivante. Cette phrase devient le fil décisionnel auquel chaque diapositive devra se rattacher; toute diapositive qui ne le sert pas est déplacée en annexe ou supprimée. L'urgence, lorsqu'elle existe, se documente par un fait vérifiable — échéance de programme, calendrier de réalisation, date d'expiration d'une offre — et jamais par une pression rhétorique.

Le fil décisionnel détermine aussi l'ordre du déroulé: on ne raconte pas le dossier chronologiquement, on construit la décision. Un support sans fil décisionnel produit une séance d'information et non une séance de décision. Lorsque le fil ne s'écrit pas en une phrase, c'est que le livrable amont n'est pas encore prêt à être présenté.

#### 2. Une idée par diapositive et un titre qui énonce la conclusion

Chaque diapositive porte une seule idée et son titre énonce la conclusion de cette idée, non son sujet. Un titre-conclusion se lit seul et se retient: il affirme que les flux couvrent le service de la dette avec une marge donnée, plutôt que d'annoncer une analyse de la capacité de remboursement. Le corps de la diapositive n'a plus qu'à démontrer ce que le titre affirme, ce qui écarte mécaniquement le contenu superflu.

Un auditeur qui parcourt uniquement les titres doit reconstituer l'argumentaire complet et arriver au même verdict. Cette discipline réduit également le temps de parole nécessaire, puisque le titre porte déjà le message. Les titres purement descriptifs sont le défaut le plus fréquent et le plus coûteux des supports institutionnels.

#### 3. Placer la recommandation dans les trois premières diapositives

La recommandation, son montant et ses conditions clés apparaissent au plus tard à la troisième diapositive. Placer la recommandation à la fin suppose que l'auditoire suivra l'intégralité du raisonnement avant de se former une opinion, ce qui ne se produit jamais dans une instance décisionnelle. En annonçant tôt, on transforme le reste du support en démonstration de la recommandation et on oriente les questions vers le fond plutôt que vers l'attente.

Les conditions majeures sont annoncées en même temps que la recommandation, pour que l'auditoire ne découvre pas une réserve en fin de parcours. Cette structure est cohérente avec R2, dont le verdict occupe la première ligne: les deux livrables portent la même position au même rang.

#### 4. Convertir les tableaux denses en visuels lisibles à distance

Un tableau conçu pour la lecture individuelle devient illisible en projection. On convertit donc les tableaux denses en visuels calibrés pour la distance: quatre à six lignes au plus, valeurs arrondies à l'unité utile, une seule dimension comparée par visuel, seuils tracés lorsqu'ils existent. Le tableau intégral demeure disponible en annexe pour l'administrateur qui souhaite le consulter.

Le choix des visualisations relève de R1 et suit la même règle: le message d'abord, la forme ensuite. On vérifie la lisibilité à la taille réelle de projection, en s'éloignant physiquement de l'écran, et non en zoomant sur un poste de travail. Les couleurs institutionnelles servent la hiérarchie de lecture et non la décoration, et aucune information n'est portée par la couleur seule.

#### 5. Prévoir les diapositives d'annexe pour les questions attendues

Les objections anticipées de R2 deviennent des diapositives d'annexe, prêtes à être appelées sans quitter le support. On prévoit typiquement le détail du montage, la sensibilité du ratio de couverture, le tableau de normalisation, la cartographie des aides publiques, l'historique du groupe d'entreprises liées et la grille de conformité à la politique. Chaque annexe porte un titre-conclusion, comme les diapositives principales, pour rester exploitable sous pression.

L'ordre des annexes suit la probabilité des questions, établie à partir des séances précédentes de la même instance. Une annexe utile est une annexe que le présentateur atteint en quelques secondes: la numérotation et le repérage comptent autant que le contenu.

#### 6. Chronométrer le déroulé par rapport au temps alloué

Le déroulé est chronométré diapositive par diapositive, puis totalisé et comparé au temps réellement alloué. On réserve d'emblée environ le tiers de la plage aux questions et aux échanges: un support qui consomme la totalité du temps laisse l'instance décider sans avoir pu interroger. Lorsque le total dépasse la plage, on retire des diapositives principales vers les annexes plutôt que d'accélérer le débit.

Le chronométrage se fait à voix haute, en conditions réelles, et non par estimation au jugé. Le déroulé chronométré fait partie des livrables du module: il accompagne le support et documente l'arbitrage effectué. Un support plus long que le temps alloué produit systématiquement une décision reportée ou une décision prise sans ses conditions.

#### 7. Vérifier la lisibilité en projection et en version imprimée

Le contrôle final s'effectue dans les deux conditions d'usage réelles. En projection, on vérifie la taille des caractères à distance, le contraste dans une salle éclairée, l'absence de texte sur des fonds qui écrasent la lisibilité et le rendu des visuels sur le matériel de la salle lorsqu'il est connu. En version imprimée, on vérifie le rendu en noir et blanc, la pagination, la présence des annexes annoncées et la lisibilité des notes du présentateur si elles sont remises.

Le support doit rester intelligible pour un administrateur qui le lira seul, après la séance, sans commentaire verbal. On vérifie enfin l'autonomie du fichier, selon la même exigence que R1: aucun contenu ne doit dépendre d'une ressource externe au moment de la séance. Le support passe ensuite le contrôle de nomenclature Q2, puis le préflight Q4.

### Architecture type d'un support de décision

Déroulé complet pour une présentation de décision de financement en séance, calibré pour une plage d'environ vingt-cinq minutes dont le tiers est réservé aux échanges. Les titres-conclusions ci-dessous sont des gabarits: ils se réécrivent avec les faits réels du dossier, faute de quoi ils redeviennent des titres descriptifs.

| Diapositive | Titre-conclusion type | Contenu | Durée |
|---|---|---|---|
| 1. Ouverture | Demande de financement à la raison sociale exacte, décision requise à la présente séance | Objet, montant total demandé, fonds visés, date de séance, présentateur | 30 s |
| 2. Recommandation | Nous recommandons le financement demandé, sous conditions préalables au décaissement | Montant par fonds, terme, amortissement, congé de capital, trois conditions clés | 1 min 30 |
| 3. Pourquoi maintenant | La décision conditionne le calendrier de réalisation du projet | Échéancier du projet, fenêtre de décision, conséquence documentée d'un report | 1 min |
| 4. Entreprise et promoteurs | L'entreprise est établie et l'équipe de direction est complète | Activité, marché desservi, effectif, actionnariat, expérience des promoteurs | 1 min 30 |
| 5. Projet | Le projet répond à une demande déjà constatée et non à une hypothèse de croissance | Nature du projet, coût total, calendrier, retombées attendues sur le territoire | 1 min 30 |
| 6. Montage financier | Le tour de financement est complet et chaque source est confirmée par écrit | Tableau Sources et Emplois simplifié qui balance, mise de fonds et sa forme, rangs de sûreté | 2 min |
| 7. Capacité de remboursement | Les flux couvrent le service de la dette dans les trois scénarios | Ratio de couverture par exercice et par scénario, seuil de rupture, besoin de marge de crédit | 2 min 30 |
| 8. Risques et atténuation | Les risques significatifs sont atténués par des conditions vérifiables | Matrice condensée aux risques cotés élevés, mitigants, risque résiduel assumé nommé | 2 min |
| 9. Conformité à la politique | Le dossier est conforme à la politique en vigueur, sans dérogation demandée | Plafonds, ratio entre les fonds, mise de fonds minimale, niveau d'autorisation requis | 1 min 30 |
| 10. Conditions de décaissement | Le décaissement est subordonné à des conditions datables et vérifiables | Conditions préalables, engagements de faire et de ne pas faire, pièces manquantes déclarées | 1 min 30 |
| 11. Décision demandée | L'instance est appelée à adopter la résolution telle que rédigée | Libellé du projet de résolution, options ouvertes et leur conséquence respective | 1 min |
| 12. Annexes | Annexes disponibles pour les questions attendues | États financiers retraités, sensibilité, normalisation, cartographie des aides, grille de conformité | Hors plage |

Lorsque la plage allouée est plus courte, on ne comprime pas le déroulé de façon uniforme: on conserve intégralement les diapositives 1, 2, 7, 10 et 11, et on bascule vers les annexes tout ou partie des diapositives 3 à 6. La recommandation, la capacité de remboursement, les conditions et la demande de décision ne se sacrifient jamais au temps.

### Sorties

- Support de présentation complet, autonome et calibré pour la projection.
- Déroulé chronométré diapositive par diapositive, avec le total comparé au temps alloué.
- Jeu d'annexes numéroté et ordonné selon la probabilité des questions attendues.
- Version imprimable éprouvée en noir et blanc, pagination et annexes vérifiées.
- Libellé du projet de résolution soumis à l'instance.
- Fil décisionnel écrit en une phrase, conservé au dossier de travail.
- Relevé des contrôles de lisibilité effectués en conditions de projection.
- Variante courte du déroulé, indiquant les diapositives conservées si la plage est réduite.

### Pièges à éviter

| Piège | Conséquence | Contrôle |
|---|---|---|
| Titres descriptifs au lieu de titres-conclusions | L'auditoire doit reconstituer le message seul et retient le sujet plutôt que la position | Lire la suite des seuls titres et vérifier qu'elle restitue l'argumentaire complet |
| Tableaux illisibles en projection | Les chiffres porteurs ne sont pas lus et la discussion se déplace vers la forme | Éprouver chaque visuel à la taille réelle de projection, en s'éloignant de l'écran |
| Recommandation en fin de support | L'auditoire se forme une opinion avant de connaître la position recommandée | Vérifier que la recommandation et ses conditions clés figurent au plus tard à la troisième diapositive |
| Support plus long que le temps alloué | La séance se termine sans décision, ou la décision se prend sans ses conditions | Chronométrer à voix haute et basculer vers les annexes plutôt qu'accélérer le débit |
| Donnée nouvelle introduite à l'étape de la présentation | Le support contredit le dossier validé et la remise est bloquée au préflight | Renvoyer toute donnée nouvelle vers son module analytique, puis vers Q1 et Q3 |
| Annexes absentes ou introuvables en séance | Une objection anticipée reste sans réponse et fragilise la recommandation | Numéroter les annexes, les ordonner par probabilité de question et éprouver l'accès en quelques secondes |

## Accessibilité et rendu : contrôles minimaux

Ces contrôles s'appliquent à tout artefact produit par R1, R2 ou R3, quel que soit le canal de diffusion. Chacun se vérifie et se consigne: un contrôle non consigné est réputé ne pas avoir été effectué.

- Contraste du texte: chaque combinaison texte-fond est mesurée, y compris les libellés d'axes, les légendes, les notes de bas de tableau, les états désactivés et le texte posé sur un aplat de couleur institutionnelle; le seuil retenu est celui de la norme d'accessibilité applicable au canal de diffusion.
- Information portée par la couleur: aucun état, seuil dépassé, écart défavorable ni catégorie n'est signalé par la couleur seule; un libellé, une forme, un motif ou une valeur double systématiquement le signal chromatique.
- Tailles de cible tactile: tout élément actionnable respecte une surface minimale et un espacement suffisant pour un usage au doigt sur tablette, condition courante en réunion et en visite d'entreprise.
- Navigation au clavier: l'ensemble des éléments interactifs est atteignable et actionnable au clavier seul, dans un ordre de tabulation qui suit l'ordre de lecture, sans piège de focus et avec un indicateur de focus visible en tout temps.
- Structure sémantique: les titres suivent une hiérarchie continue, les tableaux portent des en-têtes de colonnes et de lignes correctement associés, et toute image porteuse d'information dispose d'un texte de remplacement.
- Lisibilité en projection à distance: la taille des caractères et l'épaisseur des traits sont éprouvées à la distance réelle de la salle, dans un éclairage réaliste, et non par un zoom sur un poste de travail.
- Densité par page et par diapositive: le nombre de valeurs affichées simultanément reste compatible avec une lecture en quelques secondes; les tableaux intégraux vont en annexe.
- Rendu en impression noir et blanc: les séries et les catégories demeurent distinguables sans couleur, les fonds foncés ne consomment pas l'encre inutilement, les tableaux ne se coupent pas au milieu d'une ligne et les en-têtes se répètent sur chaque page.
- Pagination et repérage: chaque page ou diapositive porte son numéro, l'identification du dossier et la mention de version, de sorte qu'une page isolée demeure identifiable.
- Autonomie de l'artefact: le fichier s'ouvre et fonctionne intégralement hors ligne, styles, scripts, polices et images inclus, sans aucune requête vers une ressource externe au moment de l'ouverture.
- Confidentialité au rendu: aucun appel réseau ne peut révéler l'ouverture d'un artefact de dossier; le contrôle se fait en ouvrant le fichier avec le réseau désactivé.
- Comportement en mode sombre: lorsque le mode sombre est pris en charge, le contraste et la conformité de la palette institutionnelle sont vérifiés dans les deux thèmes et aucune couleur n'est définie uniquement dans l'un d'eux; lorsqu'il ne l'est pas, le thème clair est fixé explicitement plutôt que laissé à l'environnement du lecteur.
- Conformité de marque au rendu: chaque couleur, chaque famille typographique et chaque usage du logotype se rattache au guide de marque en vigueur de l'organisation; toute valeur non confirmée est marquée comme paramètre à valider et n'est jamais remplacée par une approximation.
- Poids et ouverture du fichier: la taille du fichier reste compatible avec l'envoi par courriel et son ouverture ne dépend d'aucune installation particulière sur le poste du destinataire.
- Langue et terminologie du rendu: les libellés, les axes, les légendes et les formats de date et de montant respectent les conventions françaises et le lexique normalisé appliqué par Q2.
- Preuves de contrôle: une page imprimée, un aperçu dans chaque thème pris en charge et un relevé des mesures de contraste sont joints au registre de production et repris au préflight.

## Passage au domaine suivant

La production remet au domaine 06-QA l'artefact final dans sa version exacte de diffusion, accompagné du registre des interrogations du moteur de design, du relevé des contrôles d'accessibilité et de rendu, du déroulé chronométré lorsqu'il s'agit d'un support de présentation, et de la table de correspondance entre chaque chiffre affiché et sa source au dossier. R2 déclenche la chaîne complète des contrôles Q1, Q2, Q3 et Q4, puisqu'il porte des chiffres; R1 et R3 relèvent de Q2 pour la nomenclature et de Q4 pour la barrière de sortie, tout chiffre nouvellement introduit y ramenant mécaniquement Q1 et Q3.

Aucun artefact ne quitte l'organisation sans le préflight Q4: c'est la seule étape qui vérifie que la version contrôlée est bien la version remise, que les annexes annoncées sont présentes, que le verdict ou la recommandation est explicite et en tête, et que le rendu final correspond au canal de diffusion prévu.

Un support impeccable dont un chiffre diverge du dossier, ou dont une valeur de marque a été inventée plutôt que tirée du guide en vigueur, est bloqué au préflight au même titre qu'un calcul erroné. La production est donc la dernière étape de mise en forme, jamais la dernière étape de contrôle.
