from uuid import uuid4
from json import dumps, loads
from sqlalchemy import insert
from datetime import datetime

from database import controller
from tables import Prices
from logger import log
from publisher import PublisherController


class PricesService:
    def __init__(self,
                 publisher_controller: PublisherController
                 ):

        self.__publisher = publisher_controller

    async def write_to_store(self, _package_data):
        """
        Method for writing datas in db
        :return: void
        """
        log.info(f"Callback write_to_store starting")
        insert_data = []

        datas = loads(_package_data.decode('utf-8'))
        log.debug(f"Package {datas}")
        for data in datas:
            _data = data
            _data["id"] = str(uuid4())
            _data['changed_dt'] = datetime.strptime(data['changed_dt'], "%Y-%m-%d %H:%M:%S")
            insert_data.append(
                _data
            )
        log.info(f"Insert data genned")
        log.debug(f"datas {insert_data}")
        session = next(controller.get_session())
        try:
            async with session.begin() as connection:
                await connection.execute(insert(Prices), insert_data)
        except Exception as e:
            log.error(f"Error - {e}")

    async def publish_data(self, _package_data):
        """
        Method for publishing data for all tickers in redis pubsub
        :return:
        """
        log.info(f"Callback publish_data starting")

        _ = loads(_package_data.decode('utf-8'))
        log.debug(f"Package {_}")
        try:
            for data in _:
                await self.__publisher.publish(channel=f"channel_{data['product']}", data=dumps(data))
            await self.__publisher.publish(data=dumps(_))
        except Exception as e:
            log.error(f"Error - {e}")