from aiogram.filters.state import State, StatesGroup

class OptionsNewsletter(StatesGroup):
    send_range_exp = State()
    get_text_from_send = State()