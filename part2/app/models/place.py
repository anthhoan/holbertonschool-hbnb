import uuid
from datetime import datetime
from app.models.users import User  # Assuming the User class is here

class Place:
    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialize a new Place instance with validation checks.
        """
        # Validate required fields
        if title is None or price is None or latitude is None or longitude is None or owner is None:
            raise ValueError("Title, price, latitude, longitude, and owner are required")

        # Validate title
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")

        # Validate description
        if description is not None and not isinstance(description, str):
            raise TypeError("Description must be a string")

        # Validate price
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number")

        # Validate latitude
        if not isinstance(latitude, (int, float)) or not -90.0 <= latitude <= 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")

        # Validate longitude
        if not isinstance(longitude, (int, float)) or not -180.0 <= longitude <= 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")

        # Validate owner
        if not isinstance(owner, User):
            raise TypeError("Owner must be a valid User instance")

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
        """Getter for price"""
        return self._price

    @price.setter
    def price(self, value):
        """
        Setter for price. Validates and updates timestamp.
        """
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number")
        self._price = value
        self.updated_at = datetime.now()

    def add_review(self, review):
        """Adds a review to the place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Adds an amenity to the place"""
        self.amenities.append(amenity)

    def save(self):
        """Updates the updated_at timestamp"""
        self.updated_at = datetime.now()

update