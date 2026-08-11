from celery import Celery
import time
import os

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

celery = Celery("worker", broker=CELERY_BROKER_URL, backend="rpc://")


@celery.task
def envoyer_email(email):

    time.sleep(5)

    print(f"Email envoyé à {email}")
