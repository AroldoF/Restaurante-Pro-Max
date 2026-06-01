from abc import ABC, abstractmethod
from ..models.notifications import Notification
from ..schemas.notifications import NotificationCreate

class NotificationRepositoryInteface(ABC):
    @abstractmethod
    def get_all(self) -> list[Notification]:
        pass

    @abstractmethod
    def get_by_id(self, notification_id: int) -> Notification|None:
        pass

    @abstractmethod
    def create(self, data: NotificationCreate) -> Notification:
        pass

class NotificationServiceInterface(ABC):
    @abstractmethod
    def list_all(self):
        pass

    @abstractmethod
    def get_by_id(self, notification_id: int):
        pass

    @abstractmethod
    def create(self, data: NotificationCreate):
        pass

    @abstractmethod
    def notify_order_paid(self, order_id: int):
        pass