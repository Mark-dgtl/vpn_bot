from sqlalchemy import BigInteger
from sqlalchemy.testing.suite.test_reflection import users

from app.dao.base import BaseDAO
from app.models import User
from app.session import AsyncSession
from app.shemas import NewUserS, DelUserS
from sqlalchemy import select, DateTime, update



class UserDao(BaseDAO):
    model = User

    @classmethod
    async def get_by_tg_id(cls, id: BigInteger, db: AsyncSession):
        query = select(cls.model).filter_by(tg_id=id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def ban_user(cls, id: BigInteger, db: AsyncSession):
        user = await cls.get_by_tg_id(id, db)
        user.is_banned = True
        await db.commit()
        await db.refresh(user)

    @classmethod
    async def unban_user(cls, id: BigInteger, db: AsyncSession):
        user = await cls.get_by_tg_id(id, db)
        user.is_banned = False
        await db.commit()
        await db.refresh(user)

    @classmethod
    async def activate(cls, id: BigInteger, db: AsyncSession):
        user = await cls.get_by_tg_id(id, db)
        user.is_active = True
        await db.commit()
        await db.refresh(user)

    @classmethod
    async def deactivate(cls, id: BigInteger, db: AsyncSession):
        user = await cls.get_by_tg_id(id, db)
        user.is_active = False
        await db.commit()
        await db.refresh(user)

    @classmethod # продлить подписку
    async def extend_subscription(cls, id: int, unitil_datetime: DateTime, db: AsyncSession):
        user = await cls.get_by_tg_id(id, db)
        user.subscription_end_date = unitil_datetime
        await db.commit()
        await db.refresh(user)

    @classmethod # проверка даты подписки
    async def is_subscription(cls, id: int, db: AsyncSession):
        user = await cls.get_by_tg_id(id, db)
        return user.is_subscription_active

    @classmethod
    async def update_last_activity(cls, id: int, timestamp: DateTime, db: AsyncSession):
        stmt = (
            update(cls.model)
            .where(cls.model.tg_id == id)
            .values(last_activity=timestamp)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(stmt)
        await db.commit()