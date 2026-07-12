from securite import securites
from pydantic import BaseModel
from fastapi import Query, HTTPException
from utils.loggers import logger
from utils.gui import guis, gui2

# from base_de_donnees.base_de_donnee import selection, deletion, creation, modification
from typing import Any, Dict, List
from dotenv import load_dotenv
import pybreaker
import os

try:
    from base_de_donnees.base_de_donnee import (
        selection,
        deletion,
        creation,
        modification,
    )
except Exception:
    pass


class Donnee(BaseModel):
    donnee: str
    id: int


# _________________________________
# en cour d implementation
load_dotenv()
s = os.getenv("SECRET_KEY")
# __________________________________

breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)


# Affichage de la page d'accueil
def home() -> Any:
    try:
        logger.info("API allumer")
        securites.atest()
        return guis()
    except Exception as e:
        logger.error(f"Erreur lors de l'affichage GUI : {e}-{'user10'}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "erreur interne du serveur",
                "data": {"user_id": 10},
            },
        )


def home2():
    return gui2()


# Recherche sécurisée
def recherche_donnee(item: Any) -> Dict[str, Any]:
    try:
        data = breaker.call(selection)
    except pybreaker.CircuitBreakerError:
        logger.error("Circuit ouvert : accès à la base refusé")
        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "code": "DATABASE_UNAVAILABLE",
                "message": "La base de données est temporairement indisponible.",
            },
        )

    except Exception as e:
        logger.error(f"Erreur BDD (selection) : {e}-{'user10'}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "erreur interne de la base",
                "data": {"user_id": 10},
            },
        )

    for d in data:
        try:
            if int(d["id"]) == item:
                return {"data": d}
            if str(d["data"]) == item:
                return {"data": d}

        except (ValueError, KeyError) as e:
            logger.warning(f"Donnée corrompue détectée en BDD : {e}-{'user10'}")
            continue
    raise HTTPException(
        status_code=404,
        detail={
            "success": False,
            "code": "USER_NOT_FOUND",
            "message": "valeur introuvable.",
            "data": {"user_id": 10},
        },
    )


# Obtenir les données avec une limite maximale stricte
def get_donnee(
    limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)
) -> Dict[str, Any]:
    try:
        data = breaker.call(selection)
        return {"data": data[offset : offset + limit]}
    except pybreaker.CircuitBreakerError:
        logger.error(f"erreur de db-{'user10'}")
        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "code": "DATABASE_UNAVAILABLE",
                "message": "La base de données est temporairement indisponible.",
            },
        )

    except Exception as e:
        logger.error(f"Erreur BDD (get_donnee) : {e}-{'user10'}")
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "Utilisateur introuvable.",
                "data": {"user_id": 10},
            },
        )


# Permet de créer les données de façon sécurisée
def create_donnee(item: str):
    if not item or not item.strip():
        raise HTTPException(
            status_code=403,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "valeur interdite",
                "data": {"user_id": 10},
            },
        )

    try:
        data = breaker.call(selection)
        for d in data:
            if d["donnee"] == item:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "success": False,
                        "code": "USER_NOT_FOUND",
                        "message": "la donne existe deja",
                        "data": {"user_id": 10},
                    },
                )
        breaker.call(creation, item)
        logger.info("Donnée enregistrée")
        return {"message": "La donnée a été sauvegardée"}

    except pybreaker.CircuitBreakerError:
        logger.error(f"erreur de db-{'user10'}")
        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "code": "DATABASE_UNAVAILABLE",
                "message": "La base de données est temporairement indisponible.",
            },
        )

    except HTTPException:
        raise  # On laisse passer nos propres erreurs HTTP
    except Exception as e:
        logger.error(f"Erreur critique lors de la création : {e}-{'user10'}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "imposible de sauvegarder la donneee",
                "data": {"user_id": 10},
            },
        )


# Permet la mise à jour sécurisée des données
def update_donnee(item_id: int, donnee_text: str) -> Dict[str, str]:
    if not donnee_text or not donnee_text.strip():
        raise HTTPException(
            status_code=422,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "valeur vide interdite",
                "data": {"user_id": 10},
            },
        )

    try:
        data = breaker.call(selection)
        for d in data:
            if int(d["id"]) == item_id:
                breaker.call(modification, item_id, donnee_text)
                logger.info(f"Donnée {item_id} modifiée-{'user10'}")
                return {"message": "Modification réussie"}

        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "donnee introuvable.",
                "data": {"user_id": 10},
            },
        )

    except HTTPException:
        raise

    except pybreaker.CircuitBreakerError:
        logger.error(f"erreur de db-{'user10'}")
        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "code": "DATABASE_UNAVAILABLE",
                "message": "La base de données est temporairement indisponible.",
            },
        )

    except Exception as e:
        logger.error(f"Erreur critique lors de la modification de {item_id} : {e}-{'user10'}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "erreur lors de la modification",
                "data": {"user_id": 10},
            },
        )


# Supprime proprement et gère l'absence de l'élément
def delete_donnee(item: int) -> Dict[str, Any]:
    try:
        data = breaker.call(selection)
        for d in data:
            if int(d["id"]) == item:

                breaker.call(deletion, item)
                logger.info(f"Donnée numéro {item} supprimée-{'user10'}")
                return {"message": f"La donnée {item} a bien été supprimée"}

        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "donnee introuvable",
                "data": {"user_id": 10},
            },
        )
    except pybreaker.CircuitBreakerError:
        logger.error(f"erreur de db-{'user10'}")
        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "code": "DATABASE_UNAVAILABLE",
                "message": "La base de données est temporairement indisponible.",
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur critique lors de la suppression de {item} : {e}-{'user10'}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "erreur lors de la suppresion",
                "data": {"user_id": 10},
            },
        )


def ping():
    return {"message": "Ping reussie"}


def ready():
    try:
        data = breaker.call(selection)
        if data is not None:
            return True
    except Exception:
        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "Database unavailable",
                "data": {"user_id": 10},
            },
        )
