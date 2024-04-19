from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from bot.keyboards import InlineMenu

from storage.models import User

from ..wrappers import check_user


balance_router = Router()

ITEMS = {
    'Главная': 'start',
    'Начать диалог': 'ask',
    'О боте': 'about',
}


@balance_router.message(Command('balance'))
@check_user(with_kwargs=True)
async def show_balance(message: Message, **kwargs) -> None:
    user: User = kwargs.get('user')
    menu = InlineMenu().place(**ITEMS)
    is_premium = user.pre_subscription
    status = 'Премиум' if is_premium else 'Бесплатный'
    limit = 100 if is_premium else 50
    msg = (
        f'=== <strong>Данные аккаунта</strong> ===\n\n'
        f'<em>Привет, <strong>{user.name}</strong>\n\n'
        f'Статус вашего аккаунта: <strong>{status}</strong>\n\n'
        f'🔽 <strong>Остаток ваших запросов</strong> 🔽\n\n'
        f'ChatGPT 3.5: -- <strong>{user.gpt3_requests}/{limit}</strong>\n'
        f'ChatGPT 4: ---- <strong>{user.gpt4_requests}</strong>\n'
        f'Dall-e 3: -------- <strong>{user.image_requests}</strong></em>'
    )
    await message.answer(msg, reply_markup=menu)


@balance_router.callback_query(F.data == 'balance')
async def balance_callback(callback: CallbackQuery) -> None:
    await show_balance(callback.message)
