import redis
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
print(REDIS_HOST, REDIS_PORT)
client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def get_cache(key):
    data = client.get(key)
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
