from aiogram.filters import Command
from aiogram import types, Router, F

from bot.keyboards import InlineMenu

about_router = Router()

MSG = 'Здесь будет описание бота!'
ITEMS = {
    'Главная': 'start',
    'Начать диалог': 'ask',
}


@about_router.message(Command('about'))
async def about(message: types.Message) -> None:
    menu = InlineMenu()
    await message.answer(MSG, reply_markup=menu.place(**ITEMS))


@about_router.callback_query(F.data == 'about')
async def about_callback(callback: types.CallbackQuery) -> None:
    menu = InlineMenu()
    await callback.message.answer(MSG, reply_markup=menu.place(**ITEMS))
