# app/interfaces/api/schemas/proxy.py

from pydantic import BaseModel, HttpUrl
from app.application.proxy.dtos.request_dto import ProxyRequestDTO
from app.application.proxy.dtos.response_dto import ProxyResponseDTO


class ProxyPayloadSchema(BaseModel):
    url: HttpUrl
    ttl: int = 60

    def to_dto(self) -> ProxyRequestDTO:
        return ProxyRequestDTO(
            url=str(self.url),
            ttl=self.ttl
        )


class ProxyResponseSchema(BaseModel):
    data: dict
    cached: bool

    @classmethod
    def from_result(cls, result: ProxyResponseDTO):
        return cls(
            data=result.data,
            cached=result.cached
        )