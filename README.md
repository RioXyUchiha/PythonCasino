# Casino en Python
Ce projet vise a faire un casino en python regroupant plusieurs jeux connue comme le crash, mine et blackjack.

## Requirement:
Installer pygame dans votre cmd avec la commande "pip install pygame"

## Explication des scripts:
### Serveur.py & Client.py:
Ils servent de test pour la communication entre plusieurs pc (client) qui sera utile pour pouvoir jouer a plusieurs en même temps sur des machines differentes au blackjack et un systeme de chat pour que les joueurs puisse chatter ensemble.

### Tests.py:
Il sert a tester des fonctionnaliter avant de les integrer aux vrais scripts pour eviter de faire buger le casino, d'ou le faite que le script ne marche pas la pluspart du temps.

### player_data.json:
Stock l'argent du joueur mais ser changer dans le futur par une base de donnée qui contiendra bien plus d'information.

### MineGame.py 
Gére toute la partie du jeu des mines.

## Jeu des Mines:
Le but du jeu est simple, parier une somme d'argent puis choisissez combien de bombe de 1 à 24 voullez vous qu'il y en ai dans les 25 cases. Plus il y a de bombe plus vous avez de chance de perdre mais plus d'argent vous obtiendrez. Apres chaque case bonns votre multiplicateur augmentera, ce multiplicateur affecte l'argent que vous recevrez quand vous retirer l'argent.
