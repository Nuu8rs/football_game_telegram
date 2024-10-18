from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models.item import Item
from database.models.character import Character

from bot.callbacks.items_callbacks import ViewMyItem, PutOnItem, SellMyItem, UnEquipItem
from bot.callbacks.switcher import SwitchMyItem

from .utils_keyboard import switch_buttons

emj_item = {
    "BOOTS" : "👞",
    "GAITERS" : "🧦",
    "SHORTS" : "🩳",
    "T_SHIRT" : "👕",
}

def character_keyboard():
    return (InlineKeyboardBuilder()
            .button(text = "📦 Мій інвентар", callback_data="my_inventory")
            .button(text = "🫂 Реферальна система", callback_data="referal_system")
            .adjust(1)
            .as_markup()
            )
    
    
def my_inventory_keyboard(items: list[Item], current_index: int, character: Character):
    items_per_page = 5
    
    start_index = current_index
    end_index = min(start_index + items_per_page, len(items))    

    keyboard = InlineKeyboardBuilder()
    keyboard.attach(switch_buttons(
        total_items=len(items),
        current_index=current_index,
        switch_type=SwitchMyItem,
        items_per_page=items_per_page
    ))
    
    for item in items[start_index:end_index]:
        text_item = emj_item[item.category] + (" ✅ " if item.id in character.items_ids else " ❌ ") + item.name
        keyboard.button(text = text_item, callback_data=ViewMyItem(item_id=item.id))
        
    keyboard.adjust(3, *[1]*items_per_page)
    return keyboard.as_markup()


def funtctional_item(item_id: int, character: Character):
    keyboard = InlineKeyboardBuilder()
    if item_id in character.items_ids:
        keyboard.button(text = "📤 Зняти річ", 
                        callback_data= UnEquipItem(item_id=item_id))
    else:
        keyboard.button(text="🏷 Одягнути річ",
                        callback_data= PutOnItem(item_id=item_id))
            
        
    keyboard.button(text = "💳 Продати річ",
                    callback_data=SellMyItem(item_id=item_id))
        
    return keyboard.adjust(1).as_markup()