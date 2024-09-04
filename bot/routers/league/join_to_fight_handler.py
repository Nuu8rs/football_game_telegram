from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from datetime import datetime, timedelta

from database.models import Character, UserBot
from services.club_service import ClubService

from bot.keyboards.gym_keyboard import select_type_gym, select_time_to_gym
from bot.callbacks.league_callbacks import  JoinToFight

from constants import GYM_PHOTO, const_name_characteristics, const_energy_by_time
from schedulers.scheduler_tasks import GymTaskScheduler

from league.club_fight import ClubFight

join_to_fight_router = Router()



@join_to_fight_router.callback_query(JoinToFight.filter())
async def join_to_match(query: CallbackQuery, callback_data: JoinToFight, character: Character):
    if character.character_in_training:
        return await query.answer(
            text = "Ваш персонаж на тренуванні, ви не можете взяти участь у битві"
        )
    
    
    fight_instance = ClubFight.get_fight_by_id(
        match_id=callback_data.match_id
    )
    
    current_time = datetime.now()
    if current_time > fight_instance.start_time:
        await query.answer(
            text="❌ Даний матч уже закінчився"
        )
        return await query.message.delete()
    
    if not character.club_id:
        return await query.message.answer("❌ У данного персонажа нету клуба")
    
    club = await ClubService.get_club(club_id=character.club_id)
    
    list_characters: list[Character] = fight_instance.first_club_copy.characters + fight_instance.second_club_copy.characters 
    if not any(character_in_match for character_in_match in list_characters if character.characters_user_id == character_in_match.characters_user_id):
        ClubFight.add_characters_to_club(
            character=character,
            match_id=callback_data.match_id,
            club = club
        )
        await query.message.answer(text = "✅ <b>Ваш персонаж був доданий на битву</b>")
        await query.message.edit_reply_markup(reply_markup=None)
    
    else:
        await query.answer("❌ Ваш персонаж уже й так бере участь у цьому матчі")
        


    # await join_character_to_match(
    #     message= query.message,
    #     character=character,
    #     fight_instance=fight_instance
    # )

# async def join_character_to_match(message: Message, 
#                                   character: Character, 
#                                   fight_instance: ClubFight):
    
#     club = await ClubService.get_club(club_id=character.club_id)
    
#     list_characters: list[Character] = fight_instance.first_club_copy.characters + fight_instance.second_club_copy.characters 
#     if not any(character_in_match for character_in_match in list_characters if character.characters_user_id == character_in_match.characters_user_id):
#         ClubFight.add_characters_to_club(
#             character=character,
#             match_id=fight_instance.match_id,
#             club = club
#         )
#         await message.answer(text = "✅ <b>Ваш персонаж був доданий на битву</b>")
    
#     else:
#         await message.answer("❌ Вас персонаж уже й так бере участь у цьому матчі")
        