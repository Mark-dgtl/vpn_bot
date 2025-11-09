from typing import Optional, List
from src.core.entities import Peer, Server
from src.core.exceptions import (
    UserNotFoundError,
    SubscriptionExpiredError,
    # DeviceLimitExceededError,
    ServerUnavailableError
)
from src.core.exceptions import PeerNotFoundError, UserNotFoundError
from src.core.repositories import UserRepo, SubscriptionRepo, PeerRepo, ServerRepo
from src.core.entities import Peer

class PeerUseCases:
    pass

class CreateVPNPeerUseCase:
    def __init__(
            self,
            user_repo: UserRepo,
            subscription_repo: SubscriptionRepo,
            peer_repo: PeerRepo,
            server_repo: ServerRepo
    ):
        self.user_repo = user_repo
        self.subscription_repo = subscription_repo
        self.peer_repo = peer_repo
        self.server_repo = server_repo

    def execute(self, user_id: int, server_ip: Optional[str] = None) -> Peer:
        # 1. Проверяем существование пользователя
        user = self.user_repo.find_by_user_id(user_id)
        if not user:
            raise UserNotFoundError(f"Пользователь {user_id} не найден")

        # 2. Проверяем активную подписку
        subscription = self.subscription_repo.find_active_by_user(user_id)
        if not subscription or subscription.status != "active":
            raise SubscriptionExpiredError("Подписка не активна")

        # 4. Выбираем сервер
        if server_ip:
            server = self.server_repo.find_by_ip(server_ip)
        else:
            servers = self.server_repo.get_available_servers()
            server = servers[0] if servers else None

        if not server or server.status != "online":
            raise ServerUnavailableError("Нет доступных серверов")

        # # 5. Генерируем конфиг
        # config_data = self.peer_repo(user, server_ip, subscription)

        # 6. Сохраняем peer
        peer = Peer(
            user_id=user_id,
            server_ip=server_ip,
            # config_data=config_data
        )
        return self.peer_repo.create(peer)


    # def _generate_config(self, user: User, server: Server, sub: Subscription) -> str:
    #     """Генерация конфига в формате WireGuard/OpenVPN"""
    #     # Здесь реальная логика генерации конфига
    #     return f"""
    #     # Конфиг для {user.username}
    #     [Interface]
    #     PrivateKey = {self._generate_private_key()}
    #     Address = 10.0.0.{user.chat_id}/24
    #     DNS = {server.dns}
    #
    #     [Peer]
    #     PublicKey = {server.public_key}
    #     Endpoint = {server.ip_address}:{server.port}
    #     AllowedIPs = 0.0.0.0/0
    #     """
    #
    # def _generate_private_key(self) -> str:
    #     # Реализация генерации ключа
    #     return "GENERATED_PRIVATE_KEY"


class RevokePeerUseCase:
    def __init__(self, peer_repo: PeerRepo):
        self.peer_repo = peer_repo

    def execute(self, pub_key: str) -> None:
        # 1. Проверяем существование peer
        peer = self.peer_repo.find_by_pub_key(pub_key)
        if not peer:
            raise PeerNotFoundError(f"Peer {pub_key} не найден")

        # 2. Отзываем конфигурацию
        self.peer_repo.revoke(pub_key)


class FreezePeerUseCase:
    def __init__(self, peer_repo: PeerRepo):
        self.peer_repo = peer_repo

    def execute(self, pub_key: str) -> None:
        # 1. Проверяем активные peer'ы
        peer = self.peer_repo.find_by_pub_key(pub_key)
        if not peer:
            return PeerNotFoundError

        return self.peer_repo.freeze(pub_key)



class ListPeersUseCase:
    def __init__(self, peer_repo: PeerRepo, user_repo: UserRepo):
        self.peer_repo = peer_repo
        self.user_repo = user_repo

    def execute(self, user_id: int) -> List[Peer]:
        # 1. Проверяем существование пользователя
        user = self.user_repo.get_by_user_id(user_id)
        if not user:
            raise UserNotFoundError(f"Пользователь {user_id} не найден")

        # 2. Получаем список peer'ов пользователя
        peers = self.peer_repo.find_by_user(user_id)
        return peers
