from fastapi import APIRouter

from .prices import router as prices_router
from .prices import websocket as ws_prices

router = APIRouter()
router.include_router(prices_router)
