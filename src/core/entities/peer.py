class Peer:
    """VPN-конфигурация пользователя ( peer = узел в сети)"""
    def __init__(
        self,
        pub_key: str,
        user_id: int,
        server_id: str,
        public_key: str
        # config_data: str  # Содержимое конфига (например, .ovpn)
    ):
        self.pub_key = pub_key
        self.user_id = user_id
        self.server_id = server_id
        # self.config_data = config_data
        self.public_key = public_key