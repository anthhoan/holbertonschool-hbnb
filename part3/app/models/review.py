from sqlalchemy import Column, String, Integer
from models.base_model import BaseModel, Base

class Review(BaseModel, Base):
    __tablename__ = 'reviews'

    text = Column(String(1024), nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(String(60), nullable=False)
    user_id = Column(String(60), nullable=False)

