import asyncio
import random
from datetime import datetime

from match.entities import MatchData
from match.message_sender.match_sender import MatchSender
from match.enum import TypeGoalEvent
from .goal_generator import GoalGenerator

from constants import TIME_FIGHT

class Match:
    
    
    def __init__(
        self,
        match_data: MatchData,
        start_time: datetime
    ) -> None:
        """
        Initialize a match.
        :param match_data: Match data object containing information about the match.
        """

        self.match_data = match_data
        self.match_sender = MatchSender(match_data)        
        self.count_goals = self._generate_count_goals()
        
        end_time = start_time + TIME_FIGHT
            
            
        self.goal_generator = GoalGenerator(
            start_time  = start_time,
            end_time    = end_time,
            count_goals = self.count_goals
        )
            
    def _generate_count_goals(self) -> int:
        return random.randint(3,9)
            
    async def start_match(self) -> None:
        await self.match_data.init_clubs()
        
        if not self.match_data.clubs_have_characters():
            return #TODO SEND NO HAVE CHARACTERS

        await self.match_sender.start_match()
        await self.match_sender.send_participants_match()
        asyncio.create_task(self.event_watcher())
        await asyncio.sleep(TIME_FIGHT.total_seconds())        
        
    async def event_watcher(self) -> None:
        event_func: dict[TypeGoalEvent,callable] = {
            TypeGoalEvent.NO_GOAL: self.no_goal_event,
            TypeGoalEvent.PING_DONATE_ENERGY: self.ping_donate_energy_event,
            TypeGoalEvent.GOAL: self.goal_event,
        }
        
        async for event in self.goal_generator.generate_goals():
            await event_func[event]()
        else:
            await self.match_sender.send_end_match()    

    async def no_goal_event(self) -> None:
        first_character = self.match_data.first_club.get_character_by_power()
        second_character = self.match_data.second_club.get_character_by_power()
        await self.match_sender.send_event_scene(
            goal_event = TypeGoalEvent.NO_GOAL,
            characters_scene = [first_character, second_character]
        )
        #ADD 0.25 POINT TO CHARACTERS
          
    async def ping_donate_energy_event(self) -> None:
        await self.match_sender.send_ping_donate_energy()
        
    async def goal_event(self) -> None:
        goal_club = self.match_data.get_goal_club()
        character_goal = goal_club.get_character_by_power()
        assist_character = goal_club.get_character_by_power(
            no_character=character_goal
        )
        await self.match_sender.send_event_scene(
            goal_event = TypeGoalEvent.GOAL,
            character_goal = character_goal,
            character_assist = assist_character,
        )
        ...
        
    async def end_match(self) -> None:
        