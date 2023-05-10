import asyncio

async def aiter(it):
    for _ in it: await asyncio.sleep(0) ; yield _

async def arange(*args, **kwargs) -> int:
    for _ in range(*args, **kwargs): await asyncio.sleep(0) ; yield _
