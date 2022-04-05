from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID, INTEGER, VARCHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class Prices(DeclarativeBase):
    __tablename__ = 'prices'

    id = Column(UUID, primary_key=True, nullable=False)
    product = Column(VARCHAR(30))
    changed_dt = Column(TIMESTAMP)
    price = Column(INTEGER)
    old_price = Column(INTEGER)
    price_trend = Column(INTEGER)


class PricesHistory(DeclarativeBase):
    __tablename__ = 'prices_history'

    id = Column(UUID, primary_key=True, nullable=False)
    product = Column(VARCHAR(30))
    changed_dt = Column(TIMESTAMP)
    price = Column(INTEGER)
    old_price = Column(INTEGER)
    price_trend = Column(INTEGER)
