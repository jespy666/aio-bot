from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from bot.keyboards.inline_menu import InlineMenu

from storage import crud
from ..wrappers import check_user


balance_router = Router()

ITEMS = {
    'Главная': 'start',
    'Начать диалог': 'ask',
    'О боте': 'about',
}


@balance_router.message(Command('balance'))
@check_user
async def show_balance(message: Message, **kwargs) -> None:
    menu = InlineMenu()
    session = kwargs.get('session')
    user_id = message.chat.id
    user = await crud.get_user(session, user_id)
    is_premium = user.pre_subscription
    balance = await crud.get_balance(session, user_id)
    status = 'Премиум' if is_premium else 'Бесплатный'
    limit = 100 if is_premium else 50
    msg = (
        f'=== <strong>Данные аккаунта</strong> ===\n\n'
        f'<em>Привет, <strong>{user.name}</strong>\n\n'
        f'Статус вашего аккаунта: <strong>{status}</strong>\n\n'
        f'🔽 <strong>Остаток ваших запросов</strong> 🔽\n\n'
        f'ChatGPT 3.5: -- <strong>{balance.gpt3_5}/{limit}</strong>\n'
        f'ChatGPT 4: ---- <strong>{balance.gpt4}</strong>\n'
        f'Dall-e 3: -------- <strong>{balance.dall_e3}</strong></em>'
    )
    await message.answer(msg, reply_markup=menu.place(**ITEMS))


@balance_router.callback_query(F.data == 'balance')
async def balance_callback(callback: CallbackQuery) -> None:
    await show_balance(callback.message)
