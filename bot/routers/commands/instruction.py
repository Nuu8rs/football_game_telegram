from aiogram import Router
from aiogram import Bot, F
from aiogram.types import CallbackQuery, FSInputFile

from bot.keyboards.menu_keyboard import main_menu, menu_instruction
from bot.callbacks.menu_callbacks import NextInstruction
from database.models.user_bot import UserBot

from config import INSTRUCTION

send_instruction_router = Router()



@send_instruction_router.callback_query(NextInstruction.filter())
async def send_instruction(query: CallbackQuery, callback_data: NextInstruction, user: UserBot):
    await query.message.edit_reply_markup(reply_markup=None)
    if callback_data.index_instruction == len(INSTRUCTION) -1:
        keyboard = main_menu(user)
    else:
        keyboard = menu_instruction(index_instruction=callback_data.index_instruction+1)
    
    await query.message.answer_photo(
        photo        = FSInputFile(path=f"src/learning/image_{callback_data.index_instruction}.jpg"),
        caption      = INSTRUCTION[callback_data.index_instruction],
        reply_markup = keyboard)