from datetime import datetime
from database.models.character import Character
from enum import Enum as PyEnum
from constants import PositionCharacter

def create_defender() -> Character:
    return Character(
        name="",
        technique=3,
        kicks=4,
        ball_selection=7,
        speed=6,
        endurance=5,
        gender="",
        exp=0,
        money=0
        created_at=datetime.utcnow()
    )

def create_midfielder() -> Character:
    return Character(
        name="",
        technique=4,
        kicks=3,
        ball_selection=8,
        speed=6,
        endurance=6,
        gender="",
        exp=0,
        money=0
        created_at=datetime.utcnow()
    )

def create_goalkeeper() -> Character:
    return Character(
        name="",
        technique=2,
        kicks=5,
        ball_selection=5,
        speed=5,
        endurance=8,
        gender="",
        exp=0,
        money=0
        created_at=datetime.utcnow()
    )

def create_attacker() -> Character:
    return Character(
        name="",
        technique=3,
        kicks=7,
        ball_selection=2,
        speed=7,
        endurance=6,
        gender="",
        exp=0,
        money=0
        created_at=datetime.utcnow()
    )

def CREATE_CHARACTER_CONST(position: PositionCharacter) -> Character:
    if position == PositionCharacter.DEFENDER:
        return create_defender()
    elif position == PositionCharacter.MIDFIELDER:
        return create_midfielder()
    elif position == PositionCharacter.GOALKEEPER:
        return create_goalkeeper()
    elif position == PositionCharacter.ATTACKER:
        return create_attacker()