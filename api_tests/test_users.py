import pytest
import requests
from utils.test_helpers import APITestHelper
from fixtures.test_data import TestData

class TestUserAPI:
    def setup_method(self):
        self.api_helper = APITestHelper()
        self.base_url = "https://api.techcorp.com/v1"
        self.headers = self.api_helper.get_auth_headers()

    def test_create_user_valid_data(self):
        #Test creating user with valid data
        user_data = TestData.get_valid_employee()
        response = requests.post(
            f"{self.base_url}/users",
            json=user_data,
            headers=self.headers
        )
        assert response.status_code == 201
        assert response.json()["email"] == user_data["email"]

    def test_create_user_invalid_email(self):
        #Test creating user with invalid email format
        user_data = TestData.get_valid_employee()
        user_data["email"] = "invalid-email"
        response = requests.post(
            f"{self.base_url}/users",
            json=user_data,
            headers=self.headers
        )
        assert response.status_code == 400
        assert "Invalid email format" in response.json()["message"]

    def test_get_user_by_id(self):
        #Test retrieving user by ID
        user_id = TestData.get_test_user_id()
        response = requests.get(
            f"{self.base_url}/users/{user_id}",
            headers=self.headers
        )
        assert response.status_code == 200
        assert response.json()["id"] == user_id

    def test_update_user_partial(self):
        #Test partial user update
        user_id = TestData.get_test_user_id()
        update_data = {"title": "Senior Test Engineer"}
        response = requests.patch(
            f"{self.base_url}/users/{user_id}",
            json=update_data,
            headers=self.headers
        )
        assert response.status_code == 200
        assert response.json()["title"] == update_data["title"]

    def test_delete_user(self):
        #Test user deletion
        user_id = TestData.create_test_user()
        response = requests.delete(
            f"{self.base_url}/users/{user_id}",
            headers=self.headers
        )
        assert response.status_code == 204
        # check that user is deleted
        get_response = requests.get(
            f"{self.base_url}/users/{user_id}",
            headers=self.headers
        )
        assert get_response.status_code == 404