import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
session_maker = async_sessionmaker(engine, class_=AsyncSession)

Base = declarative_base()

async def get_db():
    async with session_maker() as session:
        yield session


