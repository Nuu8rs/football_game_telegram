import random
from typing import Optional, Literal, Tuple

from dataclasses import dataclass

from database.models.club import Club
from database.models.character import Character
from database.models.club_infrastructure import ClubInfrastructure
from services.club_service import ClubService


@dataclass
class MatchClub:
    
    clud_id: int
    goals: int = 0
    
    donate_energy: int = 0
    epiіsode_donate_energy: int = 0
    
    club: Optional[Club] = None
    characters_in_match: list[Character] = []
    club_infrastructure: Optional[ClubInfrastructure] = None
    
    async def init_data(self):
        self.club = await ClubService.get_club(
            club_id=self.clud_id
        )
    
    async def join_characters(self, match_id: int):
        """
        Add characters to the club.
        :param match_id: Match ID
        """
        pass
    
    @property
    def base_power(self) -> int:
        """
        Calculate the base power of the club.
        :return: Base power of the club
        """
        return 0
    
    
    @property
    def total_power(self) -> int:
        """
        Calculate the total power of the club.
        :return: Total power of the club
        """
        return 0
    
    @property
    def club_name(self) -> str:
        """
        Get the name of the club.
        :return: Name of the club
        """
        if not self.club:
            return "Unknown Club"
        return self.club.name_club
    
    @property
    def stadium_name(self) -> str:
        """
        Get the name of the stadium.
        :return: Name of the stadium
        """
        if not self.club.custom_name_stadion:
            return "Unknown Stadium"
        return self.club.custom_name_stadion
    
    def get_charaters_by_position(
        self, 
        position: Literal[
            "Воротар",
            "Захисник",
            "Півзахисник",
            "Нападник"
        ]
    ) ->list[Character]:
        return [
            character
            for character in self.characters_in_match
            if character.position_enum == position
        ]
    
    def get_character_by_power(
        self,
        no_character: Character
    ) -> Optional[Character]:
        if not self.characters_in_match:
            return None
        
        weights = [
            character.full_power 
            for character in self.characters_in_match
            if character.characters_user_id != no_character.characters_user_id    
        ]

        selected_character = random.choices(
            self.characters_in_match,
            weights=weights, 
            k=1
        )
        return selected_character[0]
        
@dataclass
class MatchData:
    
    match_id: str
    group_id: str
    
    first_club: MatchClub
    second_club: MatchClub 
    
    @property
    def first_club_id(self) -> int:
        """
        return: ID of the first club
        """
        return self.first_club.clud_id
    
    @property
    def second_club_id(self) -> int:
        """
        return: ID of the second club
        """
        return self.second_club.clud_id
    
    async def init_clubs(self) -> None:
        """
        Initialize clubs for the match.
        """
        await self.first_club.init_data()
        await self.second_club.init_data()

    def clubs_have_characters(self) -> bool:
        """
        Check if clubs have characters.
        :return: True if clubs have characters, False otherwise
        """
        return (
                bool(self.first_club.characters_in_match) 
            and 
                bool(self.second_club.characters_in_match)
        )
    
    @property
    def all_clubs(self) -> list[MatchClub]:
        """
        Get all clubs in the match.
        :return: List of clubs
        """
        return [
            self.first_club,
            self.second_club
        ]
        
    @property
    def all_characters(self) -> list[Character]:
        """
        Get all characters in the match.
        :return: List of characters
        """
        return [
            character for club in self.all_clubs 
            for character in club.characters_in_match
        ]
        
    
    def get_chance_clubs(self) -> Tuple[int, int]:
        """
        Get the chance of clubs to score a goal.
        :return: Tuple of chances for the first and second clubs
        """
        first_club_chance = self.first_club.total_power / (
            self.first_club.total_power + self.second_club.total_power
        )
        
        second_club_chance = self.second_club.total_power / (
            self.first_club.total_power + self.second_club.total_power
        )
        
        return first_club_chance, second_club_chance
    
    def get_goal_club(self) -> MatchClub:
        values = [
            self.first_club.total_power, 
            self.second_club.total_power
        ]
        return random.choices(values, weights=values, k=1)[0]

    
    
@dataclass
class MatchGoal:
    ...
    
