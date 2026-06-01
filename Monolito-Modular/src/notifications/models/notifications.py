from sqlmodel import SQLModel, Field
from datetime import datetime

class Notification(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    order_id: int = Field(foreign_key="order.id", index=True)

    message: str

    created_at: datetime = Field(default_factory=datetime.utcnow)