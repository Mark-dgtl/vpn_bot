from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.DAO.user import UserDao
from app.session import get_db
from app.shemas import NewUserS


app = FastAPI()


@app.post("/new_user")
async def add_user(data: NewUserS, db: AsyncSession = Depends(get_db)):
    return await UserDao.create(data, db)