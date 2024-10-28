from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from database.models.user_bot import UserBot

from services.character_service import CharacterService
from services.reminder_character_service import RemiderCharacterService
from services.user_service import UserService

from bot.keyboards.menu_keyboard import menu_instruction, remove_keyboard
from bot.keyboards.create_character_keyboard import set_gender_keyboard, select_role_character, create_character
from bot.states.create_character_state import CreateCharacterState
from bot.callbacks.character_callbacks import SelectGender, SelectPositionCharacter, CreateCharacter

from constants import  get_photo_character
from config import INSTRUCTION
from const_character import CREATE_CHARACTER_CONST
from utils.character_utils import get_character_text


create_character_router = Router()

@create_character_router.message(F.text == "⚽️ Створити персонажа")
async def set_name_character(message: Message, state: FSMContext):
    await state.set_state(CreateCharacterState.send_name)
    await message.answer("Введіть нік який буде прив'язаний за персонажем")
    
@create_character_router.message(CreateCharacterState.send_name, F.chat.type == "private")
async def set_gender_character(message: Message, state: FSMContext):
    name_character = message.text
    await state.update_data(name_character = name_character)
    await state.set_state(CreateCharacterState.set_gender)
    await message.answer("Виберіть стать персонажа", 
                            reply_markup=set_gender_keyboard())
    
@create_character_router.callback_query(F.data == "back_to_select_gender", CreateCharacterState.set_position)
async def back_to_select_gender(query: CallbackQuery, state: FSMContext):
    await state.set_state(CreateCharacterState.set_gender)
    await query.message.edit_text(text="Виберіть стать персонажа", 
                            reply_markup=set_gender_keyboard())
    
    
@create_character_router.callback_query(CreateCharacterState.set_gender, SelectGender.filter())
async def select_position_character(query: CallbackQuery, state: FSMContext, callback_data:SelectGender):
    await state.set_state(CreateCharacterState.set_position)
    await state.update_data(gender_character = callback_data.gender)
    await query.message.edit_text("Оберіть роль свого персонажа",
                                reply_markup=select_role_character(callback_data.gender))
    
    
@create_character_router.callback_query(CreateCharacterState.set_position, SelectPositionCharacter.filter())
async def view_info_character(query: CallbackQuery, state: FSMContext, callback_data:SelectPositionCharacter, user: UserBot):
    if user.characters:
        return
    
    data = await state.get_data()
    character = CREATE_CHARACTER_CONST(callback_data.position)
    character.name   = data['name_character']
    character.gender = data['gender_character']
    character.position = callback_data.position
    character.current_energy = character.max_energy
    character.characters_user_id = user.user_id
    text = get_character_text(character)

    await  query.message.answer_photo(
        photo   = get_photo_character(character),
        caption = text,
        reply_markup=create_character(character)
    )
    await state.update_data(character = character)
    
@create_character_router.callback_query(CreateCharacter.filter())
async def create_character_handler(query: CallbackQuery, state: FSMContext, user: UserBot, callback_data: CreateCharacter):
    await query.message.edit_reply_markup(reply_markup=None)
    if user.characters:
        return await query.message.reply("В вас вже є персонаж")
    
    data = await state.get_data()
    
    character = CREATE_CHARACTER_CONST(callback_data.position)
    character.name   = data['name_character']
    character.gender = data['gender_character']
    character.position = callback_data.position
    character.current_energy = character.max_energy
    character.characters_user_id = user.user_id
    character.referal_user_id = user.referal_user_id
    character = await CharacterService.create_character(
        character
    )
    await RemiderCharacterService.create_character_reminder(character_id=character.id)
    await state.clear()
    user = await UserService.get_user(user_id=user.user_id)
        
    
    await query.message.reply(
        text="<b>Вітаю вас із створенням персонажа!</b>",
        reply_markup=remove_keyboard()
    )
    
    await query.message.answer_photo(
        photo        = FSInputFile(path="src/learning/image_0.jpg"),
        caption      = INSTRUCTION[0],
        reply_markup = menu_instruction(index_instruction=1)
    )