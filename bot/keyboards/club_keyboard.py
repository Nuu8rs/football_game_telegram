from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from database.models.club import Club
from database.models.character import Character

from .utils_keyboard import pagination_keyboard, menu_plosha
from ..callbacks.switcher import SwitchClub
from ..callbacks.club_callbacks import (
    SelectClubToJoin, 
    JoinToClub, 
    TransferOwner, 
    DeleteClub, 
    SelectSchema, 
    SelectClubToView, 
    ViewCharatcerClub,
    KickMember
    )
from constants import MAX_LEN_MEMBERS_CLUB, ITEM_PER_PAGE
from utils.club_shemas import SchemaClub 

def main_menu_club(character: Character):
    keybaord = ReplyKeyboardBuilder()
    if not character.club_id:
        keybaord.button(text = "⛩ Створити свій клуб")
        keybaord.button(text = "🎮 Приєднатися до клубу")
    else:
        keybaord.button(text = "🎪 Мій клуб")
        keybaord.button(text = "🧿 Переглянути інші клуби")
        
    keybaord.attach(menu_plosha())
    return keybaord.adjust(1).as_markup(resize_keyboard = True)
        
    
def club_menu_keyboard(club: Club, character: Character):
    keyboard = InlineKeyboardBuilder()
    if club.owner_id == character.characters_user_id:
        if not club.link_to_chat:
            keyboard.button(text="⚙️ Додати посилання на чат клубу",  callback_data="change_club_chat")
        else:
            keyboard.button(text="⚙️ змінити посилання на чат клубу", callback_data="change_club_chat")
        keyboard.button(text = "🔄 Змінити схему команди", callback_data="change_schema_club")
        keyboard.button(text = "⌨️ Надіслати повідомлення всьому клубу", callback_data="send_message_all_member_club")
        keyboard.button(text = "🫂 Передати права на клуб", callback_data="transfer_rights")
        keyboard.button(text = "❌ Видалити мій клуб", callback_data="delete_my_club")
        keyboard.button(text = "🦶👤 Вигнати користувача", callback_data="kick_user")
    else:
        keyboard.button(text = "🎮 Схема команди", callback_data="view_schema_club")
        keyboard.button(text = "⬅️ Вийти з клубу", callback_data="leave_club")
    keyboard.button(text="👥 Користувачі клубу",callback_data=ViewCharatcerClub(club_id=club.id))
    
    return keyboard.adjust(2, repeat=True).as_markup()


def find_club(all_clubs: list[Club], page: int = 0 ):
    keyboard = InlineKeyboardBuilder()
    
    start = page * ITEM_PER_PAGE
    end = start + ITEM_PER_PAGE
    
    
    keyboard.attach(pagination_keyboard(
        total_items  = len(all_clubs), 
        current_page = page, 
        switcher     = SwitchClub))
    
    
    for club in all_clubs[start:end]:
        text_club = "⚽ {name_club} [{current_len_members}/{all_len_members}]".format(
            name_club = club.name_club,
            current_len_members = len(club.characters),
            all_len_members = MAX_LEN_MEMBERS_CLUB
        )
        
        keyboard.button(text=text_club, callback_data=SelectClubToJoin(club_id=club.id))
    keyboard.adjust(3,2,2,2,2,2)
    return keyboard.as_markup()


def view_club(all_clubs: list[Club], page: int):
    keyboard = InlineKeyboardBuilder()
    
    start = page * ITEM_PER_PAGE
    end = start + ITEM_PER_PAGE
     
    keyboard.attach(pagination_keyboard(
        total_items  = len(all_clubs), 
        current_page = page, 
        switcher     = SwitchClub
                                        )
                    )
    
    
    for club in all_clubs[start:end]:
        text_club = "⚽ {name_club} [{current_len_members}/{all_len_members}]".format(
            name_club = club.name_club,
            current_len_members = len(club.characters),
            all_len_members = MAX_LEN_MEMBERS_CLUB
        )
        
        keyboard.button(text=text_club, callback_data=SelectClubToView(club_id=club.id))
    keyboard.adjust(3,2,2,2,2,2)
    return keyboard.as_markup()
    
def view_character_club(club_id: int):
    return (InlineKeyboardBuilder()
            .button(text="👥 Користувачі клубу",callback_data=ViewCharatcerClub(club_id=club_id))
            .adjust(1)
            .as_markup()
            )


def join_to_club_keyboard(club_id: int):
    return (InlineKeyboardBuilder()
            .button(text = "➕ Приєднатися до клубу", callback_data=JoinToClub(club_id=club_id))
            .as_markup())
    
def transfer_club_owner_keyboard(club: Club):
    keyboard = InlineKeyboardBuilder()
    for character_club in club.characters:
        if club.owner_id == character_club.characters_user_id:
            continue
        
        keyboard.button(text = f"{character_club.name}",
                        callback_data=TransferOwner(user_id_new_owner =  character_club.characters_user_id))
    keyboard.adjust(3)
    return keyboard.as_markup()


def definitely_delete_club_keyboard(club_id: int):
    return (InlineKeyboardBuilder()
            .button(text = "Точно видалити мій клуб", callback_data=DeleteClub(club_id=club_id))
            .as_markup()
            )
    
def select_schema_keyboard():
    keyboard = InlineKeyboardBuilder()
    for num_schema in range(1,6):
        
        info_schema = SchemaClub.__getattribute__(SchemaClub, f"sсhema_{num_schema}")
        text_shema = "-".join(map(str, list(info_schema.values())[:-1]))
        keyboard.button(
            text=f"Cхема [{text_shema}]",
            callback_data=SelectSchema(select_schema = f"sсhema_{num_schema}")
        )
    keyboard.adjust(2)
    return keyboard.as_markup()

def select_user_kick(members_club: list[Character]):
    keyboard = InlineKeyboardBuilder()
    for member in members_club:
        keyboard.button(text = f"Вигнати {member.name}", 
                        callback_data=KickMember(
                            character_id=member.id
                        ))
        
    return keyboard.adjust(1).as_markup()