"""Central API Client that orchestrates requests to page-specific API modules."""

import requests
import urllib3
from utils.logger import get_logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = get_logger(__name__)


class APIClient:
    """Central API client that orchestrates requests to page-specific API modules.

    Usage in tests:
        api = APIClient()
        customers = api.customer.get_customer_list()
        counts = api.dashboard.get_device_counts()
        firmwares = api.govt_server.get_all_firmware()
        user_info = api.user.get_user_data_by_id()
    """

    _default_instance = None

    def __init__(self, base_url=None, username=None, password=None):
        from config import config

        self.base_url = (base_url or getattr(config, "API_BASE_URL", "")).rstrip("/")
        self.username = username or getattr(config, "API_USERNAME", "")
        self.password = password or getattr(config, "API_PASSWORD", "")
        self.token = None
        self.user_id = None

        self.session = requests.Session()
        self.session.verify = False

        # Page-specific API modules orchestrated here
        from .customer_api import CustomerAPI
        from .device_dashboard_api import DeviceDashboardAPI
        from .government_server_api import GovtServerAPI
        from .login_api import LoginAPI
        from .role_group_api import RoleGroupAPI
        from .role_management_api import RoleManagementAPI
        from .sim_batch_api import SIMBatchAPI
        from .tml_request_api import TmlRequestAPI
        from .user_api import UserAPI
        from .atcu.ota_page_api import AtcuOtaPageAPI

        self.customer = CustomerAPI(self)
        self.dashboard = DeviceDashboardAPI(self)
        self.device_dashboard = self.dashboard  # convenient alias
        self.govt_server = GovtServerAPI(self)
        self.login_api = LoginAPI(self)
        self.role_group = RoleGroupAPI(self)
        self.role_management = RoleManagementAPI(self)
        self.sim_batch = SIMBatchAPI(self)
        self.tml = TmlRequestAPI(self)
        self.user = UserAPI(self)
        self.ota = AtcuOtaPageAPI(self)

    @classmethod
    def get_default(cls):
        """Get or create shared default client instance."""
        if cls._default_instance is None:
            cls._default_instance = cls()
        return cls._default_instance

    def _build_url(self, endpoint):
        endpoint = str(endpoint).strip()
        if endpoint.startswith("http"):
            return endpoint
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        if "sampark-qa" in self.base_url.lower() and not endpoint.startswith("/api/"):
            endpoint = f"/api{endpoint}"
        return f"{self.base_url}{endpoint}"

    def login(self):
        """Authenticate and set Bearer token on the session."""
        from config import config

        login_endpoint = getattr(config, "API_LOGIN_ENDPOINT", "/users/login")
        url = self._build_url(login_endpoint)
        payload = {"userEmail": self.username, "password": self.password}

        logger.info("Logging in to API as %s", self.username)
        response = self.session.post(url, json=payload, timeout=20)
        if not response.ok:
            raise Exception(f"API Login failed [{response.status_code}]: {response.text}")

        data = response.json()
        token = data.get("data", {}).get("token") or data.get("token")
        self.user_id = data.get("data", {}).get("id")
        self.token = token
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "token": self.token,
            "Content-Type": "application/json",
        })
        return data.get("data", {})

    def get_user_id(self):
        """Get ID of the logged in user."""
        if not self.user_id:
            self.login()
        return self.user_id

    def get(self, endpoint, params=None):
        """Send GET request."""
        if not self.token:
            self.login()
        url = self._build_url(endpoint)
        response = self.session.get(url, params=params, timeout=25)
        if response.status_code == 401:
            self.login()
            response = self.session.get(url, params=params, timeout=25)
        return response.json() if response.text else {}

    def post(self, endpoint, json=None, data=None, files=None):
        """Send POST request."""
        if not self.token:
            self.login()
        url = self._build_url(endpoint)
        headers = None
        if files:
            headers = {"Authorization": f"Bearer {self.token}", "token": self.token}
        response = self.session.post(url, json=json, data=data, files=files, headers=headers, timeout=25)
        if response.status_code == 401:
            self.login()
            response = self.session.post(url, json=json, data=data, files=files, headers=headers, timeout=25)
        return response.json() if response.text else {}

    def delete(self, endpoint):
        """Send DELETE request."""
        if not self.token:
            self.login()
        url = self._build_url(endpoint)
        response = self.session.delete(url, timeout=25)
        if response.status_code == 401:
            self.login()
            response = self.session.delete(url, timeout=25)
        return response.json() if response.text else {}

    # Backward compatibility helpers
    @classmethod
    def send_request(cls, *args, **kwargs):
        inst = cls.get_default()
        endpoint = args[0] if (args and isinstance(args[0], str)) else (args[5] if len(args) >= 6 else kwargs.get("endpoint", ""))
        method = args[1] if (args and len(args) > 1 and isinstance(args[1], str)) else (args[4] if len(args) >= 6 else kwargs.get("method", "GET"))
        if method.upper() == "GET":
            return inst.get(endpoint)
        elif method.upper() == "POST":
            return inst.post(endpoint, json=kwargs.get("json", kwargs.get("data")), files=kwargs.get("files"))
        elif method.upper() == "DELETE":
            return inst.delete(endpoint)
        return inst.get(endpoint)

    @classmethod
    def build_endpoint(cls, base_url, endpoint):
        return cls.get_default()._build_url(endpoint)

    @classmethod
    def resolve_api_credentials(cls, page=None, api_base_url=None, api_username=None, api_password=None):
        inst = cls.get_default()
        return inst.base_url, inst.username, inst.password
