import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from config.selenium_config import SeleniumConfig
from utils.test_helpers import UITestHelper


class TestResponsiveDesign:
    def setup_method(self):
        self.driver = SeleniumConfig.get_driver()
        self.ui_helper = UITestHelper(self.driver)
        self.base_url = "https://app.techcorp.com"

    def teardown_method(self):
        self.driver.quit()

    @pytest.mark.parametrize("width,height", [
        (1920, 1080),  # for Desktop
        (1024, 768),  # for Tablet
        (375, 667),  # for Mobile
    ])
    def test_responsive_layout(self, width, height):
        #Test responsive layout across different screen sizes
        self.driver.set_window_size(width, height)
        self.ui_helper.login("admin@techcorp.com", "AdminPass123!")
        self.driver.get(f"{self.base_url}/users")

        # Check if navigation is visible/accessible
        if width >= 1024:
            # Desktop/Tablet - navigation should be visible
            nav_menu = self.driver.find_element(By.ID, "main-navigation")
            assert nav_menu.is_displayed()
        else:
            # Mobile - navigation should be collapsed
            hamburger_menu = self.driver.find_element(By.ID, "hamburger-menu")
            assert hamburger_menu.is_displayed()

    def test_mobile_user_table(self):
        #Test on mobile device
        self.driver.set_window_size(375, 667)
        self.ui_helper.login("admin@techcorp.com", "AdminPass123!")
        self.driver.get(f"{self.base_url}/users")

        # On mobile, table should be replaced with cards
        user_cards = self.driver.find_elements(By.CLASS_NAME, "user-card")
        assert len(user_cards) > 0

        # check that essential info is visible
        first_card = user_cards[0]
        assert first_card.find_element(By.CLASS_NAME, "user-name").is_displayed()
        assert first_card.find_element(By.CLASS_NAME, "user-email").is_displayed()