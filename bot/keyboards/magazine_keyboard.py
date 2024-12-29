from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.magazine_callbacks import (
    SelectTypeItems, 
    SelectTypeLuxeItems,
    SelectGradationLevelItem,
    SelectLuxeGradationLevelItem,
    ByItems,
    ByLuxeItems,
    SelectBox,
)

from database.models.types import TypeBox
from bot.routers.stores.items.types import TypeItems

def menu_stores():
    return (InlineKeyboardBuilder()
            .button(text="🎽 Магазин речей", callback_data="store_items")
            .button(text="🎁 Крамниця лутбоксів", callback_data="store_boxes")
            .button(text="⚡ Крамниця енергії", callback_data="massage_room")
            .button(text="💎 Ексклюзивний магазин", callback_data="store_luxury")
            .button(text="🏦 Банк", callback_data="bank")
            .adjust(1)
            .as_markup()
            )


def select_type_items_keyboard(type_item: TypeItems = TypeItems.DEFAULT_ITEM):
    callback_data =  SelectTypeItems if type_item == TypeItems.DEFAULT_ITEM else SelectTypeLuxeItems
    
    return (InlineKeyboardBuilder()
            .button(text = "👕 Футболка", callback_data=callback_data(item="T_SHIRT"))
            .button(text = "🩳 Шорти",    callback_data=callback_data(item="SHORTS"))
            .button(text = "🧦 Гетри",    callback_data=callback_data(item="GAITERS"))
            .button(text = "👢 Бутси",    callback_data=callback_data(item="BOOTS"))
            .adjust(1)
            .as_markup()
            )
    
def gradation_values_item(
    item_сategory: str, 
    max_level_item: int,
    type_item: TypeItems = TypeItems.DEFAULT_ITEM
):
    keyboard = InlineKeyboardBuilder()
    callback_data = SelectGradationLevelItem if type_item == TypeItems.DEFAULT_ITEM else SelectLuxeGradationLevelItem
    for min_level_item in range(1,max_level_item+1):
        keyboard.button(text=f"🔰 з {min_level_item} рівня", 
                        callback_data=callback_data(
                            min_level_item=min_level_item,
                            item_category=item_сategory))
    keyboard.adjust(1)
    return keyboard.as_markup()
    
def select_items_for_buy(
    items: dict,
    type_item: TypeItems = TypeItems.DEFAULT_ITEM
):
    keyboard = InlineKeyboardBuilder()
    callback = ByLuxeItems if type_item == TypeItems.LUXE_ITEM else ByItems
    for item in items:
        keyboard.button(
            text = item['name'], 
            callback_data=callback(
                id_item = item['id']
            )
    )
    return keyboard.adjust(1).as_markup()
    
def buy_item():
    return (InlineKeyboardBuilder()
            .button(text = "🏷 Купити річ", callback_data="buy_select_item")
            .as_markup()
            )

#===================BOXES
def select_box():
    return (InlineKeyboardBuilder()
            .button(
                text="▪️ Маленький бокс футболіста", 
                callback_data=SelectBox(
                    type_box = TypeBox.SMALL_BOX
                )
            )
            .button(
                text="◾️ Середній бокс футболіста", 
                callback_data=SelectBox(
                    type_box = TypeBox.MEDIUM_BOX
                )
            )
            .button(
                text="◼️ Преміум Бокс",
                callback_data=SelectBox(
                    type_box = TypeBox.LARGE_BOX
                )
            )
            
            .adjust(1)
            .as_markup()
            )

def buy_box(url_payment: str):
    return (InlineKeyboardBuilder()
            .button(
                text = "🎁 Купити бокс", 
                url = url_payment
            )
            .as_markup()
            )