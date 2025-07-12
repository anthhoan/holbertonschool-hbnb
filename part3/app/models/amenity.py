import uuid
from datetime import datetime
from app.models.baseclass import BaseModel
from sqlalchemy.orm import relationship
from app import db

class Amenity(BaseModel):
    """Amenity model"""
    __tablename__ = 'amenities'

    _name = db.Column('name', db.String(50), nullable=False)

    # Relationship to Place (many-to-many)
    places_r = relationship("Place", secondary="place_amenity", back_populates="amenities_r")

    def __init__(self, name):
        super().__init__()
        self.name = name

    """
    NAME
    """
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        value = value.strip()
        if not value:
            raise ValueError("Amenity name cannot be empty")
        if len(value) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters")
        self._name = value

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
