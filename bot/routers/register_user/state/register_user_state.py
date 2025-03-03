from aiogram.filters.state import State, StatesGroup

class RegisterUserState(StatesGroup):
    send_name = State()
    
class JoinToClubState(StatesGroup):
    join_to_club = State()