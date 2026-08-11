import pika
import threading
import os
from dotenv import load_dotenv

# ERREUR DE ENV
load_dotenv()
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")

print(RABBITMQ_HOST)
print(RABBITMQ_PORT)
print(RABBITMQ_USER)
print(RABBITMQ_PASSWORD)


def message(messages):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD),
        )
    )

    channel = connection.channel()

    channel.queue_declare(
        queue="hello",
        durable=True,
        arguments={
            "x-dead-letter-exchange": "dead_letter_exchange",
            "x-dead-letter-routing-key": "dead",
        },
    )
    # producteur
    channel.basic_publish(exchange="", routing_key="hello", body=messages)
    print(" [x] Sent 'Hello World!'")
    connection.close()


print("Connexion OK")


def callback(ch, method, properties, body):
    message = body.decode()

    print("Message reçu :")
    print(message)
    # action a mener


def recois():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD),
        )
    )

    channel = connection.channel()

    # --- ÉTAPE 1 : On crée la Dead Letter Queue (la boîte de secours) ---
    channel.queue_declare(queue="dead_routing_key", durable=True)

    # --- ÉTAPE 2 : On crée l'échangeur et on le relie à la boîte de secours ---
    channel.exchange_declare(exchange="dead_letter_exchange", durable=True)
    channel.queue_bind(
        exchange="dead_letter_exchange", queue="dead_routing_key", routing_key="dead"
    )

    # --- ÉTAPE 3 : On crée la queue 'hello' en y attachant les options de secours ---
    channel.queue_declare(
        queue="hello",
        durable=True,
        arguments={
            "x-dead-letter-exchange": "dead_letter_exchange",
            "x-dead-letter-routing-key": "dead",
        },
    )

    # On écoute la queue principale
    channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=False)

    print(" [*] Consumer en attente avec Dead Letter Queue active...")
    channel.start_consuming()


e = threading.Thread(target=recois)
e.start()
