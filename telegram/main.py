import asyncio
import logging
import sys

from config.config import dp, bot
from handlers import router as client_router
from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(f'Привествую, {message.from_user.full_name}!\nНапишите /commands для открытия списка команд')
    

async def main() -> None:
    dp.include_router(client_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
