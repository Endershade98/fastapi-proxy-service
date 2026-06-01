# app/interfaces/api/schemas/proxy.py

from pydantic import BaseModel, HttpUrl
from typing import Any

from pydantic import (
    BaseModel,
    HttpUrl,
    Field,
)


class ProxyPayloadSchema(BaseModel):

    url: HttpUrl

    ttl: int = Field(
        default=60,
        gt=0,
        le=86400,
    )

class ProxyResponseSchema(BaseModel):
    data: Any
    from_cache: bool

    @classmethod
    def from_result(cls, result):
        return cls(
            data=result.data,
            from_cache=result.from_cache
        )