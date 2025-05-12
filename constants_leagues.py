from abc import ABC

from datetime import datetime
from enum import Enum

from apscheduler.triggers.cron import CronTrigger


class TypeLeague(Enum):
    BEST_LEAGUE = "BEST_LEAGUE"
    DEFAULT_LEAGUE = "DEFAULT_LEAGUE"
    TOP_20_CLUB_LEAGUE = "TOP_20_CLUB_LEAGUE"
    NEW_CLUB_LEAGUE = "NEW_CLUB_LEAGUE"


class BaseConfigLeague(ABC):
    DAY_START: int
    DAY_END: int
    HOUR_TIME_START_MATCH: int
    
    @property
    def TRIGGER_START_LEAGUE(self) -> CronTrigger:
        return CronTrigger(
            day=self.DAY_START,
            hour=8,
        )
    
    @property
    def TRIGGER_SEND_MESSAGE_START(self) -> CronTrigger:
        return CronTrigger(
            day=self.DAY_START,
            hour=9,
            minute=0
        )
    
    @property
    def DATETIME_START_LEAGUE(self) -> datetime:
        now = datetime.now()
        return now.replace(
            day=self.DAY_START, 
            hour=0, 
            minute=0
        )
    
    @property
    def DATETIME_END_LEAGUE(self) -> datetime:
        now = datetime.now()
        return now.replace(
            day=self.DAY_END, 
            hour=0, 
            minute=0
        )
        
        
class ConfigNewClubLeague(BaseConfigLeague):
    DAY_START = 11
    DAY_END = 20
    HOUR_TIME_START_MATCH = 15

    COUNT_GROUP = 2
    COUNT_CLUB_IN_GROUP = 15


config_new_club_league = ConfigNewClubLeague()


class GetConfig:
    configs: dict[TypeLeague, BaseConfigLeague] = {
        # TypeLeague.BEST_LEAGUE: config_new_club_league,
        # TypeLeague.DEFAULT_LEAGUE: config_new_club_league,
        # TypeLeague.TOP_20_CLUB_LEAGUE: config_new_club_league,
        TypeLeague.NEW_CLUB_LEAGUE: config_new_club_league,
    }
    
    @staticmethod
    def get_config(type_league: TypeLeague) -> BaseConfigLeague:
        return GetConfig.configs[type_league]
