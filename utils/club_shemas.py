# from config import PositionCharacter
 
# from services.match_character_service import MatchCharacterService
# from services.character_service import CharacterService

# from database.models.character import Character

# class SchemaClub:
    
#     first_sсhema = {
#         PositionCharacter.DEFENDER : 4,
#         PositionCharacter.MIDFIELDER : 4,
#         PositionCharacter.ATTACKER : 2,
#         PositionCharacter.GOALKEEPER : 1,
#     }
    
#     second_sсhema  = {
#         PositionCharacter.DEFENDER : 4,
#         PositionCharacter.MIDFIELDER : 3,
#         PositionCharacter.ATTACKER : 3,
#         PositionCharacter.GOALKEEPER : 1,
#     }
    
#     third_sсhema = {
#         PositionCharacter.MIDFIELDER : 3,
#         PositionCharacter.DEFENDER : 5,
#         PositionCharacter.ATTACKER : 2,
#         PositionCharacter.GOALKEEPER : 1,
#     }
    
#     quarter_sсhema = {
#         PositionCharacter.DEFENDER : 3,
#         PositionCharacter.MIDFIELDER : 4,
#         PositionCharacter.ATTACKER : 3,
#         PositionCharacter.GOALKEEPER : 1,
#     }
     
#     fifth_schema= {
#         PositionCharacter.DEFENDER : 5,
#         PositionCharacter.MIDFIELDER : 3,
#         PositionCharacter.ATTACKER : 2,
#         PositionCharacter.GOALKEEPER : 1,
#     }
    
#     sixth_schema= {
#         PositionCharacter.DEFENDER : 4,
#         PositionCharacter.MIDFIELDER : 5,
#         PositionCharacter.ATTACKER : 1,
#         PositionCharacter.GOALKEEPER : 1,
#     }
    
#     @classmethod
#     async def character_is_enough_room(cls, club_id: int, match_id: str, schema: str) -> bool:
#         characters_in_match = await MatchCharacterService.get_charaters_club_in_match(
#             match_id=match_id,
#             club_id=club_id)

#         characters:list[Character] = []
#         for character_match in characters_in_match:
#             character = await CharacterService.get_character_by_id(character_id=character_match.id)
#             characters.append(character)
            
#         limit_character = getattr(cls, schema)
#         count_exceeding = sum(1 for character in characters if character.position_enum > )