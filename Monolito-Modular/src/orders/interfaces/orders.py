from abc import ABC, abstractmethod
from ..models.orders import Order, OrderItem 
from ..schemas.orders import OrderCreate, OrderCreatePrivate, OrderUpdate, OrderStatus
from decimal import Decimal

class OrderRepositoryInterface(ABC):
    @abstractmethod
    def list_all(self) -> list[Order]:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Order | None:
        pass

    @abstractmethod
    def list_order_items(self, order: Order)-> list[OrderItem]:
        pass

    @abstractmethod
    def create(self, data: OrderCreatePrivate) -> Order:
        pass

    @abstractmethod
    def update(self, order: Order, data: OrderUpdate) -> Order:
        pass

    @abstractmethod
    def delete(self, order: Order) -> None:
        pass

    @abstractmethod
    def change_status(
        self,
        order: Order,
        status: OrderStatus,
    ) -> Order:
        pass

class OrderServiceInterface(ABC):
    @abstractmethod
    def calculate_amount(
        self,
        item_ids: list[int],
        data: OrderCreate,
    ) -> Decimal:
        pass

    @abstractmethod
    def list_all(self) -> list[Order]:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Order:
        pass

    @abstractmethod
    def list_order_items_by_id(self, order_id: int):
        pass

    @abstractmethod
    def create(self, data: OrderCreate) -> Order:
        pass

    @abstractmethod
    def update(
        self,
        order_id: int,
        data: OrderUpdate,
    ) -> Order | None:
        pass

    @abstractmethod
    def delete(self, order_id: int) -> bool:
        pass

    @abstractmethod
    def mark_as_finished(self, order_id: int):
        pass