from typing import Optional, Literal

from aiogram import Bot
from aiogram.types import FSInputFile, Message

from database.models.character import Character

from match.entities import MatchData
from match.enum import TypeGoalEvent

from .templates import (
    GetterTemplatesMatch,
    TemplatesMatch
)
from .render_scene import SceneRenderer

from utils.rate_limitter import rate_limiter

from loader import bot
from logging_config import logger

class Sender:
    _bot: Bot = bot
    
    async def send_messages(
        self, 
        text: str,
        characters: list[Character],
        photo: Optional[str | FSInputFile] = None
    ) -> Message:
        
        for character in characters:
            if photo:
                await self._send_photo(
                    
                )
            return await self
    
    @rate_limiter
    async def _send_message(
        self,
        text: str,
        character: Character
    ):
        try:
            await self._bot.send_message(
                chat_id = character.characters_user_id,
                text = text
            )
        except Exception as E:
            logger.error(
                f"Error sending message to {character.character_name}: {E}"
            )
        
        
    @rate_limiter
    async def _send_photo(
        self,
        character: Character,
        caption: str,
        photo: str | FSInputFile,
    ):
        try:
            await self._bot.send_photo(
                chat_id = character.characters_user_id,
                caption = caption,
                photo = photo,
            )
        except Exception as E:
            logger.error(
                f"Error sending photo to {character.character_name}: {E}"
            )


class MatchSender:
    sender = Sender()
    
    def __init__(
        self,
        match_data: MatchData,
    ) -> None:
        
        self.match_data = match_data
        self.getter_templates = GetterTemplatesMatch(match_data)

    async def start_match(self) -> None:
        for club in self.match_data.all_clubs:
            text = self.getter_templates.format_message(
                template = TemplatesMatch.START_MATCH,
                extra_context = {
                    'stadium_name': club.stadium_name
                }
            )
            await self.sender.send_messages(
                text = text,
                characters = club.characters_in_match,
                photo = None
            )
        
    async def send_participants_match(self) -> None:

        def text_participants(characters: list[Character]) -> str:
            if not characters:
                return "На матч не приїхали гравці"
            
            participants = "".join(
                TemplatesMatch.TEMPLATE_PARTICIPANT.value.format(
                    character_name = character.character_name,
                    power_user = character.full_power,
                    lvl = character.lvl
                )
                for character in characters
            )
            return participants
            
        text = self.getter_templates.format_message(
            template = TemplatesMatch.TEMPLATE_PARTICIPANTS_MATCH,
            extra_context = {
                "players_first_club": text_participants(
                    characters = self.match_data.first_club.characters_in_match
                ),
                "players_second_club": text_participants(
                    characters = self.match_data.second_club.characters_in_match
                ),
            }
        )
        await self.sender.send_messages(
            text = text,
            characters = self.match_data.all_characters,
            photo = None
        )
            
    async def send_event_scene(
        self,
        goal_event: TypeGoalEvent,
        characters_scene: list[Character] = [],
        character_goal: Optional[Character] = None ,
        character_assist: Optional[Character] = None,
    ) -> None:
        
        render_scene  = SceneRenderer(
            match_data = self.match_data,
            goal_event = goal_event,
            characters_scene = characters_scene,
            scorer = character_goal,
            assistant = character_assist
        )
        text_scene = render_scene.render()
                
        await self.sender.send_messages(
            text = text_scene,
            characters = self.match_data.all_characters,
            photo = None
        )
        
    async def send_ping_donate_energy(self) -> None:
        chance_clubs = self.match_data.get_chance_clubs()
        template = TemplatesMatch.TEMPLATE_COMING_GOAL
        text = self.getter_templates.format_message(
            template = template,
            extra_context = {
                "chance_first_club": chance_clubs[0],
                "chance_second_club": chance_clubs[1],
            }
        )
        await self.sender.send_messages(
            characters = self.match_data.all_characters,
            text = text
        )