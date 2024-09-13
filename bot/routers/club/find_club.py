from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

from database.models.club import Club
from database.models.character import Character

from services.club_service import ClubService
from services.character_service import CharacterService

from bot.states.club_states import FindClub
from bot.keyboards.club_keyboard import find_club, join_to_club_keyboard
from bot.callbacks.club_callbacks import SelectClubToJoin, JoinToClub
from bot.callbacks.switcher import SwitchClub

from loader import logger

from constants import CLUB_PHOTO
from utils.club_utils import get_club_description, send_message_characters_club

find_club_router = Router()

@find_club_router.callback_query(F.data == "join_to_club")
async def get_my_club_handler(query: CallbackQuery, state: FSMContext, character: Character):
    if character.club_id:
        return await query.message.answer("Ви вже й так у клубі")
    
    all_clubs = await ClubService.get_all_clubs_to_join()
    await state.update_data(all_clubs = all_clubs)
    if not all_clubs:
        return await query.message.reply("На даний момент немає клубів")
        
    await state.set_state(FindClub.send_name_club)
    await query.message.edit_text("Виберіть клуб зі списку, або введіть назву клубу самостійно",
                               reply_markup=find_club(
                                   all_clubs=all_clubs,
                                   current_index=0
                               ))
    
    
@find_club_router.message(FindClub.send_name_club)
async def find_clube_message(message: Message, state: FSMContext, character: Character):
    if  character.club_id:
        return await message.answer("Ви вже й так у клубі")
    data = await state.get_data()
    all_clubs: list[Club] = data['all_clubs']
    matching_clubs = [club for club in all_clubs if message.text.lower() in club.name_club.lower()]
    await state.update_data(all_clubs = matching_clubs)
    if not matching_clubs:
        return await message.answer(f"Клубів за назвою - {message.text}, не знайдено")
    
    await message.answer(f"Усі знайдені клуби за назвою - {message.text}",
                                            reply_markup=find_club(
                                                all_clubs=matching_clubs,
                                                current_index=0
                                                )
                                                )
    
@find_club_router.callback_query(SwitchClub.filter())
async def switcher_select_club(query: CallbackQuery, callback_data: SwitchClub, state: FSMContext):
    if callback_data.side == "right":
        callback_data.current_index += 1
    if callback_data.side == "left":
        callback_data.current_index -= 1

    data = await state.get_data()
    if not data.get("all_clubs", False):
        return
    return await query.message.edit_reply_markup(
        reply_markup= find_club(
            all_clubs=data['all_clubs'],
            current_index=callback_data.current_index
        )
    )


@find_club_router.callback_query(SelectClubToJoin.filter())
async def view_club(query: CallbackQuery, callback_data: SelectClubToJoin):
    club = await ClubService.get_club(club_id=callback_data.club_id)
    await query.message.answer_photo(
        photo=CLUB_PHOTO,
        caption=await get_club_description(club=club),
        reply_markup=join_to_club_keyboard(club_id=callback_data.club_id)
    )
    
@find_club_router.callback_query(JoinToClub.filter())
async def join_to_club(query: CallbackQuery, state: FSMContext, callback_data: JoinToClub, character: Character):
    if character.time_to_join_club  + timedelta(days=1) > datetime.now():
        return await query.answer("Ви не можете приєднатися до клубу, не минув 1 день після вступу до іншого клубу", show_alert=True)
    
    if character.club_id:
        return await query.message.answer("Ви вже й так у клубі")
    
    await state.clear()
    await CharacterService.update_character_club_id(
        character=character,
        club_id=callback_data.club_id
    )
    club = await ClubService.get_club(character.club_id)
    await send_message_characters_club(
        characters_club=club.characters,
        my_character=character,
        text=f"🎟 Вітаємо у вашому клубі поповнення, приєднався новий учасник <b>{character.name}</b>"
    )
    await query.message.answer("🎉 Вітаю ви приєдналися до клубу")
    
