from datetime import datetime

class Payment:
    """Данные платежа"""
    def __init__(
        self,
        payment_id: str,
        user_id: int,
        amount: float,
        currency: str,
        status: str,
        payment_date: datetime,
        transaction_id: str,
        order_id: str = None
    ):
        self.payment_id = payment_id
        self.user_id = user_id
        self.amount = amount
        self.currency = currency
        self.status = status
        self.payment_date = payment_date
        self.transaction_id = transaction_id
        self.order_id = order_id

class Order:
    """Заказ на подписку"""
    def __init__(
        self,
        order_id: str,
        user_id: int,
        plan_name: str,
        amount: float,
        status: str,  # "created", "paid", "canceled"
        created_at: datetime,
        payment_id: str = None
    ):
        self.order_id = order_id
        self.user_id = user_id
        self.plan_id = plan_name
        self.amount = amount
        self.status = status
        self.created_at = created_at
        self.payment_id = payment_id