from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from handlers.keyboards.admin_pannel import *
from database import requests as rq
from config import ADMIN_ID
import datetime

admin_router = Router()
 
class Admin(StatesGroup):
    organization = State()
    INN_KPP = State()
    FIO = State()
    address = State()
    photo = State()

class DeleteDb(StatesGroup):
    id = State()

@admin_router.message(F.text == 'Админ панель')
async def admin_panel_manage(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer('Добро пожаловать в админ панель', reply_markup=admin_panel_kb)
    else:
        await message.answer('Вы не админ')

@admin_router.callback_query(F.data == 'show_db')
async def show_database(callback: CallbackQuery):
    await callback.message.delete()
    data = await rq.get_fake_organizations()
    if data == None:
        await callback.message.answer('База данных пуста')
    else:
        for item in data:
            await callback.message.answer(f'{item.id}///{item.organization_name}/// {item.FIO}/// {item.phone_number}/// {item.email}/// {item.address}')

        await callback.message.answer('Выберите действие', reply_markup=admin_panel_kb)


@admin_router.callback_query(F.data == 'add_db')
async def add_database(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Заполните данные организации. Укажите имя организации')
    await state.set_state(Admin.organization)

@admin_router.callback_query(F.data == 'delete_db')
async def delete_database(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Укажите ID организации')
    await state.set_state(DeleteDb.id)

@admin_router.message(DeleteDb.id)
async def get_del_id(message: Message, state: FSMContext):
    await state.update_data(id_n=int(message.text))
    data = await state.get_data()
    await state.clear()
    if await rq.delete_fake_organization(data['id_n']):
        await message.answer('Организация удалена', reply_markup=admin_panel_kb)
    else:
        await message.answer('Организация не найдена', reply_markup=admin_panel_kb)
    


@admin_router.message(Admin.organization)
async def organization_name(message: Message, state: FSMContext):
    await state.update_data(name_org=message.text)
    await message.answer('Укажите ИНН и КПП')
    await state.set_state(Admin.INN_KPP)

@admin_router.message(Admin.INN_KPP)
async def get_INN_KPP(message: Message, state: FSMContext):
    await state.update_data(INN_KPP=message.text)
    await message.answer('Укажите ФИО')
    await state.set_state(Admin.FIO)


@admin_router.message(Admin.FIO)
async def get_FIO(message: Message, state: FSMContext):
    await state.update_data(FIO=message.text)
    await message.answer('Укажите адрес')
    await state.set_state(Admin.address)


@admin_router.message(Admin.address)
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer('Отправьте фото росписи')
    await state.set_state(Admin.photo)


@admin_router.message(Admin.photo)    
async def get_address(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(photo = '')
    await bot.download(
        message.photo[-1],
        destination=f"handlers/photos/{message.photo[-1].file_id}.jpg"
    )
    data = await state.get_data()
    
    await rq.create_fake_organization(data['name_org'], data['FIO'], data['phone_number'], data['email'], data["address"])
    await message.answer('Данные записаны', reply_markup=admin_panel_kb)

@admin_router.callback_query(F.data == 'main_menu')
async def return_to_menu(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Вы вернулись в главное меню', reply_markup=start_admin_panel)