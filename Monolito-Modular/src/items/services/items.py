from fastapi import HTTPException
from http import HTTPStatus
from sqlmodel import Session
from ..interfaces.items import ItemRepositoryInterface
from ..schemas.items import ItemCreate, ItemUpdate
from ..models.items import Item

class ItemService:
    def __init__(self, session: Session, repository: ItemRepositoryInterface):
        self.session = session
        self.repository = repository

    def list_all(self) -> list[Item]:
        return self.repository.list_all()

    def get_by_id(self, item_id: int) -> Item:
        item = self.repository.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Item not found"
            )
        return item

    def list_by_ids(self, item_ids: list[int]) -> list[Item]:
        items = self.repository.list_by_ids(item_ids)

        if len(items) != len(set(item_ids)):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="One or more items not found",
            )

        return items

    def create(self, payload: ItemCreate) -> Item:
        item = self.repository.create(payload)
        self.session.commit()
        self.session.refresh(item)
        return item

    def update(self, item_id: int, payload: ItemCreate) -> Item:
        item = self.get_by_id(item_id)  
        item_modify = self.repository.update(item, payload)
        self.session.commit()
        self.session.refresh(item_modify)

        return item_modify

    def delete(self, item_id: int) -> None:
        item = self.get_by_id(item_id)
        self.repository.delete(item)
        self.session.commit()

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
        self.repository.save_all(items)
        
        return items