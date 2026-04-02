from fastapi import FastAPI
from app.api.router import api_router
from app.middleware.rate_limiter import RateLimiterMiddleware

app = FastAPI(title="Proxy Server")

# Aggiunto il middleware per il rate limiting
app.add_middleware(RateLimiterMiddleware)

app.include_router(api_router)