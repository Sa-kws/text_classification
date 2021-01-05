# text_classification
Classification d'énoncés en plusieurs catégories

Avant de mettre en place les paramètres d'apprentissage ainsi que lancer l'apprentissage, il faut récupérer le bon jeu de données. Le code *'GetDomainActivities'* est donc à executer en premier, puis on pourra ensuite executer *'SetFeatures_MachineLearning'*.

## GetDomainActivities :
Parcours du dossier contenant les trois fichiers CSV composant le corpus. Pour chaque fichier, si la ligne contient *'domainActivities'* (colonne 1 : Dimension), alors on l'ajoute à la liste qu'on copie ensuite dans la nouvelle version du fichier

## SetFeatures_MachineLearning :
##### Outils :
Scikit-Learn
Pandas
SpaCy
Expression régulière (module re)
Glob

Mise en place des features : 
  - Taille de l'énoncé 
  - Présence de ponctuation spécifique
  - Forme de l'énoncé (Bag of Words)
  - Présence de caractère numérique
  - Part of Speech (Bag of Words)
  - Présence de proposition relatives
  - Lemme (Bag of Words)

## Machine Learning :
Algorithme : Random Forest
