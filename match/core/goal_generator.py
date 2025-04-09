import asyncio
import random

from typing import AsyncGenerator
from datetime import datetime, timedelta

from match.entities import MatchGoal
from match.constans import MAX_EVENTS, MIN_GAP
from match.enum import TypeGoalEvent


class GoalGenerator:
    
    def __init__(
        self, 
        start_time: datetime,
        end_time: datetime,
        count_goals: int    
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.count_goals = count_goals
        
    
    async def generate_goals(self) -> AsyncGenerator[TypeGoalEvent, None]:
        """
        Асинхронный генератор событий (голов, не-голов и PING_DONATE_ENERGY).
        """
        events = self.generate_events()
        event_times = self.generate_time_events()

        for event, event_time in zip(events, event_times):
            now = datetime.now()

            if event == TypeGoalEvent.GOAL:
                ping_time = event_time - timedelta(seconds=40)
                if ping_time > now:
                    await asyncio.sleep((ping_time - now).total_seconds())
                yield TypeGoalEvent.PING_DONATE_ENERGY

            if event_time > now:
                await asyncio.sleep((event_time - now).total_seconds())
            yield event
        
        
    def generate_events(self) -> list[TypeGoalEvent]:
        count_no_goal_event = MAX_EVENTS - self.count_goals
        no_goal_events = [
            TypeGoalEvent.NO_GOAL for _ in range(count_no_goal_event)
        ]
        goal_events = [
            TypeGoalEvent.GOAL for _ in range(self.count_goals)
        ]
        goal_events = no_goal_events + goal_events
        random.shuffle(goal_events)
        
        return goal_events
        
        
    def generate_time_events(self) -> list[datetime]:
        total_duration = (self.end_time - self.start_time).total_seconds()
        interval = total_duration / MAX_EVENTS

        event_times = []
        current_time = self.start_time

        for _ in range(MAX_EVENTS):
            if event_times and event_times[-1] + timedelta(seconds=MIN_GAP) > current_time:
                current_time = event_times[-1] + timedelta(seconds=MIN_GAP)
                
            if current_time > self.end_time:
                break
                
            event_times.append(current_time)
            current_time += timedelta(seconds=interval)

        return event_times
        