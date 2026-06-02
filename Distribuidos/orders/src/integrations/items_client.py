import httpx
import os 
from ..schemas.order import ItemResponse, ItemStockReduce


ITEMS_SERVICE_URL = os.getenv("ITEMS_SERVICE_URL", "http://localhost:8001")


class ItemsClient:
    def __init__(self, base_url: str = ITEMS_SERVICE_URL):
        self.base_url = base_url

    def get_items_by_ids(self, item_ids: list[int]) -> list[ItemResponse]:
        items = []
        with httpx.Client() as client:
            for item_id in item_ids:
                response = client.get(f"{self.base_url}/items/{item_id}/")
                if response.status_code == 404:
                    raise ValueError(f"Item {item_id} not found")
                response.raise_for_status()
                items.append(ItemResponse(**response.json()))
        return items

    def reduce_stock(self, reductions: list[ItemStockReduce]) -> None:
        with httpx.Client() as client:
            response = client.patch(
                f"{self.base_url}/items/stock/reduce/",
                json=[r.model_dump() for r in reductions],
            )
            response.raise_for_status()