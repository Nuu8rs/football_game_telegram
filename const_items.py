from database.models.item import Item
from constants import ItemCategory, BASE_STATS_ITEMS
import json

def create_t_shirt_const() -> Item:
    return Item(
    name = "👕 Футболка",
    category = ItemCategory.T_SHIRT,
    level_required = 0,
    price = 10,
    stats = json.dumps(BASE_STATS_ITEMS)

)

def create_short_const() -> Item:
    return Item(
    name = "🩳 Шорти",
    category = ItemCategory.SHORTS,
    level_required = 0,
    price = 10,
    stats = json.dumps(BASE_STATS_ITEMS)
        )

def create_gaiterst_const() -> Item:
    return Item(
    name = "🧦 Гетри",
    category = ItemCategory.GAITERS,
    level_required = 0,
    price = 10,
    stats = json.dumps(BASE_STATS_ITEMS)

)

def create_boots_const() -> Item:
    return Item(
    name = "👢 Бутси",
    category = ItemCategory.BOOTS,
    level_required = 0,
    price = 10,
    stats = json.dumps(BASE_STATS_ITEMS))



def CREATE_ITEM_CONST(position: ItemCategory) -> Item:
    if position == ItemCategory.T_SHIRT:
        return create_t_shirt_const()
    elif position == ItemCategory.SHORTS:
        return create_short_const()
    elif position == ItemCategory.GAITERS:
        return create_gaiterst_const()
    elif position == ItemCategory.BOOTS:
        return create_boots_const()