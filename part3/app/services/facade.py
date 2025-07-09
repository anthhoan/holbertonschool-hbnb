from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.users import User
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.UserRepository import UserRepository


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
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)


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
        # Review class will validate text and rating
        review = Review(text=text, rating=rating, place=place, user=user)
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
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        # Only allow updating text and rating
        allowed_fields = ["text", "rating"]
        update_data = {k: v for k, v in review_data.items() if k in allowed_fields}
        review.update(update_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        # Remove from user and place reviews lists
        if review in review.user.reviews:
            review.user.reviews.remove(review)
        if review in review.place.reviews:
            review.place.reviews.remove(review)
        self.review_repo.delete(review_id)
        return True
