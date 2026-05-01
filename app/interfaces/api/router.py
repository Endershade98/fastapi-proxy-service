# app/interfaces/api/router.py

from fastapi import APIRouter
from app.interfaces.api.routes import proxy

api_router = APIRouter()

# REGISTER ROUTES
api_router.include_router(proxy.router, prefix="/proxy", tags=["proxy"])