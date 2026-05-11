# app/bootstrap/dummies.py

class DummyRateLimiter:
    async def increment(self, key: str, window: int):
        return 0


class DummyLogger:
    async def log(self, event):
        pass