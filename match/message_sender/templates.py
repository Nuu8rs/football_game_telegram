import random

from enum import Enum

from match.entities import MatchData
from .types import SceneTemplate

NO_GOAL_EVENT_SCENES = [
    SceneTemplate(
        text="<b>{goalkeeper}</b> знову рятує свою команду! Зупиняє потужний удар від <b>{midfielder}</b>! 🧤🔥",
        required_positions=["goalkeeper", "midfielder"]
    ),
    SceneTemplate(
        text="<b>{goalkeeper}</b> вибиває м'яч з лінії воріт після удару <b>{defender}</b>! Ще один шанс для суперника змарнований! 💪🧤",
        required_positions=["goalkeeper", "defender"]
    ),
    SceneTemplate(
        text="<b>{defender}</b> чудово відпрацьовує в захисті, блокуючи удар <b>{midfielder}</b> в останній момент! 🦵⚔️",
        required_positions=["defender", "midfielder"]
    ),
    SceneTemplate(
        text="<b>{defender}</b> робить неймовірний підкат, не даючи <b>{attacker}</b> пробити по воротах! 🔥🦶",
        required_positions=["defender", "attacker"]
    ),
    SceneTemplate(
        text="<b>{midfielder}</b> розганяє контратаку, віддаючи передачу на <b>{attacker}</b>, але той не встигає замкнути! ⚡⚽",
        required_positions=["midfielder", "attacker"]
    ),
    SceneTemplate(
        text="<b>{midfielder}</b> перехоплює м'яч на половині поля, робить точну передачу на <b>{defender}</b>, але захист встигає вчасно! 🔥🎯",
        required_positions=["midfielder", "defender"]
    ),
    SceneTemplate(
        text="<b>{attacker}</b> наносить потужний удар з-за меж штрафного, але <b>{goalkeeper}</b> відбиває м'яч! 🥅⚡",
        required_positions=["attacker", "goalkeeper"]
    ),
    SceneTemplate(
        text="<b>{attacker}</b> виходить на ударну позицію, але <b>{defender}</b> встигає заблокувати м'яч! 🚫⚽",
        required_positions=["attacker", "defender"]
    )
]

GOAL_EVENT_SCENES = [
    SceneTemplate(
        text="<b>{assistant}</b> навішує у штрафний майданчик, <b>{scorer}</b> випереджає <b>{goalkeeper}</b> і головою відправляє м’яч у сітку! 🧠🥅",
        required_positions=["assistant", "scorer", "goalkeeper"]
    ),
    SceneTemplate(
        text="<b>{assistant}</b> тягне м'яч через усе поле, віддає пас п’ятою — <b>{scorer}</b> добиває! Вау! 😱🔥",
        required_positions=["assistant", "scorer"]
    ),
    SceneTemplate(
        text="<b>{midfielder}</b> елегантно відкриває фланг для <b>{assistant}</b>, той прострілює — <b>{scorer}</b> забиває у дотик! ⚡🎯",
        required_positions=["midfielder", "assistant", "scorer"]
    ),
    SceneTemplate(
        text="<b>{defender}</b> перехоплює передачу і миттєво запускає <b>{assistant}</b> у прорив. Після серії пасів <b>{scorer}</b> розстрілює ворота! 💥🏹",
        required_positions=["defender", "assistant", "scorer"]
    ),
    SceneTemplate(
        text="<b>{assistant}</b> виводить <b>{scorer}</b> один на один, і той холоднокровно переграє <b>{goalkeeper}</b>! ❄️⚽",
        required_positions=["assistant", "scorer", "goalkeeper"]
    ),
    SceneTemplate(
        text="<b>{midfielder}</b> тікає по флангу, обігрує суперника і віддає на <b>{scorer}</b>, який майстерно пробиває в нижній кут! 🎩🥅",
        required_positions=["midfielder", "scorer"]
    ),
    SceneTemplate(
        text="<b>{defender}</b> несподівано підключається до атаки і скидає на <b>{scorer}</b>, той пробиває без шансів для <b>{goalkeeper}</b>! 🚀🧤",
        required_positions=["defender", "scorer", "goalkeeper"]
    ),
    SceneTemplate(
        text="<b>{scorer}</b> самотужки проривається крізь оборону і потужно пробиває повз <b>{goalkeeper}</b>! 🦁💪",
        required_positions=["scorer", "goalkeeper"]
    ),
    SceneTemplate(
        text="<b>{scorer}</b> підбирає м’яч після рикошету, робить кілька фінтів і забиває фантастичний гол! 🎯🔥",
        required_positions=["scorer"]
    ),
    SceneTemplate(
        text="<b>{scorer}</b> несподівано підключається до атаки, обігрує трьох і кладе м'яч у дев’ятку! 🚀",
        required_positions=["scorer"]
    )
]

class TemplatesMatch(Enum):    
    START_MATCH = """
⚽️ Розпочинається епічний матч між командами <b>{name_first_club}</b> та <b>{name_second_club}</b>! 

🏟️ Місце зустрічі: <b>{stadium_name}</b>.

🔹 На поле виходять бойові склади:
- <b>{name_first_club}</b>: сила <b>{power_first_club:.2f}</b> 
- <b>{name_second_club}</b>: сила <b>{power_second_club:.2f}</b>

🔥 Нехай цей поєдинок покаже, хто найсильніший! 🏆
"""

    TEMPLATE_PARTICIPANTS_MATCH = """
📋 <b>Склад команд на матч:</b>

🔸 <b>{name_first_club}</b>
- Кількість гравців: <b>{members_first_club}</b>
- Гравці: 
{players_first_club}

🔸 <b>{name_second_club}</b>
- Кількість гравців: <b>{members_second_club}</b>
- Гравці: 
{players_second_club}

🏆 Гра обіцяє бути цікавою та напруженою!
"""
    
    TEMPLATE_PARTICIPANT = """
👤 {character_name} | ⚔️ Сила: <b>{power_user:.2f}</b> | 📈 Рівень: <b>{lvl}</b>
"""

    TEMPLATE_COMING_GOAL = """  
⚽️ <b>До вирішального моменту залишилося лише 40 секунд!</b> ⚽️  

🔥 <b>Поточні шанси на гол:</b>  
- ⚽️ Команда:{name_first_club} - <b>{chance_first_club:.2f}%</b>  
- ⚽️ Команда:{name_second_club} - <b>{chance_second_club:.2f}%</b>  

💪 <b>Ваша енергія може змінити хід гри!</b> Кожна одиниця енергії, яку ви надішлете, посилить вашу команду та збільшить ймовірність забити вирішальний гол! 🚀  

📣 <b>Підтримайте своїх! Це ваш шанс вплинути на результат матчу!</b>  

⏳ Залишилося лише 40 секунд — діяти потрібно зараз! Допоможіть вашій команді вирвати перемогу! 🏆  
"""  
    

class GetterTemplatesMatch:
    
    def __init__(self, match_data: MatchData) -> None:
        self.match_data = match_data
    
    def format_message(
        self, 
        template: TemplatesMatch, 
        extra_context: dict = {}
    ) -> str:
        
        context = {
            'name_first_club': self.match_data.first_club.club_name,
            'name_second_club': self.match_data.second_club.club_name,
            'goals_first_club': self.match_data.first_club.goals,
            'goals_second_club': self.match_data.second_club.goals,
            'power_first_club': self.match_data.first_club.total_power ,
            'power_second_club': self.match_data.second_club.total_power,
            'members_first_club': len(self.match_data.first_club.characters_in_match),
            'members_second_club': len(self.match_data.second_club.characters_in_match)
        }
        if extra_context:
            context.update(extra_context)
        return template.value.format(**context)    
