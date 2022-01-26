# Parallelisme Intro

## Données météo
- Générateur de données par capteur (classes)
  - Une par capteur
  - getData -> donne donnée ponctuelle
  - Déterministe
    - Prend time step en entrée, \todo
  - Autres fcts + tard
## Utilisateur / étudiant
- Process 1:
  - Starter un thread / capteur
  - Écrire dans un fichier les données de getData (un fichier par capteur)
  - Starter un thread qui concat les fichiers de données dans .npy
- Process 2:
  - Load les .npy
  - Passer dans un algo à déterminer
  - Écrire les outputs dans .npy
## Tests unitaires
- Tester nb threads
- Tester nb processes
- Bon chiffres dans .npy (input/output)
