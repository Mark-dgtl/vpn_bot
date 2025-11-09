from typing import Union
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, BaseFilter
from aiogram.types import Message, CallbackQuery

from src.config import settings

admin_router = Router()



class AdminFilter(BaseFilter):
    """
    Фильтр, проверяющий, является ли пользователь администратором.
    """
    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        # Получаем ID пользователя из события
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            # Если тип события не поддерживается фильтром, возвращаем False
            return False

        # Проверяем, есть ли ID пользователя в списке администраторов
        return user_id == settings.ADMIN_ID

admin_router.message.filter(AdminFilter())

@admin_router.message(CommandStart)
async def cmd_start(message: Message):
    await message.answer("Вы находитесь в админской части бота.")




