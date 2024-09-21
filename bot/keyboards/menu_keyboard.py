from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove
from database.models.user_bot import UserBot
from ..callbacks.menu_callbacks import NextInstruction

def main_menu(user: UserBot):
    keyboard = ReplyKeyboardBuilder()
    if not user.characters:
        keyboard.button(text="⚽️ Створити персонажа")
    else:
        keyboard.button(text = "🏟 Стадіон")
        keyboard.button(text ="🖲 Тренажерний зал")
        keyboard.button(text ="⚽️ Мій персонаж")
        keyboard.button(text ="🎪 Мій клуб")
        keyboard.button(text = "🏫 Навчальний центр")
        keyboard.button(text = "🗄 Тренувальна база")
        keyboard.button(text = "🏬 Магазин")
        keyboard.button(text = "🏆 Зал слави")

    
    return keyboard.adjust(2).as_markup(resize_keyboard = True)

def menu_instruction(index_instruction: int):
    return (InlineKeyboardBuilder()
            .button(text = "➡️ Далі", callback_data=NextInstruction(index_instruction=index_instruction))
            .as_markup()
            )
    
def remove_keyboard():
    return ReplyKeyboardRemove(remove_keyboard=True)