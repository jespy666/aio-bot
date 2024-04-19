# from sqlalchemy import Integer
# from sqlalchemy.orm import Mapped, mapped_column
#
# from storage.mixins import UserRelationMixin
# from .base import Base
#
#
# class Balance(UserRelationMixin, Base):
#
#     _user_back_populates = 'balance'
#
#     gpt4: Mapped[int] = mapped_column(Integer, unique=False, default=0)
#     gpt3_5: Mapped[int] = mapped_column(Integer, unique=False, default=50)
#     dall_e3: Mapped[int] = mapped_column(Integer, unique=False, default=0)
#
#     def __repr__(self):
#         return str(self)
