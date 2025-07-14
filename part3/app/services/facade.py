from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.users import User
from app.persistence.UserRepository import UserRepository
from app.persistence.repository import SQLAlchemyRepository
from app import bcrypt
from app import db


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    """
    USER
    """
    def create_user(self, user_data):
        # Extract password and create user without it
        password = user_data.pop('password')
        user = User(**user_data)
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        """Update a user and return the updated user"""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        # Only allow updating certain fields (not email or password for security)
        allowed_fields = ["first_name", "last_name"]
        update_data = {k: v for k, v in user_data.items() if k in allowed_fields}
        user.update(update_data)
        db.session.commit()
        return user

    def delete_user(self, user_id):
        """Delete a user and return True if successful"""
        user = self.user_repo.get(user_id)
        if not user:
            return False
        self.user_repo.delete(user_id)
        return True

    """
    AMENITY
    """
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return list(self.amenity_repo.get_all())

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)
    
    def add_amenity_to_place(self, place_id, amenity_id):
        place = self.place_repo.get(place_id)
        amenity = self.amenity_repo.get(amenity_id)
        if not place:
            raise ValueError("Place not found")
        if not amenity:
            raise ValueError("Amenity not found")
        place.add_amenity(amenity)
        db.session.commit()
        return place



    """
    PLACE
    """
    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)
    
    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return False
        self.place_repo.delete(place_id)
        return True



    """
    REVIEW
    """
    def create_review(self, review_data):
        # Validate required fields
        required_fields = ["text", "rating", "user_id", "place_id"]
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"Missing required field: {field}")
        user = self.user_repo.get(review_data["user_id"])
        if not user:
            raise ValueError("User not found")
        place = self.place_repo.get(review_data["place_id"])
        if not place:
            raise ValueError("Place not found")
        text = review_data["text"]
        rating = review_data["rating"]
        place_id = review_data["place_id"]
        user_id = review_data["user_id"]
        # Review class will validate text and rating
        review = Review(text=text, rating=rating, place_id=place_id, user_id=user_id)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.reviews_r

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Check if user_id is present and matches the review's user_id
        if "user_id" not in review_data:
            raise ValueError("Missing user_id for authorization")
        
        if review.user_id != review_data["user_id"]:
            raise ValueError("You are not authorized to update this review")

        # Only allow updating text and rating
        allowed_fields = ["text", "rating"]
        update_data = {k: v for k, v in review_data.items() if k in allowed_fields}
        review.update(update_data)
        db.session.commit()
        return review


    def delete_review(self, review_id):
        # SQLAlchemy will handle relationship cleanup automatically
        return self.review_repo.delete(review_id)
