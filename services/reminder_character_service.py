from database.models.reminder_character import ReminderCharacter
from database.models.character import Character
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from database.session import get_session
from datetime import datetime, timedelta

class RemiderCharacterService:
    
    @classmethod
    async def create_character_reminder(cls, character_id: int) -> ReminderCharacter:
        async for session in get_session():
            async with session.begin():
                
                reminder_obj = ReminderCharacter(
                    character_id=character_id
                )
                session.add(reminder_obj)
                merged_obj = await session.merge(reminder_obj)
                await session.commit()
                return merged_obj

    @classmethod
    async def get_characters_in_training(cls) -> list[Character]:
        async for session in get_session():
            async with session.begin():
                result = await session.execute(
                    select(Character)
                    .join(ReminderCharacter)
                    .options(joinedload(Character.reminder))  # Загружаем связанные объекты
                    .where(ReminderCharacter.character_in_training == True)
                )
                characters_in_training = result.scalars().all()
                return characters_in_training
            
    @classmethod
    async def toggle_character_training_status(cls, character_id: int) -> ReminderCharacter:
        async for session in get_session():
            async with session.begin():
                # Получаем объект ReminderCharacter, связанный с данным персонажем
                result = await session.execute(select(ReminderCharacter).where(ReminderCharacter.character_id == character_id))
                reminder_character = result.scalars().first()

                if reminder_character:
                    # Переключаем статус character_in_training
                    current_status = reminder_character.character_in_training
                    new_status = not current_status
                    reminder_character.character_in_training = new_status

                    await session.commit()
                    return reminder_character
                else:
                    raise ValueError(f"ReminderCharacter не найден для character_id: {character_id}")
                
    @classmethod
    async def update_training_info(cls, 
                        character_id: int,  
                        training_stats: str = None,
                        time_start_training: datetime = None,
                        time_training_seconds: int = None
                                   ):
        async for session in get_session():
            async with session.begin():
                result = await session.execute(select(ReminderCharacter).where(ReminderCharacter.character_id == character_id))
                reminder_character = result.scalars().first()

                reminder_character.training_stats = training_stats
                reminder_character.time_start_training = time_start_training
                reminder_character.time_training_seconds = time_training_seconds

                await session.commit()
                return reminder_character