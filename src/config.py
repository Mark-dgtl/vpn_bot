from pydantic_settings import BaseSettings, SettingsConfigDict


# from src.infrastructure.db.connection import sessionmaker


class Settings(BaseSettings):

    # DB_HOST: str
    # DB_PORT: int
    # DB_USER: str
    # DB_PASSWORD: str
    # DB_NAME: str
    BOT_TOKEN: str
    HELP_BOT_TOKEN: str
    ADMIN_ID: int
    SUPPORT_BOT_USERNAME: str

    # KEY:str
    # ALGORITHM: str

    # def url(self):
    #     return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    # class Config:
    #     env_file = "/home/mark/practice/VPN_BOT/.env"
    model_config = SettingsConfigDict(
        env_file="/home/mark/practice/VPN_BOT/.env",  # Путь к .env файлу
        env_file_encoding='utf-8'  # Рекомендуется указать кодировку
    )

settings = Settings()


# async def get_db():
#     async with sessionmaker() as session:
#         yield session