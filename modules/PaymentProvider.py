from sqlalchemy import Column, Integer, String, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from .database import Base

class PaymentProvider(Base):
    __tablename__ = 'payment_providers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)  # Description of the payment provider
    website = Column(String)  # URL of the payment provider's website
    active = Column(Boolean, default=True)  # Indicates whether the payment provider is active

    # Define the one-to-many relationship with Transactions
    transactions = relationship('Transaction', back_populates='payment_provider')

    # Define any other relationships or fields specific to your payment provider

    def __repr__(self):
        return f"<PaymentProvider(id={self.id}, name='{self.name}')>"
