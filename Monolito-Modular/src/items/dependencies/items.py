from fastapi import Depends
from ..services.items import ItemService
from ..repositories.items import ItemRepository
from ....database import get_session
from typing import Annotated
from sqlmodel import Session

def get_item_service(session: Session = Depends(get_session)) -> ItemService:
    item_repository = ItemRepository(session)
    return ItemService(session, item_repository)

ItemServiceDep = Annotated[
    ItemService,
    Depends(get_item_service),
]