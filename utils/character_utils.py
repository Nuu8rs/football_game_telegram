from constants import Gender
from database.models import Character

def get_character_text(character: Character) -> str:
    gender_specific_text = {
        Gender.MAN: "Він завжди перемагає!",
        Gender.WOMAN: "Вона - зірка на полі!"
    }
    
    character_text_template = f"""
<b>⚽ Персонаж:</b> {character.name}
<b>👤 Стать:</b> {character.gender_enum.value}
<b>🏅 Позиція:</b> {character.position_description} 

<b>🎯 Техніка:</b> {character.technique}
<b>🥋 Удари:</b> {character.kicks}
<b>🛡️ Відбір м’яча:</b> {character.ball_selection}
<b>⚡ Швидкість:</b> {character.speed}
<b>🏃 Витривалість:</b> {character.endurance}

<b>💪 Суммарна сила:</b> {character.full_power:.1f}

<b>🔋 Енергія:</b> {character.current_energy}/{character.max_energy}

<i>{gender_specific_text[character.gender_enum]}</i>
"""
    
    return character_text_template.strip()