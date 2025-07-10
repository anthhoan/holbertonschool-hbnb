from app.persistence import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.models.place import place_amenity

class Amenity(Base):
    """Amenity model"""
    __tablename__ = 'amenities'

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    _name = Column("name", String(50), nullable=False)
    places = relationship("Place", secondary=place_amenity, back_populates="amenities")


class Amenity:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    """
    NAME
    """
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        value = value.strip()
        if len(value) <= 50:
            self._name = value
        else:
            raise ValueError("Amenity name cannot exceed 50 characters")
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        self._name = name

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
