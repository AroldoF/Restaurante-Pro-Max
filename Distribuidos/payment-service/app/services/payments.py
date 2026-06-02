from ..repositories.payments import PaymentRepository
from ..schemas.payments import PaymentCreate, PaymentCreatePrivate, PaymentStatus
from fastapi import HTTPException
from http import HTTPStatus
from ..integrations.orders import OrdersIntegrations
from app.messaging.events.payment_confirm import PaymentConfirmEvent
from dataclasses import asdict
from infra.messaging.publisher import RabbitMQPublisher
from infra.messaging.constants import PAYMENT_ROUTING_KEY


class PaymentService:
    def __init__(self, repository: PaymentRepository, order_integration: OrdersIntegrations, event_publisher: RabbitMQPublisher):
        self.repository = repository
        self.order_integration = order_integration
        self.event_publisher = event_publisher


    def list(self):
        return self.repository.list()
    

    def get_by_id(self, payment_id: int):
        payment =  self.repository.get_by_id(payment_id)
        if not payment:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Payment not found"
            )

        return payment
    

    def create(self, data: PaymentCreate):
        payment = self.repository.get_by_order_id(data.order_id)

        if payment:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Payment already exists for this order",
            )
        
        
        total_amount = self.order_integration.get_order_price(data.order_id)

        data_payment = PaymentCreatePrivate(
            **data.model_dump(),
            total_amount=total_amount,
        )

        return self.repository.create(data_payment)
    

 
    def confirm(self, payment_id: int):
        payment = self.get_by_id(payment_id)

        if payment.status not in (PaymentStatus.PENDING, PaymentStatus.FAILED):
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="transaction invalid")

        payment =self.repository.change_status(payment, PaymentStatus.PAID)


        event = PaymentConfirmEvent(
            order_id=payment.order_id,
            payment_id=payment.id,
            status='PAID'
        )

        self.event_publisher.publish(
            routing_key=PAYMENT_ROUTING_KEY,
            message=asdict(event)
        )

        return payment

        