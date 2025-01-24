from typing import Any

from sqlalchemy.event import listens_for

from database.models.character import Character

from .character_low_or_no_energy import EnergyEventListener
from .character_reached_exp import ExpEventListener


energy_listener = EnergyEventListener()
exp_listener = ExpEventListener()

@listens_for(Character, 'before_update')
def listen_character(_: Any, __: Any, target) -> None:
    if hasattr(target, 'current_energy'):
        energy_listener(target)
    if hasattr(target, 'exp'):
        exp_listener(target)