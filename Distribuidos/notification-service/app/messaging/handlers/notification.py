from app.services.notifications import NotificationService
from app.schemas.notifications import NotificationCreate
from app.repositories.notifications import NotificationRepository
from app.config.database import engine 
from sqlmodel import Session

def prepare_order(data: dict):
    order_id = data.get("order_id")

    schema = NotificationCreate(
        order_id=order_id,
        message=f"Order {order_id} has been paid and can now be prepared. "
    )

    with Session(engine) as session:
        repository = NotificationRepository(session)
        service = NotificationService(repository)
        
        service.create(schema)