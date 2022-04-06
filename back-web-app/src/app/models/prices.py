from pydantic import BaseModel, UUID4
from typing import List
from datetime import datetime


class TickersModel(BaseModel):
    products: List[str]

    class Config:
        orm_mode = True


class PricesModel(BaseModel):
    id: UUID4
    product: str
    changed_dt: datetime
    price: int
    price_trend: int
    old_price: int

    class Config:
        orm_mode = True
