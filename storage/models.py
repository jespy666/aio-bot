from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    balance = Column(
        Float,
        default=0.00,
        nullable=False
    )

    def __repr__(self):
        return (f"<User(id={self.id}, name={self.name},"
                f" balance={self.balance})>")

