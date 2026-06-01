from fastapi import APIRouter, Depends
from http import HTTPStatus
from sqlmodel import Session
from ..config.database import get_session
from ..schemas.item import ItemCreate,ItemDetail, ItemUpdate, ItemStockReduce
from ..services.item import ItemService
from ..repositories.item import ItemRepository

router = APIRouter(prefix="/items", tags=["items"])


def get_item_service(session: Session = Depends(get_session)) -> ItemService:
  return ItemService(ItemRepository(session))


@router.get("/", response_model=list[ItemDetail])
def list_items(service: ItemService = Depends(get_item_service)):
  return service.list()

@router.post("/", response_model=ItemDetail, status_code=HTTPStatus.CREATED)
def create_item(payload: ItemCreate, service: ItemService = Depends(get_item_service)):
  return service.create(payload)

# Endpoint interno — chamado pelo orders-service ao confirmar pagamento
@router.patch("/stock/reduce/", response_model=list[ItemDetail])
def reduce_stock(
    reductions: list[ItemStockReduce],
    service: ItemService = Depends(get_item_service),
):
    return service.reduce_stock_bulk(reductions)

@router.get("/{item_id}/", response_model=ItemDetail)
def get_item(item_id: int, service: ItemService = Depends(get_item_service)):
  return service.get_by_id(item_id)

@router.put("/{item_id}/", response_model=ItemDetail)
def update_item(
  item_id: int, 
  payload: ItemCreate, 
  service: ItemService = Depends(get_item_service),
):
  return service.update(item_id, payload)


@router.patch("/{item_id}/", response_model=ItemDetail)
def partial_update_item(
    item_id: int,
    payload: ItemUpdate,
    service: ItemService = Depends(get_item_service),
):
    return service.update(item_id, payload)


@router.delete("/{item_id}/", status_code=HTTPStatus.NO_CONTENT)
def delete_item(item_id: int, service: ItemService = Depends(get_item_service)):
    service.delete(item_id)


