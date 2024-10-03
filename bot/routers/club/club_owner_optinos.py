from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.models.character import Character
from database.models.club import Club

from services.club_service import ClubService
from services.match_character_service import MatchCharacterService
from services.league_service import LeagueFightService

from bot.states.club_states import SendMessageMembers
from bot.callbacks.club_callbacks import TransferOwner, DeleteClub, SelectSchema
from bot.keyboards.club_keyboard import transfer_club_owner_keyboard, definitely_delete_club_keyboard, select_schema_keyboard

from utils.club_utils import send_message_characters_club, get_text_schemas, text_schemas

from datetime import timedelta, datetime
from config import EPOCH_ZERO
from loader import bot,logger

owner_option_club_router = Router()


@owner_option_club_router.callback_query(F.data == "send_message_all_member_club")
async def get_message_to_member_club(query: CallbackQuery, state: FSMContext, character: Character):
    if not character.club_id:
        return await query.answer("❌ Ви не перебуваєте в клубі на даний момент")
    
    club = await ClubService.get_club(club_id=character.club_id)
    if club.owner_id != character.characters_user_id:
        return await query.answer("❌ Ви не адмін клубу, ви не можете надіслати повідомлення")
        
    await query.message.answer("<b>Надішліть будь-яке повідомлення</b>, і воно буде доставлене всім учасникам вашого клубу")
    await state.set_state(SendMessageMembers.send_message_members)
    

@owner_option_club_router.message(SendMessageMembers.send_message_members)
async def send_message_all_member_club(message: Message, state: FSMContext, character: Character):
    if not character.club_id:
        return await message.answer("❌ Ви не перебуваєте в клубі на даний момент")

    club = await ClubService.get_club(club_id=character.club_id)
    if club.owner_id != character.characters_user_id:
        return await message.answer("❌ Ви не адмін клубу, ви не можете надіслати повідомлення")
    
    for character_club in club.characters:
        if character.characters_user_id == character_club.characters_user_id:
            continue
        try:
            await message.copy_to(
                chat_id=character_club.characters_user_id
            )            
        except Exception as E:
            logger.error(f"НЕ СМОГ ОТПРАВИТЬ СООБЩЕНИЕ {character.name}")
    await state.clear()
    
@owner_option_club_router.callback_query(F.data == "transfer_rights")
async def transfer_rights_club(query: CallbackQuery, character: Character):
    if not character.club_id:
        return await query.answer("❌ Ви не перебуваєте в клубі на даний момент")

    club = await ClubService.get_club(club_id=character.club_id)
    if club.owner_id != character.characters_user_id:
        return await query.answer("❌ Ви не адмін клубу")
    
    if len(club.characters) == 1:
        return await query.message.answer("У вас у клубі немає того, кому можна передати лідера")
    
    await query.message.answer("Виберіть персонажа, якому ви передасте права на ваш клуб",
                               reply_markup=transfer_club_owner_keyboard(club))
    
@owner_option_club_router.callback_query(TransferOwner.filter())
async def transfer_owner_club(query: CallbackQuery, character: Character, callback_data: TransferOwner):
    if not character.club_id:
        return await query.answer("❌ Ви не перебуваєте в клубі на даний момент")

    club = await ClubService.get_club(club_id=character.club_id)
    if club.owner_id != character.characters_user_id:
        return await query.answer("❌ Ви не адмін клубу")
    
    await ClubService.transfer_club_owner(
        club=club,
        new_owner_id=callback_data.user_id_new_owner
    )
    character_owner = [character for character in club.characters if character.characters_user_id == callback_data.user_id_new_owner][0]
    await query.message.answer(f"Вы передали лидера {character_owner.name}")
    await send_message_characters_club(
        characters_club=club.characters,
        my_character=character,
        text=f"👤 <b>Лідер клубу змінився з {character.name} -> {character_owner.name}</b>"
    )
    
@owner_option_club_router.callback_query(F.data == "delete_my_club")
async def delete_my_club(query: CallbackQuery, character: Character):
    if not character.club_id:
        return await query.answer("❌ Ви не перебуваєте в клубі на даний момент")

    club = await ClubService.get_club(club_id=character.club_id)
    if club.owner_id != character.characters_user_id:
        return await query.answer("❌ Ви не адмін клубу")
    
    await query.message.answer("Ви точно хочете видалити клуб?",
                               reply_markup=definitely_delete_club_keyboard(club.id))

    
@owner_option_club_router.callback_query(DeleteClub.filter())
async def delete_my_club(query: CallbackQuery, character: Character, callback_data: DeleteClub):
    if not character.club_id:
        return await query.answer("❌ Ви не перебуваєте в клубі на даний момент")

    club = await ClubService.get_club(club_id=callback_data.club_id)
    if club.owner_id != character.characters_user_id:
        return await query.answer("❌ Ви не адмін клубу")
    
    await send_message_characters_club(
        characters_club=club.characters,
        my_character=character,
        text=f"😢 Клуб был удален"
    )
    await ClubService.remove_all_characters_from_club(club)
    await query.message.delete()
    await query.message.answer("Ви видалили свій клуб")
    
    
@owner_option_club_router.callback_query(F.data == "change_schema_club")
async def switch_schema_club(query: CallbackQuery, character: Character):
    text_current_chema = get_text_schemas(character.club)
    
    await query.message.answer(text = text_current_chema,
                               reply_markup=select_schema_keyboard())
    
@owner_option_club_router.callback_query(SelectSchema.filter())
async def select_schema(query: CallbackQuery, character: Character, callback_data: SelectSchema):
    if character.club.schema == callback_data.select_schema:
        return await query.answer("У вас і так обрано цю схему", show_alert=True)

    if character.club.time_edit_schema != EPOCH_ZERO and character.club.time_edit_schema + timedelta(days=3) < datetime.now():
        return await query.answer("Для зміни схеми має минути 3 дні", show_alert=True)
    
    
    await ClubService.edit_schemas(club= character.club, new_schema=callback_data.select_schema)
    await query.message.answer(f"Ви встановили «{text_schemas[callback_data.select_schema]}»")
    await query.message.answer("<b>Сповіщаю команду про те що ви змінили схему</b>, усім хто зареєструвався сьогодні на матч, <b>треба буде ще раз зайти в матч</b> за новою схемою")
    await notification_switch_schema(
        club_id=character.club_id,
        my_character=character
    )
    
async def notification_switch_schema(club_id: int, my_character: Character):
    club = await ClubService.get_club(club_id)
    current_match_today = await LeagueFightService.get_match_today(club_id=club.id)
    await send_message_characters_club(
        characters_club=club.characters,
        my_character=my_character,
        text="<b>Лідер клубу змінив схему</b>\n\n"+get_text_schemas(club)
    )
    for character in club.characters:
            await MatchCharacterService.delete_character_from_match(
                character_id=character.id,
                match_id=current_match_today.match_id
            )
            