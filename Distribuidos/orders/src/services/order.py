from fastapi import HTTPException
from http import HTTPStatus
from decimal import Decimal
from ..repositories.order import OrderRepository
from ..models.order import Order
from ..schemas.order import (
    OrderCreate,
    OrderCreatePrivate,
    OrderUpdate,
    OrderStatus,
    ItemStockReduce,
)
from ..integrations.items_client import ItemsClient


class OrderService:
    def __init__(self, repository: OrderRepository, items_client: ItemsClient):
        self.repository = repository
        self.items_client = items_client

    def list(self) -> list[Order]:
        return self.repository.list()

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

    def calculate_amount(self, data: OrderCreate) -> Decimal:
        """
        Busca os preços dos itens no items-service via HTTP
        e calcula o total do pedido.
        """
        item_ids = [item.item_id for item in data.order_items]
        try:
            items = self.items_client.get_items_by_ids(item_ids)
        except ValueError as e:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=str(e),
            )

        items_map = {item.id: item for item in items}
        amount = Decimal("0")

        for order_item in data.order_items:
            item = items_map.get(order_item.item_id)
            if not item:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=f"Item {order_item.item_id} not found",
                )
            if not item.is_active:
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail=f"Item {order_item.item_id} is not available",
                )
            amount += item.price * order_item.quantity

        return amount

    def create(self, data: OrderCreate) -> Order:
        amount = self.calculate_amount(data)
        return self.repository.create(
            OrderCreatePrivate(
                **data.model_dump(),
                total_amount=amount,
            )
        )

    def update(self, order_id: int, data: OrderUpdate) -> Order:
        order = self.get_by_id(order_id)
        return self.repository.update(order, data)

    def delete(self, order_id: int) -> None:
        order = self.get_by_id(order_id)
        self.repository.delete(order)

    def mark_as_finished(self, order_id: int) -> Order:
        """
        Marca o pedido como finalizado e avisa o items-service
        para reduzir o estoque via HTTP.
        """
        order = self.update(
            order_id,
            OrderUpdate(status=OrderStatus.FINISHED),
        )
        reductions = [
            ItemStockReduce(
                item_id=order_item.item_id,
                quantity=order_item.quantity,
            )
            for order_item in order.order_items
        ]
        self.items_client.reduce_stock(reductions)
        return order