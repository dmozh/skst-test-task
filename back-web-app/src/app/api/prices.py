from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import Depends

from typing import Optional, List
from datetime import datetime

from ..services import PriceService
from ..models import PricesModel, TickersModel
from ..logger import log

router = APIRouter(
    prefix="/api/prices"
)


@router.get('/tickers', response_model=TickersModel)
async def get_tickers(
        service: PriceService = Depends()
):
    return await service.get_tickers()


@router.get('/{product}', response_model=List[PricesModel])
async def get_history_product(
        limit: Optional[int] = 600,
        product: Optional[str] = None,
        start_dt: Optional[datetime] = None,
        end_dt: Optional[datetime] = None,
        service: PriceService = Depends(),
):
    if start_dt is None:
        start_dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if end_dt is None:
        end_dt = datetime.now().replace(microsecond=0)
    print(start_dt, end_dt)

    return await service.get_product_history(product, start_dt, end_dt, limit)


@router.get('/', response_model=List[PricesModel])
async def get_history_all_products(
        limit: Optional[int] = 600,
        start_dt: Optional[datetime] = None,
        end_dt: Optional[datetime] = None,
        service: PriceService = Depends(),
):
    if start_dt is None:
        start_dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if end_dt is None:
        end_dt = datetime.now().replace(microsecond=0)
    print(start_dt, end_dt)

    return await service.get_all_prices('123')


# @app.websocket('/prices/ws')
async def websocket(
        websocket: WebSocket,
        product: Optional[str],
        service: PriceService = Depends()

):
    await service.send_real_time_price(websocket, product)
