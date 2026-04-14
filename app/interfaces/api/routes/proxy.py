# app/interfaces/api/routes/proxy.py
from fastapi import APIRouter, Depends, HTTPException
from app.application.proxy.use_cases.forward_request import ForwardRequestUseCase
from app.core.dependencies import get_forward_request_use_case

router = APIRouter()


async def fetch_from_upstream(url: str) -> dict:
    return {"url": url, "data": "upstream response"}


@router.post("/")
async def proxy_endpoint(
    payload: dict,
    use_case: ForwardRequestUseCase = Depends(get_forward_request_use_case)
):

    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Missing 'url'")

    result = await use_case.execute(url)

    return {
        "data": result.value,
        "cached": result.from_cache
    }