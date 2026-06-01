from fastapi import APIRouter, Depends
from http import HTTPStatus
from sqlmodel import Session
from ..config.database import get_session
from ..schemas.order import OrderCreate, OrderDetail, OrderUpdate, OrderItemDetail
from ..services.order import OrderService
from ..repositories.order import OrderRepository
from ..integrations.items_client import ItemsClient

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_order_service(session: Session = Depends(get_session)) -> OrderService:
    return OrderService(
        repository=OrderRepository(session),
        items_client=ItemsClient(),
    )


@router.get("/", response_model=list[OrderDetail])
def list_orders(service: OrderService = Depends(get_order_service)):
    return service.list()


@router.get("/{order_id}/", response_model=OrderDetail)
def get_order(order_id: int, service: OrderService = Depends(get_order_service)):
    return service.get_by_id(order_id)


@router.post("/", response_model=OrderDetail, status_code=HTTPStatus.CREATED)
def create_order(data: OrderCreate, service: OrderService = Depends(get_order_service)):
    return service.create(data)


@router.get("/{order_id}/items/", response_model=list[OrderItemDetail])
def get_order_items(order_id: int, service: OrderService = Depends(get_order_service)):
    return service.list_order_items_by_id(order_id)


@router.delete("/{order_id}/", status_code=HTTPStatus.NO_CONTENT)
def delete_order(order_id: int, service: OrderService = Depends(get_order_service)):
    service.delete(order_id)


# chamado pelo payments ao confirmar pagamento
@router.patch("/{order_id}/finish/", response_model=OrderDetail)
def finish_order(order_id: int, service: OrderService = Depends(get_order_service)):
    return service.mark_as_finished(order_id)