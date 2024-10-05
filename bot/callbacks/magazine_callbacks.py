from aiogram.filters.callback_data import CallbackData

class SelectTypeItems(CallbackData, prefix="select_type_items"):
    item: str
    
class SelectGradationLevelItem(CallbackData, prefix = "select_gradation_item"):
    min_level_item: int
    item_category: str

class ByItems(CallbackData, prefix = "buyItem"):
    id_item: int