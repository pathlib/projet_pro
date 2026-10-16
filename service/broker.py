import os
import threading
from dotenv import load_dotenv
import pika
from utils.loggers import logger

load_dotenv()

# Permet de demander l'arrêt du consumer
shutdown_event = threading.Event()

# Protection du producteur
rabbit_lock = threading.Lock()

# Protection du démarrage/arrêt du consumer
consumer_lock = threading.Lock()

# Référence vers le thread du consumer
consumer_thread = None
SHUTDOWN_TIMEOUT = 30

RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")

MAIN_QUEUE = "hello"
DEAD_EXCHANGE = "dead_letter_exchange"
DEAD_QUEUE = "dead_routing_key"
DEAD_ROUTING_KEY = "dead"


def rabbitmq():
    if not all([RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_HOST, RABBITMQ_PORT]):
        raise RuntimeError("Paramètres RabbitMQ manquants dans l'environnement")

    try:
        port = int(RABBITMQ_PORT)
    except ValueError as e:
        raise RuntimeError("RABBITMQ_PORT invalide") from e

    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=port,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD),
            heartbeat=600,
            blocked_connection_timeout=300,
            connection_attempts=3,
            retry_delay=2,
        )
    )


def declare_topology(channel):
    """Déclare exchange, DLQ et queue principale (identique côté producteur et consumer)."""
    channel.exchange_declare(
        exchange=DEAD_EXCHANGE, exchange_type="direct", durable=True
    )
    channel.queue_declare(queue=DEAD_QUEUE, durable=True)
    channel.queue_bind(
        exchange=DEAD_EXCHANGE, queue=DEAD_QUEUE, routing_key=DEAD_ROUTING_KEY
    )
    channel.queue_declare(
        queue=MAIN_QUEUE,
        durable=True,
        arguments={
            "x-dead-letter-exchange": DEAD_EXCHANGE,
            "x-dead-letter-routing-key": DEAD_ROUTING_KEY,
        },
    )


def message(messages):
    if shutdown_event.is_set():
        logger.warning("Shutdown en cours : message refusé")
        return False

    connection = None
    try:
        with rabbit_lock:
            if shutdown_event.is_set():
                logger.warning("Shutdown en cours : message refusé")
                return False

            connection = rabbitmq()
            channel = connection.channel()
            declare_topology(channel)

            channel.confirm_delivery()
            channel.basic_publish(
                exchange="",
                routing_key=MAIN_QUEUE,
                body=messages.encode("utf-8"),
                properties=pika.BasicProperties(delivery_mode=2),
                mandatory=True,
            )

            logger.info(f"Message envoyé : {messages}")
            return True

    except Exception as e:
        logger.exception(f"Erreur RabbitMQ producteur : {e}")
        return False

    finally:
        if connection is not None and connection.is_open:
            try:
                connection.close()
                logger.info("Connexion producteur fermée")
            except Exception as e:
                logger.exception(f"Erreur fermeture producteur : {e}")


def callback(ch, method, properties, body):
    # En cas d'arrêt : on ne traite pas et on n'acquitte pas.
    # Le message est automatiquement remis en queue à la fermeture de la connexion
    # (évite une boucle nack/requeue/redelivery).
    if shutdown_event.is_set():
        logger.info("Shutdown en cours : message non traité (sera remis en queue)")
        return

    try:
        message_recu = body.decode("utf-8")
        logger.info(f"Message reçu : {message_recu}")

        # Traitement du message
        # ...

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logger.exception(f"Erreur traitement RabbitMQ : {e}")
        try:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except pika.exceptions.AMQPError:
            logger.exception("Impossible de nack le message (canal fermé ?)")


# CONSUMER
def recois():
    while not shutdown_event.is_set():
        connection = None
        try:
            logger.info("Tentative de connexion du consumer RabbitMQ...")
            connection = rabbitmq()
            channel = connection.channel()
            declare_topology(channel)

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                queue=MAIN_QUEUE, on_message_callback=callback, auto_ack=False
            )

            logger.info("Consumer RabbitMQ démarré et à l'écoute")

            while not shutdown_event.is_set():
                connection.process_data_events(time_limit=1)

        except (pika.exceptions.AMQPError, OSError) as e:
            if shutdown_event.is_set():
                break
            logger.exception(
                f"Connexion perdue ou erreur réseau ({e}). Nouvelle tentative dans 5 secondes..."
            )
        except Exception as e:
            if shutdown_event.is_set():
                break
            logger.exception(f"Erreur inattendue dans le consumer : {e}")
        finally:
            if connection is not None and connection.is_open:
                try:
                    connection.close()
                except Exception:
                    pass

        # Attente avant reconnexion si non stoppé
        shutdown_event.wait(5)

    logger.info("Boucle du consommateur terminée proprement.")


# DÉMARRER LE CONSUMER
def start_consumer():
    global consumer_thread
    with consumer_lock:
        if consumer_thread is not None and consumer_thread.is_alive():
            logger.info("Consumer RabbitMQ déjà démarré")
            return consumer_thread

        shutdown_event.clear()
        consumer_thread = threading.Thread(
            target=recois, daemon=True, name="RabbitMQ-Consumer"
        )
        consumer_thread.start()
        logger.info("Thread RabbitMQ démarré")
        return consumer_thread


# ARRÊTER LE CONSUMER
def arretrabbitmq():
    global consumer_thread
    logger.info("Demande de shutdown RabbitMQ")
    shutdown_event.set()

    with consumer_lock:
        thread = consumer_thread

    if thread is None:
        logger.info("Aucun consumer RabbitMQ actif")
        return True

    if thread is not threading.current_thread():
        thread.join(SHUTDOWN_TIMEOUT)

    if thread.is_alive():
        logger.warning("Le consommateur est encore actif après le timeout")
        return False

    with consumer_lock:
        consumer_thread = None
    logger.info("Consommateur arrêté correctement")
    return True
