from aiogram import Router, F
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from docx2pdf import convert
import os

from database import requests as rq
from Docx import create_document

document_router = Router()
@document_router.message(F.text == 'Получить коммерческое предложение')
async def get_products_command(message: Message):
    table_data, sum = await rq.get_products(message.from_user.id)
    item =  await rq.get_organizations(message.from_user.id) 
    await create_document(table_data, item.organization_name, item.FIO, item.phone_number, item.email, item.address, sum)
    convert('table.docx', 'table.pdf')
    document = FSInputFile('table.pdf')
    await message.answer_document(document)
    os.remove('table.docx')
    os.remove('table.pdf')