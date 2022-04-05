import redis.asyncio as redis
from asyncio import sleep

from .settings import settings
from .logger import log


class CacheController:
    def __init__(self):
        self.connection = None

    async def get(self, key):
        try:
            log.info(f"Try get value for key: {key}")
            return await self.connection.get(key)
        except Exception as e:
            log.error(f"Error - {e}")

    async def set(self, key, value):
        try:
            log.info(f"Try set key:value = {key}:{value}")
            await self.connection.set(key, value)
        except Exception as e:
            log.error(f"Error - {e}")

    async def __aenter__(self):
        _try = 1
        retry = True
        # trying connect to cache
        while _try <= 5 and retry:
            try:
                log.info(f"Try {_try} to connect redis://{settings.cache_host}:{settings.cache_port}")
                self.connection = await redis.from_url(f"redis://{settings.cache_host}:{settings.cache_port}")
            except Exception as e:
                log.error(f'Error - {e}. Wait 5 secs')
                await sleep(5)
            else:
                retry = False
        if self.connection is not None:
            return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()
