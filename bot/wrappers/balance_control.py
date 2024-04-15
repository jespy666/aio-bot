from functools import wraps
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from crud import UserCRUD
from config import config


def balance_control(func):

    @wraps(func)
    async def wrapper(message: Message, state: FSMContext):
        session = UserCRUD(config.DATABASE_URL)
        await session.create_user(message.chat.first_name, message.chat.id)
        user = await session.get_user(message.chat.id)
        if user.balance <= 0.000001:
            await message.answer(
                'У вас недостаточно средств!\n'
                'Пополните баланс...'
            )
            await state.clear()
            return
        return await func(message, state)
    return wrapper
