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


class RegisterInTrainingSender:
    _bot: Bot = bot
    _text_register = TEXT_TRAINING.REGISTER_IN_TRAINING_MESSAGE
    _max_retries = 4
    
    def __init__(self, end_time: datetime) -> None:
        self.end_time = end_time 
        
        self.messages: dict[int, Message] = {}
        self.send_queue: asyncio.Queue[tuple[Character, int]] = asyncio.Queue()
        self._last_count: int = 0
        
        self._task_worker_sender = asyncio.create_task(
            self._worker_sender_message()
        )
        self._task_worker_edit = asyncio.create_task(
            self._worker_edit_keyboard()
        )
            
        self._task_worker_close = asyncio.create_task(
            self._worker_close()
        )
         
    @property
    def _end_time(self) -> int:
        return int(self.end_time.timestamp())
            
    async def start_send_message(self):
        all_characters = await CharacterService.get_all_users_not_bot()
        for character in all_characters:
            await self.send_queue.put((character, 0 ))
    
    @rate_limiter
    async def __send_message(self, character: Character) -> Message | None:
        try:
            message = await self._bot.send_message(
                chat_id=character.characters_user_id,
                text=self._text_register,
                reply_markup=keyboard_join_training(
                    count_users=0,
                    end_time_join=self._end_time,
                ),
            )
            return message
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения {character.characters_user_id}: {e}")
            return None

    async def _worker_sender_message(self):  
        try:
            while True:
                character, attempt = await self.send_queue.get()
                message = await self.__send_message(character)
                if message:
                    self.messages[character.characters_user_id] = message
                elif attempt < self._max_retries:
                    await asyncio.sleep(2 ** attempt)  
                    await self.send_queue.put((character, attempt + 1))
                self.send_queue.task_done()
        except asyncio.CancelledError:
            logger.info("Sender worker cancelled")
        except Exception as e:
            logger.error(e)

            
        
    async def _worker_edit_keyboard(self):
        while True:
            await asyncio.sleep(60)    
            count = await TrainingService.count_joinded_user()
            if count == self._last_count:
                continue
            for message in self.messages.values():
                await self._edit_keyboard(message, count)

            self._last_count = count
            
    @rate_limiter
    async def _edit_keyboard(self, message: Message, count: int):
        try:
            await message.edit_reply_markup(
                reply_markup = keyboard_join_training(
                    count_users = count,
                    end_time_join = self._end_time
                )
            )  
        except Exception as E:
            logger.error(E)

    async def _worker_close(self):
        current_time = time.time()
        time_sleep = self._end_time - current_time
        await asyncio.sleep(time_sleep)
        self._task_worker_edit.cancel()
        self._task_worker_sender.cancel()
        self.messages.clear()
