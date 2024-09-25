from database.models.item import Item
from database.models.character import Character

import aiofiles
import json


def view_my_item_text(item: Item) -> str:
    category_name = {
    'T_SHIRT' : "Футболки", 
    'SHORTS'  : "Шорти", 
    'GAITERS' : "Гетри", 
    'BOOTS'   : "Бутси"
    }
    
    return f"""
<b>Назва</b>: {item.name}

🏷️ <b>Категорія</b>: {category_name[item.category]}

💰 <b>Ціна</b>: {item.price}

📇 <b>Стати</b>:
⚙️ <b>Техніка:</b> {item.technique_item_stat}
🥋 <b>Удари:</b> {item.kicks_item_stat}
⚽ <b>Вибір м'яча:</b> {item.ball_selection_item_stat}
🚀 <b>Швидкість:</b> {item.speed_item_stat}
💪 <b>Витривалість:</b> {item.endurance_item_stat}
    
    """
    
    
def check_if_item_equipped(character: Character, item: Item) -> bool:
    category_field_map = {
        'T_SHIRT': character.t_shirt_id,
        'SHORTS': character.shorts_id,
        'GAITERS': character.gaiters_id,
        'BOOTS': character.boots_id
    }
    equipped_item_id = category_field_map.get(item.category)

    if equipped_item_id:
        return False
    
    return True


async def read_items():
    async with aiofiles.open("items.json", mode='r', encoding='utf-8-sig') as file:
        contents = await file.read()
        data = json.loads(contents)
        return data