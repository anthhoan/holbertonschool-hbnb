import uuid
from datetime import datetime
from app.models.users import User
from baseclass import BaseModel
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app import db

class Place(BaseModel):
    __tablename__ = 'places'
    _title = db.Column(db.String(100), nullable=False, unique=True)
    _description = db.Column(db.Text(), nullable=False)
    _price = db.Column(db.Float(), nullable=False)
    _latitude = db.Column(db.Float(), nullable=False)
    _longitude = db.Column(db.Float(), nullable=False)
    _owner_id = Column("owner_id", String(60), ForeignKey('users.id'), nullable=False)
    owner_r = relationship("User", back_populates="places_r")
    reviews_r = relationship("Review", back_populates="place_r")


    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.reviews = []
        self.amenities = amenities or []

    """
    TITLE
    """
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not 0 < len(value.strip()) <= 100:
            raise ValueError("Title must be between 1 - 100 characters")
        self._title = value.strip()

    """
    DESCRIPTION
    """
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("Description must be a string")
        if not 0 < len(value.strip()) <= 1000:
            raise ValueError("Description must be between 1 - 1000 characters in length")
        self._description = value.strip()

    """
    PRICE
    """
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        float_value = float(value)
        if float_value <= 0:
            raise ValueError("Price must be a positive number")
        self._price = float_value

    """
    LATITUDE
    """
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number")
        if not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 to 90 degrees")
        self._latitude = float(value)

    """
    LONGITUDE
    """
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number")
        if not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 to 180 degrees")
        self._longitude = float(value)

    """
    OWNER ID
    """
    @property
    def owner_id(self):
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        if not value:
            raise ValueError("Owner ID cannot be found")
        self._owner_id = str(value)

    """
    SAVE
    """
    def save(self):
        """Function to save created_at time"""
        self.updated_at = datetime.now()

    """
    UPDATE
    """
    def update(self, data):
        """Function to save updated_at time"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    """
    ADD REVIEW
    """
    def add_review(self, review):
        self.reviews.append(review)

    """
    ADD AMENITY
    """
    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)