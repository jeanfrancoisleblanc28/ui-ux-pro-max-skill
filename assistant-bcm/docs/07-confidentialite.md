# 07 — Confidentialité

## Principe fondamental : la protection dès la conception

Le Copilote BCM est conçu pour fonctionner **entièrement sans renseignements personnels identificatoires**. Ce n'est pas une consigne d'usage plaquée sur l'outil : c'est une propriété du produit. Toute la valeur clinique (structuration, radar, indice, rapport) s'obtient avec : initiales ou « la patiente / le patient », âge, sexe au besoin, contexte clinique. Rien d'autre n'est nécessaire — donc rien d'autre n'est admis.

## Ce qui ne doit jamais entrer dans une conversation

- Nom, prénom ;
- Numéro d'assurance maladie, numéro de dossier ;
- Date de naissance complète ;
- Adresse, téléphone, courriel ;
- Toute combinaison qui rendrait la personne identifiable (ex. « la mairesse de… ») ;
- Photos d'étiquettes ou de listes **comportant un nom** — en v1, pas de photo, ou nom masqué physiquement avant tout téléversement.

## Comportement de l'assistant

Règles P-01 et P-02 (`03-regles-metier.md`) : l'assistant n'exige jamais d'identifiant ; si un identifiant apparaît, il ne le répète jamais, poursuit avec [initiales] et rappelle la règle une seule fois, sans culpabiliser. La conversation n'est pas interrompue — la sécurité ne doit pas punir la spontanéité.

## Cycle de vie de l'information

1. **Pendant la collecte :** l'information vit dans la session de conversation, dépersonnalisée ;
2. **À la clôture :** le rapport est vérifié, validé et transcrit **au dossier officiel de l'usager**, qui est l'unique lieu de conservation légitime ;
3. **Après transcription :** la conversation est supprimée selon les règles locales. Aucune copie parallèle, aucun historique conservé dans l'outil.

## Cadre juridique québécois — repères

- **Loi 25** (protection des renseignements personnels) : les renseignements de santé sont des renseignements sensibles. La stratégie du projet est de **ne pas en traiter** — la dépersonnalisation à la source réduit radicalement l'exposition. Pour tout déploiement organisationnel, une **évaluation des facteurs relatifs à la vie privée (ÉFVP)** menée par l'organisation reste la voie normale, même pour un outil « sans identifiants » : c'est elle qui le confirme.
- **Tenue de dossier** : le rapport validé transcrit au dossier de l'usager suit les règles documentaires de l'établissement ; l'outil n'y touche jamais directement.
- **Obligations déontologiques** : le secret professionnel s'applique à ce que l'infirmière saisit dans tout outil ; la règle « zéro identifiant » en est l'application concrète.

## Paramétrage des plateformes (v1)

| Exigence | Pourquoi |
|---|---|
| Compte dédié à l'usage professionnel | Séparer des usages personnels |
| Entraînement sur les données **désactivé** | Aucune conversation ne doit nourrir un modèle |
| Historique réduit au besoin ; suppression des conversations après transcription | Cycle de vie ci-dessus |
| Aucune capacité superflue activée (navigation, code, images) | Réduire la surface |
| Partage de conversation désactivé | Aucune diffusion accidentelle |

## Bonnes pratiques individuelles (aide-mémoire)

- Je parle du patient par initiales et âge — jamais de nom, jamais de numéro.
- Je ne téléverse aucune photo comportant un nom.
- Je valide et transcris au dossier, puis je supprime la conversation.
- Je signale tout écart (le mien comme celui de l'outil) via le canal de gouvernance.

## Vers un déploiement organisationnel (CIUSSS)

Exigences anticipées, à porter au dossier de présentation :

1. ÉFVP menée avec le responsable de la protection des renseignements personnels (RPRP) ;
2. Choix d'une plateforme sous **entente organisationnelle** (conditions d'hébergement, localisation des données, engagement de non-entraînement, journalisation) ;
3. Politique d'utilisation signée par les utilisatrices (reprenant l'aide-mémoire ci-dessus) ;
4. Intégration au registre des outils d'IA de l'organisation, si applicable ;
5. Révision périodique conjointe (soins infirmiers, pharmacie, RPRP, ressources informationnelles).

La conception « zéro identifiant » de la v1 n'est pas un pis-aller en attendant mieux : c'est l'argument central de présentabilité du projet — l'outil démontre qu'on peut assister le BCM sans faire circuler de renseignements personnels.
