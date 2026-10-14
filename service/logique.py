from sys import audit
from securite import securites
from pydantic import BaseModel
from fastapi import Query, HTTPException, Request
from typing import Any
from utils.loggers import logger, audit
from utils.gui import guis, gui2
from typing import Any, Dict
from dotenv import load_dotenv
from service.cache import get_cache, set_cache, stopredis
from tenacity import retry, stop_after_attempt, wait_exponential
from service.broker import message, arretrabbitmq, start_consumer
from pika.exceptions import AMQPConnectionError
import threading
import pybreaker
from opentelemetry import trace
import uuid
import signal
import subprocess

try:
    from base_de_donnees.base_de_donnee import (
        selection,
        deletion,
        creation,
        modification,
        stopdb,
    )
except Exception as e:
    print(e)


class Donnee(BaseModel):
    donnee: str
    id: int


shutting_down = threading.Event()
tracer = trace.get_tracer(__name__)
# -------------
# log
users = 10
# -----------

users_id = str(uuid.uuid4())


# _________________________________
# en cour d implementation
def compte():
    users_id = str(uuid.uuid4())
    role = "users"
    ids = "1"
    passe = "12"
    a = "1"
    b = "12"

    session = 1523
    cache = get_cache(str(session))
    if session == cache:
        print("bienvenue")
        return users_id
    else:
        if a == ids and b == passe:
            print("bienvenue")
            message(str(session))
            return users_id


compte()
# __________________________________

breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)

start_consumer()


# Affichage de la page d'accueil
def home() -> Any:
    if shutting_down.is_set():
        return "shutdown"
    trace_id = str(uuid.uuid4())
    requette_id = str(uuid.uuid4())
    logs = (
        f"trace_id={trace_id} requette_id={requette_id} users_id={users_id} service=gui"
    )
    logger.info(f"api alumer {logs}")
    try:
        securites.atest()
        return guis()

    except Exception as e:
        logger.error(f"Erreur lors de l'affichage GUI-{e}-{logs}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "erreur interne du serveur",
                "data": {"user_id": "gui not found"},
            },
        )


def home2():
    if shutting_down.is_set():
        return "shutdown"
    trace_id = str(uuid.uuid4())
    requette_id = str(uuid.uuid4())
    logs = f"trace_id={trace_id} requette_id={requette_id} users_id={users_id} service=gui_V2"
    logger.info(f"API V2 allumer {logs}")
    try:
        return gui2()
    except Exception as e:
        logger.error(f"Erreur lors de l'affichage GUI{e}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "erreur interne du serveur",
                "data": {"user_id": 10},
            },
        )


# Recherche sécurisée
def recherche_donnee(item: Any) -> Dict[str, Any]:
    if shutting_down.is_set():
        return "shutdown"
    try:
        with tracer.start_as_current_span("db.recherche") as db_span:
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
        logger.error(f"Erreur BDD (selection) : {e} - {users}-{trace_id}-{users_id}")
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
            logger.warning(f"Donnée corrompue détectée en BDD : {e} - {users}")
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
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def get_donnee(
    limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)
) -> Dict[str, Any]:
    if shutting_down.is_set():
        return "shutdown"
    try:
        trace_id = str(uuid.uuid4())
        with tracer.start_as_current_span("db.get_donnee") as db_span:
            data = breaker.call(selection)
            return {"data": data[offset : offset + limit]}
    except pybreaker.CircuitBreakerError:
        logger.error(f"erreur de db-{users}-{trace_id}")
        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "code": "DATABASE_UNAVAILABLE",
                "message": "La base de données est temporairement indisponible.",
            },
        )

    except Exception as e:
        logger.error(f"Erreur BDD (get_donnee) : {e} - {users}")
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
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def create_donnee(item: str):
    if shutting_down.is_set():
        return "shutdown"

    trace_id = str(uuid.uuid4())
    requette_id = str(uuid.uuid4())
    logs = f"trace_id={trace_id} requette_id={requette_id} users_id={users_id} service= create donnee"
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
        cache = get_cache(item)
        if cache:
            return cache
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
        with tracer.start_as_current_span("db.creation") as db_span:
            c = breaker.call(creation, item)
            # erreur
            logger.info(f"un items a ete creer {logs}")
        with tracer.start_as_current_span("message rabitmq") as db_span:
            try:
                c = "probleme de cache"
                set_cache(item, c)
            except Exception as e:
                print(e)

            message(c)
            audit.info(f"Donnée enregistrée {logs}")
            return {"message": "La donnée a été sauvegardée"}

    except pybreaker.CircuitBreakerError as e:
        logger.error(f"erreur de db - {e} - {logs}")
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
        logger.exception(f"Erreur critique lors de la création : {e} - {logs}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "erreur interne",
                "data": {"user_id": 10},
            },
        )


# Permet la mise à jour sécurisée des données
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def update_donnee(item_id: int, donnee_text: str) -> Dict[str, str]:
    if shutting_down.is_set():
        return "shutdown"
    trace_id = str(uuid.uuid4())
    requette_id = str(uuid.uuid4())
    logs = f"trace_id={trace_id} requette_id={requette_id} users_id={users_id} service= update"
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
                with tracer.start_as_current_span("db.update") as db_span:
                    breaker.call(modification, item_id, donnee_text)
                    audit.info(f"un items a ete mise a jour {logs}")
                    # ajouter encienne valeur nouvelle valeur
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
        logger.error(f"erreur de la mise a jour {logs}")
        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "code": "DATABASE_UNAVAILABLE",
                "message": "La base de données est temporairement indisponible.",
            },
        )

    except Exception as e:
        logger.error(f"Erreur critique lors de la modification de {e}{logs}")
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
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def delete_donnee(item: int) -> Dict[str, Any]:
    if shutting_down.is_set():
        return "shutdown"
    trace_id = str(uuid.uuid4())
    requette_id = str(uuid.uuid4())
    logs = f"trace_id={trace_id} requette_id={requette_id} users_id={users_id} service=delete"
    try:
        data = breaker.call(selection)
        for d in data:
            if int(d["id"]) == item:
                with tracer.start_as_current_span("db.deletion") as db_span:
                    breaker.call(deletion, item)
                    audit.info(f"Donnée numéro {item} supprimée - {logs}")
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
        logger.error(f"erreur de db-{logs}")
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
        logger.error(f"Erreur critique lors de la suppression de {item} : {e} {logs}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "code": "USER_NOT_FOUND",
                "message": "erreur lors de la suppresion",
                "data": {"user_id": 10},
            },
        )


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def ping():
    if shutting_down.is_set():
        return "shutdown"
    return {"message": "Ping reussie"}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def ready():
    if shutting_down.is_set():
        return "shutdown"
    trace_id = str(uuid.uuid4())
    requette_id = str(uuid.uuid4())
    logs = f"trace_id={trace_id} requette_id={requette_id} users_id={users_id} service=base de donnee"
    try:
        with tracer.start_as_current_span("db.ready") as db_span:
            data = breaker.call(selection)
        if data is None:
            logger.error(f"base de donnee introuvable{logs}")
            return False
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


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def telemetry():
    if shutting_down.is_set():
        return "shutdown"
    tracer = trace.get_tracer("test")

    with tracer.start_as_current_span("mon-test-jaeger") as span:
        span.set_attribute("test.message", "Bonjour Jaeger")
        span.set_attribute("test.number", 123)

    return {"status": "ok"}


def stop_application():
    shutting_down.set()
