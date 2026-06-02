from app.routes.notifications import router as notification
from app.config.core import settings
from fastapi import FastAPI
from app.config.database import create_db_and_tables
import threading
from infra.messaging.worker import start_consumers
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    worker_thread = threading.Thread(target=start_consumers, daemon=True)
    worker_thread.start()
    print("Worker do RabbitMQ iniciado em background")
    
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan
)


app.include_router(notification)


create_db_and_tables()