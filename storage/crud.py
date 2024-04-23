from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from typing import Any

from storage.models import User


async def create_user(session: AsyncSession, name: str, pk: int) -> User:
    if not name:
        name = str(pk)
    user = User(id=pk, name=name)
    session.add(user)
    await session.commit()
    return user


async def get_user(session: AsyncSession, pk: int) -> User | None:
    stmt = select(User).where(User.id == pk)
    user: User | None = await session.scalar(stmt)
    return user


async def update_user(session: AsyncSession, user_id: int, **kwargs) -> None:
    stmt = update(User).where(User.id == user_id).values(**kwargs)
    await session.execute(stmt)
    await session.commit()
