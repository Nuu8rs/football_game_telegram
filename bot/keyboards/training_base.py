from aiogram.utils.keyboard import ReplyKeyboardBuilder
from .utils_keyboard import menu_plosha

def menu_training_base():
    return (ReplyKeyboardBuilder()
            .button(text = "🖲 Тренування")
            .button(text = "👨🏻‍🏫 Тренування з тренером")
            .button(text = "🏫 Навчальний центр")
            .button(text = "💪🏻 Посилення команди")
            .button(text = "🏪🔋 Крамниця енергії")
            .attach(menu_plosha())
            .adjust(1,1,2,1,1)
            .as_markup(resize_keyboard=True)
            )
    