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

### tests/

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
- Prometheus
- slowapi
- alembic
- docker

## Installation

# Installation et lancement du projet

## 1. Cloner le dépôt GitHub

```bash
git clone https://github.com/pathlib/projet_pro.git
```

## 2. Accéder au dossier du projet

```bash
cd projet_pro
```

## 3. Créer un environnement virtuel Python

```bash
python -m venv venv
```

## 4. Activer l’environnement virtuel

**Windows :**

```bash
venv\Scripts\activate
```

**Linux / macOS :**

```bash
source venv/bin/activate
```

## 5. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 6. Lancer l’API

Démarrer le serveur avec Uvicorn :

```bash
uvicorn api.api:app --reload
```

## Accès à l’API

Une fois le serveur lancé, l’API est disponible à l’adresse :

http://127.0.0.1:8000

La documentation interactive FastAPI est accessible ici :

http://127.0.0.1:8000/docs



