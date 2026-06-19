import asyncio
from contextlib import asynccontextmanager, suppress


@asynccontextmanager
async def lock_by(key):
    try:
        lock = LOCK_BY_KEY[key]
    except KeyError:
        LOCK_BY_KEY[key] = lock = asyncio.Lock()
    async with lock:
        yield
    with suppress(KeyError):
        del LOCK_BY_KEY[key]


LOCK_BY_KEY = {}
