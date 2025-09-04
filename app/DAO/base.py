from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import BigInteger

from app.session import Base


class BaseDAO:
    model = None

    @classmethod
    async def create(cls, obj_in: BaseModel, db: AsyncSession) -> Base:
        obj = cls.model(**obj_in.model_dump())
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    @classmethod
    async def get_one(cls, obj_in: BaseModel, db: AsyncSession) -> Base or None:
        stmt = select(cls.model).filter_by(**obj_in.model_dump())
        result = await  db.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def get_all(cls, db: AsyncSession) -> list[Base]:
        stmt = select(cls.model)
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def update(cls, obj_in: BaseModel, values: BaseModel, db: AsyncSession) -> Base or None:
        stmt = (
            update(cls.model)
            .filter_by(**obj_in.model_dump())
            .values(**values.model_dump())
            .returning(cls.model)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalars().first()

    @classmethod
    async def delete(cls, obj_in: BaseModel, db: AsyncSession) -> int:
        stmt = delete(cls.model).filter_by(**obj_in.model_dump())
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount

    @classmethod
    async def get_by_id(cls, id: int, db: AsyncSession) -> Base or None:
        return await db.get(cls.model, id)

    @classmethod
    async def get_by_tg_id(cls, id: BigInteger, db: AsyncSession) -> Base:
        query = select(cls.model).filter_by(tg_id=id)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def exists(cls, obj_in: BaseModel, db: AsyncSession) -> bool:
        query = select(cls.model).filter_by(**obj_in.model_dump())
        result = await db.execute(query)
        return result.scalar_one_or_none() is not None

