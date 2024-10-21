from aiohttp.web import Request, Response
from webhook_api.schemas import MonoResultSchema
from .base_endpoint import EndPoint, HTTPMethod

from services.payment_service import PaymentServise
from services.character_service import CharacterService
from loader import bot

class MonoResult(EndPoint):
    schema = MonoResultSchema
    data: MonoResultSchema
    method = HTTPMethod.POST
    
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
        
        await bot.send_message(
            chat_id = payment.user_id,
            text    = self.TEXT_TEMPLATE.format(amount_energy = payment.amount_energy)
        )
        
        


