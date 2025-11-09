from typing import Dict

from src.core.entities import Order, Subscription
from src.core.exceptions import PlanNotFoundError, SubscriptionExpiredError, PaymentRequiredError, UserNotFoundError, OrderNotFoundError, PaymentProcessingError
from src.core.repositories import UserRepo, SubscriptionPlanRepo, OrderRepo, PaymentRepo, SubscriptionRepo, \
    SubscriptionPlan, TrafficUsageRepo
from datetime import timedelta, datetime


class SubsUseCases:
    def __init__(
        self,
        user_repo: UserRepo,
        plan_repo: SubscriptionPlanRepo,
        order_repo: OrderRepo,
        payment_repo: PaymentRepo,
        subscription_repo: SubscriptionRepo
    ):
        self.user_repo = user_repo
        self.plan_repo = plan_repo
        self.order_repo = order_repo
        self.payment_repo = payment_repo
        self.subscription_repo = subscription_repo

    async def check_subs(self, user_id):
        return await self.subscription_repo.find_by_user_id(user_id)

class SubscribeToPlanUseCase:
    def __init__(
        self,
        user_repo: UserRepo,
        plan_repo: SubscriptionPlanRepo,
        order_repo: OrderRepo,
        payment_repo: PaymentRepo,
        subscription_repo: SubscriptionRepo
    ):
        self.user_repo = user_repo
        self.plan_repo = plan_repo
        self.order_repo = order_repo
        self.payment_repo = payment_repo
        self.subscription_repo = subscription_repo

    def execute(self, user_id: int, plan_name: str) -> Order:
        # 1. Проверяем пользователя
        if not self.user_repo.find_by_user_id(user_id):
            raise UserNotFoundError(f"Пользователь {user_id} не найден")

        # 2. Находим тариф
        try:
            plan = self.plan_repo.find_by_name(plan_name)
        except:
            raise PlanNotFoundError(f"Тариф {plan_name} не существует")

        # 3. Создаем заказ
        order = Order(
            order_id=f"order_{user_id}_{plan.plan_name}",
            user_id=user_id,
            plan_name=plan.plan_name,
            amount=plan.price,
            status="created"
        )
        saved_order = self.order_repo.create(order)

        # 4. Возвращаем заказ для оплаты
        return saved_order



class HandlePaymentCallbackUseCase:
    """
    Обработка успешной оплаты
    """
    def __init__(
            self,
            order_repo: OrderRepo,
            payment_repo: PaymentRepo,
            subscription_repo: SubscriptionRepo,
            user_repo: UserRepo,
            plan_repo: SubscriptionPlanRepo
    ):
        self.order_repo = order_repo
        self.payment_repo = payment_repo
        self.subscription_repo = subscription_repo
        self.user_repo = user_repo
        self.plan_repo = plan_repo

    def execute(self, payment_id: str, status: str) -> None:
        # 1. Находим платеж
        payment = self.payment_repo.find_by_id(payment_id)
        if not payment:
            raise PaymentProcessingError("Платеж не найден")

        # 2. Обновляем статус платежа
        self.payment_repo.update_status(payment_id, status)
        if status != "success":
            return

        # 3. Находим связанный заказ
        order = self.order_repo.find_by_id(payment.order_id)
        if not order:
            raise OrderNotFoundError("Заказ не найден")

        # 4. Создаем подписку
        user = self.user_repo.find_by_user_id(order.user_id)
        plan = self.plan_repo.find_by_name(order.plan_name)

        subscription = Subscription(
            sub_id=f"sub_{order.order_id}",
            user_id=order.user_id,
            plan_name=order.plan_name,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=plan.duration_days),
            status="active",
            traffic_used_gb=0.0
        )
        self.subscription_repo.create(subscription)

        # 5. Обновляем статус заказа
        self.order_repo.update_status(order.order_id, "paid")


# src/core/use_cases/renew_subscription.py

from datetime import timedelta
from src.core.entities import Subscription
from src.core.exceptions import UserNotFoundError, SubscriptionExpiredError
from src.core.repositories import SubscriptionRepo, UserRepo, SubscriptionPlanRepo

class RenewSubscriptionUseCase:
    def __init__(
        self,
        subscription_repo: SubscriptionRepo,
        user_repo: UserRepo,
        plan_repo: SubscriptionPlanRepo # Необходим для получения длительности
    ):
        self.subscription_repo = subscription_repo
        self.user_repo = user_repo
        self.plan_repo = plan_repo

    def execute(self, user_id: int) -> Subscription:
        # 1. Проверяем существование пользователя
        user = self.user_repo.get_by_user_id(user_id)
        if not user:
            raise UserNotFoundError(f"Пользователь {user_id} не найден")

        # 2. Находим текущую подписку
        current_subscription = self.subscription_repo.get_by_user_id(user_id)
        if not current_subscription:
            raise SubscriptionExpiredError("Подписка не найдена")

        # 3. Проверяем статус (можно продлевать только активные или истекшие)
        if current_subscription.status not in ["active", "expired"]:
             # Если canceled, возможно, не продлевать
             # raise ValueError("Cannot renew a canceled subscription")
             pass # Продолжаем

        # 4. Получаем длительность плана
        plan = self.plan_repo.find_by_name(current_subscription.plan_name)
        duration_days = plan.duration_days

        # 5. Рассчитываем новую дату окончания
        # Продлеваем от текущей даты окончания
        new_end_date = current_subscription.end_date + timedelta(days=duration_days)

        # 6. Обновляем подписку
        current_subscription.end_date = new_end_date
        current_subscription.status = "active" # Сбрасываем статус при продлении
        # !!! ВНИМАНИЕ: Нужен метод в репозитории для обновления существующей сущности
        # self.subscription_repo.update(current_subscription) # Не реализован в Protocol
        # Пока что создадим новую, но это может быть не желательно.
        # Альтернатива: в Protocol добавить update(sub), и в реализации обновлять по sub_id
        # Пока предположим, что update есть или что sub_id фиксирован и можно обновить через create с тем же ID (плохо)
        # !!! НЕОБХОДИМО: Добавить метод update в SubscriptionRepo
        # self.subscription_repo.update(current_subscription)
        # Возвращаем обновленную сущность
        return current_subscription # В реальности нужно обновить в БД



class UnsubscribeUseCase:
    def __init__(self, subscription_repo: SubscriptionRepo, user_repo: UserRepo):
        self.subscription_repo = subscription_repo
        self.user_repo = user_repo

    def execute(self, user_id: int) -> Subscription:
        # 1. Проверяем существование пользователя
        user = self.user_repo.get_by_user_id(user_id)
        if not user:
            raise UserNotFoundError(f"Пользователь {user_id} не найден")

        # 2. Находим текущую подписку
        current_subscription = self.subscription_repo.get_by_user_id(user_id)
        if not current_subscription:
            raise SubscriptionExpiredError("Подписка не найдена")

        # 3. Обновляем статус на "canceled"
        current_subscription.status = "canceled"
        # !!! ВНИМАНИЕ: Требуется метод update в SubscriptionRepo
        # self.subscription_repo.update_status(current_subscription.sub_id, "canceled")
        # Если update_status меняет только статус:
        self.subscription_repo.update_status(current_subscription.sub_id, "canceled")
        # Возвращаем обновленную сущность (статус)
        return current_subscription


class GetSubscriptionStatusUseCase:
    def __init__(
        self,
        subscription_repo: SubscriptionRepo,
        user_repo: UserRepo,
        traffic_repo: TrafficUsageRepo,
        plan_repo: SubscriptionPlanRepo # Для получения лимита
    ):
        self.subscription_repo = subscription_repo
        self.user_repo = user_repo
        self.traffic_repo = traffic_repo
        self.plan_repo = plan_repo

    def execute(self, user_id: int) -> Dict:
        # 1. Проверяем существование пользователя
        user = self.user_repo.get_by_user_id(user_id)
        if not user:
            raise UserNotFoundError(f"Пользователь {user_id} не найден")

        # 2. Получаем подписку
        subscription = self.subscription_repo.get_by_user_id(user_id)
        if not subscription:
            raise SubscriptionExpiredError("Подписка не найдена")

        # 3. Получаем трафик
        traffic_usage = self.traffic_repo.find_by_user(user_id)
        if not traffic_usage:
            used_gb = 0.0
        else:
            used_gb = traffic_usage.total_used_bytes / (1024**3)

        # 4. Получаем лимит трафика из плана
        plan = self.plan_repo.find_by_name(subscription.plan_name)
        limit_gb = plan.traffic_limit_gb

        # 5. Получаем количество активных peer'ов
        # !!! Требуется PeerRepo
        # from src.core.repositories import PeerRepo
        # self.peer_repo = peer_repo # Не внедрено
        # peer_count = self.peer_repo.get_count_by_user(user_id) # Не внедрено
        peer_count = 0 # Заглушка

        # 6. Формируем ответ
        return {
            "status": subscription.status,
            "plan_name": subscription.plan_name,
            "start_date": subscription.start_date.isoformat(),
            "end_date": subscription.end_date.isoformat(),
            "auto_renew": subscription.auto_renew,
            "traffic_used_gb": round(used_gb, 2),
            "traffic_limit_gb": limit_gb,
            "traffic_percent_used": round((used_gb / limit_gb) * 100 if limit_gb > 0 else 0, 2),
            "active_peers_count": peer_count # Заглушка
        }