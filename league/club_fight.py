import asyncio
import random

from asyncio import Queue

from datetime import datetime, timedelta

from constants import TIME_FIGHT, BUFFER_TIME, GET_RANDOM_NUMBER

from database.models.character import Character

from services.character_service import CharacterService
from services.league_service import LeagueFightService
from services.match_character_service import MatchCharacterService

from .club_in_match import ClubsInMatch
from .fight_sender import ClubMatchSender

from typing import Union

from loader import logger

class ClubMatchManager:
    all_fights: dict[str, "ClubMatch"] = {}
    
    @classmethod
    def register_fight(cls, fight: 'ClubMatch'):
        cls.all_fights[fight.clubs_in_match.match_id] = fight

    @classmethod
    def get_fight_by_id(cls, match_id: str) -> 'ClubMatch':
        return cls.all_fights.get(match_id)

    @classmethod
    def get_match_by_club(cls, club_id: int) -> list['ClubMatch']:
        return [fight for fight in cls.all_fights.values() 
                if fight.clubs_in_match.first_club_id == club_id 
                    or 
                fight.clubs_in_match.second_club_id == club_id]


class ClubMatch:
    def __init__(self, first_club_id: int, 
                 second_club_id: int,
                 start_time:datetime,
                 match_id: str,
                 group_id: str
                 ):
        
        self.start_time = start_time
        self.group_id   = group_id
        self.total_goals = random.randint(1,10)
        
        self.clubs_in_match = ClubsInMatch(
            first_club_id  = first_club_id,
            second_club_id = second_club_id,
            match_id = match_id,
            group_id=group_id
        )
        
        self.first_club_id  = first_club_id
        self.second_club_id = second_club_id
        
        self.club_match_sender = ClubMatchSender(self.clubs_in_match)
        self._queue_timer = Queue()
        ClubMatchManager.register_fight(self)

    async def start_match(self):
        await self.clubs_in_match.init_clubs()
        if self.clubs_in_match.clubs_is_have_no_characters:
            return await self.club_match_sender.send_messages_to_users(
                text       = self.club_match_sender.TEMPLATE_NOT_CHARACTERS,
                character  = self.clubs_in_match.all_characters_in_clubs)
        
        await asyncio.sleep(0.01)
        await self.club_match_sender.send_messages_to_users(
            text = self.club_match_sender.get_text_fight(),
            characters  = self.clubs_in_match.all_characters_in_match)
        
        
        await self.starting_taimer_match()
        await self.winners_remuneration()
        await self.club_match_sender.send_messages_to_users(
            text=self.club_match_sender.get_text_winners(),
            characters=self.clubs_in_match.all_characters_in_match)
    
    
    async def add_goal_to_character(self, character_in_club: list[Character]):
        power_chance_characters = [character.full_power for character in character_in_club]
        character_score_goal = random.choices(character_in_club, weights=power_chance_characters, k=1)[0]
        self.clubs_in_match.how_to_increment_goal = character_score_goal
        await MatchCharacterService.add_goal_to_character(match_id=self.clubs_in_match.match_id, character_id=character_score_goal.id)
                    
                    
    async def _update_score(self) -> list[Character]:
        if self.clubs_in_match.check_chance_win():
            club_id = self.clubs_in_match.first_club_id
            self.clubs_in_match.goals_first_club += 1
            chatacters_club = self.clubs_in_match.first_club_characters
        else:
            club_id = self.clubs_in_match.second_club_id
            self.clubs_in_match.goals_second_club += 1
            chatacters_club = self.clubs_in_match.second_club_characters
            
        await LeagueFightService.increment_goal(
            match_id=self.clubs_in_match.match_id,
            club_id=club_id
            )
        return chatacters_club, club_id
    
    
    
    #TAIMERS
    async def starting_taimer_match(self):
        start_time_taimer = datetime.now()
        asyncio.create_task(self._timer_event_generate(start_time_taimer))
        await self._timer_event_match(start_time_taimer)
    
    async def _timer_event_generate(self, match_time_start: datetime):
        match_time_end = match_time_start + TIME_FIGHT - BUFFER_TIME
        start_timestamp = int(match_time_start.timestamp())
        end_timestamp = int(match_time_end.timestamp())
        goal_times = sorted(random.sample(
            range(start_timestamp, end_timestamp), 
            self.total_goals
        ))
        for i, goal_time in enumerate(goal_times, 1):
            current_time = datetime.now()
            sleep_time = goal_time - current_time.timestamp() 
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                
            club_characters_score_goal, club_id_goal = await self._update_score()
            await self.add_goal_to_character(club_characters_score_goal)
            await self._queue_timer.put(club_id_goal)
        await asyncio.sleep(BUFFER_TIME.total_seconds())

    async def halfway_notification(self):
        await asyncio.sleep((TIME_FIGHT / 2).total_seconds())
        await self.club_match_sender.send_messages_to_users(
            characters=self.clubs_in_match.all_characters_in_match,
            text="Перший тайм завершено, команди розпочинають другий тайм, Ви можете підсилити свою команду прямо зараз через донат енергії⚡️🔋",
            send_photo=False
        )
    
    async def _timer_event_match(self, match_time_start: datetime):
        match_time_end = match_time_start + TIME_FIGHT
        asyncio.create_task(self.halfway_notification())
        
        CHECK_INTERVAL = TIME_FIGHT // 7
        
        while True:
                current_time = datetime.now()
                if current_time.replace(second=0, microsecond=0) >= match_time_end.replace(second=0, microsecond=0):
                    break
                timeout = min(CHECK_INTERVAL, match_time_end - current_time).total_seconds()
                try:
                    club_id_goal = await asyncio.wait_for(self._queue_timer.get(), timeout=timeout)
                    await self.sender_info_goals("goal", club_id_goal)
                except asyncio.TimeoutError:
                    await self.sender_info_goals("no_goal")
                except Exception as E:
                    print(E)
        
        
    async def sender_info_goals(self, type_event: str, club_id_goal: int|None = None) -> None:
        
        async def send_goal_event(goal_type:str, characters: list[Character]):
            text = self.club_match_sender.get_text_goal_evenet(goal_event=goal_type)
            await self.club_match_sender.send_messages_to_users(text=text, characters=characters, send_photo=False)
        
        if type_event == "goal":
            characters_goal_conceded = self.clubs_in_match.first_club_characters if club_id_goal == self.first_club_id else self.clubs_in_match.second_club_characters 
            characters_goal_increment = self.clubs_in_match.first_club_characters if club_id_goal != self.first_club_id else self.clubs_in_match.second_club_characters 
            await send_goal_event("goal", characters_goal_conceded)
            await send_goal_event("goal_conceded", characters_goal_increment)
        else:
            await send_goal_event("no_goal", self.clubs_in_match.all_characters_in_match)
        
    async def winners_remuneration(self):
        
        winners_characters = self.clubs_in_match.determine_winner_users()    
        for winner_character in winners_characters:
            if not winner_character.is_bot:
                exp,coins = GET_RANDOM_NUMBER(),GET_RANDOM_NUMBER()

                await CharacterService.add_exp_character(
                    character=winner_character,
                    amount_exp_add=exp
                )
                await CharacterService.update_money_character(
                    character=winner_character,
                    amount_money_adjustment=coins
                )
                await self.club_match_sender._send_message_to_character(
                    character=winner_character,
                    text=self.club_match_sender.get_text_send_reward(
                        exp,coins)
                )