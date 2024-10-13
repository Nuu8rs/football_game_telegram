from database.models.club import Club
from database.models.character import Character

from database.session import get_session
from sqlalchemy.future import select
from sqlalchemy import func, update
from typing import Dict, List
from constants import MAX_LEN_MEMBERS_CLUB

from datetime import datetime

class DuelService:
    ...