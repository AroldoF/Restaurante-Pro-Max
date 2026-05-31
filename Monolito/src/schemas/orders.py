from decimal import Decimal
from pydantic import BaseModel, Field
from enum import Enum
# class OrderStatus(str, Enum):
    
class OrderStatus(str, Enum):
    PENDING = "pending"
    FINISHED = "finished"
    CANCELLED = "cancelled"

class OrderItemDetail(BaseModel):
    id: int
    quantity: int = Field(default=1)
    item_id: int


class OrderItemCreate(BaseModel):
    quantity: int = Field(default=1, ge=1)
    item_id: int


class OrderDetail(BaseModel):
    id: int
    status: OrderStatus
    total_amount: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=5,
        decimal_places=3,
        ge=0,
    )

    order_items: list[OrderItemDetail]


class OrderUpdate(BaseModel):
    status: OrderStatus|None = Field(default=None)

class OrderCreate(BaseModel):
    order_items: list[OrderItemCreate]

class OrderCreatePrivate(OrderCreate):
    total_amount: Decimal
