from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from datetime import datetime, timedelta

from database.models import Character, Club
from services.character_service import CharacterService
from services.club_service import ClubService

from bot.keyboards.magazine_keyboard import select_type_items_keyboard, gradation_values_item
from bot.callbacks.magazine_callbacks import SelectTypeItems


magazine_router = Router()

@magazine_router.message(F.text == "🏬 Магазин")
async def magazine_handler(message: Message, character: Character, state: FSMContext):
    await message.answer("Выберите вещи которые хотите купить", 
                         reply_markup=select_type_items_keyboard())
    

@magazine_router.callback_query(SelectTypeItems.filter())
async def select_item(query: CallbackQuery, state: FSMContext, character: Character, callback_data: SelectTypeItems):
    await query.message.edit_text("Выберите градацию уровня", 
                                  reply_markup=gradation_values_item(callback_data.item))