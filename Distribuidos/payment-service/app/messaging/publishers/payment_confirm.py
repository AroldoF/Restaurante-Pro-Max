from messaging.events.payment_confirm import PaymentConfirmEvent
from infra.messaging.publisher import rabbitmq_publisher
from infra.messaging.constants import PAYMENT_QUEUE, PAYMENT_ROUTING_KEY
from dataclasses import asdict


def publisher_payment_confirm(event: PaymentConfirmEvent):
    rabbitmq_publisher.publish(
        queue=PAYMENT_QUEUE,
        routing_key=PAYMENT_ROUTING_KEY,
        message=asdict(event) 
    )
