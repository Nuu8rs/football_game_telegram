from aiogram import Bot
from aiohttp.web import Response
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from webhook_api.schemas import MonoResultSchema
from ..base_endpoint import EndPoint, HTTPMethod

from database.models.payment.key_payment import KeyPayment

from services.payment_service import PaymentServise
from services.character_service import CharacterService
from config import BOT_TOKEN

class MonoResultBuyTrainingKey(EndPoint):
    schema = MonoResultSchema
    data: MonoResultSchema
    method = HTTPMethod.POST
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    TEXT_TEMPLATE = """
🔑 <b>Ключ придбано!</b> ⚽🔥  

Вітаємо! Ти успішно купив ключ для входу на тренування. 🚀  
Тепер ти можеш приєднатися до найближчої сесії та покращити свої навички! 💪⚡  

⏳ <i>Слідкуй за розкладом та будь готовий увійти в гру!</i> 🏆
"""
    
    async def handle_request(self) -> Response:
        payment: KeyPayment = await PaymentServise.get_payment(
            order_id=self.data.invoiceId,
            type_payment = KeyPayment
        )
        
        if not payment:
            return
        
        if self.data.status != "success":
            return
        
        if payment.payment.status:
            return
        
        character = await CharacterService.get_character(payment.payment.user_id)
        await CharacterService.add_trainin_key(
            character_id = character.id,
        )

        await self.bot.send_message(
            chat_id = payment.payment.user_id,
            text    = self.TEXT_TEMPLATE
        )
        await PaymentServise.change_payment_status(order_id=self.data.invoiceId)
        return self.OK()


