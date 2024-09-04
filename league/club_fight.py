import asyncio
from datetime import datetime, timedelta
from copy import deepcopy
import random

from apscheduler.triggers.cron import CronTrigger

from constants import FIGHT_MENU, TIME_FIGHT, GET_RANDOM_NUMBER
from database.models import Character, Club
from loader import bot
from logging_config import logger
from services.character_service import CharacterService
from services.league_service import LeagueFightService
from utils.randomaizer import check_chance

class ClubFight:
    all_fights = {}

    def __init__(self, first_club: Club, second_club: Club, start_time: datetime, match_id: int):
        self.first_club_orig = first_club
        self.second_club_orig = second_club

        self.first_club_copy = self._create_club_copy(first_club)
        self.second_club_copy = self._create_club_copy(second_club)

        self.goals_first_club = 0
        self.goals_second_club = 0

        self.match_id = match_id
        self.start_time = start_time

        self.messages = {}
        self.total_goals = random.randint(1,10)
        self.battle_bot = BattleBot(self)

        self._register_fight()

    def _create_club_copy(self, club: Club) -> Club:
        club_copy = deepcopy(club)
        if not club_copy.is_fake_club:
            club_copy.characters = []
        return club_copy

    def _register_fight(self):
        ClubFight.all_fights[self.match_id] = {
            'first_club': self.first_club_orig,
            'second_club': self.second_club_orig,
            'start_time': self.start_time,
            'fight_instance': self
        }

    async def start(self):
        if self._clubs_have_no_characters():
            return await self.battle_bot.send_messages_to_users(
                text=self.battle_bot.TEMPLATE_NOT_CHARACTERS
            )
        
        self._calculate_chances()
        
        await self.battle_bot.send_messages_to_users(
            text=self.battle_bot.get_text_fight()
        )

        await self._fight()
        await self._winners_remuneration()
        await self._finalize_fight()

    def _clubs_have_no_characters(self) -> bool:
        return not self.first_club_copy.characters and not self.second_club_copy.characters

    def _calculate_chances(self):
        total_power = self.first_club_copy.total_power + self.second_club_copy.total_power
        self.chance_to_win_first_club = (self.first_club_copy.total_power / total_power) * 100

    def determine_winner_users(self) -> list[Character]:
        if self.goals_first_club > self.goals_second_club:
            return self.first_club_copy.characters
        elif self.goals_second_club > self.goals_first_club:
            return self.second_club_copy.characters
        else:
            return self.second_club_copy.characters + self.first_club_copy.characters


    async def _fight(self):
        start_time = datetime.now()
        while datetime.now() - start_time < TIME_FIGHT:
            await asyncio.sleep(TIME_FIGHT.total_seconds() / self.total_goals)
            await self._update_score()
            await self.battle_bot.edit_caption_text(
                text=self.battle_bot.get_text_fight()
            )

    async def _update_score(self):
        if check_chance(self.chance_to_win_first_club):
            self.goals_first_club += 1
            await LeagueFightService.increment_goal(
                match_id=self.match_id,
                club_id=self.first_club_orig.id
                )
        else:
            await LeagueFightService.increment_goal(
                match_id=self.match_id,
                club_id=self.second_club_orig.id
                )
            self.goals_second_club += 1

    async def _winners_remuneration(self):
        winners_characters = self.determine_winner_users()
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
                await self.battle_bot._send_message_to_character(
                    character=winner_character,
                    text=self.battle_bot.get_text_send_reward(
                        exp_points=exp,
                        coins=coins
                    )
                )

            

    async def _finalize_fight(self):
        
        
        await self.battle_bot.send_messages_to_users(
            text=self.battle_bot.get_text_winners()
        )


    @classmethod
    def get_match_by_club(cls, club: Club) -> 'ClubFight':
        return [
            info['fight_instance'] for _, info in cls.all_fights.items()
            if info['first_club'].id == club.id or info['second_club'].id == club.id
        ]

    @classmethod
    def get_fight_by_id(cls, match_id) -> "ClubFight":
        return cls.all_fights.get(match_id, {}).get('fight_instance')

    @classmethod
    def add_characters_to_club(cls, character: Character, 
                               match_id: int,
                               club: Club):
        fight_isistance = cls.get_fight_by_id(match_id)
        
        if club.id == fight_isistance.first_club_orig.id:
            fight_isistance.first_club_copy.characters.append(character)
        elif club.id == fight_isistance.second_club_orig.id:
            fight_isistance.second_club_copy.characters.append(character)




class BattleBot:
    TEMPLATE_FIGHT = """
⚽️ Починається епічна битва між клубами <b>{name_first_club}</b> та <b>{name_second_club}</b>! 

📊 Поточний рахунок: <b>{goals_first_club}</b> - <b>{goals_second_club}</b>.

💪 Загальна сила команд:
- <b>{name_first_club}</b>: <b>{power_first_club}</b> 
- <b>{name_second_club}</b>: <b>{power_second_club}</b>

Нехай переможе найсильніший! 🏆
    """

    TEMPLATE_END = """
🎉 Битва між клубами <b>{name_first_club}</b> та <b>{name_second_club}</b> завершена! 

📊 Кінцевий рахунок: <b>{goals_first_club}</b> - <b>{goals_second_club}</b>.

{winner_section}

🏆 Дякуємо обом клубам за чудову гру! Ви продемонстрували справжній дух суперництва та спортивності.

До нових зустрічей на футбольному полі! ⚽️
    """
    
    TEMPLATE_NOT_CHARACTERS = """
На жаль, ніхто з учасників не з'явився на цю битву. 😔
    """

    TEMPLATE_SEND_REWARD_CHARACTER = """
🎉 За цю битву між клубами '{name_first_club}' і '{name_second_club}' ви отримали:
✨ {exp_points} досвіду
💰 {coins} монет
    """


    def __init__(self, fight_instance: ClubFight):
        self.fight_instance = fight_instance
        self.messages = {}

    def _format_message(self, template: str, extra_context: dict = None) -> str:
        context = {
            'name_first_club': self.fight_instance.first_club_orig.name_club,
            'name_second_club': self.fight_instance.second_club_orig.name_club,
            'goals_first_club': self.fight_instance.goals_first_club,
            'goals_second_club': self.fight_instance.goals_second_club,
            'power_first_club': self.fight_instance.first_club_copy.total_power,
            'power_second_club': self.fight_instance.second_club_copy.total_power,
        }
        if extra_context:
            context.update(extra_context)
        return template.format(**context)

    def get_text_fight(self) -> str:
        return self._format_message(self.TEMPLATE_FIGHT)
    
    def get_text_send_reward(self, exp_points: int, coins:int) -> str:
        return self._format_message(template=self.TEMPLATE_SEND_REWARD_CHARACTER, 
                                    extra_context={"exp_points":exp_points,"coins":coins})

    def get_text_winners(self) -> str:
        if self.fight_instance.goals_first_club == self.fight_instance.goals_second_club:
            winner_section = "🎉 Битва завершилась внічию!"
        else:
            winner, loser = self._determine_winner_loser()
            winner_section = f"""
🥇 Переможець: <b>{winner['club_name']}</b> з рахунком <b>{winner['goals']}</b>! 
🥈 Друге місце: <b>{loser['club_name']}</b> з рахунком <b>{loser['goals']}</b>.
            """
        return self._format_message(self.TEMPLATE_END, {'winner_section': winner_section})

    def _determine_winner_loser(self) -> tuple[dict, dict]:
        if self.fight_instance.goals_first_club > self.fight_instance.goals_second_club:
            return (
                {'club_name': self.fight_instance.first_club_orig.name_club, 'goals': self.fight_instance.goals_first_club},
                {'club_name': self.fight_instance.second_club_orig.name_club, 'goals': self.fight_instance.goals_second_club}
            )
        else:
            return (
                {'club_name': self.fight_instance.second_club_orig.name_club, 'goals': self.fight_instance.goals_second_club},
                {'club_name': self.fight_instance.first_club_orig.name_club, 'goals': self.fight_instance.goals_first_club}
            )

    async def send_messages_to_users(self, text: str) -> dict[int, int]:
        characters: list[Character] = self.fight_instance.first_club_orig.characters + self.fight_instance.second_club_orig.characters
        for character in characters:
            await self._send_message_to_character(character, text)

    async def _send_message_to_character(self, character: Character, text: str) -> None:
        if not character.is_bot:
            try:
                message = await bot.send_photo(
                    chat_id=character.characters_user_id,
                    photo=FIGHT_MENU,
                    caption=text
                )
                self.messages[character.characters_user_id] = message.message_id
            except Exception as E:
                logger.error(f"Failed to send message to {character.owner.user_name}\nError: {E}")

    async def edit_caption_text(self, text: str) -> None:
        for user_id, message_id in self.messages.items():
            try:
                await bot.edit_message_caption(
                    chat_id=user_id,
                    message_id=message_id,
                    caption=text
                )
            except Exception as E:
                logger.error(f"Failed to edit message for {user_id}\nError: {E}")