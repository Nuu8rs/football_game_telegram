from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove

from database.models.user_bot import UserBot

from constants import date_is_get_reward_christmas_tree

from ..callbacks.menu_callbacks import NextInstruction


def main_menu(user: UserBot):
    keyboard = ReplyKeyboardBuilder()
    if not user.characters:
        keyboard.button(text="⚽️ Створити персонажа")
    else:
        keyboard.button(text="⚽️ Матчі")
        keyboard.button(text = "🖲 Тренування")
        keyboard.button(text = "🗄 Тренувальна база")
        keyboard.button(text ="🏃‍♂️ Мій футболіст")
        keyboard.button(text ="👥 Команда")
        keyboard.button(text = "🏬 Торговий квартал")
        keyboard.button(text = "🏆 Зал слави")
        # keyboard.button(text = "🥅 ПВП-пенальті")
        keyboard.button(text = "📊 Статистика")
        keyboard.button(text = "🗣 Cпілкування")
        
    if date_is_get_reward_christmas_tree():
        keyboard.button(text = "🎄 Новорічна ялинка")
    return keyboard.adjust(2).as_markup(resize_keyboard = True)

def menu_instruction(index_instruction: int):
    return (InlineKeyboardBuilder()
            .button(text = "➡️ Далі", callback_data=NextInstruction(index_instruction=index_instruction))
            .as_markup()
            )
    
def remove_keyboard():
    return ReplyKeyboardRemove(remove_keyboard=True)

def test():
    return ReplyKeyboardBuilder().button(text="TEST").as_markup(resize_keyboard = True, is_persistent=True, selective=True)
    