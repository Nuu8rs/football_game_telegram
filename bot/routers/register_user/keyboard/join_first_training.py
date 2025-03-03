from aiogram.types import InlineKeyboardMarkup

from aiogram.utils.keyboard import InlineKeyboardBuilder



def join_first_training() -> InlineKeyboardMarkup:
    return (InlineKeyboardBuilder()
            .button(
                text = "РОЗПОЧАТИ ПЕРШЕ ТРЕНУВАННЯ",
                callback_data = "join_first_training"
            )
            .as_markup()
            )