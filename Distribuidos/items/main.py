from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config.database import create_db_and_tables
from src.routes.item import router as items_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Items Service",
    description="Microservice responsible for menu items (cardapio)",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "items-service"}


app.include_router(items_router)