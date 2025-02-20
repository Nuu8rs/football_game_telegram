from uuid import uuid4

from aiogram import Bot
from loader import bot

from training.types import Stage, TextParamsTraning
from training.utils.get_params_by_stage import GetParams
from training.utils.text_stage import TextStage

from bot.training.keyboard.training import next_stage_keyboard

class Training:
    
    _bot: Bot = bot
    
    
    def __init__(
        self,
        user_id: int,
        character_id: int,
        training_id: int
    ) -> None:
        
        self.training_id: int = training_id
        self.user_id: int = user_id
        self.character_id: int = character_id
        
        self.stage: Stage = Stage.STAGE_1
        self.score: int = 0
        
    def update_stage(self, stage: Stage) -> None:
        self.stage = stage
        
    def add_score_points(self, points: int) -> int:
        self.score += points
        return self.score
    
    async def send_message_by_etap(self) -> None:
        
        text_params: TextParamsTraning = await GetParams.get_params_epizode(
            stage=self.stage,
        ) 
        await self._send_mesaage_etap(text_params=text_params)
        
    async def _send_mesaage_etap(self, text_params: TextParamsTraning):
        text_etap = TextStage.get_text(text_params)
        if text_params.patch_to_photo:
            return await self.__send_photo_etap(
                text_params = text_params,
                text_etap = text_etap
            )
            
        return await self.__send_message_etap(
            text_etap = text_etap
        )
        
    async def __send_photo_etap(
        self, 
        text_params: TextParamsTraning,
        text_etap: str
    ):
        await self._bot.send_photo(
            chat_id=self.user_id,
            photo=text_params.photo,
            caption=text_etap,
            reply_markup=next_stage_keyboard(
                current_stage = self.stage,
                training_id = self.training_id

            )
        )
        
    async def __send_message_etap(
        self, 
        text_etap: str
    ):
        await self._bot.send_message(
            chat_id=self.user_id,
            text=text_etap,
            reply_markup=next_stage_keyboard(
                current_stage = self.stage,
                training_id = self.training_id
            )
        )
