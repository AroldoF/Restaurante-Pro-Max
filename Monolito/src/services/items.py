from fastapi import HTTPException
from http import HTTPStatus
from sqlmodel import Session
from ..repositories.items import ItemRepository
from ..schemas.items import ItemCreate, ItemUpdate
from ..models.items import Item


class ItemService:
    def __init__(self, session: Session):
        self.repository = ItemRepository(session)

    def list_items(self) -> list[Item]:
        return self.repository.get_all()

    def get_item_by_id(self, item_id: int) -> Item:
        item = self.repository.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Item not found"
            )
        return item

    def create_item(self, payload: ItemCreate) -> Item:
        return self.repository.create(payload)

    def update_item(self, item_id: int, payload: ItemCreate) -> Item:
        item = self.get_item_by_id(item_id)  # Já valida se existe ou joga 404
        return self.repository.update(item, payload, partial=False)

    def partial_update_item(self, item_id: int, payload: ItemUpdate) -> Item:
        item = self.get_item_by_id(item_id)
        return self.repository.update(item, payload, partial=True)

    def delete_item(self, item_id: int) -> None:
        item = self.get_item_by_id(item_id)
        self.repository.delete(item)
