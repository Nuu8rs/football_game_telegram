from aiogram import Router
from aiogram import Bot, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from bot.keyboards.menu_keyboard import main_menu

from database.models.club import Club
from database.models.user_bot import UserBot
from database.models.character import Character
from constants import PLOSHA_PEREMOGU

start_router = Router()


@start_router.message(CommandStart())
async def start_command_handler(message: Message, state: FSMContext, user: UserBot):
    # ##############################
    # await test()
    # #############################
    await state.clear()
    bot_name = await message.bot.get_my_name()
    await message.answer(f"Вітаємо у «{bot_name.name}»– найкращому симуляторі кар'єри футболіста!"\
                         "Тут ви зможете пройти шлях від молодого таланта до легенди світового футболу."\
                         "Розвивайте свої навички, прокачуйте персонажа, приєднуйся до команд та інших граців, беріть участь у великих турнірах і ведіть свою команду до перемоги."\
                         "Ваші рішення на полі та за його межами визначать долю вашої кар'єри. Готові стати новою зіркою футболу? Час почати свою подорож до футбольної величі!",
                         reply_markup=main_menu(user))
    
 
@start_router.message(F.text == "⬅️ До площі переможців")
async def plosha(message: Message, user: UserBot):
    await message.answer_photo(photo = PLOSHA_PEREMOGU, 
                               caption=f"""
Вітаю тебе на площі героїв! Місце де всі талановиті футболісти та футболістки розпочинають свій шлях. 
Створюй свою команду або приєднуйся до граючих  команд, тренуйся щоденно в тренажерному залі, не забувай приходити на стадіон та матч! Як сильно втомишся - приходь до масажиста. 

Бажаємо тобі стати найкращим гравцем нашої гри! Та привести команду до чемпіонства.   
                            
                               """,
                               reply_markup=main_menu(user))

async def test():
    from league.create_bots import BOTS
    bot_menu = BOTS(
        average_club_strength=100,
        name_league="🟢 Ліга новачків"
    )
    await bot_menu.create_bot_clubs(
        len_bots_club=18
    )