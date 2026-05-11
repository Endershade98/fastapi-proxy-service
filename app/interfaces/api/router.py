# app/interfaces/api/router.py

from fastapi import APIRouter
from app.interfaces.api.routes import proxy
from app.interfaces.api.routes import tasks

router = APIRouter()

# REGISTER ROUTES
router.include_router(proxy.router, prefix="/proxy", tags=["proxy"])
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])