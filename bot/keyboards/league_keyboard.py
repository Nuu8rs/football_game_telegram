from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from ..callbacks.league_callbacks import JoinToFight
from .utils_keyboard import menu_plosha

def keyboard_to_join_character_to_fight(match_id: int):
    return (
        InlineKeyboardBuilder()
        .button(text = "⚽️ Приєднатися до матчу!", callback_data=JoinToFight(
            match_id=match_id
        ))
        .as_markup()
    )
    
def menu_league_zone():
    return(ReplyKeyboardBuilder()
           .button(text = "📝 Зареєструватися в матч")
           .button(text = "📋 Таблиця")
           .button(text = "📅 Календар ігор")
           .button(text = "📊 Результати")
           .attach(menu_plosha())
           .adjust(1,1,2,1)
           .as_markup(resize_keyboard = True)
           )
    
    
