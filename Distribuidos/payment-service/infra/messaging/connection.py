import pika
from app.config.core import settings

def get_connection():

    credentials = pika.PlainCredentials(
        username="guest",
        password="guest"
    )

    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials,
    )

    return pika.BlockingConnection(parameters)