import redis.asyncio as redis
from asyncio import sleep

from .settings import settings
from .logger import log


class ReceiverController:
    def __init__(self, channel):
        self.connection = None
        self.pubsub = None
        self.channel = channel

    async def __aenter__(self):
        _try = 1
        retry = True
        # trying connect to publisher
        while _try <= 5 and retry:
            try:
                log.info(f"Try {_try} to connect redis://{settings.pipe_host}:{settings.pipe_port}")
                self.connection = await redis.from_url(f"redis://{settings.pipe_host}:{settings.pipe_port}")
            except Exception as e:
                log.error(f'Error - {e}. Wait 5 secs')
                await sleep(5)
            else:
                retry = False

        if self.connection is not None:
            self.pubsub = self.connection.pubsub()
            await self.pubsub.psubscribe(self.channel)
            return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()
