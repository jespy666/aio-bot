from functools import wraps
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from storage import crud
from storage.models import User
from storage.session import Session

from bot import exceptions as e
from bot.keyboards import InlineMenu
from .states import TextDialogueStates


def check_user(with_kwargs=False):
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Message, *args, **kwargs):
            user_id = message.chat.id
            first_name = message.chat.first_name
            session = await Session().get_session()
            try:
                user: User = await crud.get_user(session, user_id)
                # create user if not exist
                if not user:
                    await crud.create_user(session, first_name, user_id)
                if with_kwargs:
                    return await func(message, session=session, user=user,
                                      *args, **kwargs)
                return await func(message, *args, **kwargs)
            finally:
                await session.flush()
        return wrapper
    return decorator


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
            await state.set_state(TextDialogueStates.choseModel)
        except e.EmptyRequestsError:
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
