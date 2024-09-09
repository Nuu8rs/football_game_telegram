from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.callbacks.magazine_callbacks import SelectTypeItems, SelectGradationLevelItem

def select_type_items_keyboard():
    return (InlineKeyboardBuilder()
            .button(text = "👕 Футболка", callback_data=SelectTypeItems(item="T-shirt"))
            .button(text = "🩳 Шорти",    callback_data=SelectTypeItems(item="Shorts"))
            .button(text = "🧦 Гетри",    callback_data=SelectTypeItems(item="Gaiters"))
            .button(text = "👢 Бутси",    callback_data=SelectTypeItems(item="Boots"))
            .adjust(1)
            .as_markup()
            )
    
def gradation_values_item(item: str):
    return (InlineKeyboardBuilder()
            .button(text = "Початковий рівень", 
                    callback_data=SelectGradationLevelItem(
                        gradation="standart",
                        item=item
                    ))
            .as_markup()
            )
    
def buy_item():
    return (InlineKeyboardBuilder()
            .button(text = "🏷 Купити річ", callback_data="buy_select_item")
            .as_markup()
            )