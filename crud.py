from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from storage.models import User


class UserCRUD:

    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url, echo=True)
        self.session = async_sessionmaker(bind=self.engine,
                                          expire_on_commit=False)

    async def create_user(self, name: str, pk: int) -> None:
        if not name:
            name = pk
        async with self.session() as session:
            user = User(id=pk, name=name)
            session.add(user)
            await session.commit()
