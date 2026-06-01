from ..interfaces.payments import PaymentRepositoryInterface
from ...orders.interfaces.orders import OrderServiceInterface
from ...notifications.interfaces.notifications import NotificationServiceInterface
from ..schemas.payments import PaymentCreate, PaymentCreatePrivate, PaymentStatus
from fastapi import HTTPException
from http import HTTPStatus
from sqlmodel import Session

class PaymentService:
    def __init__(self, session: Session, repository: PaymentRepositoryInterface, order_service: OrderServiceInterface, notification_service: NotificationServiceInterface):
        self.session = session
        self.repository = repository
        self.order_service = order_service
        self.notification_service = notification_service

    def list_all(self):
        return self.repository.list_all()

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

        payment = self.repository.create(data_payment)
        self.session.commit()
        self.session.refresh(payment)

        return payment 

    def confirm(self, payment_id: int):
        payment = self.get_by_id(payment_id)

        if payment.status not in (PaymentStatus.PENDING, PaymentStatus.FAILED):
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="transaction invalid")

        try:
            payment =self.repository.change_status(payment, PaymentStatus.PAID)
            if not payment:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to confirm payment"
                )

            order = self.order_service.mark_as_finished(payment.order_id)
            if not order:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to finish order"
                )
                
            notification = self.notification_service.notify_order_paid(order.id)
            if not notification:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to create notification"
                )
        
            self.session.commit()
            self.session.refresh(payment)

            return payment
            
        except Exception:
            self.session.rollback()
            raise

        return payment
            