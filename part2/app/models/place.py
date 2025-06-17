import uuid
from datetime import datetime

class Place:
    def __init__(self, title, description, price, latitude, longitude, owner):
        if None in (title, description, price, latitude, longitude, owner):
            raise ValueError("All attributes must be provided")

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        self.title = title
        self.description = description
        self._price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        self.reviews = []
        self.amenities = []
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        self._price = value
        self.updated_at = datetime.now()

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def save(self):
        self.updated_at = datetime.now() 

