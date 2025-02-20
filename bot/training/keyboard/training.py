import random

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.training.callbacks.training_callbacks import (
    JoinToTraining, 
    NextStage
)

from training.constans import MAX_LIMIT_JOIN_CHARACTERS
from training.types import Stage


def keyboard_join_training(
    count_users: int,
    end_time_join: int,
):
    text = "Приєднатися до тренування [{count_users}/{max_limit}]".format(
        count_users = count_users,
        max_limit = MAX_LIMIT_JOIN_CHARACTERS
    )
    
    return (
        InlineKeyboardBuilder()
        .button(text = text,
                callback_data = JoinToTraining(
                    end_time_join = end_time_join,
                )
        )
        .adjust(1)
        .as_markup()
    )
    
    
def next_stage_keyboard(
    current_stage: Stage,
    training_id: int
):
    keyboard = InlineKeyboardBuilder()
    random_points = random.sample(range(-5, 6), 3)
    emoji_points = dict(zip(["1️⃣", "2️⃣", "3️⃣"], random_points))

    for emj, score in emoji_points.items():
        keyboard.button(
            text=emj,
            callback_data=NextStage(
                next_stage=current_stage.next_stage(),
                count_score=score,
                training_id = training_id
            )
        )
    return keyboard.as_markup()