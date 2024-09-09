from database.models.item import Item
from database.session import get_session
from enum import Enum
import json


class ItemService:
    
    @classmethod
    async def create_item(cls, item_obj: Item) -> Item:
        item_obj.stats = json.dumps(item_obj.stats)
        
        if isinstance(item_obj.category, Enum):
            item_obj.category = item_obj.category.value
        
        async for session in get_session():
            async with session.begin():
                try:
                    session.add(item_obj)
                except:
                    pass
                merged_obj = await session.merge(item_obj)
                await session.commit()
                return merged_obj