from aiogram.filters.callback_data import CallbackData
from datetime import timedelta

class ViewMyItem(CallbackData, prefix="view_my_item"):
    item_id: int
    
class PutOnItem(CallbackData, prefix="put_on_item"):
    item_id: int
    

class SellMyItem(CallbackData, prefix="sell_my_item"):
    item_id: int