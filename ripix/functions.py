import asyncio
from functools import partial

async def aiter(it):
    for item in it:
        yield item
        asyncio.sleep(0)

async def arange(*args, **kwargs) -> int:
    for i in range(*args, **kwargs):
        yield i
        asyncio.sleep(0)

async def run_in_executor(loop, executor, func, *args, **kwargs):
    if loop is None: loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, partial(func, *args, **kwargs))

def wrapper_run_in_executor(loop, executor, func):
    async def wrapped_func(*args, **kwargs):
        return await run_in_executor(loop, executor, func, *args, **kwargs)
    return wrapped_func