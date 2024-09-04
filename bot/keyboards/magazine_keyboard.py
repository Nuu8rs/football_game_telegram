from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.callbacks.magazine_callbacks import SelectTypeItems

from constants import gradation_level

def select_type_items_keyboard():
    return (InlineKeyboardBuilder()
            .button(text = "👕 Футболка", callback_data=SelectTypeItems(item="T-shirt"))
            .button(text = "🩳 Шорти",    callback_data=SelectTypeItems(item="Shorts"))
            .button(text = "👢 Бутси",    callback_data=SelectTypeItems(item="Boots"))
            .button(text = "🧦 Гетри",    callback_data=SelectTypeItems(item="gaiters"))
            .adjust(1)
            .as_markup()
            )
    
def gradation_values_item(item: str):
    keyboard = InlineKeyboardBuilder()
    for gradation in gradation_level:
        keyboard.button(text = f"[{gradation}] {item}", callback_data=gradation)
    
    keyboard.adjust(2)
    return keyboard.as_markup()