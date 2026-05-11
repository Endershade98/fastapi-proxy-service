# app/application/proxy/use_cases/forward_request.py

from app.application.proxy.dtos.request_dto import ProxyRequestDTO
from app.application.proxy.dtos.response_dto import ProxyResponseDTO
from app.domain.services.http_client_interface import HttpClientInterface


class ForwardRequestUseCase:

    def __init__(
        self,
        cache_use_case,
        http_client: HttpClientInterface
    ):
        self.cache = cache_use_case
        self.http = http_client

    async def execute(
        self,
        request: ProxyRequestDTO
    ) -> ProxyResponseDTO:

        async def supplier():
            return await self.http.fetch(request.url)

        result = await self.cache.get_or_set(
            key=request.url,
            value_supplier=supplier,
            ttl=request.ttl
        )

        return ProxyResponseDTO(
            data=result.value,
            cached=result.from_cache
        )