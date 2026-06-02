from app.config.core import settings
from infra.messaging.publisher import RabbitMQPublisher
from ..integrations.orders import OrdersIntegrations
from ..config.database import get_session
from sqlmodel import Session
from ..repositories.payments import PaymentRepository
from fastapi import Depends, Request
from ..services.payments import PaymentService
from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

def get_publisher(request: Request) -> RabbitMQPublisher:
    return request.app.state.rabbitmq_publisher

PublisherDep = Annotated[RabbitMQPublisher, Depends(get_publisher)]

def get_payment_service(session: SessionDep, event_publisher: PublisherDep) -> PaymentService:
    payment_repository = PaymentRepository(session)
    order_integration = OrdersIntegrations(base_url=settings.ORDER_API_URL)
    
    return PaymentService(
        session=session,
        repository=payment_repository, 
        order_integration=order_integration,
        event_publisher=event_publisher
    )

PaymentServiceDep = Annotated[PaymentService, Depends(get_payment_service)]