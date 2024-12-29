from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import LINK_TO_CHAT

communication_router = Router()

@communication_router.message(F.text == "🗣 Cпілкування")
async def communication_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'Чат для спілкування - <a href="{LINK_TO_CHAT}">*клік*</a>')