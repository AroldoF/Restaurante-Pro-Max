from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.orders import (
    OrderCreate,
    OrderDetail,
    OrderUpdate,
    OrderItemDetail,
)
from ..dependencies.orders import OrderServiceDep


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)



    
@router.get(
    "/",
    response_model=list[OrderDetail],
)
def get_orders(
    service: OrderServiceDep,
):
    return service.list_all()


@router.get(
    "/{order_id}",
    response_model=OrderDetail,
)
def get_order(
    order_id: int,
    service: OrderServiceDep,
):
    return service.get_by_id(order_id)


@router.post(
    "/",
    response_model=OrderDetail,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    data: OrderCreate,
    service: OrderServiceDep,
):
    return service.create(data)


@router.get(
    "/{order_id}/items",
    response_model=list[OrderItemDetail],
)
def get_order_items(
    order_id: int,
    service: OrderServiceDep,
):
    return service.list_order_items_by_id(order_id)