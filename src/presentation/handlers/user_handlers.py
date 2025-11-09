from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_deep_link


from src.config import settings
from src.presentation.keyboards import (
    get_main_menu_keyboard,
    get_terms_keyboard,
    get_subscribed_user_menu
)

from src.core.UseCases.user_use_cases import UserUseCases
from src.core.UseCases.subscription_use_cases import SubsUseCases

from src.core.dtos import UserRegistrationData



user_router = Router()


@user_router.message(CommandStart())
# async def cmd_start(message: Message, user_use_cases: UserUseCases, subs_use_cases: SubsUseCases):
async def cmd_start(message: Message):

    # Извлекаем данные пользователя из Telegram
    data = UserRegistrationData(
        telegram_id=message.from_user.id,
        username = message.from_user.username,
        first_name = message.from_user.first_name,
        referral_code = None
    )
    #
    # # Проверяем реферальный код в команде /start
    # # Формат: /start ref_12345
    # if message.text and len(message.text.split()) > 1:
    #     # Извлекаем код после /start
    #     referral_code = message.text.split()[1]
    #     if referral_code.startswith("ref_"):
    #         data.referral_code = referral_code  # Оставляем как есть
    #     else:
    #         data.referral_code = None
    #
    # # Вызываем use case для регистрации или получения пользователя
    # user = await user_use_cases.find_by_id(data.telegram_id)
    #
    # # Проверяем, первый ли раз пользователь запускает бота
    # if not user:
    #     await user_use_cases.create_or_get_user(data)
    text = """📜 Перед использованием необходимо принять:
    — Политику конфиденциальности
    — Условия использования
    — Пользовательское соглашение"""
    keyboard = get_terms_keyboard()
        # text = "Туфта это"
        # keyboard = get_main_menu_keyboard()
    # elif await subs_use_cases.check_subs(data.telegram_id):
    #    text = """Привет! 👋
    #             Добро пожаловать в vpn-бота!
    #             """
    #    keyboard = get_subscribed_user_menu()
    # else:
    #     text = """Привет! 👋
    #             Добро пожаловать в vpn-бота!
    #             """
    #     keyboard = get_main_menu_keyboard(data.telegram_id)

    await message.answer(text, reply_markup=keyboard)

@user_router.callback_query(F.data == "accept_terms")
async def accept_terms(callback: CallbackQuery):
    """
    Обработчик согласия с условиями использования
    """
    # Удаляем сообщение с условиями
    await callback.message.delete()

    # user_id =# callback_query.from_user.id

    # Получаем данные пользователя
    # user =  # await user_use_cases.find_by_id(user_id)
    has_subscription = False  # await subs_use_cases.check_subs(user_id)

    # Формируем данные для передачи
    subs_status_str = "1" if has_subscription else "2"
    support_url = f"tg://resolve?domain={settings.SUPPORT_BOT_USERNAME}&start={subs_status_str}"

    await callback.message.answer(
        "Привет! 👋\n"
        "Добро пожаловать в vpn-бота!",
        reply_markup=get_main_menu_keyboard(support_url)
    )


    # Отвечаем на callback (убираем "часики" на кнопке)
    await callback.answer()

#
#
# @user_router.callback_query(F.data == "main_menu")
# async def show_main_menu(callback: CallbackQuery, user_use_cases: UserUseCases):
#     """
#     Показывает главное меню
#     """
#     user = await user_use_cases.get_user(callback.from_user.id)
#
#     # Проверяем, есть ли у пользователя активная подписка
#     has_subscription = await user_use_cases.has_active_subscription(user.id)
#
#     # Показываем разное меню в зависимости от наличия подписки
#     if has_subscription:
#         keyboard = get_subscribed_user_menu(is_admin=user.is_admin)
#         text = "Главное меню"
#     else:
#         keyboard = get_main_menu_keyboard(is_admin=user.is_admin)
#         text = "Привет! 👋\nДобро пожаловать в vpn-бота!"
#
#     # Редактируем сообщение (если это callback)
#     if isinstance(callback, CallbackQuery):
#         await callback.message.edit_text(text, reply_markup=keyboard)
#         await callback.answer()
#     else:
#         # Если это обычное сообщение
#         await callback.answer(text, reply_markup=keyboard)
#
#
#
# # Вспомогательная функция для клавиатуры "Назад"
# def get_back_keyboard():
#     """Возвращает клавиатуру с кнопкой Назад"""
#     from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="« Назад", callback_data="main_menu")]
#     ])
#     return keyboard
#
#
# from datetime import datetime