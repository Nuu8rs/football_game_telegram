import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.models.character import Character

from bot.routers.register_user.state.register_user_state import JoinToClubState
from bot.routers.register_user.routers.territory_academy import territory_academy

from constants import CLUB_PHOTO

from services.club_service import ClubService
from services.character_service import CharacterService
from services.club_infrastructure_service import ClubInfrastructureService  

from utils.club_utils import get_club_text


create_club_from_join_router = Router()

@create_club_from_join_router.callback_query(
    F.data == "create_club_new_member",
    JoinToClubState.join_to_club
)
async def create_new_club_handler(
    query: CallbackQuery,
    state: FSMContext,
    character: Character
):
    data = await state.get_data()
    message_join_to_club: Message = data.get("message_join_to_club", False)
    if message_join_to_club:
        await message_join_to_club.delete()
        
    message_send_name_club = await query.message.answer(
        "Введите назву команди, яку ви хочете створити",
    )
    await state.update_data(message_send_name_club = message_send_name_club)
    
    await state.set_state(JoinToClubState.send_name_new_club)
    
    
@create_club_from_join_router.message(
    JoinToClubState.send_name_new_club
)
async def send_name_new_club_handler(
    message: Message,
    state: FSMContext,
    character: Character
):
    if character.club_id:
        await state.clear()
        return await message.answer("Ви вже перебуваєте в команді")

    name_club = message.text
    club = await ClubService.create_club(
        name_club = name_club,
        owner_id  = character.characters_user_id
    )
    await CharacterService.update_character_club_id(character=character, club_id=club.id)
    club = await ClubService.get_club(club_id=club.id)
    await ClubInfrastructureService.create_infrastructure(club_id=club.id)
    
    await message.answer_photo(
        photo=CLUB_PHOTO,
        caption=await get_club_text(
            club = club,
            character=character
            )
    )
    await message.answer(text = f"🔹 <b>Тренер:</b> Вітаю, {character.character_name}! Тепер у тебе є власна команда!")
    await state.clear()
    
    await territory_academy(
        character= character,
        message = message,
    )