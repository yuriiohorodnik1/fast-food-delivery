from sqlalchemy import Column, String, Integer

from config.database import Base


class User(Base):
    """SQLAlchemy representation model of the user."""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    class Config:
        orm_mode = True
