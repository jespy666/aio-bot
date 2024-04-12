from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from bot.keyboards.inline_menu import InlineMenu

from crud import UserCRUD
from config import config


balance_router = Router()

ITEMS = {
    'Главная': 'start',
    'Начать диалог': 'ask',
    'О боте': 'about',
}


@balance_router.message(Command('balance'))
async def show_balance(message: Message) -> None:
    menu = InlineMenu()
    session = UserCRUD(config.DATABASE_URL)
    user = await session.get_user(message.chat.id)
    msg = (
        f'💰💰💰== <strong>Данные аккаунта</strong> ==💰💰💰\n\n'
        f'🆔 ▶️ {user.id}\n\n'
        f'<em>Остаток на счету</em> ▶️ <strong>{user.balance}</strong>'
    )
    await message.answer(msg, reply_markup=menu.place(**ITEMS))


@balance_router.callback_query(F.data == 'balance')
async def balance_callback(callback: CallbackQuery) -> None:
    menu = InlineMenu()
    session = UserCRUD(config.DATABASE_URL)
    user = await session.get_user(callback.from_user.id)
    msg = (
        f'💰💰💰== <strong>Данные аккаунта</strong> ==💰💰💰\n\n'
        f'🆔 ▶️ {user.id}\n\n'
        f'<em>Остаток на счету</em> ▶️ <strong>{user.balance}</strong>'
    )
    await callback.message.answer(msg, reply_markup=menu.place(**ITEMS))
