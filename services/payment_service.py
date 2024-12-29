from datetime import datetime
from sqlalchemy import select, update

from database.session import get_session
from database.models.payments import Payment
from bot.routers.stores.box.open_box import TypeBox

from logging_config import logger

from typing import Optional

class PaymentServise:
    @classmethod
    async def create_payment(
        cls, 
        price: int, 
        user_id: int, 
        order_id: str,
        amount_energy: Optional[int] = None,
        type_box : Optional[TypeBox] = None
    ) -> Payment:
        async for session in get_session():
            async with session as sess:  
                try:
                    new_payment  = Payment(
                        order_id      = order_id,
                        user_id       = user_id,
                        price         = price,
                        amount_energy = amount_energy,
                        type_box      = type_box
                                        )
                    sess.add(new_payment)
                    await sess.commit()
                    return new_payment
                except Exception as E:
                    logger.error(f"err create payment: {E}")
                    
    
    @classmethod
    async def get_payment(cls, order_id: str) -> Payment:
        async for session in get_session():
            async with session as sess:
                try:    
                    stmt = select(Payment).where(Payment.order_id == order_id)
                    result = await session.execute(stmt)
                    return result.scalar_one_or_none()
                except Exception as E:
                    logger.error(f"err get payment: {E}")
                    
    @classmethod
    async def change_payment_status(cls, order_id: str):
        async for session in get_session():
            async with session as sess:
                try:    
                    stmt = update(Payment).where(Payment.order_id == order_id).values(status=True)
                    await sess.execute(stmt)
                    await sess.commit()
                except Exception as E:
                    logger.error(f"err change payment status: {E}")