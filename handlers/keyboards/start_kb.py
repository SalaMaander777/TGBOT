from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Заполнить форму"),
            KeyboardButton(text="Добавить товар")], 
           [ KeyboardButton(text="Перейти к меню коммерческих передложений")
        ],
    ],
    resize_keyboard=True
)

second_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить товар"),
            KeyboardButton(text="Получить коммерческое предложение")],
            [KeyboardButton(text="Получить коммерческое предложение с наценкой")]
        ,
    ],
    resize_keyboard=True
)