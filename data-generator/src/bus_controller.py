from asyncio import sleep

from aio_pika import connect, Message
from aio_pika.abc import AbstractQueue, AbstractChannel

from settings import settings
from logger import log


class BusSenderController:
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
                    log.debug(f"Try connect to rabbit: host={settings.rabbit_host}, user={settings.rabbit_user}")
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

    async def publish(self, body: str, queue: str):
        # Creating channel
        if self.__channel is None:
            self.__channel: AbstractChannel = await self.connection.channel()

        # Declaring queue
        if queue:
            self.__queue: AbstractQueue = await self.__channel.declare_queue(
                queue,
                auto_delete=True
            )
        log.debug(f"Publish msg in {queue}")
        try:
            await self.__channel.default_exchange.publish(
                Message(body=body.encode('utf-8')
                        ),
                routing_key=queue
            )
        except Exception as e:
            log.error(f"Error - {e}")

    async def __aenter__(self):
        connection = await self.set_connection()
        if connection:
            return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        log.info(f"Close connection")
        await self.__connection.close()
