from app.routes.payments import router as payment
from app.config.core import settings
from fastapi import FastAPI
from app.config.database import create_db_and_tables
from infra.messaging.publisher import RabbitMQPublisher
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rabbitmq_publisher = RabbitMQPublisher()
    print("RabbitMQ Publisher conectado com sucesso.")
    
    yield 
    
    if hasattr(app.state, "rabbitmq_publisher"):
        app.state.rabbitmq_publisher.close()
        print("Conexão com RabbitMQ encerrada.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
)


app.include_router(payment)


create_db_and_tables()