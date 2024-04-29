from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from ..keyboards import InlineKeyboard


about_router = Router()


@about_router.message(Command('about'))
async def about(message: Message) -> None:
    menu = InlineKeyboard().place(
        {
            'Посмотреть баланс': 'balance',
            'Начать диалог (GPT)': 'ask',
            'Создать изображение': 'generate',
            'Изменить изображение': 'edit',
            'Главная': 'start',
        }
    )
    msg = (
        'Здесь будет описание бота!'
    )
    await message.answer(msg, reply_markup=menu)


@about_router.callback_query(F.data == 'about')
async def about_callback(callback: CallbackQuery) -> None:
    await about(callback.message)
