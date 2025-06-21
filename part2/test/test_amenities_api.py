import json
import unittest

from app import create_app


class TestAmenityEndpoints(unittest.TestCase):
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

    def test_create_amenity_success(self):
        """Test creating an amenity with valid data"""
        response = self.client.post("/api/v1/amenities/", json={"name": "WiFi"})

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("id", data)
        self.assertEqual(data["name"], "WiFi")

    def test_create_amenity_empty_name(self):
        """Test creating an amenity with empty name"""
        response = self.client.post("/api/v1/amenities/", json={"name": ""})

        self.assertEqual(response.status_code, 400)

    def test_create_amenity_too_long_name(self):
        """Test creating an amenity with a name that exceeds the maximum length"""
        response = self.client.post(
            "/api/v1/amenities/",
            json={
                "name": "A" * 51  # 51 characters, exceeding the 50 character limit
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        """Test retrieving all amenities"""
        # First create a few amenities
        self.client.post("/api/v1/amenities/", json={"name": "Pool"})
        self.client.post("/api/v1/amenities/", json={"name": "Gym"})
        self.client.post("/api/v1/amenities/", json={"name": "Parking"})

        # Then retrieve all amenities
        response = self.client.get("/api/v1/amenities/")

        self.assertEqual(response.status_code, 200)
        amenities = json.loads(response.data)
        self.assertIsInstance(amenities, list)
        self.assertGreaterEqual(len(amenities), 3)

    def test_get_amenity_success(self):
        """Test retrieving an existing amenity"""
        # First create an amenity
        create_response = self.client.post(
            "/api/v1/amenities/", json={"name": "Air Conditioning"}
        )
        create_data = json.loads(create_response.data)
        amenity_id = create_data["id"]

        # Then retrieve the amenity
        get_response = self.client.get(f"/api/v1/amenities/{amenity_id}")
        get_data = json.loads(get_response.data)

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_data["id"], amenity_id)
        self.assertEqual(get_data["name"], "Air Conditioning")

    def test_get_amenity_not_found(self):
        """Test retrieving a non-existent amenity"""
        response = self.client.get("/api/v1/amenities/nonexistent-id")

        self.assertEqual(response.status_code, 404)

    def test_update_amenity(self):
        """Test updating an existing amenity"""
        # First create an amenity
        create_response = self.client.post(
            "/api/v1/amenities/", json={"name": "Kitchen"}
        )
        create_data = json.loads(create_response.data)
        amenity_id = create_data["id"]

        # Then update the amenity
        update_response = self.client.put(
            f"/api/v1/amenities/{amenity_id}", json={"name": "Full Kitchen"}
        )

        self.assertEqual(update_response.status_code, 200)

        # Verify the update
        get_response = self.client.get(f"/api/v1/amenities/{amenity_id}")
        get_data = json.loads(get_response.data)

        self.assertEqual(get_data["name"], "Full Kitchen")

    def test_update_amenity_invalid_name(self):
        """Test updating an amenity with invalid name"""
        # First create an amenity
        create_response = self.client.post(
            "/api/v1/amenities/", json={"name": "Balcony"}
        )
        create_data = json.loads(create_response.data)
        amenity_id = create_data["id"]

        # Then try to update with invalid name
        update_response = self.client.put(
            f"/api/v1/amenities/{amenity_id}",
            json={
                "name": "A" * 51  # 51 characters, exceeding the 50 character limit
            },
        )

        self.assertEqual(update_response.status_code, 400)

    def test_update_amenity_not_found(self):
        """Test updating a non-existent amenity"""
        response = self.client.put(
            "/api/v1/amenities/nonexistent-id", json={"name": "Not Found Amenity"}
        )

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
