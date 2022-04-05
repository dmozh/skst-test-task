import asyncio
import redis.client
from datetime import datetime

from asyncio import sleep
from async_timeout import timeout

from fastapi import WebSocket

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, between, desc

from typing import List, Optional

from ..models import PricesModel
from ..logger import log
from ..receiver import ReceiverController
from ..database import controller
from ..tables import Prices, PricesHistory

ALL_TICKERS_RECEIVE_CHANNEL = 'channel_all_tickers'


class PriceService:
    def __init__(self):
        self.session = None

    async def get_product_history(self,
                                  product: str,
                                  start_dt: datetime,
                                  end_dt: datetime,
                                  limit=3600
            ) -> List[Prices]:
        self.session = next(controller.get_session())
        async with self.session() as session:
            session: AsyncSession
            query = select(Prices).\
                where(Prices.product == product).\
                filter(Prices.changed_dt.between(start_dt, end_dt)).\
                limit(limit).\
                order_by(desc(Prices.changed_dt))
            result = await session.execute(query)
            response = [_[0] for _ in result.all()]
            return response
        # return []

    async def send_real_time_price(self, websocket: WebSocket, channel_name: str = None):
        await websocket.accept()
        __chanel_name = f"channel_{channel_name}" if channel_name is not None else ALL_TICKERS_RECEIVE_CHANNEL

        async def receive(channel: redis.client.PubSub):
            log.info(f"Start to receive msgs from {__chanel_name}")
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
