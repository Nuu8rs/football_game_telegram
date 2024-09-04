from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from datetime import datetime, timedelta

from database.models import Character
from services.character_service import CharacterService

from bot.keyboards.gym_keyboard import menu_education_cernter
from constants import GET_RANDOM_NUMBER


education_center_router = Router()

@education_center_router.message(F.text == "🏫 Навчальний центр")
async def go_to_gym(message: Message):
    await message.answer("Ласкаво просимо до навчального центру\nТут ви зможете підняти свій рівень", reply_markup=menu_education_cernter())
    
@education_center_router.callback_query(F.data == "get_rewards_education_center")
async def get_rewards_education_cernter(query: CallbackQuery, character: Character):
    if not datetime.now() > character.last_education_reward_date:
        time_to_get_reward = character.last_education_reward_date - datetime.now()
        hours, remainder = divmod(time_to_get_reward.seconds, 3600)
        minutes, _ = divmod(remainder, 60)        

        return query.message.answer(f"<b>Залишилося часу до отримання нагороди годин {hours} і {minutes} хвилин</b>")
    
    
    exp, coins = GET_RANDOM_NUMBER(5,25), GET_RANDOM_NUMBER(5,15)
    await CharacterService.add_exp_character(
        character=character,
        amount_exp_add=exp
    )
    await CharacterService.update_money_character(
        character=character,
        amount_money_adjustment=coins
    )
    await query.message.answer("🎓 <b>Після навчального центру ваш персонаж отримав:</b>✨ {exp} <b>досвіду</b>  💰 {coins} <b>монет</b>")