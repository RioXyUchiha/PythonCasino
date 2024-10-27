# Casino en Python
Ce projet vise à créer un casino en Python regroupant plusieurs jeux connus, tels que Crash, Mine et Blackjack.

## Pré-requis :
Installez Pygame dans votre terminal avec la commande : pip install pygame
Installez Pygame Widgets dans votre terminal avec la commande : pip install pygame_widgets
Installez MySql connector dans votre terminal avec la commande : pip install mysql-connector-python
Mettez la taille de votre écran à 100 % pour éviter tout bug d'affichage

## Pré-requis :
Tout d'abord, lancez le script MineGame.py, puis dans l'output de Visual Studio Code ou PyCharm, écrivez votre username. Ensuite, vous pourrez jouer aux jeux de mine.

## Explication des scripts :
Serveur.py & Client.py (WIP) :
Ces scripts servent de test pour la communication entre plusieurs ordinateurs (clients). Cela permettra de jouer à plusieurs en même temps au Blackjack sur des machines différentes, ainsi qu’un système de chat pour que les joueurs puissent communiquer entre eux.
Lancer seulement MineGame.py et server/client si vous êtes plusieurs

### Tests.py :
Ce script permet de tester des fonctionnalités avant de les intégrer aux vrais scripts afin d’éviter de faire buguer le casino. C'est pourquoi il ne fonctionne pas la plupart du temps.

### player_data.json :
Ce fichier stocke l'argent du joueur, mais il sera remplacé dans le futur par une base de données qui contiendra bien plus d’informations.

### MineGame.py :
Gère toute la partie du jeu des Mines.

## Jeu des Mines :
Le but du jeu est de parier une somme d'argent de votre choix, puis de choisir combien de bombes (de 1 à 24) vous souhaitez qu’il y ait parmi les 25 cases. Plus il y a de bombes, plus vous avez de chances de perdre, mais vous gagnerez également plus d'argent. Après chaque bonne case choisie, votre multiplicateur augmentera. Ce multiplicateur affectera la somme d'argent que vous recevrez lorsque vous déciderez de retirer vos gains.

## Jeu du Blackjack
Le but du jeu est de parier une somme d'argent prédéfinie par le jeu, puis de recevoir deux cartes. Additionnez ensuite leurs valeurs. Un PNJ (personnage non joueur) jouera le rôle de l'adversaire et recevra également deux cartes, mais vous ne pourrez en voir qu'une seule. Vous aurez le choix de piocher ou non une carte supplémentaire. Pourquoi piocher ? Le but est de vous rapprocher le plus possible de 21, car la règle du jeu est simple : celui qui atteint ou s'approche le plus de 21 sans dépasser remporte la partie. Si vous dépassez 21, vous perdez immédiatement. Si vous décidez de ne pas piocher, la seconde carte du PNJ sera révélée. Si la somme de ses deux cartes est inférieure ou égale à 16, il piochera une troisième carte, voire plus, tant qu'il n'aura pas dépassé 16. Si le PNJ dépasse 21, il perd automatiquement. Si vous gagnez, vous recevrez le double de la mise que vous aviez pariée.

## Jeu du Crash
Ce jeu consiste à parier la somme que vous voulez avant que la fusée décolle, ensuite la fusée décollera après un certain temps laissant le temps aux joueurs de parier. Quand la fusée aura finalement décollé, le multiplicateur augmentera de façon exponentielle, mais attention à vous retirer avant que la fusée ne s'écrase, sinon vous perdrez tout. Si vous vous retirez avant qu'elle ne s'écrase, vous gagnerez la somme que vous avez pariée avec le multiplicateur appliqué dessus.

## Sources
https://github.com/anderskm/gputil
https://realpython.com/python-sockets/
https://stackoverflow.com/questions/73673458/how-to-get-accurate-process-cpu-and-memory-usage-with-python
