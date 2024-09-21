from aiogram import Router, F
from aiogram.types import  CallbackQuery

from datetime import datetime

from database.models.character import Character

from services.club_service import ClubService
from services.match_character_service import MatchCharacterService

from bot.callbacks.league_callbacks import  JoinToFight


from league.club_fight import ClubMatch, ClubMatchManager

join_to_fight_router = Router()



@join_to_fight_router.callback_query(JoinToFight.filter())
async def join_to_match(query: CallbackQuery, callback_data: JoinToFight, character: Character):
    if character.reminder.character_in_training:
        return await query.answer(
            text = "Ваш персонаж на тренуванні, ви не можете взяти участь у матчі"
        )
    
    
    fight_instance = ClubMatchManager.get_fight_by_id(
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
    

    character_in_match = await MatchCharacterService.get_character_in_match(
        character=character,
        club_in_match=fight_instance.clubs_in_match
    )
    if character_in_match is None:
        await MatchCharacterService.add_character_in_match(
            club_in_match = fight_instance.clubs_in_match,
            character=character
        )
        await query.message.answer(text = "✅ <b>Ваш персонаж був доданий на матч</b>")
        await query.message.edit_reply_markup(reply_markup=None)
    
    else:
        await query.answer("❌ Ваш персонаж уже й так бере участь у цьому матчі")
        
