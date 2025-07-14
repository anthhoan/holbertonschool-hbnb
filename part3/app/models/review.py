from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.baseclass import BaseModel


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = Column(String(1024), nullable=False)
    rating = Column(Integer, nullable=False)

    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    # Relationships
    place_r = relationship("Place", back_populates="reviews_r")
    user_r = relationship("User", back_populates="reviews_r")

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def to_dict(self):
        return {
        "id": self.id,
        "text": self.text,
        "rating": self.rating,
        "user_id": self.user_id,
        "place_id": self.place_id
    }

