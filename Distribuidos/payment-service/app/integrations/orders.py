from httpx import Client, HTTPStatusError, RequestError
from fastapi import HTTPException
from http import HTTPStatus

class OrdersIntegrations:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_order_price(self, order_id: int) -> float:
        url = f'{self.base_url}/{order_id}'

        try: 
            with Client() as client:
                response = client.get(url, timeout=5.0)

                response.raise_for_status()

                data = response.json()

                total_ammount = data.get('total_amount')

                return total_ammount
            
        except HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error retrieving request from external API: {e.response.text}"
            )
        except RequestError as e:
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail='Order service unavailable'
            )
        