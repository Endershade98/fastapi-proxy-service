from fastapi import APIRouter
from app.schemas.proxy import ProxyRequest
from app.services.proxy_service import ProxyService

router = APIRouter()
service = ProxyService()

@router.post("/")
async def proxy_endpoint(request: ProxyRequest):
    return await service.forward_request(str(request.url))