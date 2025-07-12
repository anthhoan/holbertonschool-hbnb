import uuid
from datetime import datetime
from app.models.baseclass import BaseModel
from sqlalchemy import Column, String, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app import db

place_amenity = Table('place_amenity', db.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'
    _title = db.Column('title', db.String(100), nullable=False)
    _description = db.Column('description', db.Text(), nullable=False)
    _price = db.Column('price', db.Float(), nullable=False)
    _latitude = db.Column('latitude', db.Float(), nullable=False)
    _longitude = db.Column('longitude', db.Float(), nullable=False)
    _owner_id = db.Column('owner_id', db.String(60), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    owner_r = relationship("User", back_populates="places_r")
    reviews_r = relationship("Review", back_populates="place_r")
    amenities_r = relationship("Amenity", secondary=place_amenity, back_populates="places_r")

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

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
            raise ValueError("Owner ID cannot be empty")
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
        """Add a review to this place"""
        if review not in self.reviews_r:
            self.reviews_r.append(review)

    """
    ADD AMENITY
    """
    def add_amenity(self, amenity):
        """Add an amenity to this place"""
        if amenity not in self.amenities_r:
            self.amenities_r.append(amenity)