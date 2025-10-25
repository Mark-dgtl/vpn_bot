from datetime import datetime

class TrafficUsage:
    """Учет трафика пользователя"""
    def __init__(
        self,
        user_id: int,
        total_used_bytes: int,
        reset_date: datetime,
        last_updated: datetime
    ):
        self.user_id = user_id
        self.total_used_bytes = total_used_bytes
        self.reset_date = reset_date
        self.last_updated = last_updated