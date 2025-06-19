import uuid
from datetime import datetime


class Review:
    def __init__(self, text, rating, place, user):
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string.")
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.text = text
        self.rating = rating  # Will be validated by property setter
        self.place = place  # Will be validated below
        self.user = user  # Will be validated below

        # Validate user and place
        if not hasattr(user, "reviews"):
            raise ValueError(
                "User must be a valid User instance with a 'reviews' attribute."
            )
        if not hasattr(place, "reviews"):
            raise ValueError(
                "Place must be a valid Place instance with a 'reviews' attribute."
            )

        # Add this review to user and place
        user.reviews.append(self)
        place.reviews.append(self)

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        self._rating = value
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
