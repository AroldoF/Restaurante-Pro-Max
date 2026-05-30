from sqlmodel import Session, select
from ..models.items import Item
from ..schemas.items import ItemCreate, ItemUpdate


class ItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Item]:
        return self.session.exec(select(Item)).all()

    def get_by_id(self, item_id: int) -> Item | None:
        return self.session.exec(select(Item).where(Item.id == item_id)).first()

    def get_by_ids(self, items_ids: list[int]) -> list[Item]:
        statement = select(Item).where(Item.id.in_(items_ids))
        return self.session.exec(statement).all()

    def create(self, payload: ItemCreate) -> Item:
        item = Item(**payload.model_dump())
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def update(
        self, item: Item, payload: ItemCreate | ItemUpdate, partial: bool = False
    ) -> Item:
        # exclude_none=True se for PATCH (parcial)
        item_data = payload.model_dump(exclude_none=partial)

        for key, value in item_data.items():
            setattr(item, key, value)

        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, item: Item) -> None:
        self.session.delete(item)
        self.session.commit()
