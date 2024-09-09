import datetime

from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import relationship

from database.model_base import Base

class UserBot(Base):
    __tablename__ = 'users'
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, index=True)  
    user_name = Column(String(255), index=True)  
    user_full_name = Column(String(255)) 
    user_time_register = Column(DateTime, default=datetime.datetime.utcnow)
    
    characters = relationship("Character", back_populates="owner", lazy="selectin")
    clubs = relationship("Club", back_populates="owner", lazy="selectin")