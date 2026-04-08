from fastapi import FastAPI
from app.interfaces.api.router import api_router
from app.interfaces.middleware.rate_limiter import RateLimiterMiddleware

app = FastAPI(title="Proxy Server")

# Middleware
app.add_middleware(RateLimiterMiddleware)

# Include routers
app.include_router(api_router)