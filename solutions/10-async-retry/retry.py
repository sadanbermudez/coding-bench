import asyncio
import functools


def retry(attempts=3, base_delay=0.5, factor=2.0, retry_on=(Exception,), sleep=asyncio.sleep):
    if attempts < 1:
        raise ValueError(attempts)

    def deco(fn):
        @functools.wraps(fn)
        async def wrapper(*a, **kw):
            for n in range(1, attempts + 1):
                try:
                    return await fn(*a, **kw)
                except retry_on:
                    if n == attempts:
                        raise
                    await sleep(base_delay * factor ** (n - 1))
        return wrapper
    return deco
