from aiogram.utils.keyboard import ReplyKeyboardBuilder


def to_main_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text='🏠 Головне меню')
    builder.adjust(1)
    
    return builder.as_markup(resize_keyboard=True)