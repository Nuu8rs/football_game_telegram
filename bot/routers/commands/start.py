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
    
 
@start_router.message(F.text == "⬅️ Головна площа")
async def plosha(message: Message, user: UserBot):
    await message.answer_photo(photo = PLOSHA_PEREMOGU, 
                               caption=f"""
Вітаю тебе на головній площі гри! Місце де ти можеш обрати основні функції:
<b>Стадіон</b> - реєстрація на матч та таблиці
<b>Тренажерний зал</b> - місце прокачки персонажа
<b>Навчальний центр</b> - досвід та заробіток монет.
<b>Тренувальна база</b> - покращення команди перед грою
<b>Магазин</b> - тут можна купити речі задля покращення футболіста.

                            
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