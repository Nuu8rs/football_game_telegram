from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from .utils_keyboard import menu_plosha

def menu_hall_fame():
    return (
        ReplyKeyboardBuilder()
        .button(text = "💪Рейтинг за силою гравця")
        .button(text = "📊 Рейтинг за рівнем гравця")
        .button(text = "🏆 Рейтинг команд за силою")
        .button(text = "🏃🏼 Рейтинг бомбардувальників")
        .attach(menu_plosha())
        .adjust(1,2,1)
        .as_markup(resize_keyboard = True)
    )