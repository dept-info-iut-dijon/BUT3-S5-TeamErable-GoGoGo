<h1 align="center"><img src="./todo-image" width="64" align="center" /> TODO-TITRE: TODO-SOUSTITRE</h1>
<p align="center">
  <a href="https://github.com/dept-info-iut-dijon/BUT3-S5-TeamErable-TMP/blob/master/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green" target="_blank" />
  </a>
  <img alt="Platforms: Web" src="https://img.shields.io/badge/Platforms-TODO-yellow" />
</p>

----------------------------------------------------------------------


# Projet EtiGO - Plateforme en ligne pour les passionnés de Go

L'association EtiGO, ayant rassemblé pendant plusieurs années les joueurs de Go de Dijon et de ses environs, se lance dans une initiative novatrice pour étendre son influence. Nous sommes fiers de présenter notre projet de développement d'une application web dédiée, offrant une plateforme moderne et conviviale destinée à nos membres existants et à de nouveaux joueurs.

## Objectif du Projet

L'application vise à faciliter les rencontres en ligne entre les passionnés de Go, offrant la possibilité de jouer des parties avec classement et de participer à des tournois virtuels. Notre vision est de rendre le monde fascinant du Go accessible à la jeune génération grâce à une interface intelligente et moderne, tout en préservant l'expérience des joueurs plus traditionnels moins habitués au monde du web et du numérique.

### Fonctionnalités Principales

**Parties en Ligne avec Classement :** Jouez contre d'autres membres et suivez votre progression à travers un système de classement en temps réel.

**Organisation de Tournois :** Participez à des tournois en ligne pour tester vos compétences et rencontrer d'autres passionnés de Go.

**Interface Intuitive :** Une conception conviviale adaptée à la fois aux adeptes du numérique et à ceux qui sont moins familiers avec les technologies web.

**Accessibilité Inter-Générationnelle :** Nous nous engageons à offrir une expérience sans barrières, permettant à la jeune génération de s'intégrer facilement tout en préservant l'inclusion des joueurs moins habitués au numérique.


## Prérequis
- Machine Window / Linux / MACOS ( avec python 3.11 ou plus )
- Machine Linux ( ou WSL )

## Installation

Pour installer les dépendances du projet ( sur la Machine python ) vous pouvez executer la commande suivante a la racine du projet: 
- ```python -m pip install -r requirements.txt```

Pour installer redis ( sur la machine Linux ) vous pouvez executer la commande suivante : 
- ```sudo apt-get install redis```

### Dépendances python 
#### ( si le l'installation des dépendances n'a pas fonctionné )

- Asgrief
- Django
- Plum
- Waitress
- Daphne
- Channels

### Technologies utilisés

- Python
- Django  
- Redis
- HTMX


## Lancer le serveur

Pour lancer le serveur redis, ouvrez un terminal ( sur la machine Linux ) et executer la commande suivante : 
- ```sudo service redis-server start```

Pour lancer le serveur, ouvrez un terminal ( sur la machine Python ) et executer la commande suivante a la racine du projet: 
- ```python manage.py runserver```

## Contributeurs

John GAUDRY, Hugo MRULA, Matthieu THIVARD, Samuel MONTAGNA

[//]: contributor-faces

<a href="https://github.com/JohnGdr"><img src="https://avatars.githubusercontent.com/u/104968811?v=4" title="JohnGdr" width="80" height="80"></a>   <a href="https://github.com/Lynn-Mei"><img src="https://avatars.githubusercontent.com/u/114869669?v=4" title="Lynn-Mei" width="80" height="80"></a>   <a href="https://github.com/MatthieuThivard"><img src="https://avatars.githubusercontent.com/u/104895273?v=4" title="MatthieuThivard" width="80" height="80"></a>   <a href="https://github.com/Synell"><img src="https://avatars.githubusercontent.com/u/70210528?v=4" title="Synel" width="80" height="80"></a>

[//]: contributor-faces
