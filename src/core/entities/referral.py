from datetime import datetime

class Referral:
    """Система рефералов"""
    def __init__(
        self,
        referral_id: str,
        user_id: int,
        referrer_id: int,  # Кто пригласил
        code: str,
        created_at: datetime,
        used: bool = False,
    ):
        self.referral_id = referral_id
        self.user_id = user_id
        self.referrer_id = referrer_id
        self.code = code
        self.created_at = created_at
        self.used = used
