from aiogram import Bot

from database.models.character import Character
from database.models.club import Club

from services.character_service import CharacterService
from services.club_service import ClubService

from datetime import datetime, timedelta
from loader import logger, bot

async def get_club_text(club: Club, character: Character) -> str:
    character_leader = await CharacterService.get_character(character_user_id=club.owner.user_id)
    text_leader = f"{character_leader.name} [{character_leader.owner.link_to_user}] [💪 <b>{character_leader.full_power}</b>] [<b>{character_leader.level} рів.</b>]"
    club = await ClubService.get_club(club_id=club.id)
    
    text = f"""
⚽ Гравець: {character.name}

🏆 Клуб: {club.name_club}
👑 Лідер: {text_leader}
🏅 Дивізіон: {club.league}

📊 Моє місце в рейтингу клубу: {calculate_character_rank(
        my_character=character,
        characters_list=club.characters
    )}

💪 Загальна сила клубу: {club.total_power:.2f}
👥 Кількість членів у клубі: {len(club.characters)}
    """
    if club.link_to_chat:
        text += f'\n💬 Чат клубу: <a href="{club.link_to_chat}">Чат</a>'
    
    return text


async def get_club_description(club: Club) -> str:
    character_leader = await CharacterService.get_character(character_user_id=club.owner.user_id)
    text_leader = f"{character_leader.name} [{character_leader.owner.link_to_user}] [💪 <b>{character_leader.full_power}</b>] [<b>{character_leader.level} рів.</b>]"
    club = await ClubService.get_club(club_id=club.id)

    
    text = f"""
⚽ Клуб: {club.name_club}

👑 Лідер: {text_leader}
🏅 Дивізіон: {club.league}
💪 Загальна сила клубу: {club.total_power:.2f}
👥 Кількість членів у клубі: {len(club.characters)}
    """
    return text


def calculate_character_rank(my_character: Character, characters_list: list[Character]) -> int:
    sorted_characters = sorted(characters_list, key=lambda character: character.full_power, reverse=True)
    for index, character in enumerate(sorted_characters, start=1):
        if character.id == my_character.id:
            return index
        

def get_text_education_center_reward(exp: int, coins: int, delta_time_education_reward: timedelta) -> str:
    current_time = datetime.now()
    next_reward_time = current_time + delta_time_education_reward
    next_reward_time_formatted = next_reward_time.strftime("%d-%m-%Y %H:%M:%S")
    message = f"""
🎓 <b>Після навчального центру ваш персонаж отримав:</b>
✨ {exp} <b>досвіду</b>  
💰 {coins} <b>монет</b>

🕒 <b>Ви зможете отримати наступну нагороду через:</b> {delta_time_education_reward} <b>о {next_reward_time_formatted}</b>
"""
    return message


def rating_club(club: Club, character: Character) -> str:
    def get_medal_emoji(rank: int) -> str:
        if rank == 1:
            return "🥇"
        elif rank == 2:
            return "🥈"
        elif rank == 3:
            return "🥉"
        else:
            return "🏅"

    # Сортируем персонажей по убыванию силы
    sorted_characters = sorted(club.characters, key=lambda c: c.full_power, reverse=True)
    rank_texts = []
    
    for idx, char in enumerate(sorted_characters, start=1):
        medal = get_medal_emoji(idx)
        # Формируем строку с добавлением силы и уровня персонажа
        if char.characters_user_id == character.characters_user_id:
            rank_texts.append(
                f"{medal} {idx} місце - <b><a href='tg://user?id={char.characters_user_id}'>{char.name}</a>🩳 </b> "
                f"[💪 <b>{char.full_power}</b>] [<b>{char.level} рів.</b>]"
            )
        else:
            rank_texts.append(
                f"{medal} {idx} місце - <a href='tg://user?id={char.characters_user_id}'>{char.name}</a> "
                f"[<b>💪 {char.full_power}</b>] [<b>{char.level} рів.</b>]"
            )
    
    # Объединяем строки для финального текста
    ranking_text = "\n".join(rank_texts)
    return ranking_text


async def send_message_characters_club(characters_club: list[Character],
                                       my_character: Character, text: str):
    for character in characters_club:
        if character.characters_user_id == my_character.characters_user_id:
            continue
        try:
            await bot.send_message(chat_id= character.characters_user_id, text = text)
        except Exception as E:
            logger.error("НЕ СМОГ ОТПРАВИТЬ СООБЩЕНИЕ ПЕРСОНАЖУ {}")