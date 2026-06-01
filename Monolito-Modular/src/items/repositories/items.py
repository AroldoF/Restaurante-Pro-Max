from sqlmodel import Session, select
from ..models.items import Item
from ..schemas.items import ItemCreate, ItemUpdate


class ItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> list[Item]:
        statement = select(Item).where(Item.is_active == True)
        return self.session.exec(statement).all()

    def get_by_id(self, item_id: int) -> Item | None:
        statement = select(Item).where(Item.id == item_id, Item.is_active == True)
        return self.session.exec(statement).first()

    def list_by_ids(self, item_ids: list[int]) -> list[Item]:
        statement = select(Item).where(Item.id.in_(item_ids), Item.is_active == True)
        return self.session.exec(statement).all()

    def save_all(self, items: list[Item]) -> list[Item]:
        self.session.add_all(items)

        return items

    def create(self, payload: ItemCreate) -> Item:
        item = Item(**payload.model_dump())
        self.session.add(item)
        return item

    def update(
        self, item: Item, payload: ItemUpdate
    ) -> Item:
        item_data = payload.model_dump(exclude_none=True)

        for key, value in item_data.items():
            setattr(item, key, value)

        self.session.add(item)
        return item

    def delete(self, item: Item) -> Item:
        item.is_active = False

        self.session.add(item)

        return item
        
