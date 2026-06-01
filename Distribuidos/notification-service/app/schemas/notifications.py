from pydantic import BaseModel, Field
from datetime import datetime


class NotificationDetail(BaseModel):
    id: int 
    order_id: int 
    message: str
    created_at: datetime 

class NotificationCreate(BaseModel):
    order_id: int 
    message: str