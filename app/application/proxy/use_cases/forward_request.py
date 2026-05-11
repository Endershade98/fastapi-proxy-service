# app/application/proxy/use_cases/forward_request.py

from app.application.proxy.dtos.request_dto import ProxyRequestDTO
from app.application.proxy.dtos.response_dto import ProxyResponseDTO
from app.application.proxy.use_cases.cache_management import (
    GetOrSetCacheUseCase
)
from app.domain.ports.remote_resource_port import RemoteResourcePort


class ForwardRequestUseCase:

    def __init__(
        self,
        cache_use_case: GetOrSetCacheUseCase,
        remote_resource: RemoteResourcePort
    ):
        self._cache = cache_use_case
        self._remote = remote_resource

    async def execute(
        self,
        request: ProxyRequestDTO
    ) -> ProxyResponseDTO:

        async def supplier():
            return await self._remote.fetch(request.url)

        result = await self._cache.execute(
            key=request.url,
            supplier=supplier,
            ttl_seconds=request.ttl_seconds
        )

        return ProxyResponseDTO(
            data=result.value,
            from_cache=result.from_cache
        )