from service.broker import arretrabbitmq
from base_de_donnees.base_de_donnee import stopdb
from utils.cache import stopredis
from utils.loggers import logger
from service.telemetry import stopopentelemetry
import time


def shutdowns(app):
    logger.info("Arrêt en cours")
    try:
        arretrabbitmq()
        logger.info("RabbitMQ fermé")
    except Exception as e:
        logger.exception(f"Erreur RabbitMQ{e}")

    try:
        stopredis()
        logger.info("Redis fermé")
    except Exception as e:
        logger.exception(f"Erreur Redis{e}")

    try:
        stopdb()
        logger.info("SQLite fermée")
    except Exception as e:
        logger.exception(f"Erreur SQLite {e}")
    try:
        stopopentelemetry(app)
        logger.info("OpenTelemetry fermé")
    except Exception as e:
        logger.exception(f"Erreur OpenTelemetry{e}")
    logger.info("SHUTDOWN : terminé")
