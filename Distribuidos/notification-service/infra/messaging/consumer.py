import json
from .connection import get_connection
from .constants import PAYMENT_EXCHANGE


class RabbitMQConsumer:
    def __init__(self):
        self.connection = get_connection()
        self.channel = self.connection.channel()

    def register_queue(self, exchange: str, queue: str, routing_key: str, callback: callable):

        self.channel.exchange_declare(
            exchange=exchange,
            exchange_type="topic",
            durable=True,
        )

        self.channel.queue_declare(
            queue=queue,
            durable=True
        )

        self.channel.queue_bind(
            exchange=exchange,
            queue=queue,
            routing_key=routing_key
        )

        def wrapper(ch, method, properties, body):
            try:
                data = json.loads(body)
                callback(data)

                ch.basic_ack(delivery_tag=method.delivery_tag)
            
            except Exception as e:
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        self.channel.basic_consume(
            queue=queue,
            auto_ack=False,
            on_message_callback=wrapper
        )
    
    def start(self):
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        if self.connection and not self.connection.is_closed:
            self.channel.stop_consuming()
            self.connection.close()
            print("Conexão com RabbitMQ encerrada.")