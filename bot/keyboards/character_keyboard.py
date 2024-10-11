from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models.item import Item

from bot.callbacks.items_callbacks import ViewMyItem, PutOnItem, SellMyItem
from bot.callbacks.switcher import SwitchMyItem

from .utils_keyboard import switch_buttons

def character_keyboard():
    return (InlineKeyboardBuilder()
            .button(text = "📦 Мій інвентар", callback_data="my_inventory")
            .button(text = "🫂 Реферальна система", callback_data="referal_system")
            .adjust(1)
            .as_markup()
            )
    
    
def my_inventory_keyboard(items: list[Item], current_index: int):
    items_per_page = 5
    
    keyboard = InlineKeyboardBuilder()
    keyboard.attach(switch_buttons(
        total_items=len(items),
        current_index=current_index,
        switch_type=SwitchMyItem,
        items_per_page=items_per_page
    ))
    
    for item in items:
        keyboard.button(text = item.name, callback_data=ViewMyItem(item_id=item.id))
        
    keyboard.adjust(3, *[1]*items_per_page)
    return keyboard.as_markup()

def funtctional_item(item_id: int):
    return (InlineKeyboardBuilder()
            .button(text="🏷 Одягнути річ",
                    callback_data=PutOnItem(
                                item_id=item_id
                                            )
                    )
            .button(text = "💳 Продати річ", 
                    callback_data=SellMyItem(
                        item_id=item_id
                    )
                    )
            .as_markup()
            )
