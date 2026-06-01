from fastapi import Depends
from ...items.dependencies.items import get_item_service
from ....database import get_session
from typing import Annotated
from ..repositories.orders import OrderRepository
from ..services.orders import OrderService
from sqlmodel import Session

def get_order_service(
    session: Session = Depends(get_session),
) -> OrderService:
    order_repository = OrderRepository(session)
    item_service = get_item_service(session)

    return OrderService(
        order_repository,
        item_service,
    )

OrderServiceDep = Annotated[
    OrderService,
    Depends(get_order_service),
]