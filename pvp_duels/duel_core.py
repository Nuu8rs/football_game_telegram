import asyncio

from database.models.character import Character
from pvp_duels.types import DuelUser
from pvp_duels.utils import select_random_roles
from pvp_duels.duel import Duel

class CoreDuel:
    count_users_duel = 2
    
    def __init__(self) -> None:
        self.queue_users_duel = asyncio.Queue()
        self._task_waiting = asyncio.create_task(self._waiting_users())
         
        
    async def _waiting_users(self):
        while True:
            while self.queue_users_duel.qsize() < self.count_users_duel:
                await asyncio.sleep(2)
            
            batch = []
            for _ in range(self.count_users_duel):
                user_duel = await self.queue_users_duel.get()
                batch.append(user_duel)
                
            await self.start_duel(*batch)
            batch.clear()
            
    async def start_duel(user_1: Character, user_2: Character):
        random_roles = select_random_roles() 
        duel_users = DuelUser(
            user_1      = user_1,
            role_user_1 = random_roles[0], 
            user_2      = user_2,
            role_user_2 = random_roles[1]
            )
        duel = Duel(
            user_duel=duel_users
        )
        # asyncio.create_task(duel.start_duel())