from typing import Any, Union
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

from training.core.manager_training import TrainingManager

from bot.training.callbacks.training_callbacks import (
    JoinToTraining,
    QTECallback,
    NextStage
)

ApprovedCallbacks = Union[JoinToTraining, QTECallback, NextStage]

class TrainingIsActive(BaseFilter):
    
    async def __call__(self, query: CallbackQuery ,*arg, **kwg) -> Any:
        callback_data: ApprovedCallbacks = kwg.get('callback_data', None)
        if not callback_data:
            return False
        training_id = callback_data.training_id
        if training_id != TrainingManager.training_id:
            await query.answer(
                text = "Тренування вже не активне",
                show_alert = True
            )
            await query.message.edit_reply_markup(reply_markup = None)
            return False
        return True