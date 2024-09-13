from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def switch_buttons(total_items: int, current_index: int, switch_type, items_per_page):
    def arrow_button(statement, new_index, side):
        if statement:
            return InlineKeyboardBuilder().button(
                text="➡️" if side == "right" else "⬅️", 
                callback_data=switch_type(current_index=new_index, total_items=total_items, side=side)
            )
        return InlineKeyboardBuilder().button(text="🟥", callback_data="stop")
    
    total_pages = (total_items + items_per_page - 1) // items_per_page
    current_page = current_index // items_per_page
    
    keyboard = InlineKeyboardBuilder()
    keyboard.attach(arrow_button(current_page > 0, current_index - items_per_page, 'left'))
    keyboard.button(text=f"{current_page + 1}/{total_pages}", callback_data="stop")
    keyboard.attach(arrow_button(current_page < total_pages - 1, current_index + items_per_page, 'right'))
    return keyboard


def menu_plosha():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text = "⬅️ Головна площа")
    return keyboard