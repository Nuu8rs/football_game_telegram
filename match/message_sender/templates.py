import random

from enum import Enum

from match.entities import MatchData
from .types import SceneTemplate

NO_GOAL_EVENT_SCENES = [
    SceneTemplate(
        text="Неймовірно! 🧤 <b>{goalkeeper}</b> стрибає, мов кіт, і витягує потужний удар від <b>{enemy_midfielder}</b>! Здавалося, м’яч вже летів у кут воріт, але воротар демонструє справжнє диво реакції. Команду знову врятовано! 🔥💪",
        required_positions=["goalkeeper", "enemy_midfielder"]
    ),
    SceneTemplate(
        text="Шалена напруга! <b>{enemy_defender}</b> пробиває з близької відстані після кутового, але <b>{goalkeeper}</b> в останню мить виставляє руку і вибиває м’яч з лінії воріт! Фантастичне спасіння! 🫣🧱 Команда дихає з полегшенням.",
        required_positions=["goalkeeper", "enemy_defender"]
    ),
    SceneTemplate(
        text="<b>{enemy_midfielder}</b> вже замахується на удар, але <b>{defender}</b> вчасно кидається під м’яч і блокує спробу! Миттєва реакція захисника рятує від проблем. Який самовідданий момент! 🦸‍♂️⚔️",
        required_positions=["defender", "enemy_midfielder"]
    ),
    SceneTemplate(
        text="<b>{enemy_attacker}</b> входить у штрафний майданчик і готується до удару, але <b>{defender}</b> блискавично виконує ідеальний підкат! Суперник падає, м'яч у захисника. Справжнє мистецтво оборони! 🔥🦶",
        required_positions=["defender", "enemy_attacker"]
    ),
    SceneTemplate(
        text="<b>{midfielder}</b> розганяє контратаку з центру поля, точною передачею виводить <b>{enemy_attacker}</b> на удар, але той не встигає замкнути момент! Захисники повертаються в останню мить. ⚡️⚽️",
        required_positions=["midfielder", "enemy_attacker"]
    ),
    SceneTemplate(
        text="<b>{midfielder}</b> перехоплює м’яч на половині суперника, передає на <b>{enemy_defender}</b>, який несподівано підключився до атаки, але оборона миттєво зреагувала. Ще трохи — і це міг бути гол! 🔥🎯",
        required_positions=["midfielder", "enemy_defender"]
    ),
    SceneTemplate(
        text="<b>{attacker}</b> наносить щільний удар з-за меж штрафного — м’яч летить просто під поперечину! Але <b>{enemy_goalkeeper}</b> в неймовірному стрибку парирує! Яка гра воротаря! 🥅⚡️",
        required_positions=["attacker", "enemy_goalkeeper"]
    ),
    SceneTemplate(
        text="<b>{attacker}</b> знаходить простір між захисниками, готується пробити, але <b>{enemy_defender}</b> кидається під м’яч і блокує момент! Це був останній шанс забити, і він згаяний! 🚫⚽️",
        required_positions=["attacker", "enemy_defender"]
    )
]
GOAL_EVENT_SCENES = [
    SceneTemplate(
        text="<b>{assistant}</b> навішує у штрафний майданчик, <b>{scorer}</b> випереджає <b>{enemy_goalkeeper}</b> і головою відправляє м’яч у сітку! 🧠🥅",
        required_positions=["assistant", "scorer", "enemy_goalkeeper"]
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
        text="<b>{assistant}</b> перехоплює передачу у <b>{enemy_defender}</b> і миттєво запускає <b>{scorer}</b> у прорив. Після серії пасів — розстріл воріт! 💥🏹",
        required_positions=["enemy_defender", "assistant", "scorer"]
    ),
    SceneTemplate(
        text="<b>{assistant}</b> виводить <b>{scorer}</b> один на один, і той холоднокровно переграє <b>{enemy_goalkeeper}</b>! ❄️⚽",
        required_positions=["assistant", "scorer", "enemy_goalkeeper"]
    ),
    SceneTemplate(
        text="<b>{assistant}</b> тікає по флангу, обігрує суперника і віддає на <b>{scorer}</b>, який майстерно пробиває в нижній кут! 🎩🥅",
        required_positions=["assistant", "scorer"]
    ),
    SceneTemplate(
        text="<b>{assistant}</b> несподівано підключається до атаки і скидає на <b>{scorer}</b>, той пробиває без шансів для <b>{enemy_goalkeeper}</b>! 🚀🧤",
        required_positions=["assistant", "scorer", "enemy_goalkeeper"]
    ),
    SceneTemplate(
        text="<b>{scorer}</b> самотужки проривається крізь оборону і потужно пробиває повз <b>{enemy_goalkeeper}</b>! 🦁💪",
        required_positions=["scorer", "enemy_goalkeeper"]
    ),
    SceneTemplate(
        text="<b>{scorer}</b> підбирає м’яч після рикошету, робить кілька фінтів і забиває фантастичний гол! 🎯🔥",
        required_positions=["scorer"]
    ),
    SceneTemplate(
        text="<b>{scorer}</b> несподівано підключається до атаки, обігрує трьох і кладе м'яч у дев’ятку! 🚀",
        required_positions=["scorer"]
    ),

    # enemy_goalkeeper
    SceneTemplate(
        text="<b>{scorer}</b> пробиває з дальньої дистанції — <b>{enemy_goalkeeper}</b> тягнеться, але м'яч влітає у кут! 🔥🧤",
        required_positions=["scorer", "enemy_goalkeeper"]
    ),
    SceneTemplate(
        text="<b>{assistant}</b> дає ідеальний пас на <b>{scorer}</b>, той обігрує <b>{enemy_goalkeeper}</b> і спокійно закочує м’яч у ворота. ❄️⚽",
        required_positions=["assistant", "scorer", "enemy_goalkeeper"]
    ),
    SceneTemplate(
        text="<b>{scorer}</b> виходить один на один, <b>{enemy_goalkeeper}</b> намагається скоротити кут — але без шансів! ГОЛ! 💪🥅",
        required_positions=["scorer", "enemy_goalkeeper"]
    ),

    # enemy_defender
    SceneTemplate(
        text="<b>{scorer}</b> обігрує <b>{enemy_defender}</b> двічі і потужно б’є у ближній кут! 🎯🔥",
        required_positions=["scorer", "enemy_defender"]
    ),
    SceneTemplate(
        text="<b>{assistant}</b> пускає м’яч між ніг <b>{enemy_defender}</b>, <b>{scorer}</b> підхоплює і забиває! 🤯⚽",
        required_positions=["assistant", "scorer", "enemy_defender"]
    ),
    SceneTemplate(
        text="<b>{enemy_defender}</b> намагається перехопити, але <b>{scorer}</b> блискавично реагує і добиває у ворота! ⚡🥅",
        required_positions=["scorer", "enemy_defender"]
    ),

    # enemy_midfielder
    SceneTemplate(
        text="<b>{enemy_midfielder}</b> втрачає м’яч у центрі поля — <b>{assistant}</b> перехоплює, пас на <b>{scorer}</b> — ГОЛ! 💥",
        required_positions=["enemy_midfielder", "assistant", "scorer"]
    ),
    SceneTemplate(
        text="<b>{assistant}</b> прокидає повз <b>{enemy_midfielder}</b> і знаходить <b>{scorer}</b>, який завершив атаку! 🚀🎯",
        required_positions=["assistant", "scorer", "enemy_midfielder"]
    ),
    SceneTemplate(
        text="<b>{scorer}</b> переграє <b>{enemy_midfielder}</b> в один дотик і б’є не залишаючи шансів воротарю! ⚽🔥",
        required_positions=["scorer", "enemy_midfielder"]
    ),

    # enemy_attacker
    SceneTemplate(
        text="<b>{enemy_attacker}</b> втрачає м'яч у нападі, <b>{assistant}</b> миттєво віддає на <b>{scorer}</b> — контратака успішна! 🎯💨",
        required_positions=["enemy_attacker", "assistant", "scorer"]
    ),
    SceneTemplate(
        text="<b>{enemy_attacker}</b> не встигає повернутися в оборону, і <b>{scorer}</b> користується вільним простором! 🏃‍♂️🔥",
        required_positions=["scorer", "enemy_attacker"]
    ),
    SceneTemplate(
        text="<b>{scorer}</b> перехоплює передачу від <b>{enemy_attacker}</b> і миттєво забиває з-за меж штрафного! 💥🥅",
        required_positions=["scorer", "enemy_attacker"]
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
👤 {character_name} | ⚔️ Сила: <b>{power_user:.2f}</b> | 📈 Рівень: <b>{lvl}</b>"""

    TEMPLATE_COMING_GOAL = """  
⚽️ <b>До вирішального моменту залишилося лише 40 секунд!</b> ⚽️  

🔥 <b>Поточні шанси на гол:</b>  
- ⚽️ Команда:{name_first_club} - <b>{chance_first_club:.2f}%</b>  
- ⚽️ Команда:{name_second_club} - <b>{chance_second_club:.2f}%</b>  

💥 <b>Це момент істини!</b>
Ваша енергія може стати тим самим поштовхом, що змінить усе — підтримайте свою команду, і вона проб’є точно в ціль! 🚀

✨ <b>Досягніть {min_donate_energy_bonus} енергії</b> в цьому епізоді — і отримаєте буст <b>+{koef_donate_energy}% до суми донату</b>!
Цей бонус посилить удар і збільшить шанси забити гол! ⚡️

📣 <b>Усе в ваших руках!</b>
⏳ Лише <b>40 секунд</b>, щоб вплинути на хід епізоду!
<b>Надішліть енергію</b> — і допоможіть команді пробити ворота! 🥅🏆
"""  

    TEMPLATE_END = """
🎉 Матч між командами <b>{name_first_club}</b> та <b>{name_second_club}</b> завершена! 

📊 Кінцевий рахунок: <b>{goals_first_club}</b> - <b>{goals_second_club}</b>.

{match_information}

🏆 Дякуємо обом командам за чудову гру! Ви продемонстрували справжній дух суперництва та спортивності.

До нових зустрічей на футбольному полі! ⚽️
    """
    
    DRAW_TEMPLATE = """
Матч завершився внічию! ⚽
"""
    
    WIN_LOSE_TEMPLATE = """
🥇 Переможець: <b>{winner_club_name}</b>! 
🥈 Друге місце: <b>{loser_club_name}</b>.
"""

    TEMPLATE_REWARD_CHARACTER = """
🎁 Нагорода за твій виступ у матчі між Dragons та Sharks:

🏅 Ти проявив чудову гру, і ось твої нагороди:

- 🎖 EXP: +{exp}
- 🪙 Money: +{money}
"""

    TEMPLATE_NO_CHARACTERS_IN_MATCH = """
⚠️ <b>На жаль, цього разу в матчі немає учасників!</b>

❌ Жоден гравець не приєднався до гри, тому матч не відбувся.

🔜 <b>Не переживай!</b> Продовжуй тренуватися та готуйся до наступних матчів. Твої шанси на перемогу неодмінно зростатимуть!

⚽️ Залишайся з нами, нові матчі вже на підході!
"""
    
    TEMPLATE_SCORE = """
⚽️ <b>{scoring_club}</b> забиває гол!

🏟 Матч: <b>{name_first_club}</b> — <b>{name_second_club}</b>
📊 Рахунок: <b>{goals_first_club}</b> - <b>{goals_second_club}</b>
"""

    TEMPLATE_MVP_CONGRATULATION = """
🔥 У цьому матчі яскраво проявили себе два гравці — вони стали <b>MVP зустрічі</b>!

Їхній вклад у гру був вирішальним, і за це вони отримують заслужені нагороди. 👏

🎁 <b>Нагороди вже нараховано кожному з MVP:</b>
- 🔑Ключ на тренування с тренером
{text_mvp_characters}
Велика повага цим лідерам команди!
"""
    TEMPLATE_MVP_PLAYER_POINTS = """
⭐️ <b>{nickname}</b> — {points} очок
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
            'power_first_club': self.match_data.first_club.club_power ,
            'power_second_club': self.match_data.second_club.club_power,
            'members_first_club': len(self.match_data.first_club.characters_in_match),
            'members_second_club': len(self.match_data.second_club.characters_in_match)
        }
        if extra_context:
            context.update(extra_context)
        return template.value.format(**context)    
