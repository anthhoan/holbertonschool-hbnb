import uuid
from datetime import datetime

class Amenity:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    # Amenity name
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

    # Save
    def save(self):
        """Function to save created_at time"""
        self.updated_at = datetime.now()

    # Update
    def update(self, data):
        """Function to save updated_at time"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
