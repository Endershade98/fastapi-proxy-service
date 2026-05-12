# app/interfaces/api/routes/proxy.py

from fastapi import APIRouter, Depends

from app.interfaces.api.schemas.proxy import ProxyPayloadSchema, ProxyResponseSchema
from app.application.proxy.use_cases.forward_request import ForwardRequestUseCase
from app.bootstrap.container import get_forward_request_use_case

router = APIRouter()


@router.post("/", response_model=ProxyResponseSchema)
async def proxy_endpoint(
    payload: ProxyPayloadSchema,
    use_case: ForwardRequestUseCase = Depends(get_forward_request_use_case),
):
    """
    Thin controller:
    - No validation logic
    - No DTO mapping logic
    - No response shaping logic
    """

    result = await use_case.execute(payload.to_dto())

    return ProxyResponseSchema.from_result(result)