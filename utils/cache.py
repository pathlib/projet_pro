import redis
import threading
from utils.loggers import logger
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
print(REDIS_HOST, REDIS_PORT)
client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

event = True


def get_cache(key):
    if not event:
        semaphore = threading.Semaphore(20)
        with semaphore:
            data = client.get(key)
    else:
        return None
    return data


def set_cache(key, items, ttl=3600):
    client.set(key, items, ex=ttl)
    return items


sessions = 0
MAX = 20
EXPIRATION = 60


def session(sessions: int):
    count = client.incr(sessions)
    if count == 1:
        client.expire(sessions, EXPIRATION)
        print(sessions)
    if count > MAX:
        raise HTTPException(status_code=429, detail={"Trop de requêtes"})


def stopredis():
    print("Arret redis en cour ")
    try:
        event = False
        client.close()
        print("redis arreter")
    except Exception as e:
        logger.exception("Erreur fermeture Redis")
        print(f"Erreur opération Redis impossible après fermeture : {e}", flush=True)
