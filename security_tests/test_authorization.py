import pytest
import requests
from utils.test_helpers import SecurityTestHelper


class TestAuthorization:
    def setup_method(self):
        self.security_helper = SecurityTestHelper()
        self.base_url = "https://api.techcorp.com/v1"

    def test_admin_only_endpoints(self):
        #Test that admin endpoints reject non-admin user
        regular_user_headers = self.security_helper.get_auth_headers("regular_user")

        admin_endpoints = [
            "/admin/system-config",
            "/admin/users/bulk-delete",
            "/admin/audit-logs"
        ]

        for endpoint in admin_endpoints:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                headers=regular_user_headers
            )
            assert response.status_code == 403
            assert "insufficient privileges" in response.json()["message"].lower()

    def test_tenant_isolation(self):
        #Test that users cannot access other tenant's data
        tenant_001_headers = self.security_helper.get_auth_headers("tenant_001")

        # Try to access tenant_002 data
        response = requests.get(
            f"{self.base_url}/users?tenant_id=tenant_002",
            headers=tenant_001_headers
        )
        assert response.status_code == 403

    def test_user_can_only_edit_own_profile(self):
        #Test that users can only edit their own profile
        user_headers = self.security_helper.get_auth_headers("regular_user")
        other_user_id = "user_999"

        response = requests.patch(
            f"{self.base_url}/users/{other_user_id}",
            json={"title": "Hacked Title"},
            headers=user_headers
        )
        assert response.status_code in [403, 404]