# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, As
# from src.config import settings
#
#
# DB_URL = settings.url()
#
# engine = create_async_engine(DB_URL, echo=True)
# sessionmaker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)