# app/interfaces/api/routes/proxy.py

from fastapi import APIRouter, Depends

from app.bootstrap.container import get_forward_proxy_use_case
from app.application.proxy.use_cases.forward_proxy_request import ForwardProxyRequestUseCase

from app.interfaces.api.schemas.proxy import (
    ProxyPayloadSchema,
    ProxyResponseSchema
)

router = APIRouter()


@router.post("/", response_model=ProxyResponseSchema)
async def proxy_endpoint(
    payload: ProxyPayloadSchema,
    use_case: ForwardProxyRequestUseCase = Depends(get_forward_proxy_use_case),
):
    result = await use_case.execute(
        url=str(payload.url),
        ttl=payload.ttl
    )

    return ProxyResponseSchema.from_result(result)