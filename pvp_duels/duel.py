import asyncio
import uuid

from utils.randomaizer import check_chance

from pvp_duels.types import DuelUser, RoleDuel
from pvp_duels.utils import select_random_angle

from database.models.character import Character

PERIOD_ETUP = 2
PERIOD_ETAP_FIGHT_DUEL = 3
TIMES_SLEEP_ENTRY_DATA_DUEL = 30

PROCENT_KICK_GOAL = 30
PROCENT_GOAL = 15

class DuelManager:
    active_duels: dict[str,'Duel'] = {}

    @classmethod
    def add_pool_duel(cls, duel_id:str, duel_obj: 'Duel'):
        cls.active_duels[duel_id] = duel_obj
        
    @classmethod
    def delete_pool_duel(cls, duel_id: str):
        cls.active_duels.__delitem__(duel_id)
    

class Duel:

    duel_id = str(uuid.uuid4())
    
    def __init__(self, user_duel: DuelUser) -> None:
        self.user_duel = user_duel
        
        DuelManager.add_pool_duel(
            duel_id=self.duel_id,
            duel_obj=self
            )
        
    async def _waiting_data_entry(self):
        await asyncio.sleep(TIMES_SLEEP_ENTRY_DATA_DUEL)
        if self.user_duel.position_angle_user_1 is None:
            self.user_duel.points_user_1 = select_random_angle()
            
        if self.user_duel.position_angle_user_2 is None:
            self.user_duel.points_user_2 = select_random_angle()
        
    async def start_duel(self) -> Character:
        for _ in PERIOD_ETUP:
            await self._start_etup()
            self.user_duel.change_roles_character()
            
        DuelManager.delete_pool_duel(self.duel_id)
        return self.get_winner_duel()
          
    async def _start_etup(self):
        for _ in PERIOD_ETAP_FIGHT_DUEL:
            #send_message_choise_angle
            await self._waiting_data_entry()
            winner_etap = self._choise_etap_win()
            
            self.user_duel.add_points_to_role(winner_etap, 3)
            
            self.user_duel.anulate_angle_users()
          
          
    def get_winner_duel(self) -> list[Character] | Character:
        if self.user_duel.points_user_1 == self.user_duel.points_user_2:
            return [self.user_duel.user_1, self.user_duel.user_2]
        elif self.user_duel.points_user_1 > self.user_duel.points_user_2:
            return self.user_duel.user_1
        else:
            return self.user_duel.user_2
        
    def _choise_etap_win(self) -> RoleDuel:
        user_goalkepper = self.user_duel.get_user_by_role(role=RoleDuel.GOALKEEPER)
        user_forward = self.user_duel.get_user_by_role(role=RoleDuel.FORWARD)
        
        power_forward = user_forward.full_power
        power_goalkepper = user_goalkepper.full_power
        
        if self.user_duel.position_angle_user_1 == self.user_duel.position_angle_user_2:     
            power_goalkepper =+ power_goalkepper * (PROCENT_KICK_GOAL / 100)
        else:
            power_forward =+ power_forward * (PROCENT_GOAL / 100)
        
        total_power = power_forward+power_goalkepper
        
        chance_win_forward = (power_forward/total_power) * 100 
        forward_is_win = check_chance(chance_win_forward)
        
        return RoleDuel.FORWARD if forward_is_win else RoleDuel.GOALKEEPER
        
        
