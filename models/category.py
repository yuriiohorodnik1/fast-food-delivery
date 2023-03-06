from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base


class Category(Base):
    """SQLAlchemy representation model for categories."""

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    image = Column(String, nullable=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    restaurant = relationship('Restaurant', back_populates='categories')
