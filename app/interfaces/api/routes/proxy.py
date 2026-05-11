# app/interfaces/api/routes/proxy.py

from fastapi import APIRouter, Depends, HTTPException

from app.bootstrap.container import get_forward_request_use_case
from app.application.proxy.use_cases.forward_request import ForwardRequestUseCase
from app.application.proxy.dtos.request_dto import ProxyRequestDTO
from app.interfaces.api.schemas.proxy import ProxyPayloadSchema

router = APIRouter()


@router.post("/")
async def proxy_endpoint(
    payload: ProxyPayloadSchema,
    use_case: ForwardRequestUseCase = Depends(get_forward_request_use_case),
):
    if not payload.url:
        raise HTTPException(status_code=400, detail="Missing url")

    request_dto = ProxyRequestDTO(
        url=payload.url,
        ttl=payload.ttl,
    )

    result = await use_case.execute(request_dto)

    return {
        "data": result.data,
        "cached": result.cached,
    }