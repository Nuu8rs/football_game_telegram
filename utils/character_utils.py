from constants import Gender
from database.models.character import Character

def get_character_text(character: Character) -> str:
    gender_specific_text = {
        Gender.MAN: "Він завжди перемагає!",
        Gender.WOMAN: "Вона - зірка на полі!"
    }

    current_level = character.level
    if current_level >= len(character.LEVEL_THRESHOLDS):
        next_level_threshold = "∞"
    else:
        next_level_threshold = character.LEVEL_THRESHOLDS[current_level-1]

    level_text = f"<b>🏆 Рівень:</b> {character.level} [{character.exp}/{next_level_threshold}]"
    
    # Проверка экипированных вещей
    t_shirt_text = character.t_shirt.name if character.t_shirt else "Не экипировано"
    shorts_text = character.shorts.name if character.shorts else "Не экипировано"
    gaiters_text = character.gaiters.name if character.gaiters else "Не экипировано"
    boots_text = character.boots.name if character.boots else "Не экипировано"

    # Шаблон с добавлением информации о вещах
    character_text_template = f"""
<b>⚽ Персонаж:</b> {character.name}

{level_text}
<b>💰 Монети:</b> {character.money}

<b>👤 Стать:</b> {character.gender_enum.value}
<b>🏅 Позиція:</b> {character.position_description} 

<b>🎯 Техніка:</b> {character.effective_technique}
<b>🥋 Удари:</b> {character.effective_kicks}
<b>🛡️ Відбір м’яча:</b> {character.effective_ball_selection}
<b>⚡ Швидкість:</b> {character.effective_speed}
<b>🏃 Витривалість:</b> {character.effective_endurance}

<b>💪 Сумарна сила:</b> {character.full_power:.1f}

<b>🔋 Енергія:</b> {character.current_energy}/{character.max_energy}

<b>👕 Футболка:</b> {t_shirt_text}
<b>🩳 Шорти:</b> {shorts_text}
<b>🧦 Гетри:</b> {gaiters_text}
<b>👟 Бутси:</b> {boots_text}

<i>{gender_specific_text[character.gender_enum]}</i>
"""

    return character_text_template.strip()