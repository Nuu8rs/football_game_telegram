from aiogram.filters.callback_data import CallbackData
from datetime import timedelta


class JoinToFight(CallbackData, prefix="join_to_fight"):
    match_id: str
    
    
class ViewCharacterRegisteredInMatch(CallbackData, prefix = "view_reg_match"):
    match_id: str