from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove

from datetime import datetime

from database.models.user_bot import UserBot
from ..callbacks.menu_callbacks import NextInstruction

from constants import date_is_get_reward_christmas_tree

from constants import (
    END_DAY_BEST_LEAGUE, 
    START_DAY_BEST_LEAGUE,
    START_DAY_BEST_20_CLUB_LEAGUE,
    END_DAY_BEST_20_CLUB_LEAGUE)

def menu_best_league(keyboard: ReplyKeyboardBuilder):
    current_day = datetime.now().day
    if current_day >= START_DAY_BEST_LEAGUE and current_day <= END_DAY_BEST_LEAGUE:
        keyboard.button(text = "🏆 Єврокубки")
    

def menu_best_20_club(keyboard: ReplyKeyboardBuilder):
    current_day = datetime.now().day
    if current_day >= START_DAY_BEST_20_CLUB_LEAGUE and current_day <= END_DAY_BEST_20_CLUB_LEAGUE:
        keyboard.button(text = "🏆 Національний Кубок України")
    


def main_menu(user: UserBot):
    keyboard = ReplyKeyboardBuilder()
    if not user.characters:
        keyboard.button(text="⚽️ Створити персонажа")
    else:
        keyboard.button(text = "🏟 Стадіон")
        menu_best_league(keyboard)
        menu_best_20_club(keyboard)
        keyboard.button(text = "🗄 Тренувальна база")
        keyboard.button(text ="⚽️ Мій футболіст")
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
    