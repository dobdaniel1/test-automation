import pytest
import requests
from utils.test_helpers import APITestHelper


class TestDataIsolation:
    def setup_method(self):
        self.api_helper = APITestHelper()
        self.base_url = "https://api.techcorp.com/v1"

    def test_tenant_data_isolation(self):
        #Test that users can only access their tenant's data
        tenant_001_headers = self.api_helper.get_auth_headers("tenant_001")

        # Try to access tenant_002
        response = requests.get(
            f"{self.base_url}/users?tenant_id=tenant_002",
            headers=tenant_001_headers
        )
        assert response.status_code == 403
        assert "Access denied" in response.json()["message"]

    def test_cross_tenant_user_access(self):
        #Test that users cannot access other tenant's user data
        tenant_001_headers = self.api_helper.get_auth_headers("tenant_001")
        tenant_002_user_id = "user_100"  # From tenant_002

        response = requests.get(
            f"{self.base_url}/users/{tenant_002_user_id}",
            headers=tenant_001_headers
        )
        assert response.status_code == 404