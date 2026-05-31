from sqlmodel import SQLModel, Field
from decimal import Decimal


class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, min_length=3)
    stock: int = Field(default=0, ge=0)
    price: Decimal = Field(default=Decimal("0.00"), max_digits=5, decimal_places=2, ge=0)
    is_active: bool = Field(default=True)