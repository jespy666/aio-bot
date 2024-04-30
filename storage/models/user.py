from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):

    name: Mapped[str] = mapped_column(String(32), unique=False)
    gpt3_requests: Mapped[int] = mapped_column(
        Integer, unique=False, default=50
    )
    balance: Mapped[float] = mapped_column(
        Float, unique=False, default=0.00
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
