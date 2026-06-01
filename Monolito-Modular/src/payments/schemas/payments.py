from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    PIX = "pix"

class PaymentDetail(BaseModel):
    id: int 
    order_id: int 

    total_amount: Decimal = Field(default="0.000", decimal_places=2, ge=0)
    method: PaymentMethod
    status: PaymentStatus 

    created_at: datetime 

class PaymentCreate(BaseModel):
    order_id: int 
    method: PaymentMethod
    
class PaymentCreatePrivate(PaymentCreate):
    total_amount: Decimal


