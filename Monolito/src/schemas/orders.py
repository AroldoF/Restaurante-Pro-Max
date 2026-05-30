from decimal import Decimal
from pydantic import BaseModel, Field


class OrderItemDetail(BaseModel):
    id: int
    quantity: int = Field(default=1)
    item_id: int


class OrderItemCreate(BaseModel):
    quantity: int = Field(default=1, ge=1)
    item_id: int


class OrderDetail(BaseModel):
    id: int
    total_amount: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=5,
        decimal_places=3,
        ge=0,
    )

    order_items: list[OrderItemDetail]


class OrderCreate(BaseModel):
    order_items: list[OrderItemCreate]
