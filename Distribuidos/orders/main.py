from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config.database import create_db_and_tables
from src.routes.order import router as orders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Orders Service",
    description="Microservice responsible for orders",
    version="0.1.0",
    lifespan=lifespan,
)


# @app.get("/health", tags=["Health"])
# def health_check():
#     return {"status": "ok", "service": "orders-service"}


app.include_router(orders_router)