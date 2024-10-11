from aiogram import Router,  Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.models.user_bot import UserBot
from database.models.character import Character

from services.items_service import ItemService
from services.character_service import CharacterService

from bot.keyboards.character_keyboard import my_inventory_keyboard, character_keyboard, funtctional_item
from bot.callbacks.items_callbacks import ViewMyItem, PutOnItem, SellMyItem


from utils.item_utils import view_my_item_text, check_if_item_equipped

from constants import get_photo_character, PROCENT_TO_SELL
from utils.character_utils import get_character_text, get_referal_text



menu_character_router = Router()

@menu_character_router.message(F.text == "⚽️ Мій персонаж")
async def get_my_character(message: Message, state: FSMContext, user: UserBot, character: Character):
    await CharacterService.add_exp_character(
        character=character,
        amount_exp_add=20
    )
    
    await state.clear()
    await message.answer_photo(
        photo=get_photo_character(character),
        caption=get_character_text(character),
        reply_markup=character_keyboard()
    )
    
@menu_character_router.callback_query(F.data == "my_inventory")
async def select_view_my_items(query: CallbackQuery, character: Character):
    my_items = await ItemService.get_items_from_character(character_id=character.id)
    
    if not my_items:
        return await query.answer(text = "У вас немає речей", show_alert=True)
    
    await query.message.answer("Виберіть із ваших предметів", 
                               reply_markup=my_inventory_keyboard(
                                   items=my_items,
                                   current_index=0
                               ))
    
    
@menu_character_router.callback_query(ViewMyItem.filter())
async def view_item_handler(query: CallbackQuery, callback_data: ViewMyItem):
    
    item = await ItemService.get_item(item_id=callback_data.item_id)
     
    if not item:
        return await query.answer("Цього предмета не існує")
    
    await query.message.answer(
        text=view_my_item_text(item),
        reply_markup=funtctional_item(callback_data.item_id)
    )
    
@menu_character_router.callback_query(PutOnItem.filter())
async def put_on_item(query: CallbackQuery, character: Character, callback_data: PutOnItem):
    
    item = await ItemService.get_item(item_id=callback_data.item_id)
     
    if not item:
        return await query.answer("Цього предмета не існує")
    
    if not check_if_item_equipped(character, item):
        return await query.answer(text = "У вас уже одягнений цей тип речі", show_alert=True)
    
    await CharacterService.equip_item(
        character_obj=character,
        item_obj=item
    )
    await query.message.answer(f"Ви одягнули: {item.name}")
    
    
@menu_character_router.callback_query(SellMyItem.filter())
async def sell_my_item(query: CallbackQuery, character: Character, callback_data: SellMyItem):
    item = await ItemService.get_item(callback_data.item_id)
    if not item:
        return await query.answer("Цього предмета не існує")

    if callback_data.item_id in [character.t_shirt_id, character.boots_id, character.gaiters_id, character.shorts_id]:
        await ItemService.unequip_item(
            character, item.category
        )

    price_for_salle = round(item.price * (PROCENT_TO_SELL / 100))
    await CharacterService.update_money_character(character=character, amount_money_adjustment=price_for_salle)
    await ItemService.delete_item(callback_data.item_id)
    await query.message.edit_text(f"Ви продали <b>{item.name}</b> за {price_for_salle} монет")
    
    
@menu_character_router.callback_query(F.data == "referal_system")
async def character_referal_handler(query: CallbackQuery, character: Character):
    await query.message.answer(
        text = await get_referal_text(my_character=character)
    )