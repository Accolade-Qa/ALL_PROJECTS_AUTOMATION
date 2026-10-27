"""Shared HTTP client for feature-specific API services."""

import requests

from config import config
from .atcu.ota_page_api import AtcuOtaPageAPI
from .customer_api import CustomerAPI
from .device_dashboard_api import DeviceDashboardAPI
from .government_server_api import GovtServerAPI
from .role_group_api import RoleGroupAPI
from .role_management_api import RoleManagementAPI
from .sim_batch_api import SIMBatchAPI
from .tml_request_api import TmlRequestAPI
from .user_api import UserAPI


LOGIN = "/users/login"


class APIClient:
    """Owns authentication, HTTP requests, and page-specific API services."""

    def __init__(self, base_url=None, username=None, password=None):
        self.base_url = (base_url or config.API_BASE_URL).rstrip("/")
        self.username = username or config.API_USERNAME
        self.password = password or config.API_PASSWORD
        self.session = requests.Session()
        self.token = None
        self.user_id = None

        self.customer = CustomerAPI(self)
        self.dashboard = DeviceDashboardAPI(self)
        self.govt_server = GovtServerAPI(self)
        self.role_group = RoleGroupAPI(self)
        self.role_management = RoleManagementAPI(self)
        self.sim_batch = SIMBatchAPI(self)
        self.tml = TmlRequestAPI(self)
        self.user = UserAPI(self)
        self.ota = AtcuOtaPageAPI(self)

    def _build_url(self, endpoint):
        if endpoint.startswith("http"):
            return endpoint

        endpoint = "/" + endpoint.lstrip("/")
        if "sampark-qa" in self.base_url.lower() and not endpoint.startswith("/api/"):
            endpoint = "/api" + endpoint
        return self.base_url + endpoint

    @staticmethod
    def _parse_response(response):
        response.raise_for_status()
        return response.json() if response.text else {}

    def login(self, username=None, password=None):
        """Log in, save authentication headers, and return login data."""
        self.username = username or self.username
        self.password = password or self.password

        endpoint = getattr(config, "API_LOGIN_ENDPOINT", LOGIN)
        response = self.session.post(
            self._build_url(endpoint),
            json={"userEmail": self.username, "password": self.password},
            timeout=20,
        )
        response.raise_for_status()

        result = response.json()
        login_data = result.get("data") or {}
        self.token = login_data.get("token") or result.get("token")
        self.user_id = login_data.get("id")
        if not self.token:
            raise ValueError("API login response did not contain an authentication token")

        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.token}",
                "token": self.token,
                "Content-Type": "application/json",
            }
        )
        return login_data

    def request(self, method, endpoint, **kwargs):
        """Send an authenticated request and retry once after an expired token."""
        if not self.token:
            self.login()

        url = self._build_url(endpoint)
        kwargs.setdefault("timeout", 25)
        if kwargs.get("files"):
            kwargs["headers"] = {
                "Authorization": self.session.headers["Authorization"],
                "token": self.token,
            }

        for attempt in range(2):
            response = getattr(self.session, method)(url, **kwargs)
            if response.status_code != 401 or attempt == 1:
                return self._parse_response(response)

            self.login()
            if kwargs.get("files"):
                kwargs["headers"] = {
                    "Authorization": self.session.headers["Authorization"],
                    "token": self.token,
                }

    def get(self, endpoint, params=None):
        return self.request("get", endpoint, params=params)

    def post(self, endpoint, json=None, data=None, files=None):
        return self.request(
            "post",
            endpoint,
            json=json,
            data=data,
            files=files,
        )

    def delete(self, endpoint):
        return self.request("delete", endpoint)

    def get_user_id(self):
        if self.user_id is None:
            self.login()
        return self.user_id
