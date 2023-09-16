from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
import pytz

# Define the East African Time (EAT) timezone
eat_timezone = pytz.timezone('Africa/Nairobi')

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Relate to User table
    message = Column(String)
    is_read = Column(Boolean, default=False)  # Indicates whether the notification has been read
    timestamp = Column(DateTime, default=datetime.now(eat_timezone))
    # Define the many-to-one relationship with the User table
    user = relationship('User', back_populates='notifications')

