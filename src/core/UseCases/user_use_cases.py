from src.core.dtos import UserRegistrationData
from src.core.entities import User
from src.core.repositories import UserRepo

class UserUseCases:
    def __init__(self, user_repo: UserRepo, db):
        self.user_repo = user_repo
        self.db = db

    async def create_or_get_user(self, data: UserRegistrationData) -> User:
        user = await self.user_repo.find_by_user_id(data.telegram_id)
        if user:
            return user
        return await self.user_repo.create(data)
