from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta


    
    

import asyncio
from asyncio import Queue
from database.models.character import Character
from database.models.club import Club
from services.match_character_service import MatchCharacterService
from services.club_service import ClubService
from services.character_service import CharacterService
from services.league_service import LeagueFightService

from utils.randomaizer import check_chance
from constants import GET_RANDOM_NUMBER

from typing import List
import random

TIME_FIGHT = timedelta(hours=1)

class Taimer:
    _queu_taimer = Queue()
    first_club  = None
    second_club = None
    
    total_goals = 10
    CHECK_INTERVAL = TIME_FIGHT/total_goals

    async def _taimer_match(self):
        ...
        
    async def _taimer_event(self):
        ...


    async def _taimer_match_sender(self, start_time_taimer):
        previous_goals_first_club = self.clubs_in_match.goals_first_club
        previous_goals_second_club = self.clubs_in_match.goals_second_club
        
        async def send_goal_event(goal_type:str, characters: list[Character]):
            text = self.club_match_sender.get_text_goal_evenet(goal_event=goal_type)
            await self.club_match_sender.send_messages_to_users(text=text, characters=characters, send_photo=False)
        
        sleep_first_time = TIME_FIGHT.total_seconds() / (self.total_goals + 1)
        await asyncio.sleep(sleep_first_time)
        update_current_time = TIME_FIGHT - timedelta(seconds=sleep_first_time)

        while datetime.now() - start_time_taimer < update_current_time:
            await asyncio.sleep(TIME_FIGHT.total_seconds() / (self.total_goals + 2))

            if previous_goals_first_club == self.clubs_in_match.goals_first_club and \
            previous_goals_second_club == self.clubs_in_match.goals_second_club:
                await send_goal_event("no_goal", self.clubs_in_match.all_characters_in_match)
            
            elif self.clubs_in_match.goals_first_club > previous_goals_first_club:
                await send_goal_event("goal", self.clubs_in_match.first_club_characters)
                await send_goal_event("goal_conceded", self.clubs_in_match.second_club_characters)
            
            elif self.clubs_in_match.goals_second_club > previous_goals_second_club:
                await send_goal_event("goal_conceded", self.clubs_in_match.first_club_characters)
                await send_goal_event("goal", self.clubs_in_match.second_club_characters)
                
            previous_goals_second_club = self.clubs_in_match.goals_second_club
            previous_goals_first_club = self.clubs_in_match.goals_first_club
            
    async def _taimer_match(self, start_time_taimer):
        
        sleep_time = TIME_FIGHT//10
        current_time_fight = TIME_FIGHT - sleep_time 
        while datetime.now() - start_time_taimer < current_time_fight:
            await asyncio.sleep(TIME_FIGHT.total_seconds() / self.total_goals)
            club_characters_score_goal = await self._update_score()
            await self.add_goal_to_character(club_characters_score_goal)
            
            
        await asyncio.sleep(sleep_time.total_seconds())