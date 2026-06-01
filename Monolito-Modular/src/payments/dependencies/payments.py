from fastapi import Depends
from sqlmodel import Session
from ....database import get_session
from ...orders.dependencies.orders import get_order_service
from ...notifications.dependencies.notifications import get_notification_service
from typing import Annotated
from ..repositories.payments import PaymentRepository
from ..services.payments import PaymentService

def get_payment_service(
    session: Session = Depends(get_session),
) -> PaymentService:
    order_service = get_order_service(session)
    notification_service = get_notification_service(session)
    payment_repository = PaymentRepository(session)
    return PaymentService(session, payment_repository, order_service, notification_service)

PaymentServiceDep = Annotated[
    PaymentService,
    Depends(get_payment_service)
]