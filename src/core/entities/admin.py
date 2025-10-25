from datetime import datetime


class Admin:
    """Права администратора"""
    def __init__(
        self,
        user_id: int,
        # role: str,  # "superadmin", "support"
        # permissions: list[str],  # ["manage_users", "view_payments"]
        # created_at: datetime
    ):
        self.user_id = user_id
        # self.role = role
        # self.permissions = permissions
        # self.created_at = created_at