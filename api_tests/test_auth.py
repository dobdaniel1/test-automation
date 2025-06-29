import pytest
import requests
from utils.test_helpers import AuthTestHelper

class TestAuthentication:
    def setup_method(self):
        self.auth_helper = AuthTestHelper()
        self.base_url = "https://api.techcorp.com/v1"

    def test_valid_login(self):
        #Test login with valid credentials
        credentials = {
            "email": "test.user@techcorp.com",
            "password": "TestPassword123!"
        }
        response = requests.post(
            f"{self.base_url}/auth/login",
            json=credentials
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    def test_invalid_credentials(self):
        #Test login with invalid credentials
        credentials = {
            "email": "invalid@techcorp.com",
            "password": "wrongpassword"
        }
        response = requests.post(
            f"{self.base_url}/auth/login",
            json=credentials
        )
        assert response.status_code == 401
        assert response.json()["error"] == "Invalid credentials"

    def test_jwt_token_validation(self):
        #Test token validation
        token = self.auth_helper.get_valid_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{self.base_url}/auth/validate",
            headers=headers
        )
        assert response.status_code == 200

    def test_expired_token(self):
        #Test access with expired token
        expired_token = self.auth_helper.get_expired_token()
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = requests.get(
            f"{self.base_url}/users",
            headers=headers
        )
        assert response.status_code == 401
        assert "Token expired" in response.json()["message"]