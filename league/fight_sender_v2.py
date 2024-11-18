import random
from typing import Optional

from aiogram.types import FSInputFile, InlineKeyboardButton

from bot.keyboards.league_keyboard import donate_energy_to_match

from database.models.character import Character
from database.models.club import Club

from utils.rate_limitter import rate_limiter
from .club_in_match import ClubsInMatch

from loader import bot, logger

goal_conceded = [
    "Воротар невдало відбив м'яч після удару суперника, і на добиванні нападник суперника першим опинився біля м'яча, забивши гол з близької відстані.",
    "Захисники помилилися в передачі, і нападник суперника перехопив м'яч, вийшов один на один з воротарем і відправив м'яч у сітку воріт.",
    "Після подачі з кутового нападник суперника виграв боротьбу у повітрі і головою переправив м'яч у ворота, воротар не встиг зреагувати.",
    "Півзахисник суперника пробив здалеку, і м'яч, рикошетом від захисника, змінив траєкторію, обманувши воротаря та залетівши у кут воріт.",
    "Воротар відбив пенальті, але суперник першим опинився біля м'яча і добив його в сітку.",
    "Команда суперника провела швидку контратаку, і нападник, отримавши передачу, обіграв захисників та воротаря, забивши м'яч у порожні ворота.",
    "Захисник невдало відбив м'яч після прострілу з флангу, і нападник суперника замкнув передачу точним ударом.",
    "Після подачі з кутового м'яч відскочив до нападника, який пробив точно у дальній кут.",
    "Нападник суперника отримав довгу передачу і вийшов сам на сам з воротарем, легко обігравши його.",
    "Півзахисник суперника пробив штрафний удар, і м'яч залетів точно у дев'ятку, воротар не зміг дотягнутися.",
    "Після серії передач на підступах до штрафного майданчика нападник суперника потужно пробив під перекладину.",
    "Воротар невдало вийшов на перехоплення після навісу, і захисник суперника головою відправив м'яч у сітку.",
    "Команда суперника розіграла швидку комбінацію, і нападник забив у порожні ворота після точного пасу партнера.",
    "Захисник спробував вибити м'яч, але влучив у свого партнера, і м'яч відскочив до нападника, який легко забив.",
    "Нападник суперника обіграв кількох захисників і з близької відстані пробив повз воротаря.",
    "Після рикошету м'яч опинився у штрафному майданчику, де нападник суперника першим встиг на удар.",
    "Воротар намагався вибити м'яч, але помилився, і нападник суперника перехопив м'яч, забивши у порожні ворота.",
    "Команда суперника виконала швидку атаку через центр, і нападник пробив точно в нижній кут.",
    "Після навісу з флангу м'яч відскочив до гравця суперника, який пробив у дотик, залишивши воротаря без шансів.",
    "Захисник порушив правила у штрафному майданчику, і нападник суперника впевнено реалізував пенальті."
]

no_goal = [
    "Воротар невдало відбив м'яч після удару суперника, і на добиванні нападник суперника першим опинився біля м'яча, забивши гол з близької відстані.",
    "Захисники помилилися в передачі, і нападник суперника перехопив м'яч, вийшов один на один з воротарем і відправив м'яч у сітку воріт.",
    "Після серії кутових захисники кілька разів вибивають м'яч з лінії воріт, не даючи супернику можливості пробити по воротах.",
    "Півзахисники в центрі поля ведуть запеклу боротьбу за м'яч, постійно відбираючи його один у одного, але жодна команда не може створити небезпечний момент.",
    "Нападник виходить на ударну позицію, але в останній момент захисник суперника підкатом вибиває м'яч з-під ніг.",
    "Воротар вибігає назустріч нападнику і блокує його удар в один дотик, врятувавши свою команду від голу.",
    "Після серії швидких атак захисники організовано відпрацьовують на підборах, не дозволяючи супернику завдати вирішального удару.",
    "Нападник суперника виходить на фланг, обігрує одного захисника, але інший блокує його спробу прострілу в штрафний майданчик.",
    "Півзахисник намагається пробити з-за меж штрафного, але м'яч влучає у стінку захисників.",
    "Нападник вийшов на ударну позицію, але захисник чудово відпрацював у підкаті, не давши йому можливості пробити.",
    "Після розіграшу кутового м'яч відскакує до захисників, які відразу ж виносять його подалі від воріт.",
    "Нападник суперника пробиває по воротах з близької відстані, але воротар парирує удар ногами.",
    "Півзахисник пробиває здалеку, але м'яч проходить вище воріт.",
    "Після навісу у штрафний майданчик воротар кулаками вибиває м'яч подалі від воріт.",
    "Команда намагається вивести нападника на ударну позицію, але захисник суперника в останній момент блокує передачу.",
    "Воротар упевнено ловить м'яч після подачі суперника зі штрафного.",
    "Півзахисник суперника проривається до воріт, але в останню мить захисник вибиває м'яч в підкаті.",
    "Після серії передач нападник виходить на удар, але влучає в захисника, який встиг поставити ногу під удар.",
    "Команди борються за контроль м'яча в центрі поля, не дозволяючи одна одній вийти на ударну позицію.",
    "Після швидкої атаки команда заробляє кутовий, але подача не доходить до нападників, і м'яч відлітає за межі поля."
]

goal_scored = [
    "Нападник отримав точний пас у штрафному майданчику, обіграв воротаря і спокійно відправив м'яч у порожні ворота.",
    "Після кутового захисник команди виграв боротьбу в повітрі та головою переправив м'яч у ворота суперника.",
    "Півзахисник пробив здалеку, і м'яч, минувши руки воротаря, залетів прямо в дев'ятку.",
    "Команда провела швидку контратаку, і нападник, отримавши пас від партнера, в один дотик пробив повз воротаря.",
    "Нападник відгукнувся на простріл з флангу і в дотик переправив м'яч у ворота.",
    "Гравець команди реалізував пенальті, точно пробивши у нижній кут воріт.",
    "Півзахисник обіграв кількох суперників і з-за меж штрафного майданчика пробив точно під перекладину.",
    "Після довгої комбінації нападник отримав пас у штрафному майданчику і з близької відстані пробив точно у ворота.",
    "Захисник підключився до атаки і після подачі з флангу точно пробив головою у кут воріт.",
    "Нападник реалізував вихід один на один з воротарем, пробивши точно у дальній кут.",
    "Півзахисник пробив здалеку, і м'яч пролетів повз кількох захисників та воротаря, опинившись у воротах.",
    "Нападник скористався помилкою захисників, які не змогли винести м'яч, і потужно пробив під перекладину.",
    "Після розіграшу штрафного нападник в один дотик відправив м'яч у ворота.",
    "Після серії рикошетів м'яч опинився у нападника, який пробив точно в нижній кут воріт.",
    "Команда провела швидку атаку через центр, і нападник завершив її точним ударом у кут.",
    "Півзахисник отримав м'яч на підступах до штрафного майданчика і пробив точно у кут воріт.",
    "Після довгої комбінації півзахисник віддав пас у штрафний майданчик, і нападник в один дотик забив гол.",
    "Після серії ударів по воротах нападник нарешті зумів пробити повз захисників та воротаря, забивши вирішальний гол.",
    "Команда організувала швидку атаку, і нападник забив у порожні ворота після точного пасу партнера.",
    "Захисник виграв боротьбу в повітрі після кутового і головою відправив м'яч точно у ворота суперника."
]


class TextsMatch:
    
    TEMPLATE_FIGHT = """
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
    
    TEMPLATE_PARTICIPANT = """👤 <b>{character_name:.20}</b> | ⚔️ Сила: <b>{power_user:.2f}</b> | 📈 Рівень: <b>{lvl}</b>"""
    
    TEMPLATE_NOT_CHARACTERS = """
На жаль, ніхто з учасників не з'явився на цей матч. 😔
    """

    TEMPLATE_END = """
🎉 Матч між командами <b>{name_first_club}</b> та <b>{name_second_club}</b> завершена! 

📊 Кінцевий рахунок: <b>{goals_first_club}</b> - <b>{goals_second_club}</b>.

{winner_section}

🏆 Дякуємо обом командам за чудову гру! Ви продемонстрували справжній дух суперництва та спортивності.

До нових зустрічей на футбольному полі! ⚽️
    """
    
    TEMPLATE_END_TIME = """
"⏱️ <b>Перший тайм завершено!</b> Команди повертаються на поле, щоб розпочати другий тайм. 
🔥 Підтримай свою команду та підсиль її шанси на перемогу — додай енергії через донат! ⚡️🔋 
Нехай переможе найсильніший!"
    """
    
    TEMPLATE_GOAL_EVENT = """
📊 <b>Поточний рахунок:</b>
——————————————
<b>{name_first_club}</b>   <b>{goals_first_club}</b> ⚽️ - ⚽️ <b>{goals_second_club}</b>   <b>{name_second_club}</b>
——————————————

{text_event_goal}

{text_how_to_goal}
"""
    
    TEXT_HOW_TO_GOAL = """
⚽️ <b>Гол:</b> <b>{last_goal_member}</b>
{asist_text}
    """
    
    TEXT_ASIST_GOAL = """
🅰️ <b>Асист:</b> <b>{last_assist_player}</b>
    """
    
    TEMPLATE_GET_REWARD = """
🎉 За цей матч між ви отримали:
✨ {exp_points} досвіду
💰 {coins} монет
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
  
  
class ClubMatchSender:
    
    def __init__(self, clubs_in_match: ClubsInMatch):
        self.clubs_in_match = clubs_in_match
        
    def _format_message(self, template: str, extra_context: dict = {}) -> str:
        context = {
            'name_first_club': self.clubs_in_match.first_club.name_club,
            'name_second_club': self.clubs_in_match.second_club.name_club,
            'goals_first_club': self.clubs_in_match.goals_first_club,
            'goals_second_club': self.clubs_in_match.goals_second_club,
            'power_first_club': self.clubs_in_match.first_club_power ,
            'power_second_club': self.clubs_in_match.second_club_power,
            'members_first_club': len(self.clubs_in_match.first_club_characters),
            'members_second_club': len(self.clubs_in_match.second_club_characters)
        }
        if extra_context:
            context.update(extra_context)
        return template.format(**context)
    
    async def send_start_match(self):
        text_fisrt_club = self._format_message(
            TextsMatch.TEMPLATE_FIGHT,
            extra_context = {
                "stadium_name" : self.clubs_in_match.first_club.custom_name_stadion
                }
        )
        text_second_club = self._format_message(
            TextsMatch.TEMPLATE_FIGHT,
            extra_context = {
                "stadium_name" : self.clubs_in_match.second_club.custom_name_stadion
                }
        )
        await self._send_messages(
            characters = self.clubs_in_match.first_club_characters,
            text       = text_fisrt_club,
            photo      = self.clubs_in_match.first_club.custom_photo_stadion
        )
        await self._send_messages(
            characters = self.clubs_in_match.second_club.characters,
            text  = text_second_club,
            photo = self.clubs_in_match.second_club.custom_photo_stadion
        )
        
    async def send_participants_characters(self) -> None:
        if self.clubs_in_match.first_club_characters:
            members_first_club =  "\n".join(
                TextsMatch.TEMPLATE_PARTICIPANT.format(
                    character_name=character.name, 
                    power_user=character.full_power, 
                    lvl=character.level)
                for character in self.clubs_in_match.first_club_characters)
        else:
            members_first_club = "Нема участників"
            
        if self.clubs_in_match.second_club_characters:
            members_second_club =  "\n".join(
                TextsMatch.TEMPLATE_PARTICIPANT.format(
                    character_name=character.name, 
                    power_user=character.full_power, 
                    lvl=character.level)
                for character in self.clubs_in_match.second_club_characters)
        else:
            members_second_club = "Нема участників"
            
        text = self._format_message(
            template = TextsMatch.TEMPLATE_PARTICIPANTS_MATCH,
            extra_context = {
                "players_first_club"   : members_first_club,
                "players_second_club"  : members_second_club
            }
        )
        await self._send_messages(
            characters = self.clubs_in_match.all_characters_in_match,
            text       = text,
            photo      = None
        )
        
    async def send_no_participants(self) -> None:
        await self._send_messages(
            characters = self.clubs_in_match.all_characters_in_match,
            text       = TextsMatch.TEMPLATE_NOT_CHARACTERS,
            photo      = None
        )
      
    async def send_coming_goal(self, goal_time: int) -> None:
        chance_first_club  = self.clubs_in_match.calculate_chances 
        chance_second_club = 100 - chance_first_club 
        
        text = self._format_message(
            template = TextsMatch.TEMPLATE_COMING_GOAL,
            extra_context = {
                "chance_first_club" : chance_first_club,
                "chance_second_club": chance_second_club
            }
        )
        keyboard = donate_energy_to_match(
            match_id = self.clubs_in_match.match_id,
            time_end_goal = goal_time
        )
        await self._send_messages(
            characters = self.clubs_in_match.all_characters_in_match,
            text = text,
            keyboard = keyboard
        )
        
    async def send_end_time(self) -> None:
        await self._send_messages(
            characters = self.clubs_in_match.all_characters_in_match,
            text       = TextsMatch.TEMPLATE_END_TIME,
            photo      = None
        )
    
    async def send_goal_event(self, characters: list[Character], goal_event: str) -> None:
        text_event_goal = self.get_text_goal_event(goal_event)
        text_how_to_goal = self.get_text_how_to_goal(goal_event)
        text = self._format_message(
            template = TextsMatch.TEMPLATE_GOAL_EVENT,
            extra_context = {
                "text_event_goal"  : text_event_goal,   
                "text_how_to_goal" : text_how_to_goal
            }
        )
        await self._send_messages(
            characters = characters,
            text       = text,
            photo      = None 
        )
    
    async def send_reward(self, 
                          character: Character,
                          exp: int,
                          money: int) -> None:
        text_reward = TextsMatch.TEMPLATE_GET_REWARD.format(
            exp_points = exp,
            coins = money
        )
        await self.__send_message(
            character = character,
            text = text_reward,
            photo = None
        )
    
    def get_text_goal_event(self, goal_event: str) -> str:
        if goal_event == "goal":
            return random.choice(goal_scored)
        elif goal_event == "no_goal":
            return random.choice(no_goal)
        else:
            return random.choice(goal_conceded)
    
    def get_text_how_to_goal(self, goal_event: str) -> str:
        if goal_event  == "no_goal":
            return ""
        
        text_asist_goal = ""
        if self.clubs_in_match.how_to_pass_goal:
            text_asist_goal = TextsMatch.TEXT_ASIST_GOAL.format(
                last_assist_player = self.clubs_in_match.how_to_pass_goal.name
            ) 
        return  TextsMatch.TEXT_HOW_TO_GOAL.format(
            last_goal_member   = self.clubs_in_match.how_to_increment_goal.name,
            asist_text = text_asist_goal,
            
        )
        
    def _determine_winner_loser(self) -> tuple[dict, dict]:
        if self.clubs_in_match.goals_first_club > self.clubs_in_match.goals_second_club:
            return (
                {'club_name': self.clubs_in_match.first_club.name_club, 'goals': self.clubs_in_match.goals_first_club},
                {'club_name': self.clubs_in_match.second_club.name_club, 'goals': self.clubs_in_match.goals_second_club}
            )
        else:
            return (
                {'club_name': self.clubs_in_match.second_club.name_club, 'goals': self.clubs_in_match.goals_second_club},
                {'club_name': self.clubs_in_match.first_club.name_club, 'goals': self.clubs_in_match.goals_first_club}
            )

    async def send_end_match(self) -> None:
        if self.clubs_in_match.goals_first_club == self.clubs_in_match.goals_second_club:
            winner_section = "🎉 Матч завершився внічию!"
        else:
            winner, loser = self._determine_winner_loser()
            winner_section = f"""
🥇 Переможець: <b>{winner['club_name']}</b> з рахунком <b>{winner['goals']}</b>! 
🥈 Друге місце: <b>{loser['club_name']}</b> з рахунком <b>{loser['goals']}</b>.
            """
        
        text = self._format_message(
            template = TextsMatch.TEMPLATE_END,
            extra_context = {
                "winner_section" : winner_section
            }
        )

        await self._send_messages(
            characters = self.clubs_in_match.all_characters_in_match,
            text       = text,
            photo      = None
        )
    
    async def _send_messages(self,
                             characters: list[Character],
                             text: str,
                             photo: FSInputFile | None = None,
                             keyboard: Optional[InlineKeyboardButton] = None
                             ) -> None:
        
        for character in characters:
            await self.__send_message(
                character = character,
                text      = text,
                photo     = photo,
                keyboard  = keyboard
            )
              
    async def __send_message(self, 
                             character: Character,
                             text: str, 
                             photo: FSInputFile | None = None,
                             keyboard: Optional[InlineKeyboardButton] = None

                             ) -> None:
        try:
            if character.is_bot:
                return None
            
            if not photo:
                await bot.send_message(
                    chat_id = character.characters_user_id,
                    text    = text,
                    reply_markup = keyboard
                )
            else:
                await bot.send_photo(
                    chat_id = character.characters_user_id,
                    photo = photo,
                    caption = text,
                    reply_markup = keyboard
                )
        except Exception as E:
            logger.error(f"Err {E} send message to {character.name}")