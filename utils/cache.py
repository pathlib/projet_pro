import redis
import threading
from utils.loggers import logger
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
print(REDIS_HOST, REDIS_PORT)

client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

sessions = 0
MAX = 20
EXPIRATION = 60

redis_shutdown = threading.Event()
semaphore = threading.Semaphore(20)


def get_cache(key):
    if redis_shutdown.is_set():
        return None
    with semaphore:
        data = client.get(key)
        return data


def set_cache(key, items, ttl=3600):
    if redis_shutdown.is_set():
        return None
    with semaphore:
        client.set(key, items, ex=ttl)
        return items


def session(sessions: int):
    if redis_shutdown.is_set():
        return None
    with semaphore:
        count = client.incr(sessions)
        if count == 1:
            client.expire(sessions, EXPIRATION)
            print(sessions)
        if count > MAX:
            raise HTTPException(status_code=429, detail={"Trop de requêtes"})
        return None


def stopredis():
    print("Arret redis en cour ")
    try:
        redis_shutdown.set()
        for _ in range(20):
            semaphore.acquire()
        client.close()
        print("redis arreter")
    except Exception as e:
        logger.exception("Erreur fermeture Redis")
        print(f"Erreur opération Redis impossible après fermeture : {e}", flush=True)
