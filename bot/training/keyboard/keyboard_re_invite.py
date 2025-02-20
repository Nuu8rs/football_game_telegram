import random
import time

from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.training.callbacks.training_callbacks import JoinToTraining

from database.models.character import Character
from .buy_training_key import to_menu_buy_training_key

def re_join_training(character: Character):
    if character.training_key:
        return _join_to_training()
    else:
        return to_menu_buy_training_key()
    
def _join_to_training():
    return (
        InlineKeyboardBuilder()
        .button(
            text="Присоединиться к тренировке",
            callback_data=JoinToTraining(end_time_join = 1)
        )
        .as_markup()
    )