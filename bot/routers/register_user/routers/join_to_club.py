import asyncio
from datetime import datetime

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.models.user_bot import UserBot, STATUS_USER_REGISTER
from database.models.character import Character

from bot.callbacks.club_callbacks import JoinToClub
from bot.routers.register_user.config import (
    PHOTO_STAGE_REGISTER_USER,
    TEXT_STAGE_REGISTER_USER
)
from bot.routers.register_user.state.register_user_state import JoinToClubState
from bot.routers.register_user.routers.territory_academy import territory_academy

from bot.keyboards.club_keyboard import find_club
from utils.club_utils import send_message_characters_club


from services.user_service import UserService
from services.club_service import ClubService
from services.character_service import CharacterService

from constants import CLUB_PHOTO, TIME_TO_JOIN_TO_CLUB


join_to_club_router = Router()

async def join_to_club(
    message: Message,
    character: Character,
    state: FSMContext
):
    new_status = STATUS_USER_REGISTER.JOIN_TO_CLUB
    await asyncio.sleep(5)
    await UserService.edit_status_register(
        user_id=character.characters_user_id,
        status=new_status
    )
    
    all_clubs_to_join = await ClubService.get_all_clubs_to_join()
    await state.update_data(all_clubs = all_clubs_to_join)
    await state.set_state(JoinToClubState.join_to_club)
    message_join_to_club = await message.answer_photo(
        photo=PHOTO_STAGE_REGISTER_USER[new_status],
        caption=TEXT_STAGE_REGISTER_USER[new_status],
        reply_markup=find_club(all_clubs_to_join) 
    )
    await state.update_data(message_join_to_club = message_join_to_club)

@join_to_club_router.callback_query(
    JoinToClubState.join_to_club,
    JoinToClub.filter()
)
async def join_to_club_handler(
    query: CallbackQuery,
    callback_data: JoinToClub,
    character: Character,
    state: FSMContext
):
    data = await state.get_data()
    message_join_to_club: Message = data.get("message_join_to_club", None)
    if message_join_to_club is None:
        return join_to_club(
            message=query.message,
            character=character,
            state=state
        )

    club = await ClubService.get_club(callback_data.club_id)
    await asyncio.sleep(0.5)
    if len(club.characters) >= 11:
        return await query.answer("Перевищено ліміт людей у клубі", show_alert=True)
    
    if character.club_id:
        return await query.message.answer("Ви вже й так у команді")
    
    await CharacterService.update_character_club_id(
        character=character,
        club_id=callback_data.club_id
    )

    await send_message_characters_club(
        characters_club=club.characters,
        my_character=character,
        text=f"🎟 Вітаємо у вашій команді поповнення, приєднався новий учасник <b>{character.character_name}</b>"
    )
    await message_join_to_club.edit_reply_markup(
        reply_markup = None
    )
    
    character = await CharacterService.get_character_by_id(character.id)
    await query.message.edit_caption(caption = f"🔹 <b>Тренер:</b> Вітаю, {character.character_name}! Тепер ти частина команди!")
    
    await territory_academy(
        character= character,
        message = query.message,
    )
    await state.clear()