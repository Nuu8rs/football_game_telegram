from enum import Enum
from enum import Enum as PyEnum

from aiogram.types import FSInputFile
from apscheduler.triggers.cron import CronTrigger

from database.models.character import Character
from database.models.item import Item

from datetime import datetime, timedelta

from config import PositionCharacter, Gender
import random, json


    
class ItemCategory(PyEnum):
    T_SHIRT = "T-shirt"
    SHORTS = "Shorts"
    GAITERS = "Gaiters"
    BOOTS = "Boots"
    



chance_add_point = {
    timedelta(seconds = 5)   : 90,
    timedelta(minutes = 30)  : 35,
    timedelta(minutes = 60)  : 45,
    timedelta(minutes = 90)  : 55,
    timedelta(minutes = 120) : 75,
}

const_energy_by_time = {
    timedelta(seconds = 5)   : 5,
    timedelta(minutes = 30)  : 10,
    timedelta(minutes = 60)  : 20,
    timedelta(minutes = 90)  : 40,
    timedelta(minutes = 120) : 60,
}


const_name_characteristics = {
    "technique"        : "🎯 Техніка",
    "kicks"            : "🥋 Удари",
    "ball_selection"   : "🛡️ Відбір м’яча",
    "speed"            : "⚡ Швидкість",
    "endurance"        : "🏃 Витривалість"
}

photos = {
    (Gender.MAN, PositionCharacter.MIDFIELDER): 'src/photo_character/man_midfielder.jpg',
    (Gender.WOMAN, PositionCharacter.MIDFIELDER): 'src/photo_character/woman_midfielder.jpg',
    (Gender.MAN, PositionCharacter.DEFENDER): 'src/photo_character/man_defender.jpg',
    (Gender.WOMAN, PositionCharacter.DEFENDER): 'src/photo_character/woman_defender.jpg',
    (Gender.MAN, PositionCharacter.GOALKEEPER): 'src/photo_character/man_goalkeeper.jpg',
    (Gender.WOMAN, PositionCharacter.GOALKEEPER): 'src/photo_character/woman_goalkeeper.jpg',
    (Gender.MAN, PositionCharacter.ATTACKER): 'src/photo_character/man_attacker.jpg',
    (Gender.WOMAN, PositionCharacter.ATTACKER): 'src/photo_character/woman_attacker.jpg',
}



def get_photo_character(character: Character) -> FSInputFile:
    return FSInputFile(photos.get((character.gender_enum, character.position_enum), 'path/to/default_photo.jpg'))

GYM_PHOTO        = FSInputFile("src/gym_photo.jpg")
CLUB_PHOTO       = FSInputFile("src/club_photo.jpg")
FIGHT_MENU       = FSInputFile("src/fight_club_menu.jpg")
JOIN_TO_FIGHT    = FSInputFile("src/join_to_fight.jpg")
LEAGUE_PHOTO     = FSInputFile("src/league_photo.jpg")
PLOSHA_PEREMOGU  = FSInputFile("src/plosha_peremogu.jpg") 
EDUCATION_CENTER = FSInputFile("src/education_center_photo.jpg")
HALL_FAME_PHOTO  = FSInputFile("src/hall_fame_photo.jpg")
DUEL_PHOTO       = FSInputFile("src/duel_photo.jpg")


MAX_LEN_MEMBERS_CLUB = 11

# TIME_FIGHT = timedelta(minutes=2)
TIME_FIGHT = timedelta(minutes=20)
BUFFER_TIME = timedelta(minutes=3)

TIME_RESET_ENERGY_CLUB = CronTrigger(hour=22, minute=10)
TIME_RESET_ENERGY_CHARACTER = CronTrigger(hour=22, minute=15)

END_DAY_BEST_20_CLUB_LEAGUE = 15
END_MATCH_TOP_20_CLUB = CronTrigger(day = END_DAY_BEST_20_CLUB_LEAGUE,hour=12)

SEND_GONGRATULATION_END_BEST_MATCH = CronTrigger(
    day = 15,
    hour=16, 
    minute=30
)


DELTA_TIME_EDUCATION_REWARD = timedelta(hours=12)

HOURS_END_TIME = 22

KOEF_ENERGY_DONATE = 2

PROCENT_TO_SELL = 30

REFERAL_EXP = 20
ALL_COUNT_ENERGY_BIT = [30,50,100,150]


TIME_TO_JOIN_TO_CLUB = timedelta(minutes=2)

#KEY - COUNT ENERGY | VALUE - PRICE UAH
count_energys = [5,10,20,50,70]
CONST_PRICE_ENERGY = {
    100  : 100,
    150  : 150,
    300  : 270,
    600  : 490,
    900  : 670
}


DUEL_START_DAY_SEASON = 21
DUEL_END_DAY_SEASON   = 28

X2_REWARD_WEEKEND_START_DAY = 21
X2_REWARD_WEEKEND_END_DAY   = 28

START_DAY_BEST_LEAGUE = 21
END_DAY_BEST_LEAGUE = 30

START_DAY_BEST_20_CLUB_LEAGUE = 5



ITEM_PER_PAGE = 9

def GET_RANDOM_NUMBER(LIMIT_1 = 1, LIMIT_2 = 5):
    return random.randint(LIMIT_1,LIMIT_2)