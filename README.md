![](https://i.imgur.com/pW7K0Xp.png)

# <font size="8pt"><b>Guide utilisateur</b></font>

<font size="4pt" color="112d5c"><strong>Project name : </strong>Omelette</font> 

---
<font size="3pt">_**Auteurs:**_</font>
Amir Marachly
Simon Meier
Aymeric Schmid

<font size="5pt"><b>Table des matières:</b></font>

[ToC]

---

### 1 Prérequis

L'utilisation de ce projet nécessite:
- librairie Python **ply 3.11**.
- librairie Python Graphviz 0.14.2
- librairie Python Pydot 1.4.2
- installer [Graphviz](https://graphviz.org).

### 2 Installation
Commencez par télécharger le dossier du projet [ici](https://github.com/AmirMarachly/omelette/archive/refs/heads/main.zip).

Une fois le dossier téléchargé et décompressé assurez-vous que les prérequis soit bien remplie grâce au fichier *requirements.txt* qui permet d'installer toutes les dépendances requises. 

Il suffit d'exécuter `InstallRequirements.bat` qui se trouve à la racine du projet.

Cependant, pour créer les graphes des arbres, il est nécessaire d'utiliser le paquet Graphviz. Pour ce faire, il suffit d'exécuter l'*installer* (`graphviz-install-2.50.0.exe`) disponible à la racine du projet. Cochez bien la case `Add Graphviz to the system PATH for all users` ou `Add Graphviz to the system PATH for current users`


| ![](https://i.imgur.com/77pXZQ3.png) |
| :----------------------------------: |


Après s'être assuré d'avoir tous les prérequis, il est possible d'exécuter des programmes en `Omelette`, par exemple de la manière suivante:
    - `python .\omelette.py .\input1.oml`

Une fois les étapes d'installation réalisée, vous pouvez vous lancer dans l'écriture de votre programme!

### 3 Création du premier programme
Pour commencer il vous faut créer un fichier texte avec l'extension `.oml` (exemple : salutlemonde.oml).

Une fois ceci fait il vous suffit de coder votre première phrase en `Omelette`. Elle doit commencer par une minuscule et finir par un point.

#### Exemple d'Hello World

```
afficher "Salut le monde!".
```

Voilà votre premier programme coder en `Omelette`.
