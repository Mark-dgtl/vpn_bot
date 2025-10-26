class Peer:
    """VPN-конфигурация пользователя ( peer = узел в сети)"""
    def __init__(
        self,
        # peer_id: str,
        user_id: int,
        server_id: str,
        config_data: str  # Содержимое конфига (например, .ovpn)
    ):
        # self.peer_id = peer_id
        self.user_id = user_id
        self.server_id = server_id
        self.config_data = config_data