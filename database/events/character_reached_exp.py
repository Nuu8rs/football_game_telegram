import asyncio
from sqlalchemy import event

from database.models.character import Character
from services.character_service import CharacterService

from constants import REFERAL_EXP

def on_experience_reached_exp(mapper, connection, character: Character):
    if not character.referal_user_id:
        return
    if character.exp >= 20 and not character.referral_award_is_received:
        return asyncio.create_task(send_reward_referal_user(character))
        
        

async def send_reward_referal_user(character: Character):
    from loader import bot
    
    await CharacterService.edit_status_reward_by_referal(character_user_id=character.characters_user_id)

    character_referal = await CharacterService.get_character(character_user_id=character.referal_user_id)
    await CharacterService.edit_character_energy(
        character_obj=character_referal,
        amount_energy_adjustment=150
    )
    await CharacterService.update_money_character(
        character=character_referal,
        amount_money_adjustment=20)
    try:    
        await bot.send_message(
            chat_id=character.referal_user_id,
            text=f"🏅 Ваш реферал [{character.name}] набрав {REFERAL_EXP} очок досвіду! Ви отримуєте 150 енергії та 20 монет!")
    except Exception as E:
        print(E)
        pass
    
    
event.listen(Character, 'after_update', on_experience_reached_exp)