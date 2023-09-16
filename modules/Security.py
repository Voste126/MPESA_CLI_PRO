from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class SecuritySetting(Base):
    __tablename__ = 'security_settings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)  # Relate to User table
    two_factor_enabled = Column(Boolean, default=False)  # Indicates whether two-factor authentication is enabled for the user
    password_expiry_days = Column(Integer)  # Number of days until password expiration
    password_history = Column(Integer)  # Number of previous passwords to store in history
    # Add more security-related fields as needed

    # Define the many-to-one relationship with the User table
    user = relationship('User', back_populates='security_settings')
