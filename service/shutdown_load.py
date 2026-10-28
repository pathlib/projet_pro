from service.broker import arretrabbitmq
from base_de_donnees.base_de_donnee import stopdb
from service.cache import stopredis
from utils.loggers import logger
from service.telemetry import stopopentelemetry
from service.logique import stop_application


def shutdowns(app):
    try:
        stop_application()
        logger.info("Arrêt en cours")
    except Exception as e:
        logger.exception(f"Erreur {e}")
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
