from database.models.character import Character
from database.models.club import Club
from database.models.match_character import MatchCharacter

from services.character_service import CharacterService

def generate_rankings(entities, my_entity, entity_type, sorting_attribute, display_attribute, ranking_label):
    sorted_entities = sorted(entities, key=lambda entity: getattr(entity, sorting_attribute), reverse=True)

    rankings = []
    for index, entity in enumerate(sorted_entities[:15]):
        rank_icon = "🥇" if index == 0 else "🥈" if index == 1 else "🥉" if index == 2 else "⚔️"

        entity_name = ""
        display_value = 0
        display_format = "{:>5.2f}"  

        if entity_type == 'character':
            entity_name = entity.name
            display_value = getattr(entity, display_attribute)
            if display_attribute == 'level':
                display_format = "{:>5}"  
        elif entity_type == 'club':
            entity_name = entity.name_club
            display_value = getattr(entity, display_attribute)

        rankings.append(f"{index + 1:>2}. {entity_name:<15} - {display_format.format(display_value)} {ranking_label} {rank_icon}")
        
    if entity_type == 'character':
        entity_type_label = "персонажів"
    else:
        entity_type_label = "клубів"

    top_15_header = f"Топ-15 найкращих {entity_type_label} за {ranking_label} 💪\n\n"
    top_15_text = top_15_header + "\n".join(rankings)

    my_entity_id = getattr(my_entity, 'characters_user_id' if entity_type == 'character' else 'id')
    current_entity = next((entity for entity in sorted_entities if getattr(entity, 'characters_user_id' if entity_type == 'character' else 'id') == my_entity_id), None)

    if current_entity:
        position = sorted_entities.index(current_entity) + 1
        top_15_text += f"\n\nТи посідаєш {position} місце 🏆"


    return f"{top_15_text}"

def get_top_characters_by_power(all_characters: list[Character], my_character: Character) -> str:
    return generate_rankings(all_characters, my_character, 'character', 'full_power', 'full_power', 'силою')


def get_top_characters_by_level(all_characters: list[Character], my_character: Character) -> str:
    return generate_rankings(all_characters, my_character, 'character', 'exp', 'level', 'рівня')


def get_top_club_by_power(all_clubs: list[Club], my_club: Club) -> str:
    return generate_rankings(all_clubs, my_club, 'club', 'total_power', 'total_power', 'силою')


async def get_top_bomber_raiting(all_matches: list[MatchCharacter], my_character: Character):
    sorted_charactets_match = sorted(all_matches, key=lambda entity: getattr(entity, "goals_count"), reverse=True)
    rankings = []
    for index, character_match in enumerate(sorted_charactets_match[:15]):
        rank_icon = "🥇" if index == 0 else "🥈" if index == 1 else "🥉" if index == 2 else "⚔️"
        character = await CharacterService.get_character_by_id(character_match.character_id)
        
        
        rankings.append(f"{index + 1:>2}. {character.name:<15} - {character_match.goals_count} голів {rank_icon}")
    top_15_header = f"Топ-15 найкращих бомбардирів за голами 💪\n\n"
    top_15_text = top_15_header + "\n".join(rankings)
    
    current_character = next((character_match for character_match in sorted_charactets_match if character_match.character_id == my_character.id),None)
    if current_character:
        position = sorted_charactets_match.index(current_character) + 1
        top_15_text += f"\n\nТи посідаєш {position} місце 🏆"
        
    return top_15_text