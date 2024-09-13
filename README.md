# Casino en Python
Ce projet vise à créer un casino en Python regroupant plusieurs jeux connus, tels que Crash, Mine et Blackjack.

## Requirements :
Installer Pygame dans votre terminal avec la commande : pip install pygame

## Explication des scripts :
Serveur.py & Client.py :
Ces scripts servent de test pour la communication entre plusieurs PC (clients). Cela permettra de jouer à plusieurs en même temps sur des machines différentes au Blackjack, ainsi qu’un système de chat pour que les joueurs puissent communiquer entre eux.

## Tests.py :
Ce script permet de tester des fonctionnalités avant de les intégrer aux vrais scripts afin d’éviter de faire buguer le casino. C'est pourquoi il ne fonctionne pas la plupart du temps.

## player_data.json :
Ce fichier stocke l'argent du joueur, mais sera remplacé dans le futur par une base de données qui contiendra bien plus d’informations.

## MineGame.py :
Gère toute la partie du jeu des Mines.

# Jeu des Mines :
Le but du jeu est simple : parier une somme d'argent, puis choisir combien de bombes (de 1 à 24) vous souhaitez qu’il y ait parmi les 25 cases. Plus il y a de bombes, plus vous avez de chances de perdre, mais vous gagnerez également plus d'argent. Après chaque bonne case choisie, votre multiplicateur augmentera. Ce multiplicateur affectera la somme d'argent que vous recevrez lorsque vous déciderez de retirer vos gains.

