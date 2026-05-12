# tests/unit/interfaces/api/test_proxy_schema.py

from app.interfaces.api.schemas.proxy import ProxyPayloadSchema


def test_proxy_payload_schema_conversion():

    schema = ProxyPayloadSchema(
        url="https://example.com",
        ttl=30
    )

    dto = schema.to_dto()

    assert dto.url == "https://example.com"
    assert dto.ttl == 30