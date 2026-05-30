from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..config.database import get_session
from ..repositories.orders import (
    OrderRepository,
    OrderItemRepository,
)
from ..schemas.orders import (
    OrderCreate,
    OrderDetail,
    OrderItemCreate,
    OrderItemDetail,
)
from ..services.orders import (
    OrderService,
    OrderItemService,
)
from ..repositories.items import ItemRepository

orders_router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


def get_order_service(
    session: Session = Depends(get_session),
) -> OrderService:
    order_repository = OrderRepository(session)
    item_repository = ItemRepository(session)
    return OrderService(order_repository, item_repository)


def get_order_item_service(
    session: Session = Depends(get_session),
) -> OrderItemService:
    repository = OrderItemRepository(session)

    return OrderItemService(repository)


@orders_router.get(
    "/",
    response_model=list[OrderDetail],
)
def get_orders(
    service: OrderService = Depends(get_order_service),
):
    return service.list_orders()


@orders_router.get(
    "/{order_id}",
    response_model=OrderDetail,
)
def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
):
    order = service.get_by_id(order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return order


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


@orders_router.put(
    "/{order_id}",
    response_model=OrderDetail,
)
def update_order(
    order_id: int,
    data: OrderCreate,
    service: OrderService = Depends(get_order_service),
):
    order = service.update(order_id, data)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return order


@orders_router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
):
    deleted = service.delete(order_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return None


@orders_router.get(
    "/{order_id}/items",
    response_model=list[OrderItemDetail],
)
def get_order_items(
    order_id: int,
    service: OrderItemService = Depends(get_order_item_service),
):
    return service.get_by_order_id(order_id)


@orders_router.post(
    "/{order_id}/items",
    response_model=OrderItemDetail,
    status_code=status.HTTP_201_CREATED,
)
def create_order_item(
    order_id: int,
    data: OrderItemCreate,
    service: OrderItemService = Depends(get_order_item_service),
):
    return service.create(data, order_id)


@orders_router.put(
    "/{order_id}/items/{order_item_id}",
    response_model=OrderItemDetail,
)
def update_order_item(
    order_id: int,
    order_item_id: int,
    data: OrderItemCreate,
    service: OrderItemService = Depends(get_order_item_service),
):
    order_item = service.update(
        order_item_id,
        data,
    )

    if not order_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found",
        )

    return order_item


@orders_router.delete(
    "/{order_id}/items/{order_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_order_item(
    order_id: int,
    order_item_id: int,
    service: OrderItemService = Depends(get_order_item_service),
):
    deleted = service.delete(order_item_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found",
        )

    return None
