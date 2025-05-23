from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from ..callbacks.league_callbacks import (
    JoinToFight, 
    ViewCharacterRegisteredInMatch,
    EpizodeDonateEnergyToMatch
                                        )
from .utils_keyboard import menu_plosha

def keyboard_to_join_character_to_fight(match_id: int):
    return (
        InlineKeyboardBuilder()
        .button(text = "⚽️ Приєднатися до матчу!", callback_data=JoinToFight(
            match_id=match_id
        ))
        
        .button(text = "❔ Хто зареєструвався на матч",
                callback_data=ViewCharacterRegisteredInMatch(match_id=match_id))
        .adjust(1)
        .as_markup()
    )
    
def donate_energy_to_match(match_id: str, time_end_goal: int):
    return (
        InlineKeyboardBuilder()
        .button(
            text = "🔱 Підвищити шанс голу",
            callback_data = EpizodeDonateEnergyToMatch(
                match_id      = match_id,
                time_end_goal = time_end_goal
            )
        )
        .as_markup()
    )
    
    
def menu_league_zone():
    return(ReplyKeyboardBuilder()
           .button(text = "📝 Зареєструватися в матч")
           .button(text = "📋 Таблиця")
        #    .button(text = "🔋 Задонатити в матч")
           .button(text = "📅 Календар ігор")
           .button(text = "📊 Результати")
           .attach(menu_plosha())
           .adjust(1,2,2,1)
           .as_markup(resize_keyboard = True)
           )
    
def menu_beast_league_zone():
    return(ReplyKeyboardBuilder()
           .button(text = "📝 Зареєструватися в матч Єврокубків")
           .button(text = "📋 Таблиця Єврокубків")
        #    .button(text = "🔋 Задонатити в матч")
           .button(text = "📅 Календар Єврокубків")
           .button(text = "📊 Результати Єврокубків")
           .attach(menu_plosha())
           .adjust(1,1,1,2,1)
           .as_markup(resize_keyboard = True)
           )
    
def menu_national_cup_ukraine():
    return(ReplyKeyboardBuilder()
           .button(text = "📝 Зареєструватися в матч Кубка України")
           .button(text = "📋 Таблиця Кубка України")
        #    .button(text = "🔋 Задонатити в матч Кубка України")
           .button(text = "📅 Календар Кубка України")
           .button(text = "📊 Результати Кубка України")
           .attach(menu_plosha())
           .adjust(1,1,1,2,1)
           .as_markup(resize_keyboard = True)
           )
    

def menu_new_club_league():
    return(ReplyKeyboardBuilder()
           .button(text = "📝 Зареєструватися в матч Нових клубів")
           .button(text = "📋 Таблиця Нових клубів")
        #    .button(text = "🔋 Задонатити в матч Нових клубів")
           .button(text = "📅 Календар Нових клубів")
           .button(text = "📊 Результати Нових клубів")
           .attach(menu_plosha())
           .adjust(1,1,1,2,1)
           .as_markup(resize_keyboard = True)
           )