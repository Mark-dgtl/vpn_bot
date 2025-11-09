from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from src.config import settings
# from config import config


def get_terms_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура с принятием условий использования
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="✅ Принять и продолжить",
            callback_data="accept_terms"
        )],
        [InlineKeyboardButton(
            text="📜 Политика конфиденциальности",
            url="https://example.com/privacy"
        )],
        [InlineKeyboardButton(
            text="📋 Условия использования",
            url="https://example.com/terms"
        )],
        [InlineKeyboardButton(
            text="Пользовательское соглашение",
            url="https://example.com/terms"
        )]
    ])
    return keyboard


def get_main_menu_keyboard(url) -> InlineKeyboardMarkup:
    """
    Главное меню для пользователей без подписки
    """
    # Основные кнопки для всех пользователей
    buttons = [
        [InlineKeyboardButton(
            text="🔐 Подключиться к VPN",
            callback_data="subscribe"
        )],
        [InlineKeyboardButton(
            text="🎁 Пробный период",
            callback_data="trial"
        )],
        [InlineKeyboardButton(
            text="💎 Реферальная программа",
            callback_data="referral"
        )],
        [InlineKeyboardButton(
            text="💬 Поддержка",
            # callback_data="support"
            url=url
        )]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_subscribed_user_menu(is_admin: bool = False) -> InlineKeyboardMarkup:
    """
    Меню для пользователей с активной подпиской
    """
    buttons = [
        [InlineKeyboardButton(
            text="📱 Мои подписки",
            callback_data="my_subscriptions"
        )],
        [InlineKeyboardButton(
            text="🔄 Новый конфиг",
            callback_data="new_config"
        )],
        [InlineKeyboardButton(
            text="💎 Реферальная программа",
            callback_data="referral"
        )],
        [InlineKeyboardButton(
            text="💬 Поддержка",
            callback_data="support",
            url = "@feedbackVibeVPNBot"

    )]
    ]

    # Добавляем кнопку админа
    if is_admin:
        buttons.append([InlineKeyboardButton(
            text="🔧 Админ-панель",
            callback_data="admin_panel"
        )])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_tariff_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура с выбором тарифного плана

    Returns:
        InlineKeyboardMarkup: Кнопки с тарифами
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"1 месяц - {config.plans.one_month}₽",
            callback_data="plan_1"
        )],
        [InlineKeyboardButton(
            text=f"3 месяца - {config.plans.three_months}₽",
            callback_data="plan_3"
        )],
        [InlineKeyboardButton(
            text=f"6 месяцев - {config.plans.six_months}₽",
            callback_data="plan_6"
        )],
        [InlineKeyboardButton(
            text="« Назад",
            callback_data="main_menu"
        )]
    ])
    return keyboard


def get_payment_keyboard(payment_id: int) -> InlineKeyboardMarkup:
    """
    Клавиатура для оплаты подписки

    Args:
        payment_id: ID платежа в системе

    Returns:
        InlineKeyboardMarkup: Кнопка оплаты
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💳 Оплатить",
            callback_data=f"pay_{payment_id}"
        )],
        [InlineKeyboardButton(
            text="« Назад",
            callback_data="subscribe"
        )]
    ])
    return keyboard


def get_payment_failed_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура при неудачной оплате

    Returns:
        InlineKeyboardMarkup: Кнопки повтора и поддержки
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔄 Повторить оплату",
            callback_data="retry_payment"
        )],
        [InlineKeyboardButton(
            text="💬 Связаться с поддержкой",
            callback_data="support"
        )],
        [InlineKeyboardButton(
            text="« Главное меню",
            callback_data="main_menu"
        )]
    ])
    return keyboard


def get_subscription_renewal_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для продления подписки (в уведомлении об окончании)

    Returns:
        InlineKeyboardMarkup: Кнопки продления
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"Продлить на 1 месяц — {config.plans.one_month}₽",
            callback_data="plan_1"
        )],
        [InlineKeyboardButton(
            text=f"Продлить на 3 месяца — {config.plans.three_months}₽",
            callback_data="plan_3"
        )],
        [InlineKeyboardButton(
            text=f"Продлить на 6 месяцев — {config.plans.six_months}₽",
            callback_data="plan_6"
        )]
    ])
    return keyboard


def get_review_keyboard(subscription_id: int) -> InlineKeyboardMarkup:
    """
    Клавиатура для оценки качества VPN

    Args:
        subscription_id: ID подписки для привязки отзыва

    Returns:
        InlineKeyboardMarkup: Кнопки с оценками
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="⭐⭐⭐⭐⭐ Идеально!",
            callback_data=f"review_5_{subscription_id}"
        )],
        [InlineKeyboardButton(
            text="⭐⭐⭐ Есть замечания",
            callback_data=f"review_3_{subscription_id}"
        )],
        [InlineKeyboardButton(
            text="⭐ Требуется помощь",
            callback_data=f"review_1_{subscription_id}"
        )],
        [InlineKeyboardButton(
            text="❌ Позже",
            callback_data="skip_review"
        )]
    ])
    return keyboard


def get_my_subscriptions_keyboard(has_active: bool) -> InlineKeyboardMarkup:
    """
    Клавиатура для раздела "Мои подписки"

    Args:
        has_active: Есть ли активная подписка

    Returns:
        InlineKeyboardMarkup: Кнопки управления подпиской
    """
    buttons = []

    if has_active:
        buttons.extend([
            [InlineKeyboardButton(
                text="📄 Скачать конфиг",
                callback_data="download_current_config"
            )],
            [InlineKeyboardButton(
                text="🔄 Сгенерировать новый конфиг",
                callback_data="new_config"
            )],
            [InlineKeyboardButton(
                text="➕ Продлить подписку",
                callback_data="subscribe"
            )]
        ])
    else:
        buttons.append([InlineKeyboardButton(
            text="🔐 Подключиться к VPN",
            callback_data="subscribe"
        )])

    buttons.append([InlineKeyboardButton(
        text="« Назад",
        callback_data="main_menu"
    )])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_support_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для поддержки

    Returns:
        InlineKeyboardMarkup: Кнопки связи с поддержкой
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📖 База знаний",
            url="https://example.com/faq"
        )],
        [InlineKeyboardButton(
            text="💬 Написать в поддержку",
            url="https://t.me/support_username"
        )],
        [InlineKeyboardButton(
            text="« Назад",
            callback_data="main_menu"
        )]
    ])
    return keyboard