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

    def publish(self, routing_key: str, message: dict):
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

