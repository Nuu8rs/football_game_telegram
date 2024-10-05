from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from database.models.character import Character
from database.models.user_bot import UserBot

from services.club_service import ClubService
from services.character_service import CharacterService

from bot.states.club_states import CreateClub
from bot.keyboards.club_keyboard import club_menu_keyboard, main_menu_club

from constants import CLUB_PHOTO
from utils.club_utils import get_club_text

create_club_router = Router()

@create_club_router.message(F.text == "⛩ Створити свій клуб")
async def get_my_club_handler(message: Message, state: FSMContext, character: Character):
    if character.club_id:
        return await message.answer("Не-а")
    await message.answer("Введите имя клуба")
    await state.set_state(CreateClub.send_name)
    
    
@create_club_router.message(CreateClub.send_name, F.text != "🎮 Приєднатися до клубу")
async def get_name_club(message: Message, state: FSMContext, character: Character):
    if character.club_id:
        return
    name_club = message.text
    club = await ClubService.create_club(
        name_club = name_club,
        owner_id  = character.characters_user_id
    )
    await CharacterService.update_character_club_id(character=character, club_id=club.id)
    club = await ClubService.get_club(club_id=club.id)
    
    await message.answer_photo(
        photo=CLUB_PHOTO,
        caption=await get_club_text(
            club = club,
            character=character
            ),
        reply_markup=club_menu_keyboard(
            club=club,
            character=character
        )
    )
    await message.answer("Вітаю зі створенням клубу", reply_markup=main_menu_club(character))
    await state.clear()