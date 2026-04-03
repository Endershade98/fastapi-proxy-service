from fastapi import APIRouter, HTTPException
from app.schemas.proxy import ProxyRequest
from app.services.proxy_service import ProxyService
from app.core.logging import LoggerConfig

logger = LoggerConfig.get_logger(__name__)
router = APIRouter()
service = ProxyService()


@router.post("/")
async def proxy_endpoint(request: ProxyRequest):
    logger.info(f"Proxy request: {request.url}")
    result = await service.forward_request(str(request.url))

    if "error" in result:
        logger.error(f"Proxy error: {result['error']}")
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"]
        )
    
    logger.info(f"Proxy response: {result}")
    return result