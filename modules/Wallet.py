from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True)
    balance = Column(Float)
    currency = Column(String)
    
    # Define the one-to-one relationship with Users
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)  # Make it unique
    user = relationship('User', back_populates='wallet')

    # Define the one-to-many relationship with Transactions
    transactions = relationship('Transaction', back_populates='wallet')
