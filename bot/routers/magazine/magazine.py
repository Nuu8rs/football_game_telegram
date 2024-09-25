from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.models.character import Character
from database.models.item import Item

from services.character_service import CharacterService
from services.items_service import ItemService

from bot.keyboards.magazine_keyboard import (select_type_items_keyboard, 
                                             gradation_values_item, 
                                             select_items_for_buy)
from bot.callbacks.magazine_callbacks import SelectTypeItems, SelectGradationLevelItem, ByItems
from utils.item_utils import read_items, text_info_items


import json

magazine_router = Router()

@magazine_router.message(F.text == "🏬 Магазин")
async def magazine_handler(message: Message, character: Character, state: FSMContext):
    await message.answer("Виберіть речі які хочете купити", 
                         reply_markup=select_type_items_keyboard())
    



@magazine_router.callback_query(SelectTypeItems.filter())
async def select_item(query: CallbackQuery, state: FSMContext, callback_data: SelectTypeItems):
    
    data_items = await read_items()
    await state.update_data(data_items=data_items)
    
    max_leve_item = max(item["level_required"] for item in data_items)
    
    await query.message.answer("Виберіть градацію рівня", 
                                  reply_markup=gradation_values_item(
                                      item_сategory= callback_data.item,
                                      max_level_item=max_leve_item))
    
@magazine_router.callback_query(SelectGradationLevelItem.filter())
async def select_gradation_level(query: CallbackQuery, state: FSMContext, callback_data: SelectGradationLevelItem):
    data = await state.get_data()
    
    filtered_items = [
        item for item in data['data_items'] 
        if item["category"] == callback_data.item_category and item["level_required"] == callback_data.min_level_item
    ]
    
    await query.message.answer(text = ("📍 Вибери яку річ яку хочеш купити\n" + text_info_items(filtered_items)) , 
                               reply_markup=select_items_for_buy(filtered_items))

    
    
@magazine_router.callback_query(ByItems.filter())
async def select_gradation_level(query: CallbackQuery, state: FSMContext, character: Character, callback_data: ByItems):
    data = await state.get_data()
    item = [item for item in data["data_items"] if item['id'] == callback_data.id_item][0]
    
    if character.money < item['price']:
        return await query.answer(text = "У вас не вистачає монет на купівлю цієї речі", show_alert=True)
    
    if character.level < item['level_required']:
        return await query.answer(text = "У вас не вистачає рівня, щоб купити цю річ", show_alert=True)
    item_obj = Item(
        name = item['name'],
        category = item['category'],
        level_required = item['level_required'],
        price = item['price'],
        stats = json.dumps(item['stats']),
        owner_character_id = character.id
    )
    item = await ItemService.create_item(
        item_obj=item_obj
    )
    await CharacterService.update_money_character(
        character=character,
        amount_money_adjustment= -item.price
    )

    await query.message.answer(f"Вітаю ви купили річ {item.name}")
    