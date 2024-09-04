from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database.models import UserBot

def main_menu(user: UserBot):
    keyboard = ReplyKeyboardBuilder()
    if not user.characters:
        keyboard.button(text="⚽️ Створити персонажа")
    else:
        keyboard.button(text ="⚽️ Мій персонаж")
        keyboard.button(text ="🖲 Тренажерний зал")
        keyboard.button(text ="🎪 Мій клуб")
        keyboard.button(text = "🏟 Стадіон")
        keyboard.button(text = "🏬 Магазин")
    
    return keyboard.adjust(2).as_markup(resize_keyboard = True)