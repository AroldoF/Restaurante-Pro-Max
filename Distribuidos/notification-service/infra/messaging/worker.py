from infra.messaging.consumer import RabbitMQConsumer
from infra.messaging.constants import PAYMENT_EXCHANGE, PAYMENT_ROUTING_KEY, PAYMENT_CONFIRM_QUEUE
from app.messaging.handlers.notification import prepare_order

def start_consumers():
    consumer = RabbitMQConsumer()

    consumer.register_queue(
        exchange=PAYMENT_EXCHANGE,
        queue=PAYMENT_CONFIRM_QUEUE,
        routing_key=PAYMENT_ROUTING_KEY,
        callback=prepare_order
    )

    consumer.start()