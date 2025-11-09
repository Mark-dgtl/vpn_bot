# """
# Обработчики пробного периода и реферальной программы
# """
# from aiogram import Router, F
# from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
#
# from application.use_cases.subscription_use_cases import SubscriptionUseCases
# from application.use_cases.referral_use_cases import ReferralUseCases
# from application.use_cases.user_use_cases import UserUseCases
#
# # Создаем роутер
# router = Router()
#
#
# # ============= ПРОБНЫЙ ПЕРИОД =============
#
# @router.callback_query(F.data == "trial")
# async def activate_trial(
#     callback: CallbackQuery,
#     subscription_use_cases: SubscriptionUseCases,
#     user_use_cases: UserUseCases
# ):
#     """
#     Активирует пробный период для пользователя
#
#     Args:
#         callback: Callback от кнопки "Пробный период"
#         subscription_use_cases: Use case для подписок
#         user_use_cases: Use case для пользователей
#     """
#     user_id = callback.from_user.id
#
#     # Проверяем, не использовал ли пользователь уже пробный период
#     user = await user_use_cases.get_user(user_id)
#
#     if user.trial_used:
#         # Пользователь уже использовал пробный период
#         await callback.message.edit_text(
#             "⚠️ Вы уже использовали пробный период.\n"
#             "Выберите платный тариф для продолжения использования VPN:",
#             reply_markup=get_tariff_keyboard()
#         )
#         await callback.answer()
#         return
#
#     # Активируем пробный период (3 дня)
#     subscription = await subscription_use_cases.activate_trial(
#         user_id=user_id,
#         trial_days=3
#     )
#
#     if not subscription:
#         await callback.message.edit_text(
#             "❌ Не удалось активировать пробный период. Попробуйте позже.",
#             reply_markup=get_back_keyboard()
#         )
#         await callback.answer()
#         return
#
#     # Форматируем дату окончания
#     end_date = subscription.end_date.strftime("%d.%m.%Y")
#
#     # Отправляем сообщение с конфигом
#     await callback.message.edit_text(
#         f"🎁 Пробный период активирован! Вы получаете 3 дня бесплатного доступа к VPN.\n\n"
#         f"⚠️ Важно:\n"
#         f"— Пробный период доступен только 1 раз\n"
#         f"— Чтобы продолжить пользоваться сервисом, выберите тариф после окончания "
#         f"пробного периода (до {end_date})\n\n"
#         f"Инструкция и конфигурационный файл:",
#         reply_markup=get_trial_config_keyboard(subscription.config_file)
#     )
#
#     await callback.answer("Пробный период активирован! 🎉")
#
#
# def get_trial_config_keyboard(config_file: str):
#     """
#     Клавиатура для пробного периода с конфигом
#
#     Args:
#         config_file: Путь к конфигурационному файлу
#
#     Returns:
#         InlineKeyboardMarkup: Клавиатура
#     """
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(
#             text="📄 Скачать конфиг",
#             callback_data=f"download_config_{config_file}"
#         )],
#         [InlineKeyboardButton(
#             text="📖 Инструкция по подключению",
#             url="https://example.com/instruction"
#         )],
#         [InlineKeyboardButton(
#             text="« Главное меню",
#             callback_data="main_menu"
#         )]
#     ])
#     return keyboard
#
#
# # ============= РЕФЕРАЛЬНАЯ ПРОГРАММА =============
#
# @router.callback_query(F.data == "referral")
# async def show_referral_program(
#     callback: CallbackQuery,
#     referral_use_cases: ReferralUseCases,
#     user_use_cases: UserUseCases
# ):
#     """
#     Показывает информацию о реферальной программе
#
#     Args:
#         callback: Callback от кнопки "Реферальная программа"
#         referral_use_cases: Use case для рефералов
#         user_use_cases: Use case для пользователей
#     """
#     user_id = callback.from_user.id
#
#     # Проверяем, есть ли у пользователя активная подписка
#     has_subscription = await user_use_cases.has_active_subscription(user_id)
#
#     if not has_subscription:
#         # У пользователя нет подписки - предлагаем подключиться
#         await callback.message.edit_text(
#             "✨ Стать рефералом могут только активные подписчики!\n"
#             "Подключите любой тариф и получите +1 месяц за каждого друга",
#             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
#                 [InlineKeyboardButton(text="Выбрать тариф", callback_data="subscribe")],
#                 [InlineKeyboardButton(text="« Назад", callback_data="main_menu")]
#             ])
#         )
#         await callback.answer()
#         return
#
#     # Получаем или создаем реферальную ссылку
#     referral_link = await referral_use_cases.get_or_create_referral_link(user_id)
#
#     # Получаем статистику рефералов
#     stats = await referral_use_cases.get_referral_stats(user_id)
#
#     # Формируем текст сообщения
#     text = (
#         f"🎁 Ваша реферальная ссылка:\n"
#         f"{referral_link}\n\n"
#         f"🎁 За каждого друга, который оплатит любой тариф через вашу ссылку, "
#         f"получите +1 месяц бесплатно к своей подписке.\n\n"
#         f"📊 Статистика:\n"
#         f"• Приглашено друзей: {stats['total_referrals']}\n"
#         f"• Активировали подписку: {stats['activated_referrals']}\n"
#         f"• Получено бонусных месяцев: {stats['bonus_months']}\n\n"
#         f"Как это работает:\n"
#         f"1. Поделитесь своей ссылкой\n"
#         f"2. Друг активирует подписку через вашу ссылку\n"
#         f"3. Как только он оплатит тариф — вам начисляется +1 месяц бесплатно к подписке!"
#     )
#
#     await callback.message.edit_text(
#         text,
#         reply_markup=get_referral_keyboard(referral_link)
#     )
#
#     await callback.answer()
#
#
# def get_referral_keyboard(referral_link: str):
#     """
#     Клавиатура для реферальной программы
#
#     Args:
#         referral_link: Реферальная ссылка пользователя
#
#     Returns:
#         InlineKeyboardMarkup: Клавиатура
#     """
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(
#             text="📋 Скопировать ссылку",
#             callback_data="copy_referral_link"
#         )],
#         [InlineKeyboardButton(
#             text="📤 Поделиться",
#             # Switch inline query позволяет пользователю отправить сообщение в любой чат
#             switch_inline_query=f"Подключайся к VPN! {referral_link}"
#         )],
#         [InlineKeyboardButton(
#             text="« Назад",
#             callback_data="main_menu"
#         )]
#     ])
#     return keyboard
#
#
# @router.callback_query(F.data == "copy_referral_link")
# async def copy_referral_link(
#     callback: CallbackQuery,
#     referral_use_cases: ReferralUseCases
# ):
#     """
#     "Копирует" реферальную ссылку (показывает уведомление)
#
#     Args:
#         callback: Callback от кнопки "Скопировать ссылку"
#         referral_use_cases: Use case для рефералов
#     """
#     user_id = callback.from_user.id
#
#     # Получаем реферальную ссылку
#     referral_link = await referral_use_cases.get_or_create_referral_link(user_id)
#
#     # Показываем алерт с ссылкой (пользователь может скопировать её)
#     await callback.answer(
#         f"Ссылка: {referral_link}\n\nНажмите и удерживайте для копирования",
#         show_alert=True
#     )
#
#
# # ============= УВЕДОМЛЕНИЕ О БОНУСЕ =============
#
# async def notify_referral_bonus(user_id: int, referral_name: str, bot):
#     """
#     Отправляет уведомление пользователю о полученном бонусе
#     Эта функция вызывается из use case когда реферал оплачивает подписку
#
#     Args:
#         user_id: ID пользователя (реферера)
#         referral_name: Имя друга, который активировал подписку
#         bot: Экземпляр бота
#     """
#     text = (
#         f"🎉 Ваш друг {referral_name} активировал подписку по вашей ссылке!\n"
#         f"Ваша подписка продлена на 1 месяц"
#     )
#
#     await bot.send_message(
#         chat_id=user_id,
#         text=text
#     )
#
#
# # ============= ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =============
#
# def get_back_keyboard():
#     """Клавиатура с кнопкой "Назад" """
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="« Назад", callback_data="main_menu")]
#     ])
#     return keyboard
#
#
# def get_tariff_keyboard():
#     """Клавиатура с выбором тарифов"""
#     from config import config
#
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(
#             text=f"1 месяц - {config.plans.one_month}₽",
#             callback_data="plan_1"
#         )],
#         [InlineKeyboardButton(
#             text=f"3 месяца - {config.plans.three_months}₽",
#             callback_data="plan_3"
#         )],
#         [InlineKeyboardButton(
#             text=f"6 месяцев - {config.plans.six_months}₽",
#             callback_data="plan_6"
#         )],
#         [InlineKeyboardButton(text="« Назад", callback_data="main_menu")]
#     ])
#     return keyboard