from typing import Dict, Optional
from .training import Training
from .end_training import EndTraining
from training.duel.duel_manager import DuelManager

from services.training_service import TrainingService   

from logging_config import logger


class TrainingManager:
    _trainings: Dict[int, Training] = {}
    training_id: Optional[int] = None


    @classmethod
    def get_or_create_training(cls, user_id: int, character_id: int) -> Training:
        if user_id not in cls._trainings:
            cls._trainings[user_id] = Training(
                user_id      = user_id, 
                character_id = character_id,
                training_id  = cls.training_id
            )
        return cls._trainings[user_id]

    @classmethod
    def get_training(cls, user_id: int) -> Training:
        return cls._trainings.get(user_id, None)

    @classmethod
    async def start_training(cls) -> None:
        
        day_training = await TrainingService.get_last_training_timer()
        if not day_training:
            return
        cls.training_id = day_training.id
        
        joined_users = await TrainingService.get_joined_users()
        for user in joined_users:
            if user.user_id in cls._trainings:
                continue
            await cls.start_user_training(
                user_id      = user.user_id,
                character_id = user.character_id
            )
            
    @classmethod
    async def start_user_training(cls, user_id: int, character_id: int) -> None:
        try:
            training = cls.get_or_create_training(
                user_id = user_id, 
                character_id = character_id
            )
            await training.send_message_by_etap()
        except Exception as E:
            logger.error(f"Failed to start training for user {user_id}\nError: {E}")

    @classmethod
    async def end_all_trainings(cls) -> None:
        await DuelManager.end_all_duels()
        for user_id, training in cls._trainings.items():
            end_training = EndTraining(
                training = training
            )
            await end_training.end_training()
        cls.training_id = None
        
    @classmethod
    async def end_user_training(cls, user_id: int) -> None:
        if user_id in cls._trainings:
            end_training = EndTraining(
                training = cls._trainings[user_id]
            )
            await end_training.end_training()   
            del cls._trainings[user_id]
        
    