from dataclasses import dataclass
from datetime import timedelta

@dataclass
class Plan:
    description: str  # Описание
    duration: timedelta  # Сколько длится подписка
    price: int  # Цена в копейках (или минимальных единицах валюты)
    is_free: bool = False  # Является ли план бесплатным


forever_free = Plan("Полностью бесплатный план", timedelta(days=365*2), 0, True)
seven_days_free = Plan("Первые 7 дней бесплатно", timedelta(days=7), 0, True)
one_month = Plan("Подписка на 1 месяц", timedelta(days=30), 60, False)
three_months = Plan("Подписка на 3 месяца", timedelta(days=92), 180, False)
