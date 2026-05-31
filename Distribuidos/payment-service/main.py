from app.routes.payments import router as payment
from app.config.core import settings
from fastapi import FastAPI
from app.config.database import create_db_and_tables

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
)


app.include_router(payment)


create_db_and_tables()