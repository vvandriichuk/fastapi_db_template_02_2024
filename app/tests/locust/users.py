from locust import HttpUser, task, between

JWT_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJicm9rZXJzX2hhbmRsZXIifQ.8yYsLq3TAKWafayMYMEc4D12KM59sUPTSX4M-i-Fw_k'


class UserBehavior(HttpUser):
    wait_time = between(1, 2)

    @task
    def get_users(self):
        self.client.get("/api/v1/users", headers={"Authorization": f"Bearer {JWT_TOKEN}"})

    @task
    def add_user(self):
        new_user = {"username": "testuser", "email": "test@example.com", "password": "testpassword"}
        self.client.post("/api/v1/users", json=new_user, headers={"Authorization": f"Bearer {JWT_TOKEN}"})
