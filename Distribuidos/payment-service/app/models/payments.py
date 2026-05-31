from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from decimal import Decimal
from datetime import datetime
from ..schemas.payments import PaymentMethod, PaymentStatus

class Payment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    order_id: int = Field(unique=True)

    total_amount: Decimal = Field(decimal_places=3, ge=0)
    method: PaymentMethod
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)

    created_at: datetime = Field(default_factory=datetime.utcnow)
