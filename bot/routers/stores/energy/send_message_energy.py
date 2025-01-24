from enum import Enum

from aiogram import Bot
from loader import bot

from database.models.character import Character

from logging_config import logger

class TextTypes(str, Enum):
    NO_ENERGY = """
❗ <b>Енергія на нулі!</b>  

🔋 Ваш рівень енергії повністю вичерпано, і ви не зможете продовжити гру без поповнення.  

✅ <i>Не зупиняйтесь — поновіть енергію, щоб повернутись до гри!</i>  
✅ <i>Тепер саме час поповнити запас і повернутися на поле з новими силами!</i>  

⚡️ <b>Не чекайте!</b>  
Поповніть енергію зараз і продовжуйте боротися за перемогу! 
"""

    LOW_ENERGY = """
⚠️ <b>Енергія майже на нулі!</b>  

🔋 Ваш рівень енергії впав нижче критичної позначки, і це може вплинути на ваш прогрес у грі. Не дайте цьому зупинити вас!  

✅ <i>Без перерви на відновлення — грайте без зупинок!</i>  
✅ <i>Забезпечте собі перевагу над суперниками!</i>  

⚡️ <b>Не зупиняйтесь!</b>  
Поповніть енергію прямо зараз, щоб залишатися в грі та досягати нових висот!  
"""


class SendMessageNoEnergy:
    _bot: Bot = bot
        
    
    @classmethod
    async def send_message_energy(
        cls,
        character: Character,
        type_text: TextTypes
    ):
        try:
            await cls._bot.send_message(
                chat_id=character.characters_user_id,
                text=type_text
            )
        except Exception as E:
            logger.error(f"Failed to send message to {character.name}\nError: {E}")
    
