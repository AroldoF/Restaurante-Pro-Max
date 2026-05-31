from fastapi import APIRouter, Depends
from http import HTTPStatus
from sqlmodel import Session

from ..config.database import get_session
from ..schemas.items import ItemCreate, ItemDetail, ItemUpdate
from ..services.items import ItemService
from ..repositories.items import ItemRepository
router = APIRouter(prefix="/items", tags=["Items"])


def get_item_service(session: Session = Depends(get_session)) -> ItemService:
    item_repository = ItemRepository(session)
    return ItemService(item_repository)


@router.get("/", response_model=list[ItemDetail])
def list_items(service: ItemService = Depends(get_item_service)):
    return service.list()


@router.post("/", response_model=ItemDetail, status_code=HTTPStatus.CREATED)
def create_item(payload: ItemCreate, service: ItemService = Depends(get_item_service)):
    return service.create(payload)


@router.get("/{item_id}/", response_model=ItemDetail)
def get_item(item_id: int, service: ItemService = Depends(get_item_service)):
    return service.get_by_id(item_id)


@router.put("/{item_id}/", response_model=ItemDetail)
def update_item(
    item_id: int, payload: ItemCreate, service: ItemService = Depends(get_item_service)
):
    return service.update(item_id, payload)


@router.patch("/{item_id}/", response_model=ItemDetail)
def parcial_update_item(
    item_id: int, payload: ItemUpdate, service: ItemService = Depends(get_item_service)
):
    return service.update(item_id, payload)


@router.delete("/{item_id}/", status_code=HTTPStatus.NO_CONTENT)
def delete_item(item_id: int, service: ItemService = Depends(get_item_service)):
    service.delete(item_id)
    return
