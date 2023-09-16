from sqlalchemy import Column, Integer, String, Float
from .database import Base

class CurrencyExchangeRate(Base):
    __tablename__ = 'currency_exchange_rates'

    id = Column(Integer, primary_key=True)
    from_currency = Column(String)
    to_currency = Column(String)
    rate = Column(Float)
    # Add more fields if needed
