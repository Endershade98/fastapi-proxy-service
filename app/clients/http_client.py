import httpx
from app.core.config import settings

async def fetch(url: str):
    async with httpx.AsyncClient(timeout=settings.TIMEOUT) as client:
        response = await client.get(url)
        return response