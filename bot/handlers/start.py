from aiogram.filters import Command
from aiogram import types, Router, F

from bot.keyboards.inline_menu import InlineMenu


start_router = Router()

items = {
    'О боте': 'about',
    'Начать диалог': 'ask',
    'Посмотреть баланс': 'balance',
}


@start_router.message(Command('start'))
async def start(message: types.Message):
    menu = InlineMenu()
    await message.answer(
        f'Привет, {message.from_user.first_name},\n\n'
        f'Меня зовут Aio,\n'
        f'Я могу быть полезен как AI ассистент!\n\n'
        f'🔽 Выбери опцию использования 🔽',
        reply_markup=menu.place(**items),
    )


@start_router.callback_query(F.data == 'start')
async def start_callback(callback: types.CallbackQuery) -> None:
    menu = InlineMenu()
    await callback.message.answer(
        'Добро пожаловать на главную страницу!\n\n'
        '🔽 Выбери опцию использования 🔽',
        reply_markup=menu.place(**items),
    )
