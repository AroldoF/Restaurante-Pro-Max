from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.items import Item
    from ..schemas.items import ItemCreate, ItemUpdate

class ItemRepositoryInterface(ABC):
    @abstractmethod
    def list_all(self) -> list[Item]:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> Item | None:
        pass

    @abstractmethod
    def list_by_ids(self, item_ids: list[int]) -> list[Item]:
        pass

    @abstractmethod
    def save_all(self, items: list[Item]) -> list[Item]:
        pass

    @abstractmethod
    def create(self, payload: ItemCreate) -> Item:
        pass

    @abstractmethod
    def update(
        self, item: Item, payload: ItemUpdate
    ) -> Item:
        pass

    @abstractmethod
    def delete(self, item: Item) -> None:
        pass

class ItemServiceInterface(ABC):
    @abstractmethod
    def list_all(self) -> list[Item]:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> Item:
        pass

    @abstractmethod
    def list_by_ids(self, item_ids: list[int]) -> list[Item]:
        pass

    @abstractmethod        
    def create(self, payload: ItemCreate) -> Item:
        pass

    @abstractmethod
    def update(self, item_id: int, payload: ItemCreate) -> Item:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> None:
        pass

    @abstractmethod
    def reduce_stock_bulk(self, items_quantity: dict[int, int]) -> list[Item]:
        pass