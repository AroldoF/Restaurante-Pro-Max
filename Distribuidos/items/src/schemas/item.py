from pydantic import BaseModel, Field
from decimal import Decimal


class ItemDetail(BaseModel):
  id: int 
  name: str
  stock: int
  price: Decimal = Field(default=Decimal('0.00'), decimal_places=2)
  is_active: bool

class ItemCreate(BaseModel):
  name: str  = Field(max_length=255, min_length=3)
  stock: int = Field(default=0, ge=0)
  price: Decimal = Field(default=Decimal('0.00'), max_digits=5, decimal_places=2, ge=0)


class ItemUpdate(BaseModel):
  name: str | None = Field(default=None,max_length=255, minim_length=3)
  stock: int | None = Field(default=None, ge=0)
  price: Decimal | None = Field(default=None, max_digits=5, decimal_places=2, ge=0)
  is_active: bool | None = Field(default=None)



# Contrato HTTP com o orders-service para reduzir estoque
class ItemStockReduce(BaseModel):
  item_id: int
  quantity: int = Field(ge=1)