from utils.logger import get_logger
from .endpoints import GET_USER_DETAILS

logger = get_logger(__name__)


class UserAPI:
    """User profile API operations."""

    def __init__(self, client=None):
        self._client = client

    def get_user_data_by_id(self=None, user_id=None, *args, **kwargs):
        """Fetch user profile data by ID."""
        if not isinstance(self, UserAPI):
            from .api_client import APIClient
            return APIClient.get_default().user.get_user_data_by_id(user_id, *args, **kwargs)

        for a in args:
            if isinstance(a, (int, str)) and not hasattr(a, "request"):
                user_id = a
                break

        if user_id is None:
            user_id = self._client.get_user_id()

        endpoint = GET_USER_DETAILS.format(id=user_id)
        response = self._client.get(endpoint)
        return response.get("data", {})
