from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from storage.models import User, Balance


async def create_user(session: AsyncSession, name: str, pk: int) -> None:
    if not name:
        name = str(pk)
    user = User(id=pk, name=name)
    balance = Balance(user_id=pk)
    session.add_all((user, balance))
    await session.commit()


async def get_user(session: AsyncSession, pk: int) -> User | None:
    stmt = select(User).where(User.id == pk)
    user: User | None = await session.scalar(stmt)
    return user


async def get_balance(session: AsyncSession, pk: int) -> Balance:
    stmt = select(Balance).where(Balance.user_id == pk)
    balance: Balance = await session.scalar(stmt)
    return balance


# async def get_user(session: AsyncSession, pk: int) -> User:
#     async with session.begin():
#         stmt = select(User).filter(User.id == pk)
#         response = await session.execute(stmt)
#         user = response.first()
#         return user[0]
#
#
# async def set_balance(session: AsyncSession, pk: int, net: float) -> None:
#     async with session.begin():
#         stmt = update(User).where(User.id == pk).values(balance=net)
#         await session.execute(stmt)
#         await session.commit()
