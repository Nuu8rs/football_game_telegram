from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from database.models.club import Club
from database.models.character import Character
from database.models.user_bot import UserBot

from .utils_keyboard import switch_buttons, menu_plosha
from ..callbacks.switcher import SwitchClub
from ..callbacks.club_callbacks import SelectClubToJoin, JoinToClub, TransferOwner
from constants import MAX_LEN_MEMBERS_CLUB


def create_or_join_club():
    return (InlineKeyboardBuilder()
            .button(text = "⛩ Створити свій клуб", callback_data="create_new_club")
            .button(text = "🎮 Приєднатися до клубу", callback_data="join_to_club")
            .adjust(1)
            .as_markup()
            )
    
def menu_club():
    return (ReplyKeyboardBuilder()
            .attach(menu_plosha())
            .adjust(1)
            .as_markup(resize_keyboard=True)
            )
    
def club_menu_keyboard(club: Club, user: UserBot):
    keyboard = InlineKeyboardBuilder()
    if club.owner_id == user.user_id:
        if not club.link_to_chat:
            keyboard.button(text="⚙️ Додати посилання на чат клубу",  callback_data="change_club_chat")
        else:
            keyboard.button(text="⚙️ змінити посилання на чат клубу", callback_data="change_club_chat")
        keyboard.button(text = "⌨️ Надіслати повідомлення всьому клубу", callback_data="send_message_all_member_club")
        keyboard.button(text = "🫂 Передати права на клуб", callback_data="transfer_rights")
        keyboard.button(text = "❌ Видалити мій клуб", callback_data="delete_my_club")
    else:
        keyboard.button(text = "⬅️ Вийти з клубу", callback_data="leave_club")
    keyboard.button(text="👥 Користувачі клубу",callback_data="view_all_members_club")
    
    return keyboard.adjust(2, repeat=True).as_markup()


def find_club(all_clubs: list[Club], current_index: int, items_per_page: int = 10):
    keyboard = InlineKeyboardBuilder()
    start_index = current_index
    end_index = min(start_index + items_per_page, len(all_clubs))    
    keyboard.attach(switch_buttons(total_items=len(all_clubs), current_index=current_index, switch_type=SwitchClub, items_per_page=items_per_page))
    for club in all_clubs[start_index:end_index]:
        text_club = "⚽ {name_club} [{current_len_members}/{all_len_members}]".format(
            name_club = club.name_club,
            current_len_members = len(club.characters),
            all_len_members = MAX_LEN_MEMBERS_CLUB
        )
        
        keyboard.button(text=text_club, callback_data=SelectClubToJoin(club_id=club.id))
    keyboard.adjust(3,2,2,2,2,2)
    return keyboard.as_markup()


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