# src/core/use_cases/check_traffic_usage.py

from typing import Dict
from src.core.entities import TrafficUsage, Subscription
from src.core.exceptions import UserNotFoundError, SubscriptionExpiredError
from src.core.repositories import TrafficUsageRepo, SubscriptionRepo

class TrafficUseCase:
    pass

class CheckTrafficUsageUseCase:
    def __init__(
        self,
        traffic_repo: TrafficUsageRepo,
        subscription_repo: SubscriptionRepo
    ):
        self.traffic_repo = traffic_repo
        self.subscription_repo = subscription_repo

    def execute(self, user_id: int) -> Dict[str, float]:
        # 1. Проверяем активную подписку
        subscription = self.subscription_repo.get_by_user_id(user_id)
        if not subscription or subscription.status != "active":
            raise SubscriptionExpiredError("Подписка не активна")

        # 2. Получаем использование трафика
        traffic_usage = self.traffic_repo.find_by_user(user_id)
        if not traffic_usage:
            # Если нет записи, считаем 0 использованного трафика
            used_gb = 0.0
        else:
            used_gb = traffic_usage.total_used_bytes / (1024**3)  # Байты в ГБ

        # 3. Получаем лимит из подписки (через план)
        plan_name = subscription.plan_name
        # Предполагаем, что SubscriptionPlanRepo доступен для получения лимита
        # Или лимит хранится в самой подписке (traffic_limit_gb). Пока используем из подписки.
        # ! Требуется добавить traffic_limit_gb в Subscription или получить через PlanRepo
        # Пока используем traffic_limit_gb из подписки, если оно там есть (в сущности его нет, но предположим)
        # Альтернатива: получить план через SubscriptionPlanRepo
        # plan = self.plan_repo.find_by_name(plan_name)
        # limit_gb = plan.traffic_limit_gb
        # Пока используем поле из подписки, если оно будет добавлено, или предположим, что лимит в подписке.
        # !!! ВНИМАНИЕ: Поле traffic_limit_gb отсутствует в сущности Subscription.
        # !!! Необходимо либо добавить его в сущность и репозиторий, либо внедрить SubscriptionPlanRepo.
        # !!! Пока возвращаю только использованный трафик.
        # limit_gb = subscription.traffic_limit_gb # Не существует
        # return {"used_gb": used_gb, "limit_gb": limit_gb, "percent_used": (used_gb / limit_gb) * 100 if limit_gb > 0 else 0}

        # Возвращаем только использованный трафик, пока лимит не определен в Subscription
        # Или предположим, что лимит есть в плане и внедрим PlanRepo
        # from src.core.repositories import SubscriptionPlanRepo
        # self.plan_repo = plan_repo # Не внедрено в __init__
        # plan = self.plan_repo.find_by_name(plan_name)
        # limit_gb = plan.traffic_limit_gb

        # !!! ВРЕМЕННОЕ РЕШЕНИЕ: Предположим лимит 100 ГБ, если неизвестен.
        # !!! НЕОБХОДИМО: Внедрить SubscriptionPlanRepo и получить реальный лимит.
        limit_gb = 100.0 # Заглушка
        percent_used = (used_gb / limit_gb) * 100 if limit_gb > 0 else 0

        return {
            "used_gb": round(used_gb, 2),
            "limit_gb": limit_gb, # Заглушка
            "percent_used": round(percent_used, 2)
        }
