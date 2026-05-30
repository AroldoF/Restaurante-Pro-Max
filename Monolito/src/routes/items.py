from fastapi import APIRouter, Depends
from http import HTTPStatus
from sqlmodel import Session

from ..config.database import get_session
from ..schemas.items import ItemCreate, ItemDetail, ItemUpdate
from ..services.items import ItemService

items_router = APIRouter(prefix="/items", tags=["Items"])


# Dependência para instanciar o serviço com a sessão atual do request
def get_item_service(session: Session = Depends(get_session)) -> ItemService:
    return ItemService(session)


@items_router.get("/", response_model=list[ItemDetail])
def list_items(service: ItemService = Depends(get_item_service)):
    return service.list_items()


@items_router.post("/", response_model=ItemDetail, status_code=HTTPStatus.CREATED)
def create_item(payload: ItemCreate, service: ItemService = Depends(get_item_service)):
    return service.create_item(payload)


@items_router.get("/{item_id}/", response_model=ItemDetail)
def get_item(item_id: int, service: ItemService = Depends(get_item_service)):
    return service.get_item_by_id(item_id)


@items_router.put("/{item_id}/", response_model=ItemDetail)
def update_item(
    item_id: int, payload: ItemCreate, service: ItemService = Depends(get_item_service)
):
    return service.update_item(item_id, payload)


@items_router.patch("/{item_id}/", response_model=ItemDetail)
def parcial_update_item(
    item_id: int, payload: ItemUpdate, service: ItemService = Depends(get_item_service)
):
    return service.partial_update_item(item_id, payload)


@items_router.delete("/{item_id}/", status_code=HTTPStatus.NO_CONTENT)
def delete_item(item_id: int, service: ItemService = Depends(get_item_service)):
    service.delete_item(item_id)
    return
