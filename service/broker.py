import pika
import threading
import os
import time
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))


# Permet de demander l'arrêt du consumer
shutdown_event = threading.Event()

# Protection du producteur
rabbit_lock = threading.Lock()

# Référence vers le thread du consumer
consumer_thread = None
SHUTDOWN_TIMEOUT = 30


def message(messages):

    # Ne plus accepter de nouveaux messages pendant le shutdown
    if shutdown_event.is_set():
        print("Shutdown en cours : message refusé")
        return False

    connection = None

    try:

        with rabbit_lock:

            # Vérification avant connexion
            if shutdown_event.is_set():
                print("Shutdown en cours : message refusé")
                return False

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    port=RABBITMQ_PORT,
                    credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD),
                )
            )

            # Vérification juste avant l'envoi
            if shutdown_event.is_set():
                print("Shutdown : envoi annulé")
                return False

            channel = connection.channel()

            channel.queue_declare(
                queue="hello",
                durable=True,
                arguments={
                    "x-dead-letter-exchange": "dead_letter_exchange",
                    "x-dead-letter-routing-key": "dead",
                },
            )

            channel.basic_publish(
                exchange="", routing_key="hello", body=messages.encode()
            )

            print(f"Message envoyé : {messages}")

            return True

    except Exception as e:

        print(f"Erreur RabbitMQ producteur : {e}")
        return False

    finally:

        if connection is not None and not connection.is_closed:

            try:
                connection.close()
                print("Connexion producteur fermée")

            except Exception as e:
                print(f"Erreur fermeture producteur : {e}")


def callback(ch, method, properties, body):

    try:

        message_recu = body.decode()

        print("Message reçu :")
        print(message_recu)

        # Message traité correctement
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:

        print(f"Erreur traitement : {e}")

        # Envoie le message vers la Dead Letter Queue
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


# CONSUMER


def recois():

    connection = None
    channel = None

    try:

        # CONNEXION RABBITMQ

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD),
            )
        )

        channel = connection.channel()

        # DEAD LETTER QUEUE

        channel.queue_declare(queue="dead_routing_key", durable=True)

        channel.exchange_declare(exchange="dead_letter_exchange", durable=True)

        channel.queue_bind(
            exchange="dead_letter_exchange",
            queue="dead_routing_key",
            routing_key="dead",
        )

        # QUEUE PRINCIPALE

        channel.queue_declare(
            queue="hello",
            durable=True,
            arguments={
                "x-dead-letter-exchange": "dead_letter_exchange",
                "x-dead-letter-routing-key": "dead",
            },
        )

        # CONSUMER

        channel.basic_consume(
            queue="hello", on_message_callback=callback, auto_ack=False
        )

        print("Consumer RabbitMQ démarré")
        while not shutdown_event.is_set():

            connection.process_data_events(time_limit=1)

        print("Shutdown RabbitMQ détecté")

    except Exception as e:

        print(f"Erreur consumer RabbitMQ : {e}")

    finally:

        if connection is not None and not connection.is_closed and channel.is_open:

            try:
                channel.close()
                connection.close()
                print("Connexion consumer RabbitMQ fermée")

            except Exception as e:

                print(f"Erreur fermeture consumer : {e}")


# DÉMARRER LE CONSUMER


def start_consumer():

    global consumer_thread
    if consumer_thread is not None and consumer_thread.is_alive():

        print("Consumer RabbitMQ déjà démarré")

        return consumer_thread

    # Réinitialiser le shutdown

    shutdown_event.clear()

    # Créer le thread

    consumer_thread = threading.Thread(
        target=recois, daemon=True, name="RabbitMQ-Consumer"
    )

    # Démarrer

    consumer_thread.start()

    print("Thread RabbitMQ démarré")

    return consumer_thread


# ARRÊTER LE CONSUMER


def arretrabbitmq():

    global consumer_thread

    print("Demande de shutdown RabbitMQ")

    # Signaler au consumer qu'il doit s'arrêter

    shutdown_event.set()

    print("Nouveaux messages refusés")

    # Attendre la fin du thread

    if consumer_thread is not None:

        consumer_thread.join(SHUTDOWN_TIMEOUT)

        if consumer_thread.is_alive():
            print("ATTENTION : " "le consumer RabbitMQ est encore actif")
        else:
            print("Consumer RabbitMQ arrêté")
            consumer_thread = None
    else:
        print("Aucun consumer RabbitMQ actif")
