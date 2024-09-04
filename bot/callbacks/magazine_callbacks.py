from aiogram.filters.callback_data import CallbackData
from datetime import timedelta


class SelectTypeItems(CallbackData, prefix="select_type_items"):
    item: str