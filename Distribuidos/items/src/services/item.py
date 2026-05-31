from fastapi import HTTPException
from http import HTTPStatus
from ..repositories.item import ItemRepository
from ..schemas.item import ItemCreate,ItemUpdate,ItemStockReduce
from ..models.item import Item


class ItemService: 
  def __init__(self, repository: ItemRepository):
    self.repository = repository


  def list(self)-> list[Item]:
    return self.repository.list()
  
  def get_by_id(self, item_id:int)-> Item:
    item = self.repository.get_by_id(item_id)
    if not item:
      raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Item not found"
      )
    return item
  
  def list_by_ids(self, item_ids: list[int])-> list[Item]:
    items = self.repository.list_by_ids(item_ids)
    if len(items) != len(set(item_ids)):
      raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="One or more items not found"
      )
    return items
  
  def create(self,payload: ItemCreate)-> Item:
    return self.repository.create(payload)
  
  def update(self, item_id: int, payload: ItemUpdate)-> Item:
    item = self.get_by_id(item_id)
    return self.repository.update(item, payload)
  
  def delete(self,item_id: int)-> None:
    item = self.get_by_id(item_id)
    self.repository.delete(item)

  def reduce_stock_bulk(self, reductions: list[ItemStockReduce]) -> list[Item]:
    items_ids = [r.item_id for r in reductions]
    items = self.list_by_ids(items_ids)
    items_map = {item.id: item for item in items}

    for reduction in reductions:
      item = items_map[reduction.item_id]
      if item.stock < reduction.quantity:
        raise HTTPException(
          status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
          detail=f"Insufficient stock for item {item.id}"
        )
      item.stock -= reduction.quantity

    return self.repository.save_all(items)