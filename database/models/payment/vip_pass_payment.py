from sqlalchemy import (
    Column, 
    Enum, 
    String, 
    ForeignKey, 
    Integer, 
)
from sqlalchemy.orm import relationship, Mapped

from bot.routers.stores.vip_pass.types import VipPassTypes

from database.model_base import Base

from .payments import Payment


class VipPassPayment(Base):
    __tablename__ = 'vip_pass_payment'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(String(100), ForeignKey('payments.order_id', ondelete="CASCADE"), nullable=False)  # nullable=False
    type_vip_pass  = Column(Enum(VipPassTypes), nullable=True)
    
    payment: Mapped["Payment"] = relationship("Payment", lazy="joined")
