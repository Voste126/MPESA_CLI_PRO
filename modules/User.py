from sqlalchemy import Column, Integer, String, Float, DateTime
import pytz
from sqlalchemy.orm import relationship
from .database import Base
from .hashing import get_password_hash
from datetime import datetime

# Define the East African Time (EAT) timezone
eat_timezone = pytz.timezone('Africa/Nairobi')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    phone_number = Column(String, unique=True)
    registration_date = Column(DateTime, default=lambda: datetime.now(eat_timezone))

    # Add more user-related fields as needed

     # Update the relationship to reflect the one-to-one relationship with Wallet
    wallet = relationship('Wallet', back_populates='user', uselist=False)  # uselist=False means it's a one-to-one relationship
    # Define the one-to-many relationship with Transactions
    transactions = relationship(
        "Transaction",
        back_populates="user",
        foreign_keys="[Transaction.user_id]"  # Specify the foreign key column(s)
    )

    # Define the one-to-many relationship with Logs
    logs = relationship('Log', back_populates='user')
    # Define the one-to-many relationship with Security settings 
    security_settings = relationship('SecuritySetting', back_populates='user')
    # Define the one-to-many relationship with Notification
    notifications = relationship('Notification', back_populates='user')

    def create_password_hash(self, password):
        self.password = get_password_hash(password)
