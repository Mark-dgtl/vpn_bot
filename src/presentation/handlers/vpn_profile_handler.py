#     """
# Обработчик профиля пользователя
# Управление подписками, конфигами, отзывы
# """
# from aiogram import Router, F
# from aiogram.types import CallbackQuery, Message, FSInputFile
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from datetime import datetime
#
# from application.use_cases.subscription_use_cases import SubscriptionUseCases
# from application.use_cases.user_use_cases import UserUseCases
# from presentation.keyboards.main_keyboards import (
#     get_my_subscriptions_keyboard,
#     get_review_keyboard
# )
#
# # Создаем роутер
# router = Router()
#
#
# # Состояния для отзывов
# class ReviewStates(StatesGroup):
#     """Состояния для оставления отзыва"""
#     waiting_comment = State()  # Ожидание текста отзыва
#
#
# # ============= МОИ ПОДПИСКИ =============
#
# @router.callback_query(F.data == "my_subscriptions")
# async def show_my_subscriptions(
#     callback: CallbackQuery,
#     subscription_use_cases: SubscriptionUseCases,
#     user_use_cases: UserUseCases
# ):
#     """
#     Показывает информацию о подписках пользователя
#
#     Args:
#         callback: Callback от кнопки "Мои подписки"
#         subscription_use_cases: Use case для подписок
#         user_use_cases: Use case для пользователей
#     """
#     user_id = callback.from_user.id
#
#     # Получаем все подписки пользователя
#     subscriptions = await subscription_use_cases.get_user_subscriptions(user_id)
#
#     if not subscriptions:
#         # У пользователя нет подписок
#         await callback.message.edit_text(
#             "У вас пока нет активных подписок.\n"
#             "Выберите тариф для подключения:",
#             reply_markup=get_my_subscriptions_keyboard(has_active=False)
#         )
#         await callback.answer()
#         return
#
#     # Находим активную подписку
#     active_sub = None
#     for sub in subscriptions:
#         if sub.status.value in ["active", "trial"]:
#             active_sub = sub
#             break
#
#     if active_sub:
#         # Форматируем информацию о подписке
#         end_date = active_sub.end_date.strftime("%d.%m.%Y %H:%M")
#         days_left = (active_sub.end_date - datetime.now()).days
#
#         # Определяем тип подписки
#         if active_sub.is_trial:
#             sub_type = "🎁 Пробная"
#         else:
#             sub_type = f"💎 {active_sub.plan_months} мес."
#
#         # Формируем текст
#         text = (
#             f"📱 Ваша подписка\n\n"
#             f"Тип: {sub_type}\n"
#             f"Статус: {'✅ Активна' if active_sub.status.value == 'active' else '⏰ Пробная'}\n"
#             f"Действует до: {end_date}\n"
#             f"Осталось дней: {days_left}\n\n"
#         )
#
#         if days_left <= 3:
#             text += "⚠️ Подписка скоро истечет! Рекомендуем продлить."
#
#         await callback.message.edit_text(
#             text,
#             reply_markup=get_my_subscriptions_keyboard(has_active=True)
#         )
#     else:
#         # Нет активной подписки, но есть история
#         await callback.message.edit_text(
#             "У вас нет активной подписки.\n"
#             "История подписок доступна в профиле.",
#             reply_markup=get_my_subscriptions_keyboard(has_active=False)
#         )
#
#     await callback.answer()
#
#
# # ============= СКАЧАТЬ ТЕКУЩИЙ КОНФИГ =============
#
# @router.callback_query(F.data == "download_current_config")
# async def download_current_config(
#     callback: CallbackQuery,
#     subscription_use_cases: SubscriptionUseCases
# ):
#     """
#     Отправляет текущий конфигурационный файл пользователю
#
#     Args:
#         callback: Callback от кнопки "Скачать конфиг"
#         subscription_use_cases: Use case для подписок
#     """
#     user_id = callback.from_user.id
#
#     # Получаем активную подписку
#     subscriptions = await subscription_use_cases.get_user_subscriptions(user_id)
#     active_sub = None
#
#     for sub in subscriptions:
#         if sub.status.value in ["active", "trial"]:
#             active_sub = sub
#             break
#
#     if not active_sub or not active_sub.config_file:
#         await callback.answer(
#             "❌ У вас нет активного конфига",
#             show_alert=True
#         )
#         return
#
#     # Отправляем файл
#     try:
#         file = FSInputFile(active_sub.config_file)
#         await callback.message.answer_document(
#             document=file,
#             caption="📄 Ваш конфигурационный файл VPN"
#         )
#         await callback.answer("Файл отправлен!")
#     except Exception as e:
#         await callback.answer(
#             "❌ Ошибка отправки файла. Обратитесь в поддержку.",
#             show_alert=True
#         )
#
#
# # ============= СГЕНЕРИРОВАТЬ НОВЫЙ КОНФИГ =============
#
# @router.callback_query(F.data == "new_config")
# async def generate_new_config(
#     callback: CallbackQuery,
#     subscription_use_cases: SubscriptionUseCases
# ):
#     """
#     Генерирует новый VPN конфиг для пользователя
#     Используется если старый конфиг перестал работать
#
#     Args:
#         callback: Callback от кнопки "Новый конфиг"
#         subscription_use_cases: Use case для подписок
#     """
#     user_id = callback.from_user.id
#
#     # Показываем индикатор загрузки
#     await callback.answer("⏳ Генерируем новый конфиг...")
#
#     try:
#         # Генерируем новый конфиг
#         new_config_path = await subscription_use_cases.regenerate_config(user_id)
#
#         if not new_config_path:
#             await callback.message.answer(
#                 "❌ Не удалось сгенерировать новый конфиг.\n"
#                 "Убедитесь, что у вас есть активная подписка."
#             )
#             return
#
#         # Отправляем новый конфиг
#         file = FSInputFile(new_config_path)
#         await callback.message.answer_document(
#             document=file,
#             caption=(
#                 "✅ Новый конфигурационный файл создан!\n\n"
#                 "⚠️ Старый конфиг больше не работает.\n"
#                 "Используйте этот новый файл для подключения."
#             )
#         )
#
#         await callback.answer("Готово!")
#
#     except Exception as e:
#         await callback.message.answer(
#             "❌ Произошла ошибка при генерации конфига.\n"
#             "Пожалуйста, обратитесь в поддержку."
#         )
#
#
# # ============= ПОДДЕРЖКА =============
#
# @router.callback_query(F.data == "support")
# async def show_support(callback: CallbackQuery):
#     """
#     Показывает информацию о поддержке
#
#     Args:
#         callback: Callback от кнопки "Поддержка"
#     """
#     from presentation.keyboards.main_keyboards import get_support_keyboard
#
#     support_text = (
#         "💬 Поддержка\n\n"
#         "Если у вас возникли проблемы с VPN:\n\n"
#         "1️⃣ Проверьте инструкцию по подключению\n"
#         "2️⃣ Убедитесь, что подписка активна\n"
#         "3️⃣ Попробуйте сгенерировать новый конфиг\n\n"
#         "Если ничего не помогло - свяжитесь с нами:\n"
#         "📧 Email: support@example.com\n"
#         "💬 Telegram: @support_username\n\n"
#         "Время ответа: обычно в течение 1-2 часов"
#     )
#
#     await callback.message.edit_text(
#         support_text,
#         reply_markup=get_support_keyboard()
#     )
#     await callback.answer()
#
#
# # ============= СИСТЕМА ОТЗЫВОВ =============
#
# @router.callback_query(F.data.startswith("review_"))
# async def handle_review_rating(callback: CallbackQuery, state: FSMContext):
#     """
#     Обрабатывает оценку от пользователя
#
#     Args:
#         callback: Callback с оценкой (review_1, review_3, review_5)
#         state: FSM состояние
#     """
#     # Извлекаем оценку и ID подписки
#     # Формат: review_5_123
#     parts = callback.data.split("_")
#     rating = int(parts[1])
#     subscription_id = int(parts[2])
#
#     # Сохраняем данные
#     await state.update_data(
#         rating=rating,
#         subscription_id=subscription_id
#     )
#
#     # Если оценка низкая - просим оставить комментарий
#     if rating <= 3:
#         await callback.message.edit_text(
#             f"Вы поставили {rating} {'звезду' if rating == 1 else 'звезды'} ⭐\n\n"
#             "Пожалуйста, расскажите, что можно улучшить?\n"
#             "Напишите ваш комментарий:",
#             reply_markup=None
#         )
#         await state.set_state(ReviewStates.waiting_comment)
#     else:
#         # Высокая оценка - сразу сохраняем
#         await save_review(callback, state, comment=None)
#
#     await callback.answer()
#
#
# @router.message(ReviewStates.waiting_comment)
# async def save_review_with_comment(message: Message, state: FSMContext):
#     """
#     Сохраняет отзыв с комментарием
#
#     Args:
#         message: Сообщение с комментарием
#         state: FSM состояние
#     """
#     comment = message.text
#     await save_review(message, state, comment)
#
#
# async def save_review(event, state: FSMContext, comment: str = None):
#     """
#     Сохраняет отзыв в базу данных
#
#     Args:
#         event: Message или CallbackQuery
#         state: FSM состояние
#         comment: Комментарий пользователя (опционально)
#     """
#     # Получаем данные
#     data = await state.get_data()
#     rating = data.get('rating')
#     subscription_id = data.get('subscription_id')
#
#     #  Сохранить отзыв через use case
#     # await review_use_cases.create_review(
#     #     user_id=event.from_user.id,
#     #     subscription_id=subscription_id,
#     #     rating=rating,
#     #     comment=comment
#     # )
#
#     # Благодарим за отзыв
#     thank_you_text = (
#         "✅ Спасибо за ваш отзыв!\n\n"
#         "Мы постоянно работаем над улучшением сервиса."
#     )
#
#     if rating <= 3:
#         thank_you_text += "\n\nНаша поддержка свяжется с вами в ближайшее время."
#
#     if isinstance(event, Message):
#         await event.answer(thank_you_text)
#     else:
#         await event.message.edit_text(thank_you_text)
#
#     # Очищаем состояние
#     await state.clear()
#
#
# @router.callback_query(F.data == "skip_review")
# async def skip_review(callback: CallbackQuery):
#     """
#     Пропускает оставление отзыва
#
#     Args:
#         callback: Callback от кнопки "Позже"
#     """
#     await callback.message.edit_text(
#         "Хорошо, вы можете оставить отзыв позже в разделе «Мои подписки»"
#     )
#     await callback.answer()
#
#
# # ============= УВЕДОМЛЕНИЕ О ЗАПРОСЕ ОТЗЫВА =============
#
# async def send_review_request(bot, user_id: int, subscription_id: int):
#     """
#     Отправляет запрос на отзыв пользователю
#     Вызывается через планировщик через 1 день после покупки
#
#     Args:
#         bot: Экземпляр бота
#         user_id: ID пользователя
#         subscription_id: ID подписки
#     """
#     text = (
#         "⭐ Оцените качество VPN\n\n"
#         "Вы пользуетесь нашим VPN уже сутки.\n"
#         "Поделитесь вашим мнением!"
#     )
#
#     await bot.send_message(
#         chat_id=user_id,
#         text=text,
#         reply_markup=get_review_keyboard(subscription_id)
#     )