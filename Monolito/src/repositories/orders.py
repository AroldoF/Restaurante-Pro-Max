from sqlmodel import Session, select

from ..models.orders import Order, OrderItem, OrderStatus
from ..schemas.orders import (
    OrderCreate,
    OrderCreatePrivate,
    OrderItemCreate,
)

from decimal import Decimal

class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def list(self) -> list[Order]:
        statement = select(Order)

        return self.session.exec(statement).all()

    def get_by_id(self, order_id: int) -> Order | None:
        return self.session.get(Order, order_id)

    def list_order_items(self, order: Order)-> list[OrderItem]:
        return order.order_items

    def create(self, data: OrderCreatePrivate) -> Order:
        order = Order(
            total_amount=data.total_amount,
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

    def update(self, order: Order, data: OrderUpdate) -> Order:
        order_data = data.model_dump(exclude_none=True)

        for key, value in order_data.items():
            setattr(order, key, value)

        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)

        return order

    def delete(self, order: Order) -> None:
        self.session.delete(order)
        self.session.commit()

    def change_status(
        self,
        order: Order,
        status: OrderStatus,
    ) -> Order:
        order.status = status

        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)

        return order