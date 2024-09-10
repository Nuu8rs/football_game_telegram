from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from ..callbacks.gym_calbacks import SelectGymType, SelectTimeGym, SelectCountDonateEnergy
from ..callbacks.massage_room_callbacks import SelectCountGetEnergy

from datetime import timedelta
from .utils_keyboard import menu_plosha


count_energys = [5,10,20,50,70]


def menu_gym():
    return (ReplyKeyboardBuilder()
            .button(text = "🧤 Піти на тренування")
            .button(text = "💆‍♂️ Масажний зал")
            .attach(menu_plosha())
            .adjust(2,1)
            .as_markup(resize_keyboard=True)
            )

def select_type_gym():
    return (InlineKeyboardBuilder()
        .button(text = "🎯 Техніку"      , callback_data=SelectGymType(gym_type="technique"))
        .button(text = "🥋 Удари"        , callback_data=SelectGymType(gym_type="kicks"))
        .button(text = "🛡️ Відбір м’яча" , callback_data=SelectGymType(gym_type="ball_selection"))
        .button(text = "⚡ Швидкість"    , callback_data=SelectGymType(gym_type="speed"))
        .button(text = "🏃 Витривалість" , callback_data=SelectGymType(gym_type="endurance"))
        .adjust(2)
        .as_markup()
            )
def select_time_to_gym(gym_type: str):
    return (InlineKeyboardBuilder()
            # .button(text="🕑 5 секунд"  , callback_data=SelectTimeGym(gym_time=timedelta(seconds= 5) , gym_type = gym_type))
            .button(text="🕑 30 хвилин"  , callback_data=SelectTimeGym(gym_time=timedelta(minutes = 30) , gym_type = gym_type))
            .button(text="🕒 60 хвилин"  , callback_data=SelectTimeGym(gym_time=timedelta(minutes = 60) , gym_type = gym_type))
            .button(text="🕓 90 хвилин"  , callback_data=SelectTimeGym(gym_time=timedelta(minutes = 90) , gym_type = gym_type))
            .button(text="🕔 120 хвилин" , callback_data=SelectTimeGym(gym_time=timedelta(minutes = 120), gym_type = gym_type))
            .button(text="⬅️ Назад до вибору", callback_data="back_to_select_gym_type")
            .adjust(2,2,1)
            .as_markup()
            )

def select_donate_energy_keyboard(club_id: int):
    keyboard = InlineKeyboardBuilder()
    for count_energy in count_energys:
        keyboard.button(text=f"Пожертвувати [{count_energy}] 🔋", 
                        callback_data=SelectCountDonateEnergy(
                            count_energy=count_energy,
                            club_id=club_id
                        ))
    return keyboard.adjust(1).as_markup()


def menu_education_cernter():
    return(
        InlineKeyboardBuilder()
        .button(text = "🏆 Забрати нагороду з навчального центру", callback_data= "get_rewards_education_center")
        .as_markup()
    )
    
def menu_massage_room():
    keyboard = InlineKeyboardBuilder()
    for count_energy in count_energys:
        keyboard.button(text = f"Купить [{count_energy}] 🔋", 
                        callback_data=SelectCountGetEnergy(count_energy=count_energy))
    return keyboard.adjust(1).as_markup()