import requests

from src.config.config import settings
from src.logs.config import logger


class SpaceXAPIClient:
    def __init__(self):
        self.base_urls = settings.SPACEX_API_BASE_URL
        self.default_api_versions = settings.SPACEX_API_VERSION
        self.api_versions = {
            "launches": "v5"
        }

    def get_url_for_endpoint(self, endpoint: str) -> str:
        version = self.api_versions.get(endpoint, self.default_api_versions)
        return f"{self.base_urls}{version}/{endpoint}"

    def fetch_data_by_endpoint(self, endpoint):
        url = f"{self.get_url_for_endpoint(endpoint)}"
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"Error fetching data from {url}")
            raise Exception(f"Error fetching data from {url}")
        logger.info(f"Successfully fetched data from {url}")
        data = response.json()
        return data

    def fetch_data_by_endpoint_and_id(self, endpoint, id):
        if id:
            return self.fetch_data_by_endpoint(f"{endpoint}/{id}")

    def fetch_all_or_id_by_endpoint(self, endpoint, id=None):
        if id:
            return self.fetch_data_by_endpoint(f"{endpoint}/{id}")
        return self.fetch_data_by_endpoint(endpoint)

    def fetch_all_by_endpoint_list(self, endpoints):
        return [{endpoint: self.fetch_data_by_endpoint(endpoint)} for endpoint in endpoints]
