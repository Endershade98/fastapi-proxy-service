import asyncio

def run_async(coro):
    return asyncio.get_event_loop().run_until_complete(coro)