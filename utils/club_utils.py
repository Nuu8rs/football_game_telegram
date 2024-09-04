from database.models import Club, Character

def get_club_text(club: Club, character: Character) -> str:
    text = f"""
⚽ Гравець: {character.name}

🏆 Клуб: {club.name_club}
👑 Лідер: {club.owner.user_name}
🏅 Дивізіон: {club.league}

📊 Моє місце в рейтингу клубу: {calculate_character_rank(
        my_character=character,
        characters_list=club.characters
    )}

💪 Загальна сила клубу: {club.total_power}
👥 Кількість членів у клубі: {len(club.characters)}
    """
    if club.link_to_chat:
        text += f'\n💬 Чат клубу: <a href="{club.link_to_chat}">Чат</a>'
    
    return text


def get_club_description(club: Club) -> str:
    text = f"""
⚽ Клуб: {club.name_club}

👑 Лідер: {club.owner.user_name}
🏅 Дивізіон: {club.league}
💪 Загальна сила клубу: {club.total_power}
👥 Кількість членів у клубі: {len(club.characters)}
    """
    return text


def calculate_character_rank(my_character: Character, characters_list: list[Character]) -> int:
    sorted_characters = sorted(characters_list, key=lambda character: character.full_power, reverse=True)
    for index, character in enumerate(sorted_characters, start=1):
        if character.id == my_character.id:
            return index
        


def rating_club(club: Club, character: Character) -> str:
    def get_medal_emoji(rank: int) -> str:
        if rank == 1:
            return "🥇"
        elif rank == 2:
            return "🥈"
        elif rank == 3:
            return "🥉"
        else:
            return ""

    sorted_characters = sorted(club.characters, key=lambda c: c.full_power, reverse=True)
    rank_texts = []
    for idx, char in enumerate(sorted_characters, start=1):
        medal = get_medal_emoji(idx)
        if char.characters_user_id == character.characters_user_id:
            rank_texts.append(f"{medal} {idx} місце - <b><a href='tg://user?id={char.characters_user_id}'>{char.name} 🩳</a></b>")
        else:
            rank_texts.append(f"{medal} {idx} місце - <a href='tg://user?id={char.characters_user_id}'>{char.name}</a>")
    ranking_text = "\n".join(rank_texts)
    return ranking_text