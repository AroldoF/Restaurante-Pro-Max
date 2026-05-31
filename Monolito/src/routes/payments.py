from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..repositories.payments import PaymentRepository
from ..repositories.orders import OrderRepository
from ..repositories.items import ItemRepository
from ..services.items import ItemService
from ..services.orders import OrderService
from ..services.payments import PaymentService
from ..config.database import get_session
from ..schemas.payments import PaymentDetail, PaymentCreate
from http import HTTPStatus
from ..repositories.notifications import NotificationRepository
from ..services.notifications import NotificationService

router = APIRouter(prefix='/payments', tags=['Payments'])

def get_payment_service(
    session: Session = Depends(get_session),
) -> PaymentService:
    item_repository = ItemRepository(session)
    item_service = ItemService(item_repository)
    order_repository = OrderRepository(session)
    order_service = OrderService(order_repository, item_service)
    notification_repository = NotificationRepository(session)
    notification_service = NotificationService(notification_repository)
    payment_repository = PaymentRepository(session)
    return PaymentService(payment_repository, order_service, notification_service)

@router.get("/", response_model=list[PaymentDetail])
def list_payments(service: PaymentService = Depends(get_payment_service)):
    return service.list()

@router.post("/", response_model=PaymentDetail, status_code=HTTPStatus.CREATED)
def create_payment(data: PaymentCreate, service: PaymentService = Depends(get_payment_service)):
    return service.create(data)

@router.get("/{payment_id}/", response_model=PaymentDetail)
def get_payment(payment_id: int, service: PaymentService = Depends(get_payment_service)):
    payment = service.get_by_id(payment_id)
    return payment

@router.post("/{payment_id}/confirm", response_model=PaymentDetail)
def confirm_payment(payment_id: int, service: PaymentService = Depends(get_payment_service)):
    payment = service.confirm(payment_id)
    return payment

