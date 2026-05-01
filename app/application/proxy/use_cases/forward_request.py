# app/application/proxy/use_cases/forward_request.py

class ForwardRequestUseCase:

    def __init__(self, cache_manager, http_client):
        self.cache = cache_manager
        self.http = http_client

    async def execute(self, url: str):

        async def supplier():
            return await self.http.fetch(url)

        result = await self.cache.get_or_set(
            key=url,
            value_supplier=supplier,
            ttl=60
        )

        return result