# app/application/proxy/use_cases/forward_proxy_request.py

from dataclasses import dataclass

from app.application.caching.use_cases.get_or_set_cache import (
    GetOrSetCacheUseCase,
)
from app.application.proxy.dtos.request_dto import ProxyRequestDTO
from app.application.proxy.dtos.response_dto import ProxyResponseDTO
from app.application.ports.remote_resource import RemoteResourcePort


@dataclass
class ForwardProxyRequestUseCase:
    remote_resource: RemoteResourcePort
    cache_use_case: GetOrSetCacheUseCase

    async def execute(
        self,
        request: ProxyRequestDTO,
    ) -> ProxyResponseDTO:

        result = await self.cache_use_case.execute(
            key=request.url,
            ttl_seconds=request.ttl_seconds,
            supplier=lambda: self.remote_resource.fetch(
                request.url
            ),
        )

        return ProxyResponseDTO(
            url=request.url,
            data=result.value,
            from_cache=result.from_cache,
        )