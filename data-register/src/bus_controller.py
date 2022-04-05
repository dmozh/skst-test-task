from asyncio import sleep
from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from aio_pika.abc import AbstractQueue, AbstractChannel
from json import loads

from settings import settings
from logger import log


class BusReceiverController:
    def __init__(self):
        self.__connection = None
        self.__queue = None
        self.__channel = None

        self.dsn = f"amqp://{settings.rabbit_user}:{settings.rabbit_pwd}@{settings.rabbit_host}/"

    @property
    def connection(self):
        return self.__connection

    async def set_connection(self):
        retry = True
        inq = 0
        if self.__connection:
            return self.connection()
        else:
            while retry and inq < 5:
                try:
                    log.info(f"Try connect to rabbit: host={settings.rabbit_host}, user={settings.rabbit_user}")
                    self.__connection = await connect(self.dsn)
                except Exception as e:
                    log.error("Connection error. Retry via 5 seconds")
                    await sleep(5)
                    inq += 1
                else:
                    log.info(f"Connection successful")
                    retry = False
                    return self.__connection
            else:
                return None

    async def consume(self, queue, callbacks: list):
        # Creating channel
        channel: AbstractChannel = await self.connection.channel()

        # Declaring queue
        queue: AbstractQueue = await channel.declare_queue(
            queue,
            auto_delete=True
        )

        async with queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            async for message in queue_iter:
                message: AbstractIncomingMessage
                async with message.process():
                    for callback in callbacks:
                        await callback(message.body)

    async def __aenter__(self):
        connection = await self.set_connection()
        if connection:
            return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        log.info(f"Close connection")
        await self.__connection.close()
