import requests
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class APITestHelper:
    def __init__(self):
        self.base_url = "https://api.techcorp.com/v1"
        self.auth_token = None

    def get_auth_headers(self, tenant_id="tenant_001"):
        if not self.auth_token:
            self.auth_token = self._get_auth_token(tenant_id)
        return {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }

    def _get_auth_token(self, tenant_id):
        credentials = {
            "email": "admin@techcorp.com",
            "password": "AdminPass123!",
            "tenant_id": tenant_id
        }
        response = requests.post(
            f"{self.base_url}/auth/login",
            json=credentials
        )
        return response.json()["access_token"]


class UITestHelper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login(self, email, password):
        self.driver.get("https://app.techcorp.com/login")

        email_field = self.wait.until(
            ec.presence_of_element_located((By.ID, "email"))
        )
        email_field.send_keys(email)

        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(password)

        login_btn = self.driver.find_element(By.ID, "login-btn")
        login_btn.click()

        # Wait for redirect to dashboard path
        self.wait.until(
            ec.url_contains("/dashboard")
        )

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(locator)
        )


class SecurityTestHelper:
    def __init__(self):
        self.base_url = "https://api.techcorp.com/v1"

    def get_auth_headers(self, user_type="admin"):
        credentials = {
            "admin": {
                "email": "admin@techcorp.com",
                "password": "AdminPass123!"
            },
            "regular_user": {
                "email": "user@techcorp.com",
                "password": "UserPass123!"
            },
            "tenant_001": {
                "email": "tenant1@techcorp.com",
                "password": "TenantPass123!"
            }
        }

        creds = credentials[user_type]
        response = requests.post(
            f"{self.base_url}/auth/login",
            json=creds
        )
        token = response.json()["access_token"]

        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }


class PerformanceTestHelper:
    def __init__(self):
        self.base_url = "https://api.techcorp.com/v1"

    def get_auth_headers(self):
        credentials = {
            "email": "admin@techcorp.com",
            "password": "AdminPass123!"
        }
        response = requests.post(
            f"{self.base_url}/auth/login",
            json=credentials
        )
        token = response.json()["access_token"]

        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }


class AuthTestHelper:
    def __init__(self):
        self.base_url = "https://api.techcorp.com/v1"

    def get_valid_token(self):
        credentials = {
            "email": "test.user@techcorp.com",
            "password": "TestPassword123!"
        }
        response = requests.post(
            f"{self.base_url}/auth/login",
            json=credentials
        )
        return response.json()["access_token"]

    def get_expired_token(self):
        # Return a simulated expired token
        return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkV4cGlyZWQgVG9rZW4iLCJpYXQiOjE1MTYyMzkwMjIsImV4cCI6MTUxNjIzOTAyM30.expired_token_signature"