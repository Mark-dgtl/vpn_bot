from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.user import UserDao
from app.session import get_db
from app.shemas import NewUserS
from app.routers import user
from app.routers import payment


app = FastAPI()


app.include_router(user.router)
app.include_router(payment.router)