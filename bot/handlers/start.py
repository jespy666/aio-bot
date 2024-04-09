from aiogram.filters import Command
from aiogram import types, Router

from bot.keyboards.main_menu import MainMenu

start_router = Router()


@start_router.message(Command('start'))
async def start(message: types.Message):
    menu = MainMenu().place()
    await message.answer(
        f'Привет, {message.from_user.first_name},\n\n'
        f'Меня зовут Aio,\n'
        f'Я могу быть полезен как AI ассистент!\n\n'
        f'🔽 Выбери опцию использования 🔽',
        reply_markup=menu,
    )


async def start_callback(callback: types.CallbackQuery) -> None:
    menu = MainMenu().place()
    await callback.message.answer(
        'Добро пожаловать на главную страницу!\n\n'
        '🔽 Выбери опцию использования 🔽',
        reply_markup=menu,
    )
