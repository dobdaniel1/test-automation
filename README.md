# Test Automation Project

A comprehensive test automation framework built with Selenium WebDriver and pytest for end-to-end testing.

### Prerequisites
- Python3
- Selenium
- Chrome browser etc
- ChromeDriver etc

### Installation
```bash
pip install -r requirements.txt
```

### Run Tests
```bash
# To run all tests
pytest

# To run specific test category
pytest api_tests/
pytest ui_tests/
pytest security_tests/
pytest performance_tests/

# With reporting
pytest --html=reports/test_report.html
```

### This project was majorly done using the Core Technologies below:
- **Selenium WebDriver**: Browser automation
- **pytest**: Test framework and execution
- **Python**: Primary programming language
- **pytest-html**: report generator, thereby making the report_generator.py redundant


It was assumed that app.techcorp.com is the web url and api.techcorp.com/v1 is the base url for the api


