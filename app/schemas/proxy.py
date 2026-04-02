from pydantic import BaseModel, HttpUrl

class ProxyRequest(BaseModel):
    url: HttpUrl

class ProxyResponse(BaseModel):
    status_code: int
    data: dict