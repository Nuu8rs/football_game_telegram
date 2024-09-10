from database.models.character import Character
from database.models.item import Item

from database.session import get_session
from sqlalchemy import select, update
from config import DatabaseType, CONST_ENERGY
from datetime import datetime, timedelta
from enum import Enum

class CharacterService:

    @classmethod
    async def get_all_users_not_bot(cls) -> list[Character]:
        async for session in get_session():
            async with session.begin():
                result = await session.execute(
                    select(Character).where(Character.is_bot == False)
                )
                all_characters_not_bot = result.scalars().all()
                return all_characters_not_bot
   
    @classmethod
    async def get_character(cls, character_user_id: int) -> Character:
        async for session in get_session():
            async with session.begin():
                result = await session.execute(
                    select(Character).where(Character.characters_user_id == character_user_id)
                )
                current_character = result.scalar_one_or_none()
                return current_character
    
    @classmethod
    async def create_character(cls, character_obj: Character) -> Character:
        character_obj.gender = character_obj.gender.value
        character_obj.position = character_obj.position.value
        
        async for session in get_session():
            async with session.begin():
                try:
                    session.add(character_obj)
                except:
                    pass
                merged_obj = await session.merge(character_obj)
                await session.commit()
                return merged_obj
            
    @classmethod
    async def update_character_field(cls, character_obj: Character, param: str, add_point: int) -> Character:
        async for session in get_session():
            async with session.begin():
                try:
                    session.add(character_obj)
                except:
                    pass
                merged_obj = await session.merge(character_obj)
                current_value = getattr(merged_obj, param, 0)
                setattr(merged_obj, param, current_value + add_point)
                await session.commit()
         

    @classmethod
    async def update_training_params(cls, character_obj: Character, characteristic: str, training_time: datetime) -> Character:
        async for session in get_session():
            async with session.begin():
                try:
                    session.add(character_obj)
                except:
                    pass
                merged_obj = await session.merge(character_obj)
                setattr(merged_obj, 'training_characteristic', characteristic)
                setattr(merged_obj, 'time_character_training', training_time)
                await session.commit()
                return merged_obj

    @classmethod
    async def get_characters_in_training(cls) -> list[Character]:
        async for session in get_session():
            async with session.begin():
                result = await session.execute(select(Character).where(Character.character_in_training == True))
                characters_in_training = result.scalars().all()
                return characters_in_training



    @classmethod
    async def consume_energy(cls, character_obj: Character, energy_consumed: int) -> Character:
        async for session in get_session():
            async with session.begin():
                try:
                    session.add(character_obj)
                except:
                    pass
                merged_obj = await session.merge(character_obj)
                current_energy = getattr(merged_obj, 'current_energy', 0)
                new_energy = current_energy - energy_consumed
                setattr(merged_obj, 'current_energy', max(new_energy, 0))
                await session.commit()
                
    
    @classmethod
    async def edit_character_energy(cls, character_obj: Character,  amount_energy_adjustment: int) -> Character:
        async for session in get_session():
            async with session.begin():
                try:
                    session.add(character_obj)
                except:
                    pass
                merged_obj = await session.merge(character_obj)
                current_energy = getattr(merged_obj, 'current_energy', 0)
                new_energy = current_energy + amount_energy_adjustment
                setattr(merged_obj, 'current_energy', max(new_energy, 0))
                await session.commit()

     
    @classmethod
    async def toggle_character_training_status(cls, character_obj: Character) -> Character:
        async for session in get_session():
            async with session.begin():
                try:
                    session.add(character_obj)
                except:
                    pass
                merged_obj = await session.merge(character_obj)
                current_status = getattr(merged_obj, 'character_in_training', False)
                new_status = not current_status
                setattr(merged_obj, 'character_in_training', new_status)
                await session.commit()
                
    @classmethod        
    async def update_character_club_id(cls,character: Character ,club_id: int):
        async for session in get_session():
            async with session.begin():
                try:
                    session.add(character)
                except:
                    pass
                character.club_id = club_id
                merged_obj = await session.merge(character)
                await session.commit()
                return merged_obj
            
    @classmethod
    async def update_energy_for_non_bots(cls):
        async for session in get_session():
            async with session.begin():
                try:
                    stmt = (
                        update(Character) 
                        .where(Character.is_bot == False)
                        .values(current_energy=CONST_ENERGY)
                    )
                    await session.execute(stmt)
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    raise e
                
    @classmethod
    async def leave_club(cls, character: Character):
        async for session in get_session():
            async with session.begin():
                try:
                    character.club_id = None
                    session.add(character)
                    merged_obj = await session.merge(character)
                    await session.commit()
                    return merged_obj
                except Exception as e:
                    await session.rollback()
                    raise e
                
    async def update_money_character(character: Character, amount_money_adjustment: int):
        async for session in get_session():
            async with session.begin():
                try:
                    session.add(character)
                except:
                    pass
                character.money = character.money+amount_money_adjustment
                merged_obj = await session.merge(character)
                await session.commit()
                return merged_obj
            
    async def add_exp_character(character: Character, amount_exp_add: int):
        async for session in get_session():
            async with session.begin():
                try:
                    session.add(character)
                except:
                    pass
                character.exp = character.exp+amount_exp_add
                merged_obj = await session.merge(character)
                await session.commit()
                return merged_obj
            
    async def update_character_education_time(character: Character, amount_add_time: timedelta):
        async for session in get_session():
            async with session.begin():
                try:
                    session.add(character)
                except:
                    pass
                character.education_reward_date = datetime.now()+amount_add_time
                merged_obj = await session.merge(character)
                await session.commit()
                return merged_obj
            
                
    @classmethod
    async def equip_item(cls, character_obj: Character, item_obj: Item) -> Character:
        category_field_map = {
            'T-SHIRT': 't_shirt_id',
            'SHORTS': 'shorts_id',
            'GAITERS': 'gaiters_id',
            'BOOTS': 'boots_id'
        }
        item_category = item_obj.category.value.upper() if isinstance(item_obj.category, Enum) else item_obj.category.upper()
        field_name = category_field_map.get(item_category)

        async for session in get_session():
            async with session.begin():
                try:
                    session.add(character_obj)
                except:
                    pass
                
                merged_character = await session.merge(character_obj)
                setattr(merged_character, field_name, item_obj.id)
                await session.commit()
                
                return merged_character