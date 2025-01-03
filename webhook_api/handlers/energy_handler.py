from aiogram import Bot
from aiohttp.web import Response
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from webhook_api.schemas import MonoResultSchema
from ..base_endpoint import EndPoint, HTTPMethod

from services.payment_service import PaymentServise
from services.character_service import CharacterService
from config import BOT_TOKEN

class MonoResultEnergy(EndPoint):
    schema = MonoResultSchema
    data: MonoResultSchema
    method = HTTPMethod.POST
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    TEXT_TEMPLATE = """
<b>Ви оплатили замовлення, вам нараховано</b>: {amount_energy} 🔋
    """
    
    async def handle_request(self) -> Response:
        payment = await PaymentServise.get_payment(order_id=self.data.invoiceId)
        
        if not payment:
            return
        
        if self.data.status != "success":
            return
        
        if payment.status:
            return
        
        character = await CharacterService.get_character(payment.user_id)
        await PaymentServise.change_payment_status(order_id=self.data.invoiceId)
        
        await CharacterService.edit_character_energy(character, amount_energy_adjustment=payment.amount_energy)
        await self.bot.send_message(
            chat_id = payment.user_id,
            text    = self.TEXT_TEMPLATE.format(amount_energy = payment.amount_energy)
        )
        
        


