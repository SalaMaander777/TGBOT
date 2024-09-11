
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton



start_admin_panel = ReplyKeyboardMarkup (
    keyboard=[
[
KeyboardButton(text="Заполнить форму"),
KeyboardButton(text="Добавить товар"),
],
[KeyboardButton(text='Админ панель')],
[KeyboardButton(text="Перейти к меню коммерческих передложений")]
], resize_keyboard=True
)


admin_second_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить товар"),
            KeyboardButton(text="Получить коммерческое предложение")],
            [KeyboardButton(text="Получить коммерческое предложение с наценкой")], 
            [KeyboardButton(text='Админ панель')]
    ],
    resize_keyboard=True
)
admin_get_files_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Получить коммерческое предложение"),
            KeyboardButton(text="Получить коммерческое предложение с наценкой ")],
            [KeyboardButton(text='Админ панель')],
            [KeyboardButton(text='Главное меню')]
        ],
    
    resize_keyboard=True
)


admin_panel_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Посмотреть записи в базе данных', callback_data='show_db')],
                                                     [InlineKeyboardButton(text='Добавить запись в базу данных', callback_data='add_db')],
                                                     [InlineKeyboardButton(text='Удалить запись из базы данных', callback_data='delete_db')],
                                                     [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')]])