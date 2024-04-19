from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):

    name: Mapped[str] = mapped_column(String(32), unique=False)
    pre_subscription: Mapped[bool] = mapped_column(
        Boolean, unique=False, default=False
    )
    gpt3_requests: Mapped[int] = mapped_column(
        Integer, unique=False, default=50
    )
    gpt4_requests: Mapped[int] = mapped_column(
        Integer, unique=False, default=0
    )
    image_requests: Mapped[int] = mapped_column(
        Integer, unique=False, default=0
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
