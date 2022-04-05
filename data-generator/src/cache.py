import redis.asyncio as redis
import redis as sync_cache
from time import sleep as s_sleep

from asyncio import sleep

from settings import settings
from logger import log


class CacheController:
    def __init__(self):
        self.connection = None

    async def get(self, key):
        log.debug(f"Try get value for key: {key}")
        try:
            log.debug(f"Try get value for key: {key}")
            res = await self.connection.get(key)
            if res:
                return res.decode('utf-8')
            else:
                return
        except Exception as e:
            log.debug(f"{self.connection}")
            log.error(f"Error - {e}")
        finally:
            log.debug(f"Success get value for key: {key}")

    async def set(self, key, value):
        try:
            log.debug(f"Try set key:value = {key}:{value}")
            await self.connection.set(key, value)
        except Exception as e:
            log.error(f"Error - {e}")
        finally:
            log.debug(f"Success set value for key: {key}")

    async def mset(self, mapping):
        try:
            log.debug(f"Try mset key:value = {mapping}")
            await self.connection.mset(mapping)
        except Exception as e:
            log.error(f"Error - {e}")
        finally:
            log.debug(f"Success mset value for key: {mapping}")

    async def mget(self, mapping: list):
        try:
            log.debug(f"Try mget key:value = {mapping}")
            res = await self.connection.mget(mapping)
            if res:
                return [elem.decode('utf-8') for elem in res]
        except Exception as e:
            log.error(f"Error - {e}")
        finally:
            log.debug(f"Success mget value for key: {res}")

    async def __aenter__(self):
        """
        Async context mngs for caching
        :return:
        """
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
            log.info(f"Success to connect redis://{settings.cache_host}:{settings.cache_port}")
            return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()
