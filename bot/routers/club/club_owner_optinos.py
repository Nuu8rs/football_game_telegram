from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from database.models.character import Character

from services.club_service import ClubService

from bot.states.club_states import SendMessageMembers
from bot.callbacks.club_callbacks import TransferOwner, DeleteClub
from bot.keyboards.club_keyboard import transfer_club_owner_keyboard, definitely_delete_club_keyboard

from utils.club_utils import send_message_characters_club

from loader import logger
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