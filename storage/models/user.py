from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .balance import Balance


class User(Base):

    name: Mapped[str] = mapped_column(String(32), unique=False)
    pre_subscription: Mapped[bool] = mapped_column(
        Boolean, unique=False, default=False
    )
    balance: Mapped['Balance'] = relationship(back_populates='user')

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id},"
                f" username={self.name!r})")

    def __repr__(self):
        return str(self)
