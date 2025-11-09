from dataclasses import dataclass

@dataclass
class UserRegistrationData:
    telegram_id: int
    username: str | None
    first_name: str
    referral_code: str | None