from enum import Enum

from aiogram.types import FSInputFile
from apscheduler.triggers.cron import CronTrigger
from database.models import Character
from datetime import datetime, timedelta

from config import PositionCharacter, Gender
import random

DEFENDER_character_const = Character(
    name="",
    technique=3,
    kicks=4,
    ball_selection=7,
    speed=6,
    endurance=5,
    gender="",
    created_at=datetime.utcnow()   
)
MIDFIELDER_character_const = Character(
    name="",
    technique=4,
    kicks=3,
    ball_selection=8,
    speed=6,
    endurance=6,
    gender="",
    created_at=datetime.utcnow()   
)
GOALKEEPER_character_const = Character(
    name="",
    technique=2,
    kicks=5,
    ball_selection=5,
    speed=5,
    endurance=8,
    gender="",
    created_at=datetime.utcnow()   
)
ATTACKER_character_const  = Character(
    name="",
    technique=3,
    kicks=7,
    ball_selection=2,
    speed=7,
    endurance=6,
    gender="",
    created_at=datetime.utcnow()   
)
    
    
gradation_level = ("E","F","D","C","B","A","S")
    
chance_add_point = {
    timedelta(seconds = 5)   : 90,
    timedelta(minutes = 30)  : 25,
    timedelta(minutes = 60)  : 35,
    timedelta(minutes = 90)  : 50,
    timedelta(minutes = 120) : 65,
}

const_energy_by_time = {
    timedelta(seconds = 5)   : 5,
    timedelta(minutes = 30)  : 10,
    timedelta(minutes = 60)  : 20,
    timedelta(minutes = 90)  : 40,
    timedelta(minutes = 120) : 60,
}

const_character = {
    PositionCharacter.DEFENDER   : DEFENDER_character_const,
    PositionCharacter.ATTACKER   : ATTACKER_character_const,
    PositionCharacter.GOALKEEPER : GOALKEEPER_character_const,
    PositionCharacter.MIDFIELDER : MIDFIELDER_character_const,
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

GYM_PHOTO       = FSInputFile("src/gym_photo.jpg")
CLUB_PHOTO      = FSInputFile("src/club_photo.jpg")
FIGHT_MENU      = FSInputFile("src/fight_club_menu.jpg")
JOIN_TO_FIGHT   = FSInputFile("src/join_to_fight.jpg")
LEAGUE_PHOTO    = FSInputFile("src/league_photo.jpg")
PLOSHA_PEREMOGU = FSInputFile("src/plosha_peremogu.jpg") 


MAX_LEN_MEMBERS_CLUB = 11

TIME_FIGHT = timedelta(seconds=20)
TIME_RESET_ENERGY = CronTrigger(hour=12, minute=45)

DELTA_TIME_EDUCATION_REWARD = timedelta(hours=12)

HOURS_END_TIME = 22


def GET_RANDOM_NUMBER(LIMIT_1 = 1, LIMIT_2 = 5):
    return random.randint(LIMIT_1,LIMIT_2)