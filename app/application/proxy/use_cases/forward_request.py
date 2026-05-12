# app/application/proxy/use_cases/forward_request.py

from app.application.proxy.dtos.request_dto import ProxyRequestDTO
from app.application.proxy.dtos.response_dto import ProxyResponseDTO
from app.domain.ports.remote_resource_port import RemoteResourcePort
from app.domain.ports.cache_port import CachePort


class ForwardRequestUseCase:

    def __init__(
        self,
        remote_resource: RemoteResourcePort,
        cache: CachePort
    ):
        self.remote_resource = remote_resource
        self.cache = cache

    async def execute(self, dto: ProxyRequestDTO) -> ProxyResponseDTO:
        cached = await self.cache.get(dto.url)

        if cached:
            return ProxyResponseDTO(data=cached, cached=True)

        data = await self.remote_resource.fetch(dto.url)

        await self.cache.set(dto.url, data, ttl=dto.ttl)

        return ProxyResponseDTO(data=data, cached=False)