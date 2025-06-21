import json
import unittest

from app import create_app
from app.services.facade import HBnBFacade


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Clear all repositories to ensure test isolation
        from app.services import facade

        facade.user_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        self.app_context.pop()

    def test_create_user_success(self):
        """Test creating a user with valid data"""
        response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
            },
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", data)
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["last_name"], "Doe")
        self.assertEqual(data["email"], "john.doe@example.com")

    def test_create_user_invalid_email(self):
        """Test creating a user with invalid email format"""
        response = self.client.post(
            "/api/v1/users/",
            json={"first_name": "Jane", "last_name": "Doe", "email": "invalid-email"},
        )

        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_name(self):
        """Test creating a user with empty name fields"""
        response = self.client.post(
            "/api/v1/users/",
            json={"first_name": "", "last_name": "", "email": "valid@example.com"},
        )

        self.assertEqual(response.status_code, 400)

    def test_get_user_success(self):
        """Test retrieving an existing user"""
        # First create a user
        create_response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "Alice",
                "last_name": "Smith",
                "email": "alice.smith@example.com",
            },
        )
        create_data = json.loads(create_response.data)
        user_id = create_data["id"]

        # Then retrieve the user
        get_response = self.client.get(f"/api/v1/users/{user_id}")
        get_data = json.loads(get_response.data)

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_data["id"], user_id)
        self.assertEqual(get_data["first_name"], "Alice")

    def test_get_user_not_found(self):
        """Test retrieving a non-existent user"""
        response = self.client.get("/api/v1/users/nonexistent-id")

        self.assertEqual(response.status_code, 404)

    def test_create_duplicate_email(self):
        """Test creating a user with an email that's already registered"""
        # First create a user
        self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "Original",
                "last_name": "User",
                "email": "duplicate@example.com",
            },
        )

        # Try to create another user with the same email
        response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "Duplicate",
                "last_name": "User",
                "email": "duplicate@example.com",
            },
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
