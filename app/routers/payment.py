from fastapi import FastAPI, APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.session import get_db
from app.shemas import NewPaymentS
from app.dao.payments import PaymentDao

router = APIRouter(tags=["Payments"])


@router.post("/new_payment")
async def add_payment(data: NewPaymentS, db: AsyncSession = Depends(get_db)):
    return await PaymentDao.create(data, db)

@router.get("/get_payments")
async def get_payments(id: int, db: AsyncSession = Depends(get_db)):
    return await PaymentDao.get_payments_by_id(id, db)