from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from handlers.keyboards import start_kb, admin_pannel, get_files_kb
from database import requests as rq
from config import ADMIN_ID

start_router = Router()

class StartFilling(StatesGroup):
    organization_name = State()
    FIO = State()
    phone_number = State()
    email = State()
    address = State()

@start_router.message(CommandStart())
async def start_command(message: Message) -> None:
    await rq.get_user(tg_id=message.from_user.id,)
    if message.from_user.id == ADMIN_ID:
        keyboard = admin_pannel.start_admin_panel
    else:
        keyboard = start_kb.start_keyboard

    await message.answer(f'Привет, я бот который автоматизирует рутинный процесс заполнения коммерческого приложения!', reply_markup=keyboard)

@start_router.message(F.text.lower() == 'отмена')
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Отменено', reply_markup=start_kb.start_keyboard)

@start_router.message(F.text == 'Заполнить форму')
async def fill_command(message: Message, state: FSMContext) -> None: 
    
   
    await message.answer("Укажите название организации", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await state.set_state(StartFilling.organization_name)

@start_router.message(StartFilling.organization_name)
async def organization_name(message: Message, state: FSMContext)-> None:
    await state.update_data(name_org=message.text)
    await message.answer("Укажите ФИО")
    await state.set_state(StartFilling.FIO)

@start_router.message(StartFilling.FIO)
async def get_FIO(message: Message, state: FSMContext)-> None:
    await state.update_data(FIO=message.text)
    await message.answer("Укажите номер телефона")
    await state.set_state(StartFilling.phone_number)

@start_router.message(StartFilling.phone_number)
async def get_phone_number(message: Message, state: FSMContext)-> None:
    await state.update_data(phone_number=message.text)
    await message.answer("Укажите почту")
    await state.set_state(StartFilling.email)

@start_router.message(StartFilling.email)
async def get_email(message: Message, state: FSMContext)-> None:
    await state.update_data(email=message.text)
    await message.answer("Укажите адрес")
    await state.set_state(StartFilling.address)

@start_router.message(StartFilling.address)
async def get_address(message: Message, state: FSMContext)-> None:
    await state.update_data(address=message.text)
    data = await state.get_data()
    #await message.answer(f'{data['name_org']}/// {data['FIO']}/// {data['phone_number']}/// {data['email']}/// {data['address']}')
    await rq.create_real_organization(message.from_user.id, data['name_org'], data['FIO'], data['phone_number'], data['email'], data["address"])
    if message.from_user.id == ADMIN_ID:
        keyboard = admin_pannel.admin_second_keyboard
    else:
        keyboard = start_kb.second_keyboard

    await message.answer("Спасибо! Данные записаны!", reply_markup= keyboard)
    await state.clear()

@start_router.message(F.text == "Перейти к меню коммерческих передложений")
async def second_menu(message: Message):
    if message.from_user.id == ADMIN_ID:
        keyboard = admin_pannel.admin_get_files_keyboard
    else:
        keyboard = get_files_kb.get_files_keyboard
    await message.answer("Вы перешли в меню коммерческих предложений", reply_markup=keyboard)

@start_router.message(F.text == "Главное меню")
async def return_menu(message: Message):
    if message.from_user.id == ADMIN_ID:
        keyboard = admin_pannel.start_admin_panel
    else:
        keyboard = start_kb.start_keyboard
    await message.answer("Вы вернулись в главное меню", reply_markup=keyboard)
