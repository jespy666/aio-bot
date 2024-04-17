from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, update

from storage.models import User


class UserCRUD:

    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url, echo=True)
        self.async_session = async_sessionmaker(bind=self.engine,
                                                expire_on_commit=False)

    async def create_user(self, name: str, pk: int) -> None:
        if not name:
            name = str(pk)
        async with self.async_session() as session:
            async with session.begin():
                stmt = select(User).filter(User.id == pk)
                response = await session.execute(stmt)
                if response.fetchone():
                    return
            user = User(id=pk, name=name)
            session.add(user)
            await session.commit()

    async def get_user(self, pk: int) -> User:
        async with self.async_session() as session:
            async with session.begin():
                stmt = select(User).filter(User.id == pk)
                response = await session.execute(stmt)
                user = response.first()
                return user[0]

    async def set_balance(self, pk: int, net_balance: float) -> None:
        async with self.async_session() as session:
            async with session.begin():
                stmt = update(User).where(User.id == pk).values(
                    balance=net_balance
                )
                await session.execute(stmt)
                await session.commit()
