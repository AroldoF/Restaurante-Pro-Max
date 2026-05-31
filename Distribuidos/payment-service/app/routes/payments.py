from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..repositories.payments import PaymentRepository
from ..services.payments import PaymentService
from ..integrations.orders import OrdersIntegrations
from ..config.database import get_session
from ..schemas.payments import PaymentDetail, PaymentCreate
from http import HTTPStatus
from app.config.core import settings


router = APIRouter(prefix='/payments', tags=['Payments'])


# Ajustar rotas
def get_payment_service(
    session: Session = Depends(get_session),
) -> PaymentService:
    payment_repository = PaymentRepository(session)
    order_integration = OrdersIntegrations(base_url=settings.ORDER_API_URL)
    return PaymentService(payment_repository, order_integration)

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

# @router.post("/{payment_id}/confirm", response_model=PaymentDetail)
# def confirm_payment(payment_id: int, service: PaymentService = Depends(get_payment_service)):
#     payment = service.confirm(payment_id)
#     return payment

