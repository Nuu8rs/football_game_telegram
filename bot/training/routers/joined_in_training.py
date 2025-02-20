from datetime import datetime
from typing import Optional, Tuple

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from bot.training.callbacks.training_callbacks import JoinToTraining 
from bot.training.keyboard.buy_training_key import to_menu_buy_training_key

from constants import NEED_TRAINING_KEY

from training.constans import TIME_REGISTER_TRAINING
from training.core.manager_training import TrainingManager

from database.models.character import Character
from database.models.training import CharacterJoinTraining, TrainingTimer

from services.training_service import TrainingService
from services.character_service import CharacterService

from loader import bot
from logging_config import logger

from training.constans import (
    MAX_LIMIT_JOIN_CHARACTERS,
    TIME_TRAINING
)


join_trainig_router = Router()

@join_trainig_router.callback_query(
    JoinToTraining.filter(),
)
async def joined_to_training(
    query: CallbackQuery,
    callback_data: JoinToTraining,
    character: Character
):
    join_training = TrainingJoinManager(character)
    text_join, keyboard = await join_training.join()
    if keyboard:
        return await query.message.answer_photo(
            photo = NEED_TRAINING_KEY,
            caption = text_join,
            reply_markup = keyboard
        )
    await query.answer(
        text = text_join,
        show_alert=True,
        cache_time=5
    )
    
@join_trainig_router.message(
    F.text == "👨🏻‍🏫 Тренування з тренером"
)
async def joined_to_training(
    message: Message,
    character: Character
):
    _text = """
🔑 <b>Ваші ключі: {count}</b>  

Ключі потрібні для участі у тренуваннях. ⚽🏆  
Один ключ = один вхід на тренування.  

⏳ Не забувайте використовувати їх, щоб покращити навички та стати кращим гравцем!  
"""
    
    await message.answer(
        text = _text.format(
            count = character.training_key
        )
    )
    join_training = TrainingJoinManager(character)
    text_join, keyboard = await join_training.join()
    if keyboard:
        return await message.answer_photo(
            photo = NEED_TRAINING_KEY,
            caption = text_join,
            reply_markup = keyboard
        )
    await message.answer(
        text = text_join,
        reply_markup = keyboard
    )
    
class TrainingJoinManager:
    def __init__(self, character: Character) -> None:
        self.character: Character = character
        self.user_id: int = character.characters_user_id
        self.joined_user: Optional[CharacterJoinTraining] = None
        self.training_timer: Optional[TrainingTimer] = None
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    async def join(self) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
        await self._load_training_data()
        
        if not self.training_timer:
            return "Тренування не зареєстровано", None
        
        if self._is_user_already_joined():
            return "Ви вже зареєстровані на тренування", None
    
        if self._is_training_finished():
            return "Тренування завершено", None    
    
        if not self._is_user_already_joined() and self.joined_user:
            if not self._has_training_key():
                return "⚽ <b>Ти вже пройшов тренування, але можеш повернутися ще раз!</b> 🏆\n\n🔑 Вхід можливий лише за ключі. Готовий знову випробувати свої сили?", to_menu_buy_training_key()
            else:
                return await self._start_training_by_key()
        
        if not self._is_registration_open():
            return "Не час для реєстрації на тренування", None
        
        if not self._has_training_key():
            return "У вас немає ключа для тренування", None
        

        
        if await self._is_training_full() and not self.character.vip_pass_is_active:
            return "Немає вільних місць на тренування", None

        return await self._register_user()

    async def _load_training_data(self) -> None:
        self.joined_user: Optional[CharacterJoinTraining] = await TrainingService.user_is_join_to_training(self.user_id)
        self.training_timer = await TrainingService.get_last_training_timer()
        if self.training_timer:
            self.start_time = self.training_timer.time_start
            self.end_time = self.start_time + TIME_TRAINING

    def _is_registration_open(self) -> bool:
        return bool(self.start_time and (self.start_time - TIME_REGISTER_TRAINING) < datetime.now() < self.start_time)

    def _is_training_finished(self) -> bool:
        return bool(self.end_time and self.end_time < datetime.now())

    def _has_training_key(self) -> bool:
        return self.character.training_key > 0

    def _is_user_already_joined(self) -> bool:
        return bool(self.joined_user and not self.joined_user.training_is_end)

    async def _is_training_full(self) -> bool:
        joined_users: list = await TrainingService.get_joined_users()
        return len(joined_users) >= MAX_LIMIT_JOIN_CHARACTERS

    async def _register_user(self) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
        await TrainingService.add_character_to_training(
            user_id = self.user_id, 
            character_id = self.character.id
        )
        await CharacterService.remove_training_key(self.character.id)
        return "Ви успішно зареєструвались на тренування", None

    async def _start_training_by_key(self) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
        await TrainingManager.start_user_training(
            user_id = self.user_id,
            character_id = self.character.id
        )
        await CharacterService.remove_training_key(self.character.id)
        await TrainingService.anulate_user_training(self.user_id)
        return "Ви успішно зареєструвались на тренування за ключ", None
