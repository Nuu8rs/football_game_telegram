from aiogram import Router
from aiogram import Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command

from bot.keyboards.menu_keyboard import main_menu

from database.models.user_bot import UserBot
from services.user_service import UserService
from loader import bot

from constants import PLOSHA_PEREMOGU

start_router = Router()

from database.models.character import Character


@start_router.message(CommandStart())
async def start_command_handler(message: Message, state: FSMContext, user: UserBot, command: Command):
    if command.args:
        await register_referal(user=user, referal=command.args)
    # ##############################
    # await test(character)
    # #############################
    await state.clear()
    bot_name = await message.bot.get_my_name()
    await message.answer(f"Вітаємо у «{bot_name.name}»– найкращому симуляторі кар'єри футболіста!"\
                         "Тут ви зможете пройти шлях від молодого таланта до легенди світового футболу."\
                         "Розвивайте свої навички, прокачуйте персонажа, приєднуйся до команд та інших граців, беріть участь у великих турнірах і ведіть свою команду до перемоги."\
                         "Ваші рішення на полі та за його межами визначать долю вашої кар'єри. Готові стати новою зіркою футболу? Час почати свою подорож до футбольної величі!",
                         reply_markup=main_menu(user))

async def register_referal(user: UserBot, referal: str):
    if not "ref_" in referal:
        return
    referal_user_id = referal.split("ref_")[1]
    await UserService.add_referal_user_id(
        my_user_id=user.user_id,
        referal_user_id= referal_user_id
    )
    try:
        await bot.send_message(
            chat_id=referal_user_id,
            text=f"🎉 <b>У вас з'явився новий реферал!</b>\n\n{user.link_to_user}")
    except:
        pass
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

async def test(character: Character):
    from utils.club_shemas import SchemaSerivce
    from services.club_service import ClubService
    from utils.club_utils import get_text_schemas
    club = await ClubService.get_club(club_id=character.club_id)
    text = get_text_schemas(club)
    print(text)
    # await SchemaSerivce.character_is_enough_room(
    #     match_id="0aac6013-13fc-44cd-be92-ed67d4fb5671",
    #     club = club,
    #     my_character=character
        
    # )