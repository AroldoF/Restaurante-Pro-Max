from ..interfaces.notifications import NotificationRepositoryInteface
from fastapi import HTTPException
from http import HTTPStatus
from ..schemas.notifications import NotificationCreate
from sqlmodel import Session

class NotificationService:
    def __init__(self, session: Session, repository: NotificationRepositoryInteface):
        self.session = session
        self.repository = repository

    def list_all(self):
        return self.repository.get_all()

    def get_by_id(self, notification_id: int):
        notification = self.repository.get_by_id(notification_id)

        if not notification:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Notification not found!")

        return notification

    def create(self, data: NotificationCreate):
        notification = self.repository.create(data)
        
        self.session.commit()
        self.session.refresh(notification)

        return notification 

    def notify_order_paid(self, order_id: int):
        notification = NotificationCreate(
            order_id=order_id,
            message=f"Pedido {order_id} foi pago! Pode preparar!"
        )

        return self.repository.create(notification)