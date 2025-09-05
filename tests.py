import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models import Base, Payment
from app.DAO.payments import PaymentDao
from pydantic import BaseModel


# Pydantic-схема для создания Payment
class PaymentCreate(BaseModel):
    tg_id: int =  12345
    amount: int = 150
    number_of_months: int = 3
    status: str = "pending"


# Фикстура для тестовой базы
@pytest.fixture(scope="module")
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_create_payment(db_session: AsyncSession):
    obj_in = PaymentCreate(tg_id=12345, amount=100, number_of_months=1)
    payment = await PaymentDao.create(obj_in, db_session)

    assert payment.id is not None
    assert payment.amount == 100
    assert payment.status == "pending"


@pytest.mark.asyncio
async def test_get_payment_by_id(db_session: AsyncSession):
    obj_in = PaymentCreate(tg_id=12345, amount=200, number_of_months=2)
    new_payment = await PaymentDao.create(obj_in, db_session)

    # ⚠️ у тебя в Dao нет метода get_by_id (есть только кривой get_payment_by_id)
    payment = await db_session.get(Payment, new_payment.id)

    assert payment is not None
    assert payment.amount == 200


@pytest.mark.asyncio
async def test_get_list_payments_by_status(db_session: AsyncSession):
    obj1 = PaymentCreate(tg_id=111, amount=50, number_of_months=1, status="confirmed")
    obj2 = PaymentCreate(tg_id=222, amount=75, number_of_months=1, status="pending")

    await PaymentDao.create(obj1, db_session)
    await PaymentDao.create(obj2, db_session)

    confirmed = await PaymentDao.get_list_payments_by_status("confirmed", db_session)
    pending = await PaymentDao.get_list_payments_by_status("pending", db_session)

    assert all(p.status == "confirmed" for p in confirmed)
    assert all(p.status == "pending" for p in pending)
