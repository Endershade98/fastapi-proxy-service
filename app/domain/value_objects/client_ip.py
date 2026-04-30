# app/domain/value_objects/client_ip.py
import ipaddress

class ClientIP:
    def __init__(self, ip: str):
        try:
            self._ip = ipaddress.ip_address(ip)
        except ValueError:
            raise ValueError(f"Invalid IP address: {ip}")

    @property
    def value(self) -> str:
        return str(self._ip)

    def __str__(self):
        return self.value