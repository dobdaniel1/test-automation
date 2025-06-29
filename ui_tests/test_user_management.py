import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from utils.test_helpers import UITestHelper
from config.selenium_config import SeleniumConfig


class TestUserManagement:
    def setup_method(self):
        self.driver = SeleniumConfig.get_driver()
        self.ui_helper = UITestHelper(self.driver)
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "https://app.techcorp.com"

    def teardown_method(self):
        self.driver.quit()

    def test_create_new_user(self):
        #Test creating a new user through UI
        # Login
        self.ui_helper.login("admin@techcorp.com", "AdminPass123!")

        # Navigate to users page
        self.driver.get(f"{self.base_url}/users")

        # Click create user button
        create_btn = self.wait.until(
            ec.element_to_be_clickable((By.ID, "create-user-btn"))
        )
        create_btn.click()

        # Fill user form
        self.driver.find_element(By.ID, "first-name").send_keys("Test")
        self.driver.find_element(By.ID, "last-name").send_keys("User")
        self.driver.find_element(By.ID, "email").send_keys("testuser@techcorp.com")
        self.driver.find_element(By.ID, "department").send_keys("IT")
        self.driver.find_element(By.ID, "title").send_keys("Test Engineer")

        # Submit form
        self.driver.find_element(By.ID, "submit-btn").click()

        # Verify success message
        success_msg = self.wait.until(
            ec.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "User created successfully" in success_msg.text

    def test_search_user(self):
        #Test user search functionality
        self.ui_helper.login("admin@techcorp.com", "AdminPass123!")
        self.driver.get(f"{self.base_url}/users")

        # Search for user
        search_box = self.driver.find_element(By.ID, "user-search")
        search_box.send_keys("testuser@techcorp.com")
        search_box.submit()

        # Verify search results
        self.wait.until(
            ec.presence_of_element_located((By.CLASS_NAME, "user-row"))
        )
        user_rows = self.driver.find_elements(By.CLASS_NAME, "user-row")
        assert len(user_rows) == 1
        assert "testuser@techcorp.com" in user_rows[0].text

    def test_edit_user_details(self):
        #Test editing user details
        self.ui_helper.login("admin@techcorp.com", "AdminPass123!")
        self.driver.get(f"{self.base_url}/users")

        # Find and click edit button for first user on the table
        edit_btn = self.wait.until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, ".user-row:first-child .edit-btn"))
        )
        edit_btn.click()

        # Update title
        title_field = self.wait.until(
            ec.presence_of_element_located((By.ID, "title"))
        )
        title_field.clear()
        title_field.send_keys("Senior Test Engineer")

        # Save changes
        self.driver.find_element(By.ID, "save-btn").click()

        # Verify update
        success_msg = self.wait.until(
            ec.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "User updated successfully" in success_msg.text

    def test_delete_user(self):
        #Test user deletion
        self.ui_helper.login("admin@techcorp.com", "AdminPass123!")
        self.driver.get(f"{self.base_url}/users")

        # Click delete button
        delete_btn = self.wait.until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, ".user-row:last-child .delete-btn"))
        )
        delete_btn.click()

        # Confirm deletion in modal
        confirm_btn = self.wait.until(
            ec.element_to_be_clickable((By.ID, "confirm-delete"))
        )
        confirm_btn.click()

        # Verify deletion
        success_msg = self.wait.until(
            ec.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "User deleted successfully" in success_msg.text