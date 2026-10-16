from celery import Celery
from tenacity import retry, stop_after_attempt, wait_exponential
import time
import os
from dotenv import load_dotenv

load_dotenv()


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def retrys():
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    if not CELERY_BROKER_URL:
        raise ValueError("CELERY_BROKER_URL not found")
    app = Celery("worker", broker=CELERY_BROKER_URL, backend="rpc://")
    return celery


app = retrys()


@app.task
def envoyer_email(email):

    time.sleep(5)

    print(f"Email envoyé à {email}")
