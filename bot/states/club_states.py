from aiogram.filters.state import State, StatesGroup

class CreateClub(StatesGroup):
    send_name    = State()

class ChangeClubChatLink(StatesGroup):
    send_chat_link = State()
    
class FindClub(StatesGroup):
    send_name_club = State()