import requests

from src.utils.logger import logger


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        self.session.headers.update({"x-api-key": "reqres-free-v1"})
        logger.info(f"APIClient initialized: {self.base_url}")

    def get_user(self, path, user_id):
        url = f"{self.base_url}{path}{user_id}"
        logger.info(f"GET {url}")
        resp = self.session.get(url)
        logger.info(f"Response {resp.status_code}")
        return resp

    def post(self, path, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        logger.info(f"POST {url} | Payload: {kwargs.get('json')}")
        resp = self.session.post(url, **kwargs)
        logger.info(f"Response {resp.status_code}")
        return resp
