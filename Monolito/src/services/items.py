from fastapi import HTTPException
from http import HTTPStatus
from sqlmodel import Session
from ..repositories.items import ItemRepository
from ..schemas.items import ItemCreate, ItemUpdate
from ..models.items import Item


class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def list(self) -> list[Item]:
        return self.repository.list()

    def get_by_id(self, item_id: int) -> Item:
        item = self.repository.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Item not found"
            )
        return item

    def list_by_ids(self, item_ids: list[int]):
        items = self.repository.list_by_ids(item_ids)

        if len(items) != len(set(item_ids)):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="One or more items not found",
            )

        return items

    def create(self, payload: ItemCreate) -> Item:
        return self.repository.create(payload)

    def update(self, item_id: int, payload: ItemCreate) -> Item:
        item = self.get_by_id(item_id)  
        return self.repository.update(item, payload)

    def delete(self, item_id: int) -> None:
        item = self.get_by_id(item_id)
        self.repository.delete(item)

    def reduce_stock_bulk(
        self,
        items_quantity: dict[int, int],
    ) -> list[Item]:
        items = self.list_by_ids(list(items_quantity.keys()))

        for item in items:
            quantity = items_quantity[item.id]

            if quantity <= 0:
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail="Quantity must be greater than zero",
                )

            if item.stock < quantity:
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail=f"Insufficient stock for item {item.id}",
                )

            item.stock -= quantity

        return self.repository.save_all(items)