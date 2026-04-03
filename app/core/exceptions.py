class ProxyException(Exception):
    pass


class UpstreamServiceError(ProxyException):
    def __init__(self, status_code: int, message: str = "Upstream error"):
        self.status_code = status_code
        self.message = message


class UpstreamTimeoutError(ProxyException):
    def __init__(self, message: str = "Upstream timeout"):
        self.message = message


class InvalidResponseError(ProxyException):
    def __init__(self, message: str = "Invalid response format"):
        self.message = message