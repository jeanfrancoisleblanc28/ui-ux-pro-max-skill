# Boîte à outils productivité — gratuit, solo, sans Azure

Complément de [`setup-gratuit-solo.md`](./setup-gratuit-solo.md). Ici, du concret :
des **prompts prêts à copier**, des **routines** et des **workflows par tâche**
pour gagner du temps tous les jours, sans rien payer.

---

## 1. Le prompt de contexte (à coller en début de session)

Collez ceci une fois en début de conversation Copilot Chat / Perplexity. Tout ce
qui suit sera plus précis et personnalisé.

```
Contexte : je suis [métier / rôle]. Mon secteur est [secteur].
Mon objectif principal cette semaine : [objectif].
Mon ton : [direct / professionnel / pédagogique].
Quand tu réponds : va à l'essentiel, structure en listes, et propose une action
concrète à la fin. Pose-moi une question si une info te manque.
```

---

## 2. 10 prompts qui font gagner du temps

| Besoin | Prompt à copier |
|---|---|
| **Résumer un long texte** | « Résume ce texte en 5 points clés + 1 action recommandée : [coller] » |
| **Rédiger un e-mail pro** | « Rédige un e-mail [ton] à [destinataire] pour [objectif]. Court, clair, avec un objet accrocheur. » |
| **Répondre à un e-mail difficile** | « Voici un e-mail que j'ai reçu : [coller]. Propose 2 réponses possibles : une diplomate, une ferme. » |
| **Préparer une réunion** | « Crée un ordre du jour de 30 min pour une réunion sur [sujet], avec objectifs et temps par point. » |
| **Transformer des notes en compte-rendu** | « Voici mes notes brutes : [coller]. Transforme-les en compte-rendu clair avec décisions et prochaines étapes. » |
| **Brainstormer** | « Donne-moi 10 idées originales pour [problème], puis classe-les par facilité de mise en œuvre. » |
| **Analyser un tableau Excel** | « Voici des données : [coller]. Quelles tendances ressortent ? Donne 3 insights actionnables. » |
| **Créer un plan d'action** | « Décompose l'objectif [X] en un plan d'étapes avec échéances réalistes sur [durée]. » |
| **Vulgariser un sujet** | « Explique [sujet complexe] comme si j'avais 15 ans, avec une analogie. » |
| **Améliorer un texte** | « Réécris ce texte pour qu'il soit plus clair, plus court et plus percutant : [coller] » |

---

## 3. Workflows par tâche (quel outil, dans quel ordre)

**Produire un document propre**
1. Copilot Chat → brouillon à partir d'un prompt
2. Office Web (Word) → mise en forme + sauvegarde
3. Copilot Chat → « relis et corrige le ton/les fautes »

**Préparer une présentation**
1. Copilot Chat → structure (titres + points clés)
2. Gamma → coller la structure, générer les slides
3. Gamma éditeur → ajuster visuels

**Répondre à beaucoup d'e-mails**
1. NotebookLM → y déposer vos modèles de réponses fréquents
2. Copilot Chat → générer la réponse à partir du modèle
3. Coller dans votre messagerie

**Faire une veille / recherche sourcée**
1. Perplexity → question précise (il cite ses sources)
2. Copilot Chat → « synthétise ces infos en note d'1 page »
3. NotebookLM → archiver pour réinterroger plus tard

---

## 4. Routine quotidienne (15 min le matin)

1. **5 min** — Copilot Chat : « Voici mes 3 priorités du jour : [...]. Aide-moi à
   les ordonner et estime le temps de chacune. »
2. **5 min** — Traiter les e-mails urgents avec les prompts de réponse.
3. **5 min** — Noter dans NotebookLM ce qui doit être retenu pour plus tard.

**Routine hebdo (vendredi, 15 min)** : « Voici ce que j'ai fait cette semaine :
[...]. Fais-moi un bilan + 3 priorités pour la semaine prochaine. »

---

## 5. Réflexes qui multiplient la productivité

- **Itérez au lieu de tout réécrire** : « rends-le plus court », « change le ton »,
  « ajoute un exemple » — affinez en 2-3 allers-retours.
- **Demandez le format de sortie** : tableau, liste, e-mail, JSON… précisez-le.
- **Faites-vous challenger** : « quels sont les angles morts de mon plan ? »
- **Créez vos prompts réutilisables** : gardez un fichier `mes-prompts.txt` avec
  ceux qui marchent pour vous.
- **Vérifiez les faits importants** : l'IA peut se tromper — recoupez chiffres,
  dates, citations.

---

## 6. Mesurer que ça marche (gratuit)

Une fois par semaine, notez : *« Combien de temps l'IA m'a fait gagner cette
semaine ? Sur quelles tâches ? »* Gardez ce qui fait gagner du temps, abandonnez
le reste. C'est votre boucle d'amélioration — et elle ne coûte rien.
