from dataclasses import dataclass


@dataclass
class PaymentConfirmEvent:
    order_id: str
    payment_id: str
    status: str