import pytest
import requests
from utils.test_helpers import SecurityTestHelper


class TestInputValidation:
    def setup_method(self):
        self.security_helper = SecurityTestHelper()
        self.base_url = "https://api.techcorp.com/v1"
        self.headers = self.security_helper.get_auth_headers()

    @pytest.mark.parametrize("xss_payload", [
        "<script>alert('XSS')</script>",
        "javascript:alert('XSS')",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "';alert('XSS');//"
    ])
    def test_xss_prevention(self, xss_payload):
        #Test XSS payload prevention
        user_data = {
            "first_name": xss_payload,
            "last_name": "Test",
            "email": "test@techcorp.com",
            "department": "IT",
            "title": "Engineer"
        }
        response = requests.post(
            f"{self.base_url}/users",
            json=user_data,
            headers=self.headers
        )
        # Should either reject or sanitize the input
        if response.status_code == 201:
            # If accepted, verify it's sanitized
            created_user = response.json()
            assert "<script>" not in created_user["first_name"]
            assert "javascript:" not in created_user["first_name"]

    @pytest.mark.parametrize("sql_payload", [
        "'; DROP TABLE users; --",
        "' OR '1'='1",
        "'; UPDATE users SET password='hacked' WHERE email='admin@techcorp.com'; --",
        "' UNION SELECT * FROM sensitive_data --",
        "admin'--"
    ])
    def test_sql_injection_prevention(self, sql_payload):
        #Test SQL injection prevention
        # Test in search parameter
        response = requests.get(
            f"{self.base_url}/users",
            params={"search": sql_payload},
            headers=self.headers
        )
        # Should not cause server error or return unexpected data
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            # Verify no sensitive data leaked
            assert "password" not in str(response.json())

    def test_email_validation(self):
        #Test email format validation
        invalid_emails = [
            "not-an-email",
            "@invalid.com",
            "user@",
            "",
            "a" * 256 + "@test.com"
        ]

        for invalid_email in invalid_emails:
            user_data = {
                "first_name": "Test",
                "last_name": "User",
                "email": invalid_email,
                "department": "IT",
                "title": "Engineer"
            }
            response = requests.post(
                f"{self.base_url}/users",
                json=user_data,
                headers=self.headers
            )
            assert response.status_code == 400
            assert "email" in response.json()["errors"]