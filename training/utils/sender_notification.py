import asyncio
from datetime import datetime
import time

from aiogram import Bot
from aiogram.types import Message

from bot.training.keyboard.training import keyboard_join_training

from database.models.character import Character
from services.character_service import CharacterService
from services.training_service import TrainingService
from utils.rate_limitter import rate_limiter

from loader import bot
from logging_config import logger

from .text_stage import TEXT_TRAINING



class NotificationSender:
    _bot: Bot = bot
    _text_notification = TEXT_TRAINING.START_TRAINING_MESSAGE

    def __init__(self, start_time: datetime) -> None:
        self.start_time = start_time
        self.send_queue = asyncio.Queue()

    @property
    def start_time_notification(self):
        hours = self.start_time.hour
        minutes = self.start_time.minute
        return f"{hours}:{minutes}"
        
    async def send_notification(self):
        all_characters = await CharacterService.get_all_users_not_bot()
        for character in all_characters:
            await self.send_queue.put(character)

        asyncio.create_task(self._send_notification())
        
    async def _send_notification(self):
        while not self.send_queue.empty():
            character = await self.send_queue.get()
            await self.__send_message(character)
    
    
    @rate_limiter        
    async def __send_message(self, character: Character):
        try:
            await self._bot.send_message(
                chat_id=character.characters_user_id,
                text=self._text_notification.format(
                    time_start = self.start_time_notification
                ),
            )
        except Exception as E:
            logger.error(f"Failed to send message to {character.characters_user_id}\nError: {E}")