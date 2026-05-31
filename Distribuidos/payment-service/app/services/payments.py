from ..repositories.payments import PaymentRepository
from ..schemas.payments import PaymentCreate, PaymentCreatePrivate, PaymentStatus
from fastapi import HTTPException
from http import HTTPStatus
from ..integrations.orders import OrdersIntegrations



class PaymentService:
    def __init__(self, repository: PaymentRepository, order_integration: OrdersIntegrations):
        self.repository = repository
        self.order_integration = order_integration


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


        ## ajustar pois a criação da notificação é via mensageria 

        order = self.order_service.mark_as_finished(payment.order_id)
        
        # self.notification_service.create(
        #    NotificationCreate(
        #     order_id=order.id,
        #     message=f"Pedido {order.id} foi pago! Pode preparar!")
        # )
        
        return payment

        