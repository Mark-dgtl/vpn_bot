from pydantic import BaseModel
from sqlalchemy import BigInteger, select

from app.dao.base import BaseDAO
from app.models import Payment
from app.session import AsyncSession


class PaymentDao(BaseDAO):
    model = Payment

    @classmethod
    async def get_payments_by_id(cls, id: int, db: AsyncSession):
        query = select(cls.model).filter_by(tg_id=id)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_list_payments_by_status(cls, status: str, db: AsyncSession):
        query = select(cls.model).filter_by(status=status)
        result = await db.execute(query)
        return result.scalars().all()

