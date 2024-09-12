from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message
from datetime import datetime
from constants import HOURS_END_TIME

class CheckTimeFilterMessage(BaseFilter):
    
    def __init__(self) -> None:
        pass
        
    async def __call__(self, event: Message) -> Any:
        current_date = datetime.now() 
        # if current_date.hour >= HOURS_END_TIME:
        #     await event.answer("Ви не можете поповнити енергію в поточний момент")
        #     return False
        # elif current_date.day >= 19:
        #     await event.answer("Ліга вже закінчилася, ви зможе🗄 Тренувальна базате поповнити енергію, після початку нової ліги")
        #     return False
        return True