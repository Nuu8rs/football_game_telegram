from aiogram.utils.keyboard import ReplyKeyboardBuilder
from .utils_keyboard import menu_plosha

from datetime import datetime

from constants import DUEL_START_DAY_SEASON, DUEL_END_DAY_SEASON

def menu_hall_fame():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text = "💪Рейтинг за силою гравця")
    keyboard.button(text = "📊 Рейтинг за рівнем гравця")
    keyboard.button(text = "🏆 Рейтинг команд за силою")
    keyboard.button(text = "🏃🏼 Рейтинг бомбардирів")
    keyboard.button(text = "📊 Клубний рейтинг")
    
    
    if (datetime.now().day >= DUEL_START_DAY_SEASON) and (datetime.now().day <= DUEL_END_DAY_SEASON):
        keyboard.button(text = "👥 Рейтинг ПВП-пеналті") 
    
    keyboard.attach(menu_plosha())    
    keyboard.adjust(2,2,1,1)
    return keyboard.as_markup(resize_keyboard = True)
    