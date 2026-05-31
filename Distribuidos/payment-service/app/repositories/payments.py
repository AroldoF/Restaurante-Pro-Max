from sqlmodel import Session, select
from ..models.payments import Payment
from ..schemas.payments import PaymentCreatePrivate, PaymentStatus


class PaymentRepository:
    def __init__(self, session: Session):
        self.session = session

    def list(self) -> list[Payment]:
        statement = select(Payment)
        return self.session.exec(statement).all()

    def get_by_id(self, payment_id: int) -> Payment|None:
        return self.session.get(Payment, payment_id)

    def get_by_order_id(self, order_id: int) -> Payment | None:
        statement = select(Payment).where(
            Payment.order_id == order_id
        )

        return self.session.exec(statement).first()

    def create(self, data: PaymentCreatePrivate) -> Payment:
        pay = Payment(**data.model_dump())

        self.session.add(pay)
        self.session.commit()
        self.session.refresh(pay)

        return pay

    def change_status(self, payment: Payment, status: PaymentStatus) -> Payment:
        payment.status = status

        self.session.commit()
        self.session.refresh(payment)

        return payment
        