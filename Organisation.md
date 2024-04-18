# PHOTOFEELER PROJECT

## Photofeeler
PF est un site pour noter ses photos selon plusieurs catégories sur plusieurs critères. Par exemple une photo dans la catégorie "dating" sera noté sur les critères "smart", "trustworthy" et "attractive".
Les photos sont notées par des vraies personnes. Pour obtenir des votes, ils faut voter les photos des autres.

## Objectifs
scrapper les données de ses photos du site pour pouvoir les analyser par la suite.
- Quel sont les critères les plus stables et ceux les plus variables ?
    - les 'no' et les 'yes' sont assez variables et ne sont pas représentatif du score global
- Est-il plus important d'avoir des "very" ou beaucoup de "yes" ?
    - les 'yes' sont plus importants de manière général. Donc si on commence à avoir plus de 'yes' que de 'somewhat' il est interressant de laisser la photo pour que le score puisse monter
- Quel est l'impact moyen d'un "no" ou d'un "somewhat" ?
    - le 'somewhat' semble est le vote moyen, donc une photo avec une majorité de 'somewhat' aura un score compris entre 4 et 6
- Quels sont les éléments de la photos qui jouent le plus sur les notes, ou plutôt qui ont une corrélation (luminosité, émotion affichée, extérieur/intérieur, arrière-plan, regard direct, vêtements élégants ou non, posture ...)

## Code
### étape 1 : se connecter au site
créer un objet feelerconnect à travers lequel on naviguera sur le site et sur lequel on utilisera des méthodes pour changer de page ou collecter la donnée.
### étape 2 : récupérer les données de chaque photo
- [x] récupérer les liens vers la page de chaque photo
- [x] extraire les données :
    - nb vote
    - gender voters
    - la qualité du score
    - les infos du sujet
    - catégory :
        - critère1 :
            - no
            - sw
            - yes
            - very
        - critère2 :
            - no
            - sw
            - yes
            - very
        - critère3 :
            - no
            - sw
            - yes
            - very
- [x] stocker les données de la meilleurs manière, base de données ou json (json semble plus adapté). Ce sera une bd avec une table par catégorie (dating, business et social)
- [x] récupérer l'image, ce sera ensuite plus facile pour la caractériser, pas nécessaire de l'avoir en haute résolution
- [ ] faire en sorte que les données ne soit pas écrite plusieurs fois dans la db, pour l'instant quand on relance le script plusieurs fois il ajoute des nouvelles lignes à chaque fois

### étape 3 : catégoriser les photos (luminosité, qualité ...)
pour ça je veux utiliser l'interface web avec du JS et du npm (ou d'autres librairies). Cliquer sur les boutons et ajuster les curseurs sera beaucoup plus agréable.
voir même lancer un serveur en local utilisant flask ou django
mais c'est pas l'immédiat.
### étape 4 : analyser les photos, établir des corrélation avec les notes
- les 'no' et les 'yes' sont assez variables et ne sont pas représentatif du score global
- les 'yes' sont plus importants de manière général. Donc si on commence à avoir plus de 'yes' que de 'somewhat' il est interressant de laisser la photo pour que le score puisse monter
- le 'somewhat' semble est le vote moyen, donc une photo avec une majorité de 'somewhat' aura un score compris entre 4 et 6

## ce qui a à faire pour la prochaine fois
le scrapper fonctionne et avec une boucle sur toutes les photos il récupère toutes les données.
Il faut donc :
- [x] faire la boucle sur chaque photo
- [x] récupérer les données de la photo
- [x] stocker les données dans la bd correspondante à la catégorie (ou la créer s'il elle n'existe pas)
- [x] tout est prêt pour l'analyse

#### bonus
- [ ] utiliser les décorateurs pour calculer le temps moyen de chaque fonction
- [ ] créer un module de test