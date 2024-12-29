from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.models.character import Character


from bot.keyboards.magazine_keyboard import (
    menu_stores, 
    select_type_items_keyboard,
    select_box
)
from .items.types import TypeItems

from constants import (
    MAGAZINE_PHOTO, 
    BOXES_PHOTO,
    LUXE_STORE_PHOTO,
    DEFAULT_MAGAZINE_PHOTO
)


menu_magazine_router = Router()

@menu_magazine_router.message(F.text == "🏬 Торговий квартал")
async def magazine_handler(message: Message, character: Character):
    await message.answer_photo(
        photo=MAGAZINE_PHOTO, 
        caption=(
    "🏬 Ласкаво просимо до <b>Торгового кварталу!</b> "
    "Тут ви знайдете все необхідне: <b>речі, бокси та приємні пропозиції</b>\n"
    "Розпочніть свої покупки просто зараз!"
),
        reply_markup = menu_stores()
    )
    

@menu_magazine_router.callback_query(F.data == "store_items")
async def magazine_handler(query: CallbackQuery):
    await query.message.answer_photo(
        photo   = DEFAULT_MAGAZINE_PHOTO, 
        caption = (
        "👋 Вітаємо в нашому футбольному магазині! ⚽\n"
        "Тут ти знайдеш усе необхідне для гри: зручні футболки, "
        "міцні бутси та стильні шорти. 🛒\n"
        "Обирай, що потрібно, та грай як справжній чемпіон! 🏆"
        ),
        reply_markup=select_type_items_keyboard())

@menu_magazine_router.callback_query(F.data == "store_boxes")
async def magazine_handler(query: CallbackQuery):
    
    await query.message.answer_photo(
        photo   = BOXES_PHOTO,
        caption = (
            "💥 Ласкаво просимо до магазину лутбоксів! 🎁⚽\n"
            "Тут на тебе чекають захопливі сюрпризи: відкривай бокси та "
            "отримуй монети, досвід і рідкісні футбольні нагороди! 🪙📈✨\n"
            "Грай, відкривай і ставай справжньою легендою! 🏆🔓"
            ), 
            reply_markup=select_box())
    
@menu_magazine_router.callback_query(F.data == "store_luxury")
async def magazine_handler(query: CallbackQuery):
    await query.message.answer_photo(
        photo   = LUXE_STORE_PHOTO,
        caption =(
        "✨ Ласкаво просимо до нашого преміум-магазину футбольної "
        "екіпіровки! 💎⚽\n"
        "Ми пропонуємо тільки найкраще для справжніх поціновувачів "
        "якісного спорядження. 👕👟\n"
        "Обирай елітні товари та стань зіркою на полі й поза ним! 🌟"
        ), 
        reply_markup=select_type_items_keyboard(
            TypeItems.LUXE_ITEM
        )
    )

    
