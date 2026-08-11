from celery import Celery
import time
from dotenv import load_dotenv
import os

load_dotenv()
BROKER_URL = os.getenv("BROKER_URL")
BROKER_PORT = os.getenv("BROKER_PORT")
celery = Celery("worker", broker=BROKER_URL, backend=BROKER_PORT)

"""@celery.task
def envoyer_email(email):

    time.sleep(5)

    print(f"Email envoyé à {email}")"""
