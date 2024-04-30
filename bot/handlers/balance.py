from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message


from ..keyboards import InlineKeyboard

from storage.models import User

from converter import CurrencyParser

from config import config

balance_router = Router()


@balance_router.message(Command('balance'))
async def show_balance(message: Message, user: User) -> None:
    menu = InlineKeyboard().place(
        {
            'Главная': 'start',
            'Как пользоваться?': 'about',
            'Создать изображение': 'generate',
            'Изменить изображение': 'edit',
            'Начать диалог (GPT)': 'ask',
            'Пополнить баланс': 'payment',
            'Посмотреть цены': 'price',

        }
    )
    balance = user.balance
    parser = CurrencyParser(config.PARSED_URL)
    currency = await parser.get_rate(
        config.PARSED_NAME, class_=config.PARSED_CLASS
    )
    rate = parser.convert_to_roubles(balance, currency)
    msg = (
        f'=== <strong>Данные аккаунта</strong> ===\n\n'
        f'<em>Привет, <strong>{user.name}</strong>\n\n'
        f'🔽 <strong>Ваш баланс</strong> 🔽\n\n'
        f'Бесплатные\nChatGPT 3.5: -- <strong>{user.gpt3_requests}/50</strong>'
        f'\nБаланс: ------- <strong>{balance}$ | {rate}₽</strong></em>'
    )
    await message.answer(msg, reply_markup=menu)


@balance_router.callback_query(F.data == 'balance')
async def balance_callback(callback: CallbackQuery, user: User) -> None:
    await show_balance(callback.message, user)
