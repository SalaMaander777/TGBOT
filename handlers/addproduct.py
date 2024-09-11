from aiogram import Router, F
import os

from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.state import StatesGroup, State
from database import requests as rq
from handlers.keyboards.get_files_kb import get_files_keyboard
from docx2pdf import convert
from Docx import create_document


keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Да', callback_data='yes'), InlineKeyboardButton(text='Нет', callback_data='no')]])


product_router = Router()

class Product(StatesGroup):
    name = State()
    price = State()
    amount = State()

@product_router.message(F.text == 'Добавить товар')
async def add_product(message: Message, state: FSMContext):
    await rq.delete_product(message.from_user.id)
    await state.set_state(Product.name)
    await message.answer("Напишите название товара", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

@product_router.message(Product.name) 
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Напишите цену")
    await state.set_state(Product.price)

@product_router.message(Product.price)
async def get_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Напишите количество")
    await state.set_state(Product.amount)

@product_router.message(Product.amount)
async def get_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    data = await state.get_data()
    await message.answer(f'{data["name"]}/// {data["price"]}/// {data["amount"]}')
    await rq.add_product(message.from_user.id, data['name'], data['price'], data['amount'])
    await message.answer('Добавить еще товар?', reply_markup=keyboard)


@product_router.callback_query(F.data == 'yes')
async def answer_yes(callback: Message, state: FSMContext):   
    await state.set_state(Product.name)
    await callback.message.answer('Напишите название продукта')

@product_router.callback_query(F.data == 'no')
async def answer_no(callback: Message, state: FSMContext):
    await state.clear()
    await callback.message.answer('Добавление товаров окончено', reply_markup=get_files_keyboard)
    
# @product_router.message(Command('getdocument'))
# async def get_products_command(message: Message):
#     table_data, sum = await rq.get_products(message.from_user.id)
#     item =  await rq.get_organizations(message.from_user.id) 
#     await create_document(table_data, item.organization_name, item.FIO, item.phone_number, item.email, item.address, sum)
#     convert('table.docx', 'table.pdf')
#     document = FSInputFile('table.pdf')
#     await message.answer_document(document)
#     os.remove('table.docx')
#     os.remove('table.pdf')