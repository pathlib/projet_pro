import redis
import threading
from utils.loggers import logger
from fastapi import HTTPException
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def retrys():
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    if not REDIS_HOST:
        raise Exception("REDIS_HOST not found")
    if not REDIS_PORT:
        raise Exception("REDIS_PORT not found")

    redis_port = int(REDIS_PORT)
    client = redis.Redis(host=REDIS_HOST, port=redis_port, decode_responses=True)
    if not client.ping():
        raise Exception("Erreur de connexion Redis")
    return client


client = retrys()

MAX_REQUESTS = 20
EXPIRATION = 60

redis_shutdown = threading.Event()
semaphore = threading.Semaphore(20)


def get_cache(key):
    if redis_shutdown.is_set():
        return None
    with semaphore:
        try:
            data = client.get(key)
            return data
        except redis.RedisError as e:
            logger.error(f"Erreur Redis rate limit: {e}")
            return None


def set_cache(key, items, ttl=3600):
    if redis_shutdown.is_set():
        return None
    with semaphore:
        try:
            client.set(key, items, ex=ttl)
            return items
        except redis.RedisError as e:
            logger.error(f"Erreur Redis rate limit: {e}")
            return None


def session(session_id: str):
    if redis_shutdown.is_set():
        return None
    with semaphore:
        try:
            count = client.incr(session_id)
            if count == 1:
                client.expire(session_id, EXPIRATION)
                print(session_id)
            if count > MAX_REQUESTS:
                raise HTTPException(status_code=429, detail="Trop de requêtes")
        except redis.RedisError as e:
            logger.error(f"Erreur Redis rate limit: {e}")
            raise HTTPException(
                status_code=503,
                detail="Service temporairement indisponible",
            )
        except HTTPException:
            # On relance l'exception HTTP 429 pour qu'elle soit renvoyée au client FastAPI
            raise
        return None


def stopredis():
    print("Arrêt Redis en cours...")
    try:
        redis_shutdown.set()
        client.close()
        print("redis arreter")
    except Exception as e:
        logger.exception("Erreur fermeture Redis")
        print(f"Erreur opération Redis impossible après fermeture : {e}")
