from functools import wraps

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot import exceptions as e
from bot.keyboards import InlineMenu

from .states import TextStates


def validators(func):
    @wraps(func)
    async def wrapper(message: Message, state: FSMContext, *args, **kwargs):
        context = await state.get_data()
        cancel_btn = context.get('cancel_btn')
        try:
            return await func(message, state, *args, **kwargs)
        except e.IncorrectModelError:
            models_kb = context.get('models_kb')
            msg = (
                '🔴🔴🔴\n\n'
                '<strong>Некорректная модель!</strong>'
            )
            msg2 = (
                '<em>Нажмите кнопку с корректной моделью</em>'
            )
            await message.answer(msg, reply_markup=cancel_btn)
            await message.answer(msg2, reply_markup=models_kb)
            await state.set_state(TextStates.choseModel)
        except e.InsufficientFundsError:
            menu = InlineMenu().place(
                **{
                    'Докупить запросы': 'buy',
                    'На главную': 'start',
                    'Начать новый диалог': 'ask',
                }
            )
            msg = (
                '🔴🔴🔴\n\n'
                '<strong>У вас закончились запросы 😔</strong>\n\n'
                '<em>Пополните баланс или выберите другую модель!</em>'
            )
            await message.answer(msg, reply_markup=menu)
            await state.clear()
    return wrapper
