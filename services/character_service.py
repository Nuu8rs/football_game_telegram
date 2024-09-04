from database.models import Character
from database.session import get_session
from sqlalchemy import select, update
from config import DatabaseType, CONST_ENERGY
from datetime import datetime, timedelta

class CharacterService:

    
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
                character.education_reward_date = character.education_reward_date+amount_add_time
                merged_obj = await session.merge(character)
                await session.commit()
                return merged_obj