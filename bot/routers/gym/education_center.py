from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from datetime import datetime, timedelta

from database.models.character import Character

from services.character_service import CharacterService

from bot.keyboards.gym_keyboard import menu_education_cernter
from schedulers.scheduler_education import EducationRewardReminderScheduler
from constants import GET_RANDOM_NUMBER, DELTA_TIME_EDUCATION_REWARD, EDUCATION_CENTER
from utils.club_utils import get_text_education_center_reward


education_center_router = Router()

@education_center_router.message(F.text == "🏫 Навчальний центр")
async def go_to_gym(message: Message):
    await message.answer_photo(photo=EDUCATION_CENTER,
        caption="Ласкаво просимо до навчального центру\nТут ви зможете підняти свій рівень", reply_markup=menu_education_cernter()
        )
    
@education_center_router.callback_query(F.data == "get_rewards_education_center")
async def get_rewards_education_cernter(query: CallbackQuery, character: Character):
    if not datetime.now() > character.education_reward_date:
        time_to_get_reward = character.education_reward_date - datetime.now()
        hours, remainder = divmod(time_to_get_reward.seconds, 3600)
        minutes, _ = divmod(remainder, 60)        

        return query.message.answer(f"<b>Залишилося часу до отримання нагороди годин {hours} і {minutes} хвилин</b>")
    
    
    exp, coins = GET_RANDOM_NUMBER(1,3), GET_RANDOM_NUMBER(5,10)
    await CharacterService.add_exp_character(
        character=character,
        amount_exp_add=exp
    )
    await CharacterService.update_money_character(
        character=character,
        amount_money_adjustment=coins
    )
    await CharacterService.update_character_education_time(
        character=character,
        amount_add_time=DELTA_TIME_EDUCATION_REWARD
    )
    
    scheduler_reward_education = EducationRewardReminderScheduler()
    await scheduler_reward_education.add_job_remind(
        character=character,
        time_get_reward=datetime.now() + DELTA_TIME_EDUCATION_REWARD
    ) 
    await query.message.answer(get_text_education_center_reward(
        exp = exp,
        coins=coins,
        delta_time_education_reward=DELTA_TIME_EDUCATION_REWARD
    ))