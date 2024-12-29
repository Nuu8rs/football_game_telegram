from datetime import datetime

from sqlalchemy import (
    Column, 
    BigInteger, 
    String, 
    ForeignKey, 
    DateTime, 
    Integer, 
    Boolean,
    Enum
)

from database.models.types import TypeBox

from database.model_base import Base



class Payment(Base):
    __tablename__ = 'payments'
    
    id                   = Column(BigInteger, primary_key=True, index=True)

    order_id             = Column(String(100), nullable=False)
    user_id              = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    
    price                = Column(Integer, nullable=False)
    
    amount_energy        = Column(Integer, nullable=True)
    type_box             = Column(Enum(TypeBox), nullable=True)
    
    created_time_payment = Column(DateTime, default=datetime.utcnow, nullable=False)
    payment_time         = Column(DateTime, nullable=True)
    status               = Column(Boolean, default=False, server_default="0")