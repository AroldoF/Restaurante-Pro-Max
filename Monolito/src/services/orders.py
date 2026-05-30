from ..models.orders import Order, OrderItem
from ..repositories.orders import (
    OrderRepository,
    OrderItemRepository,
)
from ..schemas.orders import (
    OrderCreate,
    OrderItemCreate,
)
from ..repositories.items import ItemRepository
from decimal import Decimal

class OrderService:
    def __init__(self, order_repository: OrderRepository, item_repository: ItemRepository):
        self.order_repository = order_repository
        self.item_repository = item_repository

    def calculate_amount(self, item_ids: list[int], data) -> Decimal:
        items = self.item_repository.get_by_ids(item_ids)

        items_map = {item.id: item for item in items}

        amount = 0

        for order_item in data.order_items:
            item = items_map.get(order_item.item_id)

            if item:
                amount += item.price * order_item.quantity

        return amount

    def list_orders(self) -> list[Order]:
        return self.order_repository.get_all()

    def get_by_id(self, order_id: int) -> Order | None:
        return self.order_repository.get_by_id(order_id)

    def create(self, data: OrderCreate) -> Order:
        item_ids = [item.item_id for item in data.order_items]

        amount = self.calculate_amount(item_ids, data)

        return self.order_repository.create(data, amount)

    def update(
        self,
        order_id: int,
        data: OrderCreate,
    ) -> Order | None:
        return self.order_repository.update(order_id, data)

    def delete(self, order_id: int) -> bool:
        return self.order_repository.delete(order_id)


class OrderItemService:
    def __init__(self, repository: OrderItemRepository):
        self.repository = repository

    def get_by_id(
        self,
        order_item_id: int,
    ) -> OrderItem | None:
        return self.repository.get_by_id(order_item_id)

    def get_by_order_id(
        self,
        order_id: int,
    ) -> list[OrderItem]:
        return self.repository.get_by_order_id(order_id)

    def create(
        self,
        data: OrderItemCreate,
        order_id
    ) -> OrderItem:
        return self.repository.create(data, order_id)

    def update(
        self,
        order_item_id: int,
        data: OrderItemCreate,
    ) -> OrderItem | None:
        return self.repository.update(
            order_item_id,
            data,
        )

    def delete(
        self,
        order_item_id: int,
    ) -> bool:
        return self.repository.delete(order_item_id)
