from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
import pytz

# Define the East African Time (EAT) timezone
eat_timezone = pytz.timezone('Africa/Nairobi')

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    recipient_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    transaction_type = Column(String)
    timestamp = Column(DateTime, default=datetime.now(eat_timezone))
    status = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Define the many-to-one relationship with User
    user = relationship('User', back_populates='transactions', foreign_keys=[user_id])
    # Define the many-to-one relationship with Users for sender and recipient
    sender = relationship('User', foreign_keys=[sender_id], back_populates='transactions')
    recipient = relationship('User', foreign_keys=[recipient_id], back_populates='transactions')

    # Define the many-to-one relationship with Wallets
    wallet_id = Column(Integer, ForeignKey('wallets.id'))
    wallet = relationship('Wallet', back_populates='transactions')

    # Define the many-to-one relationship with PaymentProviders
    payment_provider_id = Column(Integer, ForeignKey('payment_providers.id'))
    payment_provider = relationship('PaymentProvider', back_populates='transactions')

    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, type='{self.transaction_type}')>"

    @classmethod
    def make_deposit(cls, user, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than 0.")
        
        wallet = user.wallet
        wallet.balance += amount
        
        transaction = cls(
            user=user,
            amount=amount,
            transaction_type="deposit",
            status="completed"
        )
        return transaction

    @classmethod
    def make_withdrawal(cls, user, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than 0.")
        
        wallet = user.wallet
        if wallet.balance < amount:
            raise ValueError("Insufficient balance for withdrawal.")
        
        wallet.balance -= amount
        
        transaction = cls(
            user=user,
            amount=amount,
            transaction_type="withdrawal",
            status="completed"
        )
        return transaction

    @staticmethod
    def check_wallet_balance(user):
        wallet = user.wallet
        return wallet.balance
