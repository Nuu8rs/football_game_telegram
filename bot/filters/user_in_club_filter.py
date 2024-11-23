from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message

from datetime import datetime

from database.models.character import Character

from services.best_club_league import BestLeagueService

from constants import START_DAY_BEST_LEAGUE, END_DAY_BEST_LEAGUE

class UserInClub(BaseFilter):
    
    def __init__(self) -> None:
        pass
        
    async def __call__(self, event: Message, character: Character) -> Any:
        if character.club_id is None:
            await event.answer("Ви не перебуваете в клубі")
            return False
        return True
    
class ClubInBeastLeague(BaseFilter):
    
    def __init__(self) -> None:
        pass
    
    async def __call__(self, event: Message, character: Character) -> Any:
        current_day = datetime.now().day
        
        if not (current_day >= START_DAY_BEST_LEAGUE and current_day <= END_DAY_BEST_LEAGUE):
            return False
        
        club_in_beast_league = await BestLeagueService.my_club_in_beast_league(
            club_id = character.club_id
        )
        
        if not club_in_beast_league:
            return False
        
        return True
        
        

