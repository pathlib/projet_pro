?? Le projet est actuellement en cours de d�veloppement. Certaines fonctionnalit�s ne sont pas encore disponibles ou pas encore corrig�es. ??

# API PYTHON CRUD
Projet Python de d�veloppement d'une API CRUD
## Description

Les diff�rentes fonctionnalit�s sont?:

API et gestion des requ�tes
Services m�tier
Gestion des donn�es
S�curit� et contr�le d'acc�s
Journalisation des �v�nements
Tests qualit�

# Structure du projet
api/
base_de_donnees/
securite/
service/
utils/
quality_tests/
.gitignore
README.md


### api/

Contient les endpoints, la logique de communication et le traitement des requ�tes.

### base_de_donnees/

Gestion de la base de donn�es, requ�tes et stockage des informations.

### securite/

Fonctions li�es � la s�curit� :

- validation
- contr�le d'acc�s
- protection des donn�es

### service/

Logique m�tier principale de l'application.

### utils/

Outils compl�mentaires :

- logger
- interface graphique
- utilitaires divers

### quality_tests/

Tests unitaires et v�rification du bon fonctionnement des modules.

---
## Technologies utilis�es

- Python 3.13
- Pytest
- Logging
- Git
- GitHub
- black
- ruff

  ## Installation

Cloner le d�p�t :
git clone https://github.com/pathlib/projet_pro.git

Acc�der dans le dossier :
cd pathlib

Installer les d�pendances :
pip install -r requirements.txt

## Lancement
Ex�cuter l'application :
python main.py

## Tests

Lancer les tests :
pytest

## Projet

D�velopp� dans le cadre d'un apprentissage avanc� de Python, du d�veloppement logiciel et des bonnes pratiques de programmation.
