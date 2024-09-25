from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.callbacks.magazine_callbacks import SelectTypeItems, SelectGradationLevelItem
from bot.callbacks.magazine_callbacks import ByItems

def select_type_items_keyboard():
    return (InlineKeyboardBuilder()
            .button(text = "👕 Футболка", callback_data=SelectTypeItems(item="T_SHIRT"))
            .button(text = "🩳 Шорти",    callback_data=SelectTypeItems(item="SHORTS"))
            .button(text = "🧦 Гетри",    callback_data=SelectTypeItems(item="GAITERS"))
            .button(text = "👢 Бутси",    callback_data=SelectTypeItems(item="BOOTS"))
            .adjust(1)
            .as_markup()
            )
    
def gradation_values_item(item_сategory: str, max_level_item):
    keyboard = InlineKeyboardBuilder()
    
    for min_level_item in range(1,max_level_item+1):
        keyboard.button(text=f"🔰 з {min_level_item} рівня", 
                        callback_data=SelectGradationLevelItem(
                            min_level_item=min_level_item,
                            item_category=item_сategory))
    keyboard.adjust(1)
    return keyboard.as_markup()
    
def select_items_for_buy(items: dict):
    keyboard = InlineKeyboardBuilder()
    
    for item in items:
        keyboard.button(text = item['name'], callback_data=ByItems(
            id_item = item['id']
        ))
    return keyboard.adjust(1).as_markup()
    
def buy_item():
    return (InlineKeyboardBuilder()
            .button(text = "🏷 Купити річ", callback_data="buy_select_item")
            .as_markup()
            )