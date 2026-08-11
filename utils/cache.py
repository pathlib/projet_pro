import redis
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

client = redis.Redis(host=HOST, port=PORT, decode_responses=True)


def get_cache(key):
    data = client.get(key)
    return data


def set_cache(key, items, ttl=3600):
    client.set(key, items, ex=ttl)
    return items


sessions = "bienvenue"
MAX = 20
n = 60


def session(sessions: str):
    count = client.incr(sessions)
    if count == 1:
        client.expire(sessions, n)
        print(sessions)
    if count > MAX:
        raise HTTPException(status_code=429, detail={"Trop de requêtes"})
