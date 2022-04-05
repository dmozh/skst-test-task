from pydantic import BaseModel


class Ticker(BaseModel):
    product: str
    changed_dt: str
    price: int
    old_price: int
    price_trend: int
