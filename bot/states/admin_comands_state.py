from aiogram.filters.state import State, StatesGroup

class SendAllUserMessage(StatesGroup):
    get_text_from_send = State()