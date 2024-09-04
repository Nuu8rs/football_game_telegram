from aiogram.filters.callback_data import CallbackData

class SwitchClub(CallbackData, prefix="switch_club"):
    current_index:int
    total_items:int
    side:str