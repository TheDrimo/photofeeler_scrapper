# PHOTOFEELER PROJECT

## Photofeeler
PF est un site pour noter ses photos selon plusieurs catégories sur plusieurs critères. Par exemple une photo dans la catégorie "dating" sera noté sur les critères "smart", "trustworthy" et "attractive".
Les photos sont notées par des vraies personnes. Pour obtenir des votes, ils faut voter les photos des autres.

## Objectifs
scrapper les données de ses photos du site pour pouvoir les analyser par la suite.
- Quel sont les critères les plus stables et ceux les plus variables ?
- Est-il plus important d'avoir des "very" ou beaucoup de "yes" ?
- Quel est l'impact moyen d'un "no" ou d'un "somewhat" ?
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
- [ ] stocker les données de la meilleurs manière, base de données ou json (json semble plus adapté). Ce sera une bd avec une table par catégorie (dating, business et social)

### étape 3 : catégoriser les photos (luminosité, qualité ...)
### étape 4 : analyser les photos, établir des corrélation avec les notes

## ce qui a à faire pour la prochaine fois
le scrapper fonctionne et avec une boucle sur toutes les photos il récupère toutes les données.
Il faut donc :
- [ ] faire la boucle sur chaque photo
- [ ] récupérer les données de la photo
- [ ] stocker les données dans la bd correspondante à la catégorie (ou la créer s'il elle n'existe pas)
- [ ] tout est prêt pour l'analyse

#### bonus
- [ ] utiliser les décorateurs pour calculer le temps moyen de chaque fonction
- [ ] créer un module de test