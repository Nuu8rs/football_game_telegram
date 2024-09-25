
from dataclasses import dataclass, field
from database.models.character import Character
from database.models.match_character import MatchCharacter

from services.club_service import ClubService
from services.character_service import CharacterService

from utils.randomaizer import check_chance

from constants import KOEF_ENERGY_DONATE

from typing import List


@dataclass
class ClubsInMatch:
    first_club_id: int
    second_club_id: int
    match_id: str
    group_id: str
    
    first_club_characters: list[Character] = field(default_factory=list)
    second_club_characters: list[Character] = field(default_factory=list)
    
    goals_first_club: int = 0
    goals_second_club: int = 0

    donate_energy_first_club = 0
    donate_energy_second_club = 0


    async def init_clubs(self):
        self.first_club  = await ClubService.get_club(club_id=self.first_club_id)
        self.second_club = await ClubService.get_club(club_id=self.second_club_id)
        await self.add_characters_in_match()


    async def add_characters_in_match(self):
        from services.match_character_service import MatchCharacterService

        characters_in_match = await MatchCharacterService.get_characters_from_match(
            match_id=self.match_id
        )
        await self.__add_character_in_match(characters_in_match)
        if self.first_club.is_fake_club:
            characater_bot = await CharacterService.get_character_by_id(character_id=self.first_club.characters[0].id)
            await MatchCharacterService.add_character_in_match(club_in_match=self, character=characater_bot)
            self.first_club_characters.append(characater_bot)
            
        if self.second_club.is_fake_club:
            characater_bot = await CharacterService.get_character_by_id(character_id=self.second_club.characters[0].id)
            await MatchCharacterService.add_character_in_match(club_in_match=self, character=characater_bot)
            self.second_club_characters.append(characater_bot)
            
    
    async def __add_character_in_match(self, characters: list[MatchCharacter]):
        for character_match in characters:
            character = await CharacterService.get_character_by_id(character_id=character_match.character_id)
            if character.club_id == self.first_club_id:
                self.first_club_characters.append(character)
            elif character.club_id == self.second_club_id:
                self.second_club_characters.append(character)



    def determine_winner_users(self) -> list[Character]:
        if self.goals_first_club > self.goals_second_club:
            return self.first_club_characters
        elif self.goals_second_club > self.goals_first_club:
            return self.second_club_characters
        else:
            return self.second_club_characters + self.first_club_characters


    @property
    def clubs_is_have_no_characters(self) -> bool:
        return not self.first_club_characters and not self.second_club_characters
    
    @property
    def first_club_power(self) -> float:
        return sum([character.full_power for character in self.first_club_characters]) + self.donate_energy_first_club//KOEF_ENERGY_DONATE

    @property
    def second_club_power(self) -> float:
        return sum([character.full_power for character in self.second_club_characters]) + self.donate_energy_second_club//KOEF_ENERGY_DONATE

    @property
    def calculate_chances(self):
        total_power = self.first_club_power + self.second_club_power
        
        return (self.first_club_power / total_power) * 100
  
    @property
    def all_characters_in_clubs(self) -> list[Character]:
        return self.first_club.characters + self.second_club.characters
    
    @property
    def all_characters_in_match(self) -> list[Character]:
        return self.first_club_characters + self.second_club_characters
    
    def check_chance_win(self):
        return check_chance(self.calculate_chances)