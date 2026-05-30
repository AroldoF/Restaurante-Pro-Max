from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal


class ItemBase(SQLModel):
    name: str = Field(max_length=255, min_length=3)
    stock: int = Field(default=0, ge=0)
    price: Decimal = Field(default=0, max_digits=5, decimal_places=2, ge=0)


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    order_items: list["OrderItem"] = Relationship(back_populates="item")
