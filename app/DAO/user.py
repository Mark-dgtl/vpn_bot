from sqlalchemy import BigInteger
from sqlalchemy.testing.suite.test_reflection import users

from app.DAO.base import BaseDAO
from app.models import User
from app.session import AsyncSession
from app.shemas import NewUserS, DelUserS
from sqlalchemy import select, DateTime



class UserDao(BaseDAO):
    model = User

    @classmethod
    async def add_user(cls, data: NewUserS, db: AsyncSession):
        new_user = await cls.create(data, db)
        return new_user

    @classmethod
    async def del_user(cls, data: DelUserS, db: AsyncSession):
        return await cls.delete(data, db)

    @classmethod
    async def get_by_tg_id(cls, id: BigInteger, db: AsyncSession):
        query = select(cls.model).filter_by(tg_id=id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def ban_user(cls, id: BigInteger, db: AsyncSession):
        user = cls.get_by_tg_id(id, db)
        user.is_banned = True
        await db.commit()
        await db.refresh(user)

    @classmethod
    async def unban_user(cls, id: BigInteger, db: AsyncSession):
        user = cls.get_by_tg_id(id, db)
        user.is_banned = False
        await db.commit()
        await db.refresh(user)

    @classmethod
    async def activate(cls, id: BigInteger, db: AsyncSession):
        user = cls.get_by_tg_id(id, db)
        user.is_active = True
        await db.commit()
        await db.refresh(user)

    @classmethod
    async def deactivate(cls, id: BigInteger, db: AsyncSession):
        user = cls.get_by_tg_id(id, db)
        user.is_active = False
        await db.commit()
        await db.refresh(user)

    @classmethod # продлить подписку
    async def extend_subscription(cls, id: BigInteger, unitil_datetime: DateTime, db: AsyncSession):
        user = cls.get_by_tg_id(id, db)
        user.subscription_end_date = unitil_datetime
        await db.commit()
        await db.refresh(user)

    @classmethod # проверка даты подписки
    async def is_subscription(cls, id: BigInteger, db: AsyncSession):
        user = cls.get_by_tg_id(id, db)
        return user.is_subscription_active()

    @classmethod # обновить последнюю активность
    async def update_last_activity(cls, id: BigInteger, timestamp: DateTime, db: AsyncSession):
        pass