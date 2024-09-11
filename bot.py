import asyncio
import logging

from config import TOKEN, DEBUG
from aiogram import Bot, Dispatcher

from handlers.startcommand import start_router
from handlers.addproduct import product_router
from handlers.get_doc import document_router
from handlers.admin_handler import admin_router
from database.models import async_main


bot = Bot(token=TOKEN)

dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(product_router)
dp.include_router(document_router)
dp.include_router(admin_router)

async def main():
    await async_main()  
    await dp.start_polling(bot) 

if __name__ == '__main__':
    if DEBUG:
        logging.basicConfig(level=logging.INFO)
    try: 
        asyncio.run(main()) 
    except (KeyboardInterrupt, SystemExit):
        print('Bye!')
