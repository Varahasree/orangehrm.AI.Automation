
import requests

from config.config import API_BASE_URL, API_TIMEOUT


class APIClient:
    def __init__(
        self,
        base_url=API_BASE_URL,
        timeout=API_TIMEOUT,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )

    def post(self, endpoint, json=None, headers=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.post(
            url,
            json=json,
            headers=headers,
            timeout=self.timeout,
        )

    def close(self):
        self.session.close()

