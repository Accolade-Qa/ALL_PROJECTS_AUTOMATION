from utils.logger import get_logger

logger = get_logger(__name__)


class LoginAPI:
    """User login API operations."""

    def __init__(self, client=None):
        self._client = client

    def login(self=None, username=None, password=None, *args, **kwargs):
        """Authenticate and obtain login response data."""
        if not isinstance(self, LoginAPI):
            from .api_client import APIClient
            return APIClient.get_default().login_api.login(username, password, *args, **kwargs)

        if isinstance(username, str):
            self._client.username = username
        if isinstance(password, str):
            self._client.password = password

        return self._client.login()
