# app/interfaces/api/schemas/proxy.py

from pydantic import BaseModel, HttpUrl


class ProxyPayloadSchema(BaseModel):
    url: HttpUrl
    ttl: int = 60