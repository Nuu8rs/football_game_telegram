import asyncio
from sqlalchemy import event

from database.models.character import Character
from services.character_service import CharacterService

from constants import REFERAL_EXP


referral_lock = asyncio.Lock()

async def handle_referral_reward(character: Character):
    from loader import bot
    async with referral_lock:
        character = await CharacterService.get_character_by_id(character_id=character.id)        
        character_referal = await CharacterService.get_character(character_user_id=character.referal_user_id)
        
        await CharacterService.edit_character_energy(
            character_obj=character_referal,
            amount_energy_adjustment=150
        )
        await CharacterService.update_money_character(
            character_id=character_referal.id,
            amount_money_adjustment=20
        )
        
        try:    
            await bot.send_message(
                chat_id=character.referal_user_id,
                text=f"🏅 Ваш реферал [{character.character_name}] набрав {REFERAL_EXP} очок досвіду! Вы получаете 150 энергии и 20 монет!"
            )
        except Exception as e:
            print(f"Error sending message: {e}")
        
        await CharacterService.edit_status_reward_by_referal(character_user_id=character.characters_user_id)

def on_experience_reached_exp(mapper, connection, character: Character):
    if character.referal_user_id and character.exp >= 20 and not character.referral_award_is_received:
        asyncio.create_task(handle_referral_reward(character))

event.listen(Character, 'after_update', on_experience_reached_exp)