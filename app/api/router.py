from fastapi import APIRouter
from app.api.routes import proxy

api_router = APIRouter()
api_router.include_router(proxy.router, prefix="/proxy", tags=["proxy"])