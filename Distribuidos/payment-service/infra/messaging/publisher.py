import json
import pika  
from .connection import get_connection
from .constants import PAYMENT_EXCHANGE

class RabbitMQPublisher:
    def __init__(self):
        self.connection = get_connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=PAYMENT_EXCHANGE,
            exchange_type="topic",
            durable=True,
        )

    def publish(self, queue: str, routing_key: str, message: dict):
        self.channel.queue_declare(
            queue=queue,
            durable=True,
        ) # o ideal é que não tenha nada relacionado a fila, pois ele vai publicar apenas para o exchange com a routing key

        self.channel.queue_bind(
            exchange=PAYMENT_EXCHANGE,
            queue=queue,
            routing_key=routing_key,
        )

        self.channel.basic_publish(
            exchange=PAYMENT_EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2, 
            )
        )

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

