from datetime import datetime

from database.models.character import Character
from database.models.club import Club
from database.models.match_character import MatchCharacter
from database.models.duel import Duel
from database.models.league_fight import LeagueFight

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
        entity_type_label = "команд"

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

def get_top_duelists_ranking(all_duels: list[Duel], my_character: Character):
    total_points_by_character = defaultdict(int)
    characters_dict = {}

    # Подсчет очков за каждый дуэль и сбор информации о персонажах
    for duel in all_duels:
        characters_dict[duel.user_1.id] = duel.user_1.name
        characters_dict[duel.user_2.id] = duel.user_2.name
        
        if duel.get_winner_duel == [duel.user_1, duel.user_2]:
            # Ничья, каждому игроку по 1 очку
            total_points_by_character[duel.user_1.id] += 1
            total_points_by_character[duel.user_2.id] += 1
        else:
            # Победитель получает 3 очка
            winner = duel.get_winner_duel
            loser = duel.user_1 if winner == duel.user_2 else duel.user_2
            total_points_by_character[winner.id] += 3
            total_points_by_character[loser.id] += 0  # проигравший не получает очков

    # Преобразование словаря в список кортежей (id персонажа, очки)
    sorted_characters = sorted(total_points_by_character.items(), key=lambda item: item[1], reverse=True)

    rankings = []

    index = 0
    for character_id, total_points in sorted_characters[:15]:
        # Используем имя персонажа из дуэлей
        character_name = characters_dict.get(character_id, "Unknown")
        rank_icon = "🥇" if index == 0 else "🥈" if index == 1 else "🥉" if index == 2 else "⚔️"
        rankings.append(f"{index + 1:>2}. <b>{character_name:<10}</b> - {total_points:>5} очков {rank_icon}")
        index += 1
    
    top_15_header = f"Топ-15 дуелянтів за очками ⚔️\n\n"
    top_15_text = top_15_header + "\n".join(rankings)

    # Проверяем, есть ли персонаж среди тех, чьи очки были учтены
    my_character_id = my_character.id
    my_total_points = total_points_by_character.get(my_character_id, 0)
    
    if my_character_id in total_points_by_character:
        # Определение позиции пользователя на основе его ID
        position = [i for i, (char_id, _) in enumerate(sorted_characters) if char_id == my_character_id][0] + 1
        top_15_text += f"\n\nТи займаєш {position} місце з {my_total_points} очками 🏆"
    else:
        top_15_text += f"\n\nТи не увійшов у топ-15, але у тебе {my_total_points} очок 🏅"

    return top_15_text


def get_top_24_clubs(fights: list[LeagueFight]) -> str:
    club_points = {}
    club_goals_scored = {}
    club_goals_conceded = {}

    for fight in fights:
        for club_id in [fight.first_club_id, fight.second_club_id]:
            if club_id not in club_points:
                club_points[club_id] = 0
                club_goals_scored[club_id] = 0
                club_goals_conceded[club_id] = 0

        if fight.time_to_start <= datetime.now():
            club_points[fight.first_club_id] += fight.total_points_first_club
            club_goals_scored[fight.first_club_id] += fight.goal_first_club
            club_goals_conceded[fight.first_club_id] += fight.goal_second_club

            club_points[fight.second_club_id] += fight.total_points_second_club
            club_goals_scored[fight.second_club_id] += fight.goal_second_club
            club_goals_conceded[fight.second_club_id] += fight.goal_first_club

    rankings = []
    for club_id, points in club_points.items():
        club = next(fight.first_club if fight.first_club_id == club_id else fight.second_club
                    for fight in fights if fight.first_club_id == club_id or fight.second_club_id == club_id)

        goals_scored = club_goals_scored[club_id]
        goals_conceded = club_goals_conceded[club_id]
        goal_difference = goals_scored - goals_conceded

        rankings.append({
            'club_id': club_id,
            'club_name': club.name_club,
            'points': points,
            'goals_scored': goals_scored,
            'goals_conceded': goals_conceded,
            'goal_difference': goal_difference,
            'total_power': club.total_power  # Добавляем значение total_power
        })

    sorted_rankings = sorted(rankings, key=lambda x: (-x['points'], -x['goal_difference'], -x['goals_scored']))

    champions_league = sorted_rankings[:8]
    europa_league = sorted_rankings[8:16]
    conference_league = sorted_rankings[16:24]

    def format_league_section(league, title, emoji):
        return f"{title}\n" + "\n".join(
            f"<b>{index + 1}.</b> {rank['club_name']} {emoji} [💪 {rank['total_power']:.2f}] "
            f"[ОЧ {rank['points']}], "
            f"[РГ {'+' if rank['goal_difference'] >= 0 else ''}{rank['goal_difference']}]"
            for index, rank in enumerate(league)
        ) + "\n\n"

    ranking_table = "🏆 <b>Рейтинг команд</b>\n\n"
    ranking_table += format_league_section(champions_league, "<b><u>Ліга Чемпіонів</u></b>\n", "🏆")
    ranking_table += format_league_section(europa_league, "<b><u>Ліга Європи</u></b>\n", "⚽️")
    ranking_table += format_league_section(conference_league, "<b><u>Ліга Конференції</u></b>\n", "🌟")

    return ranking_table