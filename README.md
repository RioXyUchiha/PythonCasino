# PythonCasino
Ce projet vise a faire un casino en python regroupant plusieurs jeux connue comme le crash, mine et blackjack.

Requirement:
Installer pygame dans votre cmd avec la commande "pip install pygame"

Les scripts Server.py et Client.py sont des scripts de test pour la communication entre plusieurs pc (client) qui sera utile pour pouvoir jouer a plusieurs en même temps sur des machines differentes au blackjack et un systeme de chat pour que les joueurs puisse chatter ensemble.

Le script Tests.py sert a tester des fonctionnaliter avant de les integrer aux vrais scripts pour eviter de faire buger le casino, d'ou le faite que le script ne marche pas la pluspart du temps.

Le script player_data.json stock l'argent du joueur mais ser changer dans le futur par une base de donnée qui contiendra bien plus d'information.

Le script MineGame.py gére toute la partie du jeu mine.

## Mine 
Le but du jeu est simple, parier une somme d'argent puis choisissez combien de bombe entre 1 à 24 voullez vous qu'il y en ai dans les 25 cases. Plus il y a de bombe plus vous avez de chance de perdre mais plus d'argent vous obtiendrez.