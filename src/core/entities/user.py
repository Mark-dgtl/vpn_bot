from datetime import datetime

class User:
    """Информация о пользователе Telegram"""
    def __init__(
        self,
        id: int,
        username: str = None,
        created_at: datetime = None,
        is_blocked: bool = False
    ):
        self.id = id
        self.username = username
        self.created_at = created_at or datetime.now()
        self.is_blocked = is_blocked