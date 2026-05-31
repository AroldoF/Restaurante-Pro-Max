from ..repositories.payments import PaymentRepository
from ..services.orders import OrderService
from ..services.notifications import NotificationService
from ..schemas.payments import PaymentCreate, PaymentCreatePrivate, PaymentStatus
from fastapi import HTTPException
from http import HTTPStatus
from ..schemas.notifications import NotificationCreate
class PaymentService:
    def __init__(self, repository: PaymentRepository, order_service: OrderService, notification_service: NotificationService):
        self.repository = repository
        self.order_service = order_service
        self.notification_service = notification_service

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
        order = self.order_service.get_by_id(data.order_id)

        payment = self.repository.get_by_order_id(data.order_id)

        if payment:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Payment already exists for this order",
            )

        data_payment = PaymentCreatePrivate(
            **data.model_dump(),
            total_amount=order.total_amount,
        )

        return self.repository.create(data_payment)

    def confirm(self, payment_id: int):
        payment = self.get_by_id(payment_id)
        if payment.status not in (PaymentStatus.PENDING, PaymentStatus.FAILED):
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="transaction invalid")

        payment =self.repository.change_status(payment, PaymentStatus.PAID)
        order = self.order_service.mark_as_finished(payment.order_id)
        self.notification_service.create(
           NotificationCreate(
            order_id=order.id,
            message=f"Pedido {order.id} foi pago! Pode preparar!")
        )
        return payment

        