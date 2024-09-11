from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

get_files_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Получить коммерческое предложение")],
            [KeyboardButton(text="Получить коммерческое предложение с наценкой ")
        ],
        [KeyboardButton(text="Главное меню")]
    ],
    resize_keyboard=True
)