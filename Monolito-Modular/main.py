from fastapi import FastAPI
from .src.items.routes.items import router as items_router
from .src.orders.routes.orders import router as orders_router
from .src.notifications.routes.notifications import router as notifications_router
from .src.payments.routes.payments import router as payments_router
from .database import create_db_and_tables

app = FastAPI()
app.include_router(items_router)
app.include_router(orders_router)
app.include_router(notifications_router)
app.include_router(payments_router)

create_db_and_tables()

if __name__ == "__main__":
    main()
