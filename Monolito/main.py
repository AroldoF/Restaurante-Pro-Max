from fastapi import FastAPI
from .src.routes.items import router as items_router
from .src.routes.orders import orders_router
from .src.routes.payments import router as payment_router
from .src.routes.notifications import router as notification_router
from .src.config.database import create_db_and_tables
app = FastAPI()
app.include_router(items_router)
app.include_router(orders_router)
app.include_router(payment_router)
app.include_router(notification_router)

create_db_and_tables()
