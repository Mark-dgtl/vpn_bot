# src/core/exceptions.py

class VPNServiceError(Exception):
    """Базовое исключение для VPN-сервиса"""
    pass

class UserNotFoundError(VPNServiceError):
    """Пользователь не найден"""
    pass

class SubscriptionExpiredError(VPNServiceError):
    """Подписка истекла или не активна"""
    pass

class DeviceLimitExceededError(VPNServiceError):
    """Превышен лимит подключенных устройел"""
    pass

class ServerUnavailableError(VPNServiceError):
    """Сервер недоступен или не найден"""
    pass

class PeerNotFoundError(VPNServiceError):
    """Peer (конфигурация) не найден"""
    pass

class PlanNotFoundError(VPNServiceError):
    """Тарифный план не найден"""
    pass

class PaymentRequiredError(VPNServiceError):
    """Требуется оплата"""
    pass

class OrderNotFoundError(VPNServiceError):
    """Заказ не найден"""
    pass

class PaymentProcessingError(VPNServiceError):
    """Ошибка обработки платежа"""
    pass

class ReferralCodeInvalidError(VPNServiceError):
    """Реферальный код недействителен"""
    pass

class TrafficLimitExceededError(VPNServiceError):
    """Превышен лимит трафика"""
    pass

class AdminPermissionError(VPNServiceError):
    """Недостаточно прав администратора"""
    pass

class SessionNotFoundError(VPNServiceError):
    """Сессия подключения не найдена"""
    pass

class TrafficUsageError(VPNServiceError):
    """Ошибка учета трафика"""
    pass

class InvalidInputError(VPNServiceError):
    """Неверные входные данные"""
    pass