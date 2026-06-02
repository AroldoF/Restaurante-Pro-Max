from ..repositories.notifications import NotificationRepository
from fastapi import HTTPException
from http import HTTPStatus
from ..schemas.notifications import NotificationCreate


class NotificationService:
    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    def list_all(self):
        return self.repository.get_all()

    def get_by_id(self, notification_id: int):
        notification = self.repository.get_by_id(notification_id)

        if not notification:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Notification not found!")

        return notification

    def create(self, data: NotificationCreate):
        return self.repository.create(data)