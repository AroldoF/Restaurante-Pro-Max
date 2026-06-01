from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    total_amount: Decimal = Field(default=Decimal("0.000"), max_digits=8, decimal_places=3, ge=0)
    order_items: list["OrderItem"] = Relationship(
        back_populates="order",
        cascade_delete=True,
    )


class OrderItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    quantity: int = Field(default=1, ge=1)
    order_id: int = Field(foreign_key="order.id", ondelete="CASCADE")
    item_id: int = Field(foreign_key=None)
    order: "Order" = Relationship(back_populates="order_items")