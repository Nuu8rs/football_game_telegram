from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery

from database.models.character import Character

from bot.training.callbacks.training_callbacks import NextStage 
from bot.training.routers.qte_stage import start_qte_training
from bot.training.filter.get_training import GetTraining
from bot.training.filter.training_is_active import TrainingIsActive

from services.training_service import TrainingService

from training.core.training import Training
from training.core.manager_training import TrainingManager
from training.types import Stage
from training.constans import QTE_STAGES



answer_etap_router = Router()


@answer_etap_router.callback_query(
    NextStage.filter(),
    GetTraining(),
    TrainingIsActive()
)
async def next_etap_handler(
    query: CallbackQuery,
    callback_data: NextStage,
    character: Character,
    training: Training
):
    
    await query.message.edit_reply_markup(
        reply_markup = None
    )
    stage = callback_data.next_stage
    if stage == Stage.END_TRAINIG:
        return await TrainingManager.end_user_training(
            user_id = character.characters_user_id
        )
        
    if stage in QTE_STAGES:
        return await start_qte_training(
            query,
            character
        )
    
    training.update_stage(callback_data.next_stage)
    
    score: int = training.add_score_points(callback_data.count_score)
    
    await TrainingService.update_score_user(
        user_id = character.characters_user_id,
        score = score
    )
    
    await training.send_message_by_etap()