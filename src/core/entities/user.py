from datetime import datetime

class User:
    """Информация о пользователе Telegram"""
    def __init__(
        self,
        id: int,
        first_name: str,
        username: str = None,
        created_at: datetime = None,
        is_blocked: bool = False
    ):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.created_at = created_at or datetime.now()
        self.is_blocked = is_blocked