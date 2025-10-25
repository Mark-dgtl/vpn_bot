from datetime import datetime

class Server:
    """Информация о VPN-сервере"""
    def __init__(
        self,
        server_id: str,
        location: str,  # "US East", "DE Frankfurt"
        ip_address: str,
        port: int,
        status: str,  # "online", "offline", "maintenance"
        load_percent: int,
        created_at: datetime = None
    ):
        self.server_id = server_id
        self.location = location
        self.ip_address = ip_address
        self.port = port
        self.status = status
        self.load_percent = load_percent
        self.created_at = created_at or datetime.now()