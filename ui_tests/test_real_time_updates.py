import pytest
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.test_helpers import UITestHelper, APITestHelper
from config.selenium_config import SeleniumConfig


class TestRealTimeUpdates:
    def setup_method(self):
        self.driver = SeleniumConfig.get_driver()
        self.ui_helper = UITestHelper(self.driver)
        self.api_helper = APITestHelper()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "https://app.techcorp.com"

    def teardown_method(self):
        self.driver.quit()

    def test_real_time_user_creation_notification(self):
        #Test real-time notification when user is created
        self.ui_helper.login("admin@techcorp.com", "AdminPass123!")
        self.driver.get(f"{self.base_url}/users")

        # Get initial user count
        initial_users = len(self.driver.find_elements(By.CLASS_NAME, "user-row"))

        # Create user via API in background thread
        def create_user_via_api():
            time.sleep(2)
            user_data = {
                "first_name": "RealTime",
                "last_name": "Test",
                "email": "realtime@techcorp.com",
                "department": "IT",
                "title": "Test Engineer"
            }
            headers = self.api_helper.get_auth_headers()
            import requests
            requests.post(
                "https://api.techcorp.com/v1/users",
                json=user_data,
                headers=headers
            )

        # Start background thread
        thread = threading.Thread(target=create_user_via_api)
        thread.start()

        # Listen for real-time update notification
        notification = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "notification"))
        )
        assert "New user created" in notification.text

        # check that user appears in list without refresh
        self.wait.until(
            lambda driver: len(driver.find_elements(By.CLASS_NAME, "user-row")) > initial_users
        )

        thread.join()

    def test_concurrent_user_updates(self):
        #Test handling of concurrent user updates
        self.ui_helper.login("admin@techcorp.com", "AdminPass123!")
        self.driver.get(f"{self.base_url}/users")

        # Open user edit modal
        edit_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".user-row:first-child .edit-btn"))
        )
        edit_btn.click()

        # Start editing
        title_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "title"))
        )
        title_field.clear()
        title_field.send_keys("Updated Title")

        # Simulate concurrent update via API
        def update_via_api():
            user_data = {"title": "API Updated Title"}
            headers = self.api_helper.get_auth_headers()
            import requests
            requests.patch(
                "https://api.techcorp.com/v1/users/user_001",
                json=user_data,
                headers=headers
            )

        thread = threading.Thread(target=update_via_api)
        thread.start()

        # Try to save UI changes
        save_btn = self.driver.find_element(By.ID, "save-btn")
        save_btn.click()

        # Should show conflict warning
        conflict_warning = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "conflict-warning"))
        )
        assert "Another user has modified this record" in conflict_warning.text

        thread.join()