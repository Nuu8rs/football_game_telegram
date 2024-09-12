from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.models.character import Character
from database.models.item import Item

from services.character_service import CharacterService
from services.items_service import ItemService

from bot.keyboards.magazine_keyboard import select_type_items_keyboard, gradation_values_item, buy_item
from bot.callbacks.magazine_callbacks import SelectTypeItems, SelectGradationLevelItem

from constants import  ItemCategory
from const_items import CREATE_ITEM_CONST

magazine_router = Router()

@magazine_router.message(F.text == "🏬 Магазин")
async def magazine_handler(message: Message, character: Character, state: FSMContext):
    await message.answer("Выберите вещи которые хотите купить", 
                         reply_markup=select_type_items_keyboard())
    

@magazine_router.callback_query(SelectTypeItems.filter())
async def select_item(query: CallbackQuery, state: FSMContext, character: Character, callback_data: SelectTypeItems):
    await query.message.edit_text("Выберите градацию уровня", 
                                  reply_markup=gradation_values_item(callback_data.item))
    
@magazine_router.callback_query(SelectGradationLevelItem.filter())
async def select_gradation_level(query: CallbackQuery, state: FSMContext, character: Character, callback_data: SelectGradationLevelItem):
    item_category = ItemCategory(callback_data.item)
    item_obj = CREATE_ITEM_CONST(item_category)
    await state.update_data(select_buy_item = item_obj)
    await query.message.answer(f"Вы хотите купить ({item_obj.name})\n\nЦена - {item_obj.price} 💵", 
                               reply_markup=buy_item())
    
def check_if_item_equipped(character: Character, item: Item):
    category_field_map = {
        'T_SHIRT': character.t_shirt_id,
        'SHORTS': character.shorts_id,
        'GAITERS': character.gaiters_id,
        'BOOTS': character.boots_id
    }
    equipped_item_id = category_field_map.get(item.category.name)

    if equipped_item_id:
        return False
    
    return True
    
@magazine_router.callback_query(F.data == "buy_select_item")
async def select_gradation_level(query: CallbackQuery, state: FSMContext, character: Character):
    data = await state.get_data()
    item: Item = data.get("select_buy_item", False)
    if not item:
        return query.answer(text = "Оберіть ще раз річ яку хочете купити", show_alert=True)
    
    if character.money < item.price:
        return await query.answer(text = "У вас не вистачає монет на купівлю цієї речі", show_alert=True)
    
    if character.level < item.level_required:
        return await query.answer(text = "У вас не вистачає рівня, щоб купити цю річ", show_alert=True)
    
    if not check_if_item_equipped(character, item):
        return await query.answer(text = "У вас уже одягнений цей тип речі", show_alert=True)
    
    item = await ItemService.create_item(
        item_obj=item
    )
    await CharacterService.update_money_character(
        character=character,
        amount_money_adjustment= -item.price
    )
    await CharacterService.equip_item(
        character_obj=character,
        item_obj=item
    )
    await query.message.answer(f"Вітаю ви купили річ {item.name}")
    