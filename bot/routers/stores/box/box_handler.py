from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from api.monobank.create_payment import CreatePayment

from bot.callbacks.magazine_callbacks import SelectBox, BuyBox
from bot.keyboards.magazine_keyboard import buy_box

from database.models.character import Character

from services.payment_service import PaymentServise

from constants import lootboxes
from config import CALLBACK_URL_WEBHOOK_BOX


open_box_roter = Router()

TEXT_TEMPLATE = """
🎁 <b>Лутбокс</b>: {name_lootbox}

⚡ <b>Енергія</b>: {min_energy} - {max_energy} 💥  
💰 <b>Монети</b>: {min_money} - {max_money} 💎  
🎓 <b>Досвід</b>: {min_exp} - {max_exp} 📈  

💸 <b>Ціна</b>: {price} UAH
"""


@open_box_roter.callback_query(SelectBox.filter())
async def select_box_handler(
    query: CallbackQuery,
    callback_data: SelectBox,
    character: Character
):
    text_lootbox = TEXT_TEMPLATE.format(**lootboxes.get(callback_data.type_box))
    type_box = callback_data.type_box

    from .open_box import OpenBoxService
    op = OpenBoxService(
        type_box = type_box,
        character = character,
        bot = query.message.bot 
    )
    await op.open_box()
    # price_box = lootboxes[type_box]['price']

    
    # payment = CreatePayment(
    #     price=price_box,
    #     name_product=lootboxes[type_box]['name_lootbox'],
    #     webhook_url=CALLBACK_URL_WEBHOOK_BOX
    # )
    # url_payment_response = await payment.send_request()
    # if not url_payment_response:
    #     return await query.answer("Сталася помилка під час створення платежу")
    
    # order_id = url_payment_response['invoiceId']
    # url_payment = url_payment_response['pageUrl']
    
    # await query.message.edit_caption(
    #     caption=text_lootbox,
    #     reply_markup=buy_box(url_payment)

    # )

    # await PaymentServise.create_payment(
    #     price    = price_box,
    #     user_id  = character.characters_user_id,
    #     order_id = order_id,
    #     type_box = type_box
    # )