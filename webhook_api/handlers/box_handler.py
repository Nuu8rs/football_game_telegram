import asyncio

from aiogram import Bot
from aiohttp.web import Response
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from webhook_api.schemas import MonoResultSchema
from ..base_endpoint import EndPoint, HTTPMethod

from bot.routers.stores.box.open_box import OpenBoxService
from services.payment_service import PaymentServise
from services.character_service import CharacterService
from config import BOT_TOKEN
from constants import lootboxes

class MonoResultBox(EndPoint):
    schema = MonoResultSchema
    data: MonoResultSchema
    method = HTTPMethod.POST
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    TEXT_TEMPLATE = """
<b>Ви оплатили замовлення, ви отримали</b>: {name_box}
Він буде автоматично відкритий через 30 сек
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
        
        name_box = lootboxes[payment.type_box]['name_lootbox']
        await self.bot.send_message(
            chat_id = payment.user_id,
            text    = self.TEXT_TEMPLATE.format(name_box = name_box)
        )
        open_box = OpenBoxService(
            type_box = payment.type_box,
            character = character,
            bot = self.bot
        )
        await asyncio.sleep(30)
        asyncio.create_task(open_box.open_box())