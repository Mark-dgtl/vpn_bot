from datetime import datetime

class SubscriptionPlan:
    """Тарифный план (описание возможностей)"""
    def __init__(
        self,
        name: str,
        duration_days: int,
        price: float,
        currency: str,
        traffic_limit_gb: int,
    ):
        self.name = name
        self.duration_days = duration_days
        self.price = price
        self.currency = currency
        self.traffic_limit_gb = traffic_limit_gb

class Subscription:
    """Активная подписка пользователя"""
    def __init__(
        self,
        sub_id: str,
        user_id: int,
        plan_name: str,
        start_date: datetime,
        end_date: datetime,
        status: str,  # "active", "expired", "canceled"
        auto_renew: bool = True,
        traffic_used_gb: float = 0.0
    ):
        self.sub_id = sub_id
        self.user_id = user_id
        self.plan_name = plan_name
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.auto_renew = auto_renew
        self.traffic_used_gb = traffic_used_gb