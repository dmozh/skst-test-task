import redis.asyncio as redis
from asyncio import sleep

from settings import settings
from logger import log
from typing import Optional


class PublisherController:
    def __init__(self, channel: str):
        """
        Constructor for publisher controller
        :param channel: Main channel
        """
        self.connection = None
        self.pubsub = None
        self.channel = channel

    async def publish(self, data: str, channel: Optional[str] = None):
        """
        Wrap function on publish method
        :param data:
        :param channel: queue str
        :return:
        """
        log.debug(f"Publishing in queue {channel} data {data}")
        try:
            if channel:
                _channel = channel
            else:
                _channel = self.channel
            await self.connection.publish(_channel, data)
        except Exception as e:
            log.error(f"Error - {e}")

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
            log.info(f"Success to connect redis://{settings.pipe_host}:{settings.pipe_port}")
            self.pubsub = self.connection.pubsub()
            await self.pubsub.psubscribe(self.channel)
            return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()
