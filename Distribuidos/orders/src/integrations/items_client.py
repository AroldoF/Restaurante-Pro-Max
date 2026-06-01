import httpx
from ..schemas.order import ItemResponse, ItemStockReduce

ITEMS_SERVICE_URL = "http://localhost:8001"


class ItemsClient:
    def __init__(self, base_url: str = ITEMS_SERVICE_URL):
        self.base_url = base_url

    def get_items_by_ids(self, item_ids: list[int]) -> list[ItemResponse]:
        """
        Busca os dados de múltiplos itens no items-service.
        Usado para calcular o total_amount do pedido.
        """
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
        """
        Envia uma lista de {item_id, quantity} para o items-service
        reduzir o estoque. Chamado quando um pedido é finalizado.
        """
        with httpx.Client() as client:
            response = client.patch(
                f"{self.base_url}/items/stock/reduce/",
                json=[r.model_dump() for r in reductions],
            )
            response.raise_for_status()