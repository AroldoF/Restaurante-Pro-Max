from sqlmodel import Session, select

from ..models.orders import Order, OrderItem
from ..schemas.orders import (
    OrderCreate,
    OrderItemCreate,
)
from decimal import Decimal

class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Order]:
        statement = select(Order)

        return self.session.exec(statement).all()

    def get_by_id(self, order_id: int) -> Order | None:
        return self.session.get(Order, order_id)

    def create(self, data: OrderCreate, amount: Decimal) -> Order:
        order = Order(
            total_amount=amount,
            order_items=[
                OrderItem(
                    quantity=item.quantity,
                    item_id=item.item_id,
                )
                for item in data.order_items
            ],
        )


        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)

        return order

    def update(self, order_id: int, data: OrderCreate) -> Order | None:
        order = self.get_by_id(order_id)

        if not order:
            return None

        order.total_amount = data.total_amount

        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)

        return order

    def delete(self, order_id: int) -> bool:
        order = self.get_by_id(order_id)

        if not order:
            return False

        self.session.delete(order)
        self.session.commit()

        return True


class OrderItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, order_item_id: int) -> OrderItem | None:
        return self.session.get(OrderItem, order_item_id)

    def get_by_order_id(self, order_id: int) -> list[OrderItem]:
        statement = select(OrderItem).where(OrderItem.order_id == order_id)

        return self.session.exec(statement).all()

    def create(self, data: OrderItemCreate, order_id: int) -> OrderItem:
        order_item = OrderItem(
            quantity=data.quantity,
            order_id=order_id,
            item_id=data.item_id,
        )

        self.session.add(order_item)
        self.session.commit()
        self.session.refresh(order_item)

        return order_item

    def update(
        self,
        order_item_id: int,
        data: OrderItemCreate,
    ) -> OrderItem | None:
        order_item = self.get_by_id(order_item_id)

        if not order_item:
            return None

        order_item.quantity = data.quantity
        order_item.order_id = data.order_id
        order_item.item_id = data.item_id

        self.session.add(order_item)
        self.session.commit()
        self.session.refresh(order_item)

        return order_item

    def delete(self, order_item_id: int) -> bool:
        order_item = self.get_by_id(order_item_id)

        if not order_item:
            return False

        self.session.delete(order_item)
        self.session.commit()

        return True
