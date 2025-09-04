from pydantic import BaseModel
from datetime import datetime

from sqlalchemy import BigInteger

from app.models import PaymentStatus


class NewUserS(BaseModel):
    username: str
    first_name: str
    is_active: bool
    is_banned: bool
    subscription_end_date: datetime or None
    created_at: datetime
    last_activity: datetime

class DelUserS(BaseModel):
    tg_id: int

# class NewPaymentsS(BaseModel):
#     user_id: BigInteger
#     amount:
#     payment_screenshot:
#     status: strint