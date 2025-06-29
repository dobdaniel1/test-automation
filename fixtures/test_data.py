import random
import string

class TestData:
    @staticmethod
    def get_valid_employee():
        #Return valid employee data for testing
        return {
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.doe.{random.randint(1000, 9999)}@techcorp.com",
            "department": "IT",
            "title": "Software Engineer"
        }

    @staticmethod
    def get_test_user_id():
        #Return an existing test user ID
        return "user_123"

    @staticmethod
    def create_test_user():
        #Create a test user and return its ID
        return f"user_{random.randint(1000, 9999)}"
