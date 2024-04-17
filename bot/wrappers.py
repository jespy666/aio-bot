from functools import wraps
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from storage.models import User
from storage import crud
from storage.session import Session


def check_balance(func):
    @wraps(func)
    async def wrapper(message: Message, state: FSMContext, **kwargs):
        context = await state.get_data()
        session = kwargs.get('session')
        if not session:
            session = Session().get_session()
        # for performance optimization, check the user from FSM context
        user: User = context.get('user')
        if not user:
            user: User = await crud.get_user(session, message.chat.id)
        balance: float = user.balance
        await state.update_data(user=user, session=session)
        if balance <= 0.000001:
            await message.answer(
                'У вас недостаточно средств!\n'
                'Пополните баланс...'
            )
            await state.clear()
            return
        return await func(message, state, **kwargs)
    return wrapper


def check_user(func):

    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        session = await Session().get_session()
        user_id = message.chat.id
        user = await crud.get_user(session, user_id)
        if not user:
            await crud.create_user(session, user_id)
        return await func(message, session=session, *args, **kwargs)

    return wrapper
