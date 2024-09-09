
from database.models.club import Club
from database.models.user_bot import UserBot
from database.models.character import Character

from logging_config import logger
from loader import bot
from bot.keyboards.league_keyboard import keyboard_to_join_character_to_fight
from constants import JOIN_TO_FIGHT


class UserSender:
    TEMPLATE_JOIN_TO_FIGHT = """
    ⚽️ Матч між клубами <b>{name_first_club}</b> та <b>{name_second_club}</b>! 
    
    """
    
    
    def __init__(self, 
                 first_club: Club,
                 second_club: Club,
                 match_id: int) -> None:
        self.first_club = first_club
        self.second_club = second_club
        
        
        self.characters = first_club.characters + second_club.characters
        self.match_id = match_id
        
    async def send_messages_to_users(self):
        for character in self.characters:
            await self.__send_message(character)

    def __get_text(self):
        return self.TEMPLATE_JOIN_TO_FIGHT.format(
            name_first_club  = self.first_club.name_club,
            name_second_club = self.second_club.name_club
        )

    async def __send_message(self, character: Character):
        try:
            if not character.is_bot:
                await bot.send_photo(
                    chat_id=character.characters_user_id,
                    photo=JOIN_TO_FIGHT,
                    caption= self.__get_text(),
                    reply_markup=keyboard_to_join_character_to_fight(
                        match_id=self.match_id
                    )
                )
        except Exception as E:
            logger.error(f"Failed to send message to {character.owner.user_name}\nError: {E}")
