from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta


    
    

import asyncio
from database.models.character import Character
from database.models.club import Club
from services.match_character_service import MatchCharacterService
from services.club_service import ClubService
from services.character_service import CharacterService
from services.league_service import LeagueFightService

from utils.randomaizer import check_chance
from constants import GET_RANDOM_NUMBER

from typing import List
import random

TIME_FIGHT = timedelta(hours=1)



