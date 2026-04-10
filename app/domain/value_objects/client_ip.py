# app/domain/value_objects/client_ip.py
import ipaddress


class ClientIP:
    def __init__(self, ip: str):
        try:
            self._ip = str(ipaddress.ip_address(ip))
        except ValueError:
            raise ValueError("Invalid IP address")

    @property
    def value(self) -> str:
        return self._ip

    def __str__(self):
        return self._ip