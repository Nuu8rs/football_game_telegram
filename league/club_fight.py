import asyncio
import random

from datetime import datetime, timedelta

from constants import TIME_FIGHT, GET_RANDOM_NUMBER

from database.models.character import Character

from services.character_service import CharacterService
from services.league_service import LeagueFightService
from services.match_character_service import MatchCharacterService

from .club_in_match import ClubsInMatch
from .fight_sender import ClubMatchSender

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
        self.total_goals = random.randint(1,8)
        
        self.clubs_in_match = ClubsInMatch(
            first_club_id  = first_club_id,
            second_club_id = second_club_id,
            match_id = match_id,
            group_id=group_id
        )
        self.club_match_sender = ClubMatchSender(self.clubs_in_match)
        ClubMatchManager.register_fight(self)

    async def start_match(self):
        await self.clubs_in_match.init_clubs()
        if self.clubs_in_match.clubs_is_have_no_characters:
            return await self.club_match_sender.send_messages_to_users(
                text       = self.club_match_sender.TEMPLATE_NOT_CHARACTERS,
                character  = self.clubs_in_match.all_characters_in_clubs)
        
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
        if self.clubs_in_match.first_club_id in [1,2] or self.clubs_in_match.second_club_id == [1,2]:
            logger.error(f"КЛУБ: {self.clubs_in_match.first_club.name_club} |СИЛА КЛУБА: {self.clubs_in_match.first_club_power}")
            logger.error(f"КЛУБ: {self.clubs_in_match.second_club.name_club} |СИЛА КЛУБА: {self.clubs_in_match.second_club_power}")
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
        return chatacters_club
    
    #TAIMERS
    async def starting_taimer_match(self):
        start_time_taimer = datetime.now()
        asyncio.create_task(self._taimer_match_sender(start_time_taimer))    
        await self._taimer_match(start_time_taimer)
    
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