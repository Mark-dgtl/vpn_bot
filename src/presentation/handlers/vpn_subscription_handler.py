# """
# Обработчик выбора тарифов и оплаты подписки
# """
# from aiogram import Router, F
# from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
#
# # Импорты
# from presentation.keyboards.payment_keyboards import (
#     get_tariff_keyboard,
#     get_payment_keyboard,
#     get_payment_failed_keyboard
# )
# from application.use_cases.subscription_use_cases import SubscriptionUseCases
# from application.use_cases.payment_use_cases import PaymentUseCases
# from config import config
#
# # Создаем роутер
# router = Router()
#
#
# # Состояния для FSM (машина состояний)
# class SubscriptionStates(StatesGroup):
#     """Состояния процесса оформления подписки"""
#     choosing_plan = State()     # Выбор тарифа
#     waiting_payment = State()   # Ожидание оплаты
#
#
# @router.callback_query(F.data == "subscribe")
# async def show_tariffs(callback: CallbackQuery, state: FSMContext):
#     """
#     Показывает доступные тарифы
#
#     Args:
#         callback: Callback от кнопки "Подключиться к VPN"
#         state: Состояние FSM для отслеживания процесса
#     """
#     # Показываем тарифы
#     await callback.message.edit_text(
#         "Выберите тариф:",
#         reply_markup=get_tariff_keyboard()
#     )
#
#     # Устанавливаем состояние выбора тарифа
#     await state.set_state(SubscriptionStates.choosing_plan)
#     await callback.answer()
#
#
# @router.callback_query(F.data.startswith("plan_"))
# async def select_plan(
#     callback: CallbackQuery,
#     state: FSMContext,
#     payment_use_cases: PaymentUseCases
# ):
#     """
#     Обрабатывает выбор тарифного плана
#
#     Args:
#         callback: Callback с данными о выбранном тарифе (plan_1, plan_3, plan_6)
#         state: Состояние FSM
#         payment_use_cases: Use case для работы с платежами
#     """
#     # Извлекаем количество месяцев из callback_data
#     # Формат: plan_1, plan_3, plan_6
#     months = int(callback.data.split("_")[1])
#
#     # Определяем цену в зависимости от тарифа
#     prices = {
#         1: config.plans.one_month,
#         3: config.plans.three_months,
#         6: config.plans.six_months
#     }
#     price = prices[months]
#
#     # Сохраняем выбранный тариф в состояние
#     await state.update_data(
#         plan_months=months,
#         plan_price=price
#     )
#
#     # Создаем предварительный платеж в системе
#     user_id = callback.from_user.id
#     payment = await payment_use_cases.create_payment(
#         user_id=user_id,
#         amount=price,
#         plan_months=months
#     )
#
#     # Сохраняем ID платежа
#     await state.update_data(payment_id=payment.id)
#
#     # Показываем инструкцию по оплате
#     await callback.message.edit_text(
#         f"Выбран тариф: {months} мес. — {price}₽\n\n"
#         "1. Нажмите кнопку «Оплатить»\n"
#         "2. Вернитесь сюда, чтобы получить доступ к VPN",
#         reply_markup=get_payment_keyboard(payment.id)
#     )
#
#     # Переходим в состояние ожидания оплаты
#     await state.set_state(SubscriptionStates.waiting_payment)
#     await callback.answer()
#
#
# @router.callback_query(F.data.startswith("pay_"))
# async def process_payment(callback: CallbackQuery, state: FSMContext):
#     """
#     Инициирует процесс оплаты через Telegram Payments
#
#     Args:
#         callback: Callback с ID платежа
#         state: Состояние FSM
#     """
#     # Получаем данные из состояния
#     data = await state.get_data()
#     plan_price = data.get("plan_price")
#     plan_months = data.get("plan_months")
#
#     # Формируем заголовок и описание для платежа
#     title = f"VPN подписка на {plan_months} мес."
#     description = f"Подписка на VPN сервис ({plan_months} мес.)"
#
#     # Создаем список цен (требуется для Telegram Payments API)
#     prices = [
#         LabeledPrice(label=title, amount=plan_price * 100)  # Цена в копейках
#     ]
#
#     # Отправляем инвойс (счет на оплату)
#     await callback.message.answer_invoice(
#         title=title,
#         description=description,
#         payload=f"subscription_{plan_months}",  # Данные для идентификации платежа
#         provider_token=config.payment.provider_token,
#         currency="RUB",
#         prices=prices,
#         start_parameter="subscription",
#         # Можно добавить фото товара
#         # photo_url="https://example.com/vpn_image.jpg",
#         # photo_width=640,
#         # photo_height=480
#     )
#
#     await callback.answer()
#
#
# @router.pre_checkout_query()
# async def pre_checkout_handler(
#     pre_checkout_query: PreCheckoutQuery,
#     payment_use_cases: PaymentUseCases
# ):
#     """
#     Обработчик предварительной проверки платежа
#     Вызывается перед финальной оплатой для валидации
#
#     Args:
#         pre_checkout_query: Запрос от Telegram о подтверждении платежа
#         payment_use_cases: Use case для работы с платежами
#     """
#     # Здесь можно добавить дополнительную валидацию
#     # Например, проверить доступность серверов
#
#     # Подтверждаем платеж
#     await pre_checkout_query.answer(ok=True)
#
#
# @router.message(F.successful_payment)
# async def successful_payment_handler(
#     message: Message,
#     state: FSMContext,
#     payment_use_cases: PaymentUseCases,
#     subscription_use_cases: SubscriptionUseCases
# ):
#     """
#     Обработчик успешного платежа
#     Вызывается автоматически после успешной оплаты
#
#     Args:
#         message: Сообщение с данными об успешном платеже
#         state: Состояние FSM
#         payment_use_cases: Use case для платежей
#         subscription_use_cases: Use case для подписок
#     """
#     # Получаем информацию о платеже
#     payment_info = message.successful_payment
#
#     # Получаем данные из состояния
#     data = await state.get_data()
#     plan_months = data.get("plan_months")
#     payment_id = data.get("payment_id")
#
#     # Обновляем статус платежа в БД
#     await payment_use_cases.mark_payment_successful(
#         payment_id=payment_id,
#         provider_payment_id=payment_info.telegram_payment_charge_id
#     )
#
#     # Создаем подписку для пользователя
#     user_id = message.from_user.id
#     subscription = await subscription_use_cases.create_subscription(
#         user_id=user_id,
#         plan_months=plan_months
#     )
#
#     # Проверяем, был ли пользователь приглашен по реферальной ссылке
#     # Если да - начисляем бонус рефереру
#     await payment_use_cases.process_referral_bonus(user_id)
#
#     # Форматируем дату окончания подписки
#     end_date = subscription.end_date.strftime("%d.%m.%Y")
#
#     # Отправляем успешное сообщение с конфигом
#     await message.answer(
#         f"✅ Оплата прошла успешно! Доступ к VPN активирован до {end_date}.\n\n"
#         "Инструкция и конфигурационный файл:",
#         reply_markup=get_config_keyboard(subscription.config_file)
#     )
#
#     # Очищаем состояние
#     await state.clear()
#
#     # Планируем отправку запроса на отзыв через 1 день
#     # Это делается через планировщик задач (scheduler)
#
#
# @router.callback_query(F.data == "payment_failed")
# async def payment_failed_handler(callback: CallbackQuery):
#     """
#     Обработчик неудачной оплаты
#
#     Args:
#         callback: Callback от системы оплаты
#     """
#     await callback.message.edit_text(
#         "❌ Оплата не прошла! Возможные причины:\n"
#         "— Недостаточно средств на карте\n"
#         "— Ошибка в реквизитах\n\n"
#         "Попробуйте ещё раз:",
#         reply_markup=get_payment_failed_keyboard()
#     )
#     await callback.answer()
#
#
# @router.callback_query(F.data == "retry_payment")
# async def retry_payment(callback: CallbackQuery, state: FSMContext):
#     """
#     Повторная попытка оплаты
#
#     Args:
#         callback: Callback от кнопки "Повторить оплату"
#         state: Состояние FSM
#     """
#     # Возвращаемся к выбору тарифа
#     await show_tariffs(callback, state)
#
#
# def get_config_keyboard(config_file: str):
#     """
#     Создает клавиатуру с конфигом и инструкцией
#
#     Args:
#         config_file: Путь к файлу конфигурации
#
#     Returns:
#         InlineKeyboardMarkup: Клавиатура с кнопками
#     """
#     from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(
#             text="📄 Скачать конфиг",
#             # Здесь должна быть ссылка на файл или callback для отправки файла
#             callback_data=f"download_config_{config_file}"
#         )],
#         [InlineKeyboardButton(
#             text="📖 Инструкция по подключению",
#             url="https://example.com/instruction"  # Ссылка на статью с инструкцией
#         )],
#         [InlineKeyboardButton(
#             text="« Главное меню",
#             callback_data="main_menu"
#         )]
#     ])
#     return keyboard
#
#
# @router.callback_query(F.data.startswith("download_config_"))
# async def send_config_file(callback: CallbackQuery):
#     """
#     Отправляет конфигурационный файл пользователю
#
#     Args:
#         callback: Callback с именем файла
#     """
#     # Извлекаем имя файла
#     config_file = callback.data.replace("download_config_", "")
#
#     # Отправляем файл
#     from aiogram.types import FSInputFile
#
#     file = FSInputFile(config_file)
#     await callback.message.answer_document(
#         document=file,
#         caption="Ваш конфигурационный файл для VPN"
#     )
#
#     await callback.answer("Файл отправлен!")