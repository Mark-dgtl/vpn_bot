from src.core.exceptions import ReferralCodeInvalidError
from src.core.repositories import NotificationRepo, SubscriptionRepo, ReferralRepo, UserRepo, TrafficUsageRepo
from datetime import datetime, timedelta
from src.core.entities import Notification

class ReferalUseCases:
    pass

class ApplyReferralCodeUseCase:
    def __init__(
            self,
            referral_repo: ReferralRepo,
            user_repo: UserRepo,
            traffic_repo: TrafficUsageRepo,
            subs_repo: SubscriptionRepo,
            notif_repo: NotificationRepo
    ):
        self.referral_repo = referral_repo
        self.user_repo = user_repo
        self.traffic_repo = traffic_repo
        self.subs_repo = subs_repo
        self.notif_repo = notif_repo

    def execute(self, user_id: int, code: str) -> float:
        # 1. Находим реферал
        referral = self.referral_repo.find_by_code(code)
        if not referral or referral.used:
            raise ReferralCodeInvalidError("Код недействителен")

        # 2. Проверяем что пользователь не сам себе реферер
        if referral.user_id == user_id:
            raise ReferralCodeInvalidError("Нельзя использовать свой код")

        # 3. Начисляем бонус
        subscription = self.subs_repo.get_by_user_id(user_id)
        self.referral_repo.update_date_end(subscription)
        # 4. Помечаем как использованный
        self.referral_repo.mark_as_used(referral.referral_id)

        message = "..."
        notification = Notification(
            user_id = user_id,
            message = message,
            sent_at = datetime.utcnow(),
            is_read = False,
            )
        return self.notif_repo.create(notification)