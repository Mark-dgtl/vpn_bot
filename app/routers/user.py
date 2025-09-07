from datetime import datetime

from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.user import UserDao
from app.session import get_db
from app.shemas import NewUserS
from sqlalchemy import DateTime


router = APIRouter(tags=["Users"])


@router.post("/new_user")
async def add_user(data: NewUserS, db: AsyncSession = Depends(get_db)):
    return await UserDao.create(data, db)

@router.post("/delete_user")
async def delete_user(id: int, db:AsyncSession = Depends(get_db)):
    await UserDao.delete(id, db)

@router.get("/get_user_by_id")
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    return await UserDao.get_by_tg_id(id, db)

@router.post("/ban_user")
async def banned_user(id: int, db: AsyncSession = Depends(get_db)):
    await UserDao.ban_user(id, db)

@router.post("/unban_user")
async def unbanned_user(id: int, db:AsyncSession = Depends(get_db)):
    await UserDao.unban_user(id, db)

@router.post("/activate_user")
async def activate_user(id: int, db:AsyncSession = Depends(get_db)):
    await UserDao.activate(id, db)

@router.post("/deactivate_user")
async def deactivate_user(id: int, db:AsyncSession = Depends(get_db)):
    await UserDao.deactivate(id, db)

@router.patch("/extend_subscription")
async def extend_subscription(id: int, unitil_datetime: datetime, db:AsyncSession = Depends(get_db)):
    await UserDao.extend_subscription(id, unitil_datetime, db)

@router.get("/is_subscription")
async def is_subscription(id: int, db: AsyncSession = Depends(get_db)):
    return await UserDao.is_subscription(id, db)

@router.post("/update_last_activity")
async def update_last_activity(id: int, db: AsyncSession = Depends(get_db)):
    await UserDao.update_last_activity()