# app/application/proxy/use_cases/forward_proxy_request.py

from dataclasses import dataclass

from app.domain.ports.remote_resource_port import (
    RemoteResourcePort,
)

from app.application.proxy.dtos.response_dto import (
    ProxyResponseDTO,
)

from app.application.caching.use_cases.get_or_set_cache import (
    GetOrSetCacheUseCase,
)


@dataclass
class ForwardProxyRequestUseCase:

    remote_resource: RemoteResourcePort
    cache_use_case: GetOrSetCacheUseCase

    async def execute(
        self,
        url: str,
        ttl: int = 60,
    ) -> ProxyResponseDTO:

        result = await self.cache_use_case.execute(
            key=url,
            ttl_seconds=ttl,
            supplier=lambda: self.remote_resource.fetch(url),
        )

        return ProxyResponseDTO(
            data=result.value,
            from_cache=result.from_cache,
        )