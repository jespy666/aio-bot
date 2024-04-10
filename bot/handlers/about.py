from aiogram.filters import Command
from aiogram import types, Router, F

from bot.keyboards.inline_menu import InlineMenu

about_router = Router()

msg = 'Здесь будет описание бота!'
items = {
    'Главная': 'start',
    'Начать диалог': 'ask',
}


@about_router.message(Command('about'))
async def about(message: types.Message) -> None:
    menu = InlineMenu()
    await message.answer(msg, reply_markup=menu.place(**items))


@about_router.callback_query(F.data == 'about')
async def about_callback(callback: types.CallbackQuery) -> None:
    menu = InlineMenu()
    await callback.message.answer(msg, reply_markup=menu.place(**items))
