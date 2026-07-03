Le projet est actuellement en cours de développement. Certaines fonctionnalitès ne sont pas encore disponibles ou pas encore corrigèes.
# API Python CRUD

Projet Python de développement d’une API CRUD.

## Description

Les différentes fonctionnalités sont :

- API et gestion des requêtes  
- Services métier  
- Gestion des données  
- Sécurité et contrôle d’accès  
- Journalisation des événements  
- Tests de qualité  

# Structure du projet

api/
base_de_donnees/
securite/
service/
utils/
quality_tests/
.gitignore
README.md

---

### api/

Contient les endpoints, la logique de communication et le traitement des requêtes.

### base_de_donnees/

Gestion de la base de données, requêtes et stockage des informations.

### securite/

Fonctions liées à la sécurité :

- validation
- contrôle d’accès
- protection des données

### service/

Logique métier principale de l’application.

### utils/

Outils complémentaires :

- logger
- interface graphique
- utilitaires divers

### quality_tests/

Tests unitaires et vérification du bon fonctionnement des modules.

---

## Technologies utilisées

- Python 3.13
- Pytest
- Logging
- Git
- GitHub
- Black
- Ruff

## Installation

Cloner le dépôt :

