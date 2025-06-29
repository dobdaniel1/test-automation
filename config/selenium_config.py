from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os


class SeleniumConfig:
    @staticmethod
    def get_driver(browser="chrome", headless=False):
        if browser.lower() == "chrome":
            options = Options()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            return webdriver.Chrome(options=options)

        elif browser.lower() == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")

            return webdriver.Firefox(options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser}")

    @staticmethod
    def get_mobile_driver():
        options = Options()
        options.add_argument("--headless")
        options.add_experimental_option("mobileEmulation", {
            "deviceName": "iPhone 12"
        })

        return webdriver.Chrome(options=options)