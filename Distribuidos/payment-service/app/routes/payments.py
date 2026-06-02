from fastapi import APIRouter, Depends
from ..schemas.payments import PaymentDetail, PaymentCreate
from http import HTTPStatus
from app.dependencies.payments import PaymentServiceDep

router = APIRouter(prefix='/payments', tags=['Payments'])

@router.get("/", response_model=list[PaymentDetail])
def list_payments(service: PaymentServiceDep):
    return service.list()

@router.post("/", response_model=PaymentDetail, status_code=HTTPStatus.CREATED)
def create_payment(data: PaymentCreate, service: PaymentServiceDep):
    return service.create(data)

@router.get("/{payment_id}/", response_model=PaymentDetail)
def get_payment(payment_id: int, service: PaymentServiceDep):
    payment = service.get_by_id(payment_id)
    return payment

@router.post("/{payment_id}/confirm", response_model=PaymentDetail)
def confirm_payment(payment_id: int, service: PaymentServiceDep):
    payment = service.confirm(payment_id)
    return payment

