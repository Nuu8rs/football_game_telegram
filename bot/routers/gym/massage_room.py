from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from database.models.character import Character

from services.character_service import CharacterService

from bot.keyboards.gym_keyboard import menu_massage_room
from bot.callbacks.massage_room_callbacks import SelectCountGetEnergy


massage_room_router = Router()

@massage_room_router.message(F.text == "💆‍♂️ Масажний зал")
async def massage_room_handler(message: Message):
    await message.answer("Вітаю у массажному залі", reply_markup=menu_massage_room())
    
    
@massage_room_router.callback_query(SelectCountGetEnergy.filter())
async def select_count_add_energy_handler(query: CallbackQuery, callback_data: SelectCountGetEnergy, character: Character):
    await query.message.answer("👩🏼 Масажить у відпустці")
    # await CharacterService.edit_character_energy(
    #     character_obj=character,
    #     amount_energy_adjustment=callback_data.count_energy
    # )
    # await query.message.answer(f"Вітаю ви купили {callback_data.count_energy} 🔋")