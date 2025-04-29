from aiogram.types import InlineKeyboardMarkup

from aiogram.utils.keyboard import InlineKeyboardBuilder


def new_member_bonus_keyboard() -> InlineKeyboardMarkup:
    return (
        InlineKeyboardBuilder()
        .button(
            text = "Получити додаткові характеристики",
            callback_data = "get_new_member_bonus"
        )
        .as_markup()
    )