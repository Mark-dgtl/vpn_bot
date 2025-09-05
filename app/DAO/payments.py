from pydantic import BaseModel
from sqlalchemy import BigInteger, select

from app.DAO.base import BaseDAO
from app.models import Payment
from app.session import AsyncSession


class PaymentDao(BaseDAO):
    model = Payment

    @classmethod
    async def create(cls, obj_in: BaseModel, db: AsyncSession):
        return BaseDAO.create(obj_in, db)

    @classmethod
    async def get_payment_by_id(cls, id: BigInteger, db: AsyncSession):
        payment =  cls.get_by_tg_id(id, db)

    @classmethod
    async def get_list_payments_by_status(cls, status: str, db: AsyncSession):
        query = select(cls.model).filter_by(status=status)
        result = await db.execute(query)
        return result.scalars().all()

