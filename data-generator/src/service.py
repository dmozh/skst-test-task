import sys

from random import random
from datetime import datetime
from json import dumps
from copy import deepcopy

from settings import settings
from logger import log
from cache import CacheController
from models import Ticker

__ticker_old_price = {}  # mem storage

# _T = namedtuple('Ticker', ('product', 'changed_dt', 'price', 'old_price', 'price_trend'))


def correcting_name(i):
    if i > 9:
        return str(i)
    else:
        return f"0{i}"


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


async def init_datas(cache_controller: CacheController):
    timestamp = str(datetime.now().replace(microsecond=0))
    returned = []
    for i in range(settings.tickers_num):
        name = f"ticker_{correcting_name(i)}"
        # s = await cache_controller.get(name)
        if await cache_controller.get(name):
            return None
        __ticker_old_price[name] = 0
        returned.append(Ticker(product=name, changed_dt=timestamp, price=0, old_price=0, price_trend=0).dict())
    await cache_controller.mset(__ticker_old_price)
    if returned:
        __ticker_old_price.clear()
        return dumps(returned)


async def generate_datas(cache_controller):
    log.info(f"Starting generate datas")
    _data_package = []
    _package_size = settings.tickers_num // settings.data_parts  # define _package_size

    timestamp = str(datetime.now().replace(microsecond=0))  # generate timestamp

    inq = 1
    _names = []
    log.info(f"Generate names and package for return")
    for i in range(settings.tickers_num):
        name = f"ticker_{correcting_name(i)}"  # gen name
        _names.append(name)
        if inq == _package_size:  # every "_package_size" count we generate 1 package
            try:
                old_prices = await cache_controller.mget(_names)  # getting old_prices for names
            except Exception as e:
                log.error(f'Error -  {e}')
                sys.exit(-1)
            log.info(f"Generate package for tickers {_names}")
            for idx, old_price in enumerate(old_prices):  # for every old price gen data
                log.debug(f"{idx} - {old_price}")
                trend = generate_movement()  # generate trend
                new_price = int(old_price) + trend  # define new price
                __ticker_old_price[_names[idx]] = new_price  # replace old price
                # gen data
                _data_package.append(Ticker(product=_names[idx],
                                            changed_dt=timestamp,
                                            price=new_price,
                                            old_price=old_price,
                                            price_trend=trend).dict()
                                     )
            log.info("Returned package")
            await cache_controller.mset(__ticker_old_price)  # set in cache
            yield dumps(_data_package)  # returned
            # clear
            log.info(f"Clear temp structures")
            _data_package.clear()
            _names.clear()
            inq = 1
        else:
            inq += 1
    else:
        log.info("Returned odds datas")
        if _data_package:
            await cache_controller.mset(__ticker_old_price)
            yield dumps(_data_package)
        else:
            if _names:
                log.info(f"Generate package for names {_names}")
                try:
                    old_prices = await cache_controller.mget(_names)  # getting old_prices for names
                except Exception as e:
                    log.error(f'Error -  {e}')
                    sys.exit(-1)
                for idx,old_price in enumerate(old_prices):
                    log.debug(f"{idx} - {old_price}")
                    trend = generate_movement()  # generate trend
                    new_price = int(old_price) + trend  # define new price
                    __ticker_old_price[_names[idx]] = new_price  # replace old price
                    _data_package.append(Ticker(product=_names[idx],
                                                changed_dt=timestamp,
                                                price=new_price,
                                                old_price=old_price,
                                                price_trend=trend).dict()
                                         )
                log.info("Returned package")
                await cache_controller.mset(__ticker_old_price)
                yield dumps(_data_package)
        _data_package.clear()
        _names.clear()