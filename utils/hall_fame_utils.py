from database.models.character import Character
from database.models.club import Club
from database.models.match_character import MatchCharacter

from collections import defaultdict


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
    total_goals_by_character = defaultdict(int)
    
    for match in all_matches:
        total_goals_by_character[match.character_id] += match.goals_count
    
    sorted_characters = sorted(total_goals_by_character.items(), key=lambda item: item[1], reverse=True)
    rankings = []
    
    all_real_characters = []
    
    index = 0
    for character_id, total_goals in sorted_characters:
        character = await CharacterService.get_character_by_id(character_id)
        if character.is_bot:
            continue
        rank_icon = "🥇" if index == 0 else "🥈" if index == 1 else "🥉" if index == 2 else "⚔️"
        rankings.append(f"{index + 1:>2}. <b>{character.name:<10}</b> - {total_goals:>5} забитих голів {rank_icon}")
        
        all_real_characters.append(character)
        index += 1
        
    top_15_header = f"Топ-15 бомбардирів за забитими голами ⚽\n\n"
    top_15_text = top_15_header + "\n".join(rankings[:15])

    my_character_id = my_character.id
    my_total_goals = total_goals_by_character.get(my_character_id, 0)
    
    if my_character_id in total_goals_by_character:
        position = [i for i, character in enumerate(all_real_characters) if character.id == my_character_id][0] + 1
        top_15_text += f"\n\nТи посідаєш {position} місце з {my_total_goals} голами 🏆"

    return top_15_text