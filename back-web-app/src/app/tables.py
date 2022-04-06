from sqlalchemy import Column, Integer, DateTime, VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class Prices(DeclarativeBase):
    __tablename__ = 'prices'

    id = Column(UUID, primary_key=True, nullable=False)
    product = Column(VARCHAR(30))
    changed_dt = Column(DateTime)
    price = Column(Integer)
    price_trend = Column(Integer)
    old_price = Column(Integer)
