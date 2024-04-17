from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session
)
from asyncio import current_task

from config import config


class Session:

    TIMEOUT = 180

    def __init__(self):
        self.engine = create_async_engine(config.DATABASE_URL, echo=True)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    def _get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def get_session(self) -> AsyncSession:
        scoped_session = self._get_scoped_session()
        async with scoped_session() as session:
            return session
