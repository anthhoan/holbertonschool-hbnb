import uuid
from datetime import datetime
from app.models.baseclass import BaseModel
from sqlalchemy.orm import relationship
from app import db


class Review(BaseModel):
    __tablename__ = 'reviews'

    _text = db.Column('text', db.String(1024), nullable=False)
    _rating = db.Column('rating', db.Integer, nullable=False)
    _place_id = db.Column('place_id', db.String(60), db.ForeignKey('places.id'), nullable=False)
    _user_id = db.Column('user_id', db.String(60), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    place_r = relationship("Place", back_populates="reviews_r")
    user_r = relationship("User", back_populates="reviews_r")

    def __init__(self, text, rating, place_id, user_id):
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string.")
        super().__init__()
        self.text = text
        self.rating = rating  # Will be validated by property setter
        self.place_id = place_id
        self.user_id = user_id

    """
    TEXT
    """
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError("Text must be a string")
        if not value.strip():
            raise ValueError("Review text cannot be empty")
        self._text = value.strip()

    """
    RATING
    """
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        self._rating = value
        self.updated_at = datetime.now()

    """
    PLACE ID
    """
    @property
    def place_id(self):
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        if not value:
            raise ValueError("Place ID cannot be empty")
        self._place_id = str(value)

    """
    USER ID
    """
    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if not value:
            raise ValueError("User ID cannot be empty")
        self._user_id = str(value)

    """
    SAVE
    """
    def save(self):
        self.updated_at = datetime.now()

    """
    UPDATE
    """
    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

