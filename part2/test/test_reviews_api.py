import json
import unittest

from app import create_app


class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a test user
        user_response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "Review",
                "last_name": "Writer",
                "email": "review.writer@example.com",
            },
        )
        self.user_data = json.loads(user_response.data)
        # Ensure user_data has an id field
        if "id" not in self.user_data:
            self.user_data = {"id": "test-user-id"}

        # Create a test place
        place_response = self.client.post(
            "/api/v1/places/",
            json={
                "title": "Place for Reviews",
                "description": "A place to test reviews",
                "price": 120.00,
                "latitude": 37.7749,
                "longitude": -122.4194,
                "owner_id": self.user_data["id"],
                "amenities": [],
            },
        )
        self.place_data = json.loads(place_response.data)
        # Ensure place_data has an id field
        if "id" not in self.place_data:
            self.place_data = {"id": "test-place-id"}

    def tearDown(self):
        # Clear all repositories to ensure test isolation
        from app.services import facade

        facade.user_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        self.app_context.pop()

    def test_create_review_success(self):
        """Test creating a review with valid data"""
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "This place was amazing! Would definitely stay again.",
                "rating": 5,
                "user_id": self.user_data["id"],
                "place_id": self.place_data.get("id", ""),
            },
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("id", data)
        self.assertEqual(
            data["text"], "This place was amazing! Would definitely stay again."
        )
        self.assertEqual(data["rating"], 5)
        self.assertEqual(data["user_id"], self.user_data["id"])
        self.assertEqual(data["place_id"], self.place_data["id"])

    def test_create_review_invalid_rating(self):
        """Test creating a review with invalid rating"""
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "This place was okay.",
                "rating": 6,  # Invalid rating (>5)
                "user_id": self.user_data["id"],
                "place_id": self.place_data.get("id", ""),
            },
        )

        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "This place was terrible.",
                "rating": 0,  # Invalid rating (<1)
                "user_id": self.user_data["id"],
                "place_id": self.place_data.get("id", ""),
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_create_review_empty_text(self):
        """Test creating a review with empty text"""
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "",  # Empty text should be rejected
                "rating": 3,
                "user_id": self.user_data["id"],
                "place_id": self.place_data.get("id", ""),
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user(self):
        """Test creating a review with non-existent user"""
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Great place!",
                "rating": 4,
                "user_id": "nonexistent-user-id",
                "place_id": self.place_data.get("id", ""),
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_place(self):
        """Test creating a review with non-existent place"""
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Great place!",
                "rating": 4,
                "user_id": self.user_data["id"],
                "place_id": "nonexistent-place-id",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        """Test retrieving all reviews"""
        # First create a review
        self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Review for all reviews test",
                "rating": 4,
                "user_id": self.user_data["id"],
                "place_id": self.place_data.get("id", ""),
            },
        )

        # Then get all reviews
        response = self.client.get("/api/v1/reviews/")

        self.assertEqual(response.status_code, 200)
        reviews = json.loads(response.data)
        self.assertIsInstance(reviews, list)
        self.assertGreaterEqual(len(reviews), 1)

        # Check structure of a review in the list
        review = reviews[0]
        self.assertIn("id", review)
        self.assertIn("text", review)
        self.assertIn("rating", review)
        self.assertIn("user_id", review)
        self.assertIn("place_id", review)

    def test_get_review_by_id(self):
        """Test retrieving a specific review by ID"""
        # First create a review
        create_response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Review to be retrieved",
                "rating": 5,
                "user_id": self.user_data["id"],
                "place_id": self.place_data.get("id", ""),
            },
        )
        create_data = json.loads(create_response.data)
        review_id = create_data.get("id")

        # Then get the review by ID
        response = self.client.get(f"/api/v1/reviews/{review_id}")

        self.assertEqual(response.status_code, 200)
        review = json.loads(response.data)
        self.assertEqual(review["id"], review_id)
        self.assertEqual(review["text"], "Review to be retrieved")
        self.assertEqual(review["rating"], 5)
        self.assertEqual(review["user_id"], self.user_data["id"])
        self.assertEqual(review["place_id"], self.place_data["id"])

    def test_get_nonexistent_review(self):
        """Test retrieving a review that doesn't exist"""
        response = self.client.get("/api/v1/reviews/nonexistent-review-id")
        self.assertEqual(response.status_code, 404)

    def test_get_reviews_for_place(self):
        """Test retrieving reviews for a specific place"""
        # First create a review
        self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Wonderful stay!",
                "rating": 5,
                "user_id": self.user_data["id"],
                "place_id": self.place_data.get("id", ""),
            },
        )

        # Then get reviews for the place
        response = self.client.get(
            f"/api/v1/reviews/places/{self.place_data.get('id', '')}/reviews"
        )

        self.assertEqual(response.status_code, 200)
        reviews = json.loads(response.data)
        self.assertGreaterEqual(len(reviews), 1)

        # Check structure of a review in the list
        if reviews:
            review = reviews[0]
            self.assertIn("id", review)
            self.assertIn("text", review)
            self.assertIn("rating", review)

    def test_get_reviews_for_nonexistent_place(self):
        """Test retrieving reviews for a place that doesn't exist"""
        response = self.client.get(
            "/api/v1/reviews/places/nonexistent-place-id/reviews"
        )
        self.assertEqual(response.status_code, 404)

    def test_update_review(self):
        """Test updating an existing review"""
        # First create a review
        create_response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Initial review text",
                "rating": 3,
                "user_id": self.user_data["id"],
                "place_id": self.place_data.get("id", ""),
            },
        )
        create_data = json.loads(create_response.data)
        review_id = create_data.get("id")

        # Then update the review
        update_response = self.client.put(
            f"/api/v1/reviews/{review_id}",
            json={"text": "Updated review text", "rating": 4},
        )

        self.assertEqual(update_response.status_code, 200)

        # Verify the update
        get_response = self.client.get(f"/api/v1/reviews/{review_id}")
        get_data = json.loads(get_response.data)

        self.assertEqual(get_data["text"], "Updated review text")
        self.assertEqual(get_data["rating"], 4)

    def test_update_review_invalid_data(self):
        """Test updating a review with invalid data"""
        # First create a review
        create_response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Review for invalid update test",
                "rating": 3,
                "user_id": self.user_data["id"],
                "place_id": self.place_data.get("id", ""),
            },
        )
        create_data = json.loads(create_response.data)
        review_id = create_data.get("id")

        # Try to update with invalid rating
        update_response = self.client.put(
            f"/api/v1/reviews/{review_id}",
            json={"rating": 6},  # Invalid rating (>5)
        )

        self.assertEqual(update_response.status_code, 400)

    def test_update_nonexistent_review(self):
        """Test updating a review that doesn't exist"""
        response = self.client.put(
            "/api/v1/reviews/nonexistent-review-id",
            json={"text": "Updated text", "rating": 4},
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_review(self):
        """Test deleting a review"""
        # First create a review
        create_response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Review to be deleted",
                "rating": 2,
                "user_id": self.user_data["id"],
                "place_id": self.place_data.get("id", ""),
            },
        )
        create_data = json.loads(create_response.data)
        review_id = create_data.get("id")

        # Then delete the review
        delete_response = self.client.delete(f"/api/v1/reviews/{review_id}")
        self.assertEqual(delete_response.status_code, 200)

        # Verify it's deleted
        get_response = self.client.get(f"/api/v1/reviews/{review_id}")
        self.assertEqual(get_response.status_code, 404)

    def test_delete_nonexistent_review(self):
        """Test deleting a review that doesn't exist"""
        response = self.client.delete("/api/v1/reviews/nonexistent-review-id")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
