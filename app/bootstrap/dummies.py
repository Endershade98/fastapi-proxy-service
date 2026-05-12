# app/bootstrap/dummies.py

class DummyRateLimiter:
    async def is_allowed(self, key: str) -> bool:
        return True

    async def increment(self, key: str, window_seconds: int) -> int:
        return 0


class DummyLogger:
    async def log(self, event):
        pass