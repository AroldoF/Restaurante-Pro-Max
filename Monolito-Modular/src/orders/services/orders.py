from ..models.orders import Order, OrderItem
from ..interfaces.orders import (
    OrderRepositoryInterface,
)
from ..schemas.orders import (
    OrderCreate,
    OrderCreatePrivate,
    OrderUpdate, 
    OrderStatus
)
from ...items.interfaces.items import ItemRepositoryInterface
from decimal import Decimal
from fastapi import HTTPException
from http import HTTPStatus

class OrderService:
    def __init__(self, repository: OrderRepositoryInterface, item_service: ItemRepositoryInterface):
        self.repository = repository
        self.item_service = item_service

    def calculate_amount(
        self,
        item_ids: list[int],
        data: OrderCreate,
    ) -> Decimal:
        items = self.item_service.list_by_ids(item_ids)

        items_map = {item.id: item for item in items}

        amount = Decimal("0")

        for order_item in data.order_items:
            item = items_map.get(order_item.item_id)

            if not item:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=f"Item {order_item.item_id} not found",
                )

            amount += item.price * order_item.quantity

        return amount

    def list_all(self) -> list[Order]:
        return self.repository.list_all()

    def get_by_id(self, order_id: int) -> Order:
        order = self.repository.get_by_id(order_id)

        if not order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Order not found",
            )

        return order

    def list_order_items_by_id(self, order_id: int):
        order = self.get_by_id(order_id)
        return self.repository.list_order_items(order)

    def create(self, data: OrderCreate) -> Order:
        item_ids = [item.item_id for item in data.order_items]

        amount = self.calculate_amount(item_ids, data)

        return self.repository.create(
            OrderCreatePrivate(
                **data.model_dump(),
                total_amount=amount,
            )
        )

    def update(
        self,
        order_id: int,
        data: OrderUpdate,
    ) -> Order | None:
        order = self.get_by_id(order_id)
        return self.repository.update(order, data)

    def delete(self, order_id: int) -> bool:
        order = self.get_by_id(order_id)
        return self.repository.delete(order)

    def mark_as_finished(self, order_id: int):
        order = self.update(
            order_id,
            OrderUpdate(status=OrderStatus.FINISHED),
        )

        items_quantity = {
            order_item.item_id: order_item.quantity
            for order_item in order.order_items
        }

        self.item_service.reduce_stock_bulk(
            items_quantity
        )

        return order