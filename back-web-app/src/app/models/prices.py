from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class PricesModel(BaseModel):
    id: UUID4
    product: str
    changed_dt: datetime
    price: int
    price_trend: int

    class Config:
        orm_mode = True
