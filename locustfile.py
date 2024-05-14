import logging
import uuid
from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.register()

    def on_stop(self):
        self.client.get("logout/")

    def register(self):
        """ Registers a new user """
        self.unique_username = f"user_{uuid.uuid4().hex[:8]}"
        self.password = "testpass09037"
        self.email = f"{self.unique_username}@example.com"

        response = self.client.get("register/")
        csrf_token = self._get_csrf_token(response)
        if csrf_token:
            register_data = {
                "username": self.unique_username,
                "Name": "New User",
                "email": self.email,
                "password1": self.password,
                "password2": self.password,
                "csrfmiddlewaretoken": csrf_token
            }
            headers = {'Referer': self.host + '/register/'}
            register_response = self.client.post(
                "register/", data=register_data, headers=headers)
            logging.info(
                f"Registration attempt for {self.unique_username} - Status: {register_response.status_code}")
            if register_response.status_code == 302:
                self.client.post(
                    '/login/', data=register_data, headers=headers)

    @task
    def members(self):
        """ Accesses the members page """
        members_response = self.client.get("members/")
        logging.info(
            f"Members page request - Status: {members_response.status_code}")

    def _get_csrf_token(self, response):
        """ Extract CSRF token from the response """
        return response.cookies.get('csrftoken', None)
