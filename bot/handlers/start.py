from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from ..keyboards import InlineKeyboard

from storage.models import User


start_router = Router()


@start_router.message(Command('start'))
async def start(message: Message, user: User):
    menu = InlineKeyboard().place(
        {
            'Как пользоваться?': 'about',
            'Посмотреть баланс': 'balance',
            'Начать диалог (GPT)': 'ask',
            'Создать изображение': 'generate',
            'Изменить изображение': 'edit',
        }
    )
    await message.answer(
        f'Привет, {user.name},\n\n'
        f'Меня зовут Aio,\n'
        f'Я могу быть полезен как AI ассистент!\n\n'
        f'🔽 Выбери опцию использования 🔽',
        reply_markup=menu,
    )


@start_router.callback_query(F.data == 'start')
async def start_callback(callback: CallbackQuery, user: User) -> None:
    await start(callback.message, user)
