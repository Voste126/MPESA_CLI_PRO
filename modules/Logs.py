from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    action = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))  # You can relate this to the User table if needed
    # Add more fields for logging details

    # Define a many-to-one relationship with the User table
    user = relationship('User', back_populates='logs')
