from typing import Any, Awaitable, Callable, Dict

from aiogram.types import TelegramObject
from aiogram import BaseMiddleware

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from storage.models import User
from storage import crud


class UserMiddleware(BaseMiddleware):

    def __init__(self, session_pool: async_sessionmaker) -> None:
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with self.session_pool() as session:
            if 'user' not in data:
                if event.callback_query:
                    user_id = event.callback_query.from_user.id
                    first_name = event.callback_query.from_user.first_name
                else:
                    user_id = event.message.chat.id
                    first_name = event.message.chat.first_name
                user: User | None = await self._get_user(session, user_id)
                if not user:
                    user: User = await self._create_user(
                        session, first_name, user_id
                    )
                data['user'] = user
            return await handler(event, data)

    @staticmethod
    async def _get_user(session: AsyncSession, user_id: int) -> User:
        return await crud.get_user(session, user_id)

    @staticmethod
    async def _create_user(session: AsyncSession, name: str, pk: int) -> User:
        return await crud.create_user(session, name, pk)
