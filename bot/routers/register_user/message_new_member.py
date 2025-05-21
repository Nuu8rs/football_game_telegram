import asyncio
from aiogram import Bot

from loader import bot
from logging_config import logger

from .constans import ADITIONAL_INFO_PHOTO

TEXT_TEMPLATE_NEW_USER = """
<b>Основні питання та відповіді для новачків ⚽️</b>

<b>❓Як грати?</b>
Основне — це <b>тренуватися в тренажерному залі</b> та <b>грати матчі з командою</b>. 
Чим частіше тренування — тим ефективніше зростає сила гравця 💪
Також тренуватися можна з <b>тренером</b> 🧑‍🏫 — за <b>ключі до тренувань</b> 🔑

<b>❓Як отримувати досвід та монети?</b>
📚 <b>Навчальний центр</b> — кожні <b>12 годин</b>
🏆 <b>Перемоги у матчах</b>
💥 <b>Персональні тренування</b> з тренером (три рази на день)

<b>❓Як та коли проходять матчі?</b>
🕘 <b>Щодня о 21:00</b>  
📅 <b>Сезон стартує 1 числа кожного місяця</b>  
⚙️ Результати визначає математична модель: чим більша сила команди — тим вищі шанси на перемогу

🏆 <b>Топ-20 команд по силі</b> — <i>Кубок України</i>  
🌍 <b>Топ-24 команд Рейтингу</b> — <i>Єврокубкові матчі</i>

<b>👥 Команди‼️</b>
Дуже важливо — грати в <b>команді</b>!  
🔹 Створи свою  
🔹 Запроси друзів  
🔹 Або приєднуйся до існуючої  

<b>⚠️ Матчі можливі лише якщо ти в команді!</b>

<b>💬 Долучайся до нашого чату</b> — ми допоможемо з будь-якими питаннями!
👉 <a href="https://t.me/tgfootballchat">https://t.me/tgfootballchat</a>
"""

class SendMessageNewMember:
    _bot: Bot = bot
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        
    @classmethod
    async def send_message(cls, user_id: int):
        instance = cls(user_id)
        asyncio.create_task(instance._await())
    
    async def _await(self):
        await asyncio.sleep(3*60*60)
        await self._send_message()
        
    async def _send_message(self):
        try:
            await self._bot.send_photo(
                photo=ADITIONAL_INFO_PHOTO,
                chat_id=self.user_id,
                caption=TEXT_TEMPLATE_NEW_USER,
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error sending message to {self.user_id}: {e}")
        