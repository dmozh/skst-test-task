import asyncio
import redis.client
from datetime import datetime

from asyncio import sleep
from async_timeout import timeout

from fastapi import WebSocket

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, between, desc

from typing import List, Optional

from ..models import TickersModel
from ..logger import log
from ..receiver import ReceiverController
from ..database import controller
from ..tables import Prices

ALL_TICKERS_RECEIVE_CHANNEL = 'channel_all_tickers'


class PriceService:
    def __init__(self):
        self.session = None

    async def get_tickers(self) -> dict:
        """
        Функция на получение всех тикеров
        Получаю дистинктом из базы истории, потому что лень было делать отдельную таблицу в базе
        :return:
        """
        log.info(f"Getting tickers")
        self.session = next(controller.get_session())
        async with self.session() as session:
            session: AsyncSession
            query = select(Prices.product).distinct()
            log.debug(f'{query}')
            result = await session.execute(query)
            response = sorted([_[0] for _ in result.all()])
            log.debug(f"{response}")
            return {"products": response}

    async def get_product_history(self,
                                  product: str,
                                  start_dt: datetime,
                                  end_dt: datetime,
                                  limit: int
                                  ) -> List[Prices]:
        """
        Функция получения истории изменения цены
        :param product: тикер
        :param start_dt: начало
        :param end_dt: конец
        :param limit: лимит по строкам
        :return:
        """
        log.info(f"Getting price history for ticker {product} with params start dt {start_dt} end dt {end_dt} limit {limit}")
        self.session = next(controller.get_session())
        log.debug(f"{self.session}")
        async with self.session() as session:
            session: AsyncSession
            query = select(Prices). \
                where(Prices.product == product). \
                filter(Prices.changed_dt.between(start_dt, end_dt)). \
                limit(limit). \
                order_by(desc(Prices.changed_dt))
            log.debug(f"{query}")
            result = await session.execute(query)
            response = [_[0] for _ in result.all()]
            log.debug(f"{response}")
            return response
        # return []

    async def send_real_time_price(self, websocket: WebSocket, channel_name: str = None):
        """
        Функция обрабооки веб сокет роута
        Отправялет к подключенному сокету сообщения из бродкастера
        :param websocket:
        :param channel_name:
        :return:
        """
        await websocket.accept()
        __chanel_name = f"channel_{channel_name}" if channel_name is not None else ALL_TICKERS_RECEIVE_CHANNEL

        async def receive(channel: redis.client.PubSub):
            log.debug(f"Start to receive msgs from {__chanel_name}")
            while True:
                try:
                    async with timeout(1):
                        msg = await channel.get_message(ignore_subscribe_messages=True)
                        if msg is not None:
                            log.debug(f"{msg}")
                            await websocket.send_text(msg['data'].decode('utf-8'))
                        await sleep(0.01)
                except asyncio.TimeoutError as e:
                    log.error(f"Error for receive msgs - {e}")

        async with ReceiverController(channel=__chanel_name) as controller:
            future = asyncio.create_task(receive(controller.pubsub))
            await future
