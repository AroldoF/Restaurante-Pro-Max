from sqlmodel import Session, select
from ..schemas.notifications import NotificationCreate
from ..models.notifications import Notification

class NotificationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Notification]:
        statement = select(Notification)
        return self.session.exec(statement).all()

    def get_by_id(self, notification_id: int) -> Notification|None:
        return self.session.get(Notification, notification_id)

    def create(self, data: NotificationCreate) -> Notification:
        notification = Notification(**data.model_dump())

        self.session.add(notification)

        return notification