from datetime import datetime

class Notification:
    """Уведомления для пользователя"""
    def __init__(
        self,
        notification_id: str,
        user_id: int,
        message: str,
        sent_at: datetime,
        is_read: bool = False,
        priority: str = "low"  # "low", "medium", "high"
    ):
        self.notification_id = notification_id
        self.user_id = user_id
        self.message = message
        self.sent_at = sent_at
        self.is_read = is_read
        self.priority = priority