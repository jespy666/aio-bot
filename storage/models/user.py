from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):

    name: Mapped[str] = mapped_column(String(32), unique=False)

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id},"
                f" username={self.name!r})")

    def __repr__(self):
        return str(self)

