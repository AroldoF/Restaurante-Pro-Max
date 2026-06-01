from fastapi import APIRouter, Depends
from http import HTTPStatus
from ..schemas.items import ItemCreate, ItemDetail, ItemUpdate
from ..dependencies.items import ItemServiceDep

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/", response_model=list[ItemDetail])
def list_items(service: ItemServiceDep):
    return service.list_all()


@router.post("/", response_model=ItemDetail, status_code=HTTPStatus.CREATED)
def create_item(payload: ItemCreate, service: ItemServiceDep):
    return service.create(payload)


@router.get("/{item_id}/", response_model=ItemDetail)
def get_item(item_id: int, service: ItemServiceDep):
    return service.get_by_id(item_id)


@router.put("/{item_id}/", response_model=ItemDetail)
def update_item(
    item_id: int, payload: ItemCreate, service: ItemServiceDep
):
    return service.update(item_id, payload)


@router.patch("/{item_id}/", response_model=ItemDetail)
def parcial_update_item(
    item_id: int, payload: ItemUpdate, service: ItemServiceDep
):
    return service.update(item_id, payload)


@router.delete("/{item_id}/", status_code=HTTPStatus.NO_CONTENT)
def delete_item(item_id: int, service: ItemServiceDep):
    service.delete(item_id)
    return
