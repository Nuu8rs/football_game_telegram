
from database.models.user_bot import STATUS_USER_REGISTER
from .constans import (
    START_REGISTER_PHOTO,
    CREATER_CHARACTER_PHOTO,
    SEND_NAME_CHARACTER_PHOTO,
    SELECT_POSITION_PHOTO,
    TERRITORY_ACADEMY_PHOTO,
    JOIN_TO_CLUB_PHOTO,
    FIRST_TRAINING_PHOTO,
    FORGOT_TRAINING_PHOTO,
    SELECT_GENDER_PHOTO,
)

PHOTO_STAGE_REGISTER_USER = {
    STATUS_USER_REGISTER.START_REGISTER : START_REGISTER_PHOTO, 
    STATUS_USER_REGISTER.CREATER_CHARACTER : CREATER_CHARACTER_PHOTO,
    STATUS_USER_REGISTER.SEND_NAME_CHARACTER : SEND_NAME_CHARACTER_PHOTO,
    STATUS_USER_REGISTER.SELECT_GENDER : SELECT_GENDER_PHOTO, 
    STATUS_USER_REGISTER.SELECT_POSITION : SELECT_POSITION_PHOTO,
    STATUS_USER_REGISTER.TERRITORY_ACADEMY : TERRITORY_ACADEMY_PHOTO,
    STATUS_USER_REGISTER.JOIN_TO_CLUB : JOIN_TO_CLUB_PHOTO,
    STATUS_USER_REGISTER.FIRST_TRAINING : FIRST_TRAINING_PHOTO,
    STATUS_USER_REGISTER.FORGOT_TRAINING : FORGOT_TRAINING_PHOTO
}
from config import LINK_TO_CHAT


TEXT_STAGE_REGISTER_USER = {
    
    STATUS_USER_REGISTER.START_REGISTER : """
<b>WELCOME TO THE GAME</b>
    
📍 <b>Локація: Ворота футбольної академії</b>

<i>(Ти виходиш з автобуса, тримаючи сумку з екіпіруванням. Перед тобою – величезні ворота з емблемою академії.)</i>    
""",

    STATUS_USER_REGISTER.CREATER_CHARACTER : """
🔹 <b>Тренер</b>:
<i>— Нарешті! Новенький? Добре, що прийшов.</i>

<b>У нас тут справжня</b> <b>онлайн гра</b> <b>-</b> <b>турнір</b>, де сотні гравців щодня виходять на поле. Команди, матчі, боротьба — усе по-справжньому. ⚽️🔥

Але перш ніж зробиш свій перший пас —
ти маєш створити персонажа

<b><u>🔽 НАТИСКАЙ КНОПКУ “СТВОРИТИ ПЕРСОНАЖА” 🔽</u></b>
""",

    STATUS_USER_REGISTER.SEND_NAME_CHARACTER : """
🔹 <b>Тренер</b>: Як тебе звати на полі?    
""",

    STATUS_USER_REGISTER.SELECT_POSITION : """
🔹 <b>Тренер</b>: А тепер визначимо твою позицію на полі!

🥅 <b>Воротар</b> – останній рубіж оборони.
🛡️ <b>Захисник</b> – непрохідна стіна для суперників.
🎩 <b>Півзахисник</b> – мозок команди, керує грою.
⚽ <b>Нападник</b> – головний бомбардир, забиває голи.    
""",

    STATUS_USER_REGISTER.TERRITORY_ACADEMY : """
📍 <b>Локація: Територія Академії</b>

<i>(Тренер веде тебе територією академії, пояснюючи основні місця.)</i>

⚽️ <b>Матчі</b> – тут проходять матчі. Саме тут ти зможеш проявити себе і заробити славу.
💪 <b>Тренування</b> – місце, де ти будеш тренуватися та покращувати свої навички.
📚 <b>Навчальний центр</b> – тут ти можеш вчитися новим прийомам і тактикам.
🛒 <b>Магазин –</b> тут знайдеш екіпірування, бонуси та корисні предмети.
🏆 <b>Зал слави</b> – місце, де зберігаються досягнення найкращих гравців.

🔹 <b>Тренер</b>: Запам’ятав? Чудово!    
""",

    STATUS_USER_REGISTER.JOIN_TO_CLUB : """
<b>🧢 Тренер:</b>
<i>-Тепер найважливіше — обирай команду або створюй свою! ⚽️</i>

<b>🔹 Ти новенький у грі?</b>
<i>👉 Раджу приєднатися до існуючої команди.</i>
Там вже є досвідчені гравці, вони допоможуть розібратись.
📈 Так ти швидко почнеш грати та розвиватись.

<b>🔹 Хочеш бути капітаном і керувати?</b>
<i>👉 Тоді створюй свою команду.</i>
Але май на увазі:
📆 Нова команда почне грати тільки з 1 числа наступного місяця.
Тобто, якщо створиш її зараз — доведеться чекати старту сезону.
""",

    STATUS_USER_REGISTER.FIRST_TRAINING : """
🔹 <b>Тренер</b>: Ну що ж, тепер ти в команді, але це лише початок. Справжні легенди народжуються на тренуваннях.

⚽ <b>Перше тренування допоможе тобі отримати перші навички та бонуси. Не пропусти!</b>    
🔽 <b>НАТИСКАЙ КНОПКУ "РОЗПОЧАТИ ПЕРШЕ ТРЕНУВАННЯ" </b>🔽
""",

    STATUS_USER_REGISTER.SELECT_GENDER : """
🔹 <b>Тренер</b>: Яка стать у твого персонажа?
""",

    STATUS_USER_REGISTER.END_TRAINING : f"""
🔹 <b>Тренер:</b> Вітаю із завершенням базового тренування! Тепер перед тобою відкритий світ TG Football. Уже за 5 хвилин ти завершиш своє перше повноцінне тренування!

Що далі?
✅ <b><a href="{LINK_TO_CHAT}">Приєднуйся до нашого чату</a></b> – спілкуйся з іншими гравцями.
✅ <b>Реєструйся у найближчий матч</> (локація: Стадіон) – виходь на поле разом із командою!
✅ <b>Тренуйся, розвивай свого футболіста та досягай перемог разом із командою!</b>

Разом – до вершини! ⚽️🔥
""",

    STATUS_USER_REGISTER.FORGOT_TRAINING : """
🔹 Тренер:
— Залишився лише один крок! Пройди створення гравця до кінця — і отримай 300 сили в подарунок, а також гроші і досвід для перших покупок екіпірування: футболки, бутсів і шортів. ⚡️👕👟🩳🔥

Твоя команда вже чекає на тебе в грі. Почни зараз і вийди на поле сильнішим!
"""
}


TEXT_CHARACTER = """
<b>⚽ Персонаж:</b> {character_name}

<i>Це ваш стартовий персонаж з початковими статами для обраної позиції.</i>

<b>👤 Стать:</b> {gender}
<b>🎯 Техніка:</b> {effective_technique:.1f}
<b>🥋 Удари:</b> {effective_kicks:.1f}
<b>🛡️ Відбір м’яча:</b> {effective_ball_selection:.1f}
<b>⚡ Швидкість:</b> {effective_speed:.1f}
<b>🏃 Витривалість:</b> {effective_endurance:.1f}

<b>💪 Сумарна сила:</b> {full_power:.1f}
"""