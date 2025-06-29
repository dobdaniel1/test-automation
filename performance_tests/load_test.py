import pytest
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.test_helpers import PerformanceTestHelper


class TestLoadPerformance:
    def setup_method(self):
        self.perf_helper = PerformanceTestHelper()
        self.base_url = "https://api.techcorp.com/v1"
        self.headers = self.perf_helper.get_auth_headers()

    def test_api_load_performance(self):
        #Test API performance under load

        def make_request():
            start_time = time.time()
            response = requests.get(
                f"{self.base_url}/users",
                headers=self.headers
            )
            end_time = time.time()
            return {
                "status_code": response.status_code,
                "response_time": end_time - start_time
            }

        # Run 100 concurrent requests
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(make_request) for _ in range(100)]
            results = [future.result() for future in as_completed(futures)]

        # Analyze results
        response_times = [r["response_time"] for r in results]
        successful_requests = [r for r in results if r["status_code"] == 200]

        avg_response_time = sum(response_times) / len(response_times)
        success_rate = len(successful_requests) / len(results)

        assert avg_response_time < 0.5 
        assert success_rate > 0.95  
        assert max(response_times) < 2.0  

    def test_user_creation_performance(self):
        #Test user creation performance

        def create_user(user_id):
            user_data = {
                "first_name": f"User{user_id}",
                "last_name": "Test",
                "email": f"user{user_id}@techcorp.com",
                "department": "IT",
                "title": "Engineer"
            }
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/users",
                json=user_data,
                headers=self.headers
            )
            end_time = time.time()
            return {
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "user_id": user_id
            }

        # Create 50 users concurrently
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(create_user, i) for i in range(50)]
            results = [future.result() for future in as_completed(futures)]

        # Analyze results
        response_times = [r["response_time"] for r in results]
        successful_requests = [r for r in results if r["status_code"] == 201]

        avg_response_time = sum(response_times) / len(response_times)
        success_rate = len(successful_requests) / len(results)

        assert avg_response_time < 1.0  # 1 second average for creation
        assert success_rate > 0.90  # 90% success rate