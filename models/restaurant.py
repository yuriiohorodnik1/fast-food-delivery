from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from config.database import Base


class Restaurant(Base):
    """SQLAlchemy model representation for a restaurant."""

    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(Text)
    image = Column(String, nullable=True)

    categories = relationship('Category', back_populates='restaurant', cascade='all, delete')
