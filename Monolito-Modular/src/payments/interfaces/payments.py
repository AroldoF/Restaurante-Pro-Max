from abc import ABC, abstractmethod
from ..models.payments import Payment
from ..schemas.payments import PaymentCreatePrivate, PaymentStatus
class PaymentRepositoryInterface(ABC):
    @abstractmethod
    def list_all(self) -> list[Payment]:
        pass

    @abstractmethod
    def get_by_id(self, payment_id: int) -> Payment|None:
        pass

    @abstractmethod
    def get_by_order_id(self, order_id: int) -> Payment | None:
        pass

    @abstractmethod
    def create(self, data: PaymentCreatePrivate) -> Payment:
        pass

    @abstractmethod
    def change_status(self, payment: Payment, status: PaymentStatus) -> Payment:
        pass
        