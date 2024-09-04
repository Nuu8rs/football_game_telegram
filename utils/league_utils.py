from database.models import Club, LeagueFight
from league.club_fight import ClubFight
from datetime import datetime
from services.league_service import LeagueFightService

def get_future_matches_by_club(club: Club) -> list[ClubFight]: 
    current_time = datetime.now()
    
    all_fights_club = ClubFight.get_match_by_club(club)
    return [match for match in all_fights_club if match.start_time > current_time]
    
    
async def get_text_league(club: Club):

    current_match = await LeagueFightService.get_next_league_fight_by_club(club_id=club.id)
    if not current_match:
        return "⚽️ Твоя ліга: <b>{name_league}</b>\n\nМатчів немає, відпочивайте".format(name_league = club.league)
    
    fight_istance = ClubFight.get_fight_by_id(match_id=current_match.match_id)
    enemy_club = fight_istance.second_club_orig if club.id != fight_istance.second_club_orig.id else fight_istance.first_club_orig 
    
    text = """
⚽️ Твоя ліга: <b>{name_league}</b>

⚔️ <b>Наступний матч</b> ⚔️

🛑 <code>{first_name_club}</code>
<b>VS</b>
✳️ <code>{second_name_club}</code>

⏰ Час початку: <b>{time_fight}</b>
    """
    
    return text.format(
        name_league      = club.league,
        first_name_club  = club.name_club,
        second_name_club = enemy_club.name_club,
        time_fight       = fight_istance.start_time.strftime("%d:%m:%Y - %H:%M")
    )
    

def get_text_calendar_matches(matches: list[LeagueFightService], club_id: int):
    sorted_fights = sorted(matches, key=lambda fight: fight.time_to_start)

    schedule_table = "📅 <b>Розклад битв</b>\n\n"
    
    current_time = datetime.now()
    next_match_index = None

    for index, fight in enumerate(sorted_fights, start=1):
        if fight.first_club_id == club_id:
            my_club = fight.first_club
            opponent_club = fight.second_club
        else:
            my_club = fight.second_club
            opponent_club = fight.first_club
        
        if fight.time_to_start < current_time:
            match_status = "♟ Битва пройшла"
        else:
            match_status = "📍 Скоро буде"
            if next_match_index is None:
                next_match_index = index
                match_status = "🧤 Скоро буде"
        
        schedule_table += (
            f"{index}- тур. <b>{my_club.name_club}</b> vs <b>{opponent_club.name_club}</b>\n"
            f"🕒 Час початку: {fight.time_to_start.strftime('%d.%m.%Y %H:%M')}\n"
            f"<code>{match_status}</code>\n\n"
        )
    
    return schedule_table


def get_text_result(fights: list[LeagueFight], club_id: int):
    current_time = datetime.now()

    filtered_fights = [fight for fight in fights if fight.time_to_start < current_time]
    sorted_fights:list[LeagueFight] = sorted(filtered_fights, key=lambda fight: fight.time_to_start)

    schedule_table = "📅 <b>Результати битв</b>\n\n"
    
    for index, fight in enumerate(sorted_fights, start=1):
        if fight.first_club_id == club_id:
            my_club = fight.first_club
            opponent_club = fight.second_club
            my_score = fight.goal_first_club
            opponent_score = fight.goal_second_club
        else:
            my_club = fight.second_club
            opponent_club = fight.first_club
            my_score = fight.goal_second_club
            opponent_score = fight.goal_first_club
        
        # Определяем результат
        if my_score > opponent_score:
            result = "Перемога"
        elif my_score < opponent_score:
            result = "Поразка"
        else:
            result = "Нічия"
        
        schedule_table += (
            f"{index}-тур. <b>{my_club.name_club}</b> vs <b>{opponent_club.name_club}</b>\n"
            f"⚽ Рахунок: {my_score} : {opponent_score}\n"
            f"📊 Результат: {result}\n\n"
        )
    
    return schedule_table


def get_text_rating(fights):
    # Словари для подсчета очков, голов забитых, пропущенных и разницы голов
    club_points = {}
    club_goals_scored = {}
    club_goals_conceded = {}

    for fight in fights:
        # Инициализация данных для клубов, если еще не существует
        if fight.first_club_id not in club_points:
            club_points[fight.first_club_id] = 0
            club_goals_scored[fight.first_club_id] = 0
            club_goals_conceded[fight.first_club_id] = 0
        if fight.second_club_id not in club_points:
            club_points[fight.second_club_id] = 0
            club_goals_scored[fight.second_club_id] = 0
            club_goals_conceded[fight.second_club_id] = 0
        
        # Если время битвы еще не наступило, очки не добавляем
        if fight.time_to_start <= datetime.now():
            # Подсчет очков, забитых и пропущенных голов
            club_points[fight.first_club_id] += fight.total_points_first_club
            club_goals_scored[fight.first_club_id] += fight.goal_first_club
            club_goals_conceded[fight.first_club_id] += fight.goal_second_club
            
            club_points[fight.second_club_id] += fight.total_points_second_club
            club_goals_scored[fight.second_club_id] += fight.goal_second_club
            club_goals_conceded[fight.second_club_id] += fight.goal_first_club

    # Создание списка для сортировки
    rankings = []
    for club_id, points in club_points.items():
        club = next(fight.first_club if fight.first_club_id == club_id else fight.second_club
                    for fight in fights if fight.first_club_id == club_id or fight.second_club_id == club_id)
        
        goals_scored = club_goals_scored[club_id]
        goals_conceded = club_goals_conceded[club_id]
        goal_difference = goals_scored - goals_conceded

        rankings.append({
            'club_name': club.name_club,
            'points': points,
            'goals_scored': goals_scored,
            'goals_conceded': goals_conceded,
            'goal_difference': goal_difference
        })

    # Сортировка по очкам и разнице голов
    sorted_rankings = sorted(rankings, key=lambda x: (-x['points'], -x['goal_difference'], -x['goals_scored']))

    # Формирование таблицы рейтинга
    ranking_table = "🏆 <b>Таблиця Рейтингів</b>\n\n"
    medals = ["🥇", "🥈", "🥉"]
    for index, rank in enumerate(sorted_rankings, start=1):
        medal = medals[index-1] if index <= 3 else f"{index}."
        club_info = f"<b>{rank['club_name']}</b>"
        
        ranking_table += (
            f"{medal} {club_info}\n"
            f"Очки: {rank['points']}, ГЗ {rank['goals_scored']}; ГП {rank['goals_conceded']}, "
            f"РГ {'+' if rank['goal_difference'] >= 0 else ''}{rank['goal_difference']}\n\n"
        )
    
    return ranking_table