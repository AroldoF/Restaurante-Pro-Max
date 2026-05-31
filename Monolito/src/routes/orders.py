from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..config.database import get_session
from ..repositories.orders import (
    OrderRepository,
)
from ..schemas.orders import (
    OrderCreate,
    OrderDetail,
    OrderUpdate,
    OrderItemDetail,
)
from ..services.orders import (
    OrderService,
)
from ..repositories.items import ItemRepository
from ..services.items import ItemService

orders_router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


def get_order_service(
    session: Session = Depends(get_session),
) -> OrderService:
    order_repository = OrderRepository(session)
    item_repository = ItemRepository(session)

    item_service = ItemService(item_repository)

    return OrderService(
        order_repository,
        item_service,
    )
    
@orders_router.get(
    "/",
    response_model=list[OrderDetail],
)
def get_orders(
    service: OrderService = Depends(get_order_service),
):
    return service.list()


@orders_router.get(
    "/{order_id}",
    response_model=OrderDetail,
)
def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
):
    return service.get_by_id(order_id)


@orders_router.post(
    "/",
    response_model=OrderDetail,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    data: OrderCreate,
    service: OrderService = Depends(get_order_service),
):
    return service.create(data)


@orders_router.get(
    "/{order_id}/items",
    response_model=list[OrderItemDetail],
)
def get_order_items(
    order_id: int,
    service: OrderService = Depends(get_order_service),
):
    return service.list_order_items_by_id(order_id)