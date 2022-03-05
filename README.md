# Introduction au parallélisme

Dans le cadre de cet exercice vous aurez à faire un mini-projet impliquant à la fois du multiprocessing et du 
multithreading. 

### Contexte
Vous vous faites une petite station météo avec un petit ordinateur n'ayant pas beaucoup de ressources
computationel. En effet, votre ordinateur a accès à seulement 3 CPU, un nombre plutot étrange, mais 
qui fera l'affaire pour les besoins de la cause. Vous n'avez pas beaucoup de CPU, mais vous voulez tous les utiliser 
ce qui est normal, car quand on achète une machine étrange à 3 CPU, on veut utiliser les 3 CPU. Vous avez également
4 senseurs:
- Un thermomètre;
- Un détecteur de point de rosé;
- Un détecteur d'humidité;
- Un détecteur de pression.

### Objectif
Vous voulez enregistrer des statistiques des senseurs à tous les jours et les afficher en temps
réel, question de voir ce qui se passe dehors depuis les derniers jours. De plus, vous voulez utiliser
vos 3 CPU et vous voulez que le tout soit le plus parraléliser possible. Voici donc ce qui va se passer
sur les différents processus de votre application:

__Processus principal__:
Ce processus servira à gérer les autre processus, c'est-à-dire à les lancer en début de journée et à les arrêter
en fin de journée.

__Processus des senseurs__:
Dans ce processus vous voudrais lancer k threads pour lire et enregistrer les mesures prises par chacun de vos k 
senseurs.

Vous allez devoir enregistrer toutes les statistiques de tous vos senseurs dans le même fichier de la façon suivante:

| Date   |TempHighF| TempAvgF     | TempLowF | DewPointHighF | DewPointAvgF | DewPointLowF | HumidityHighPercent | HumidityAvgPercent | HumidityLowPercent |
|--------|----|--------------|----------|---------------|--------------|--------------|---------------------|--------------------|--------------------|
| date 0 |max temp| moyenne temp | min temp | max temp| moyenne temp | min temp| max %| moyenne %| min %|
| date 1 |max temp| moyenne temp | min temp | max temp| moyenne temp | min temp| max %| moyenne %| min %|
| ...    |...|...|...|...|...|...|...|...|...|
| date N |max temp| moyenne temp | min temp | max temp| moyenne temp | min temp| max %| moyenne %| min %|

Donc, dans une seule journée, vous allez lire des mesures de vos senseurs avec la méthode Sensor.read et vous allez
devoir garder en mémoire la valeur minimale courante de la journée ainsi que la valeur maximale et moyenne de cette 
journée.

*Tips*: Vous allez avoir k threads qui écrivent dans un même ficher 'en même temps', vous allez donc surement avoir
besoin d'utiliser une serrure (un Lock).


__Processus d'affichage__:
Dans ce processus, vous aller lire ce que vous avez enregistré avec vos threads de senseurs. Vous pouvez faire ce que
vous voulez pour que ce soit agréable à regarder. Dans notre, cas nous avons affiché les données des jours précédants 
et nous ajustons les données du jour courant en temps réel. Chaque senseur est dans un subplot différants et nous avons 
utilisé matplotlib.


### Tâche
Vous devez implémenter toutes les méthodes du folder .exercice contenant un 'TODO' dans la documentation. Ces méthodes
lance chacune une exception de non-implémentation. Vous pouvez donc lancer le script './_\_main__.py' et implémenter les
méthodes qui lancent ce type d'erreur.


## Setup

- Cloner le répertoire présent.
- Créer votre environnement virtuel pour ce mini-projet
- Installer les dépendances avec 
  - ```pip install -r requirements.txt```


## Références
- Pour plus d'information sur comment utiliser git:
    - [TutorielPython-Manuel/git](https://github.com/JeremieGince/TutorielPython-Manuel/tree/master/Cycle-de-developpement-avec-git)
- Pour plus d'information sur comment créer un environnement virtuel:
    - [TutorielPython-Manuel/Environments](https://github.com/JeremieGince/TutorielPython-Manuel/tree/master/Environments)
- Si vous désirez avoir des ressources au niveau de l'affichage avec python:
  - [Atelier de visualisation du ProgFest](https://github.com/rem657/AtelierVisualisation)
- Pour plus d'information sur le parralélisme avec python:
  - [GabGabG/pythonMultiprocessing](https://github.com/GabGabG/pythonMultiprocessing)


## Solution
La solution est fournie dans le dossier './solution'.










