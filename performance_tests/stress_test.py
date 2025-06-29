import pytest
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.test_helpers import PerformanceTestHelper
import statistics


class TestStressPerformance:
    def setup_method(self):
        self.perf_helper = PerformanceTestHelper()
        self.base_url = "https://api.techcorp.com/v1"
        self.headers = self.perf_helper.get_auth_headers()

    def test_database_connection_pool_stress(self):
        #Test database connection pool under stress

        def make_db_intensive_request():
            # Request that requires multiple DB queries
            start_time = time.time()
            response = requests.get(
                f"{self.base_url}/users?include=department,projects,permissions",
                headers=self.headers
            )
            end_time = time.time()
            return {
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "data_size": len(response.content) if response.status_code == 200 else 0
            }

        # Stress test with 200 concurrent requests
        with ThreadPoolExecutor(max_workers=200) as executor:
            futures = [executor.submit(make_db_intensive_request) for _ in range(500)]
            results = [future.result() for future in as_completed(futures)]

        # Analyze results
        response_times = [r["response_time"] for r in results]
        successful_requests = [r for r in results if r["status_code"] == 200]

        avg_response_time = statistics.mean(response_times)
        median_response_time = statistics.median(response_times)
        p95_response_time = statistics.quantiles(response_times, n=20)[18]
        success_rate = len(successful_requests) / len(results)

        print(f"Stress Test Results:")
        print(f"Total Requests: {len(results)}")
        print(f"Success Rate: {success_rate:.%}")
        print(f"Average Response Time: {avg_response_time:.f}s")
        print(f"Median Response Time: {median_response_time:.f}s")
        print(f"95th Percentile: {p95_response_time:.f}s")

        assert success_rate > 0.85  # 85% success rate under stress
        assert avg_response_time < 3.0  # 3 seconds average under stress
        assert p95_response_time < 8.0  # 8 seconds for 95th percentile

    def test_memory_leak_detection(self):
        #Test for potential memory leaks during extended operation
        response_times = []

        # Make requests over extended period
        for i in range(100):
            start_time = time.time()
            response = requests.get(
                f"{self.base_url}/users",
                headers=self.headers
            )
            end_time = time.time()
            response_times.append(end_time - start_time)
            time.sleep(0.1)

        # Check if response times are degrading over time
        first_quarter = response_times[:25]
        last_quarter = response_times[-25:]

        first_quarter_avg = statistics.mean(first_quarter)
        last_quarter_avg = statistics.mean(last_quarter)

        # Response time shouldn't degrade significantly
        degradation_ratio = last_quarter_avg / first_quarter_avg
        assert degradation_ratio < 1.5

    def test_rapid_user_creation_deletion(self):
        #Test rapid creation and deletion of users
        created_users = []

        def create_and_delete_user(user_id):
            try:
                # Create user
                user_data = {
                    "first_name": f"StressUser{user_id}",
                    "last_name": "Test",
                    "email": f"stress.user.{user_id}@techcorp.com",
                    "department": "IT",
                    "title": "Stress Test Engineer"
                }

                create_response = requests.post(
                    f"{self.base_url}/users",
                    json=user_data,
                    headers=self.headers
                )

                if create_response.status_code == 201:
                    user_id = create_response.json()["id"]
                    created_users.append(user_id)

                    # Immediately delete
                    delete_response = requests.delete(
                        f"{self.base_url}/users/{user_id}",
                        headers=self.headers
                    )

                    return {
                        "create_status": create_response.status_code,
                        "delete_status": delete_response.status_code,
                        "success": create_response.status_code == 201 and delete_response.status_code == 204
                    }

                return {"create_status": create_response.status_code, "success": False}

            except Exception as e:
                return {"error": str(e), "success": False}

        # Run 100 rapid create/delete operations
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(create_and_delete_user, i) for i in range(100)]
            results = [future.result() for future in as_completed(futures)]

        successful_operations = [r for r in results if r.get("success", False)]
        success_rate = len(successful_operations) / len(results)

        print(f"Rapid Create/Delete Results:")
        print(f"Success Rate: {success_rate:.2%}")
        print(f"Successful Operations: {len(successful_operations)}/100")

        assert success_rate > 0.90