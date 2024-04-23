from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.keyboards import InlineMenu


about_router = Router()


@about_router.message(Command('about'))
async def about(message: Message) -> None:
    menu = InlineMenu()
    msg = (
        'Здесь будет описание бота!'
    )
    menu_items = {
        'Главная': 'start',
        'Начать диалог': 'ask',
    }
    await message.answer(msg, reply_markup=menu.place(**menu_items))


@about_router.callback_query(F.data == 'about')
async def about_callback(callback: CallbackQuery) -> None:
    await about(callback.message)
