from utils.logger import get_logger
from .endpoints import (
    GET_ALL_FIRMWARES,
    GET_ALL_STATE_SERVERS,
    GET_FIRMWARES_NOT_ADDED_IN_STATE,
    GET_STATE_FIRMWARES,
    GET_STATE_SERVER_DETAILS,
)

logger = get_logger(__name__)


class GovtServerAPI:
    """Government server and firmware API operations."""

    def __init__(self, client=None):
        self._client = client

    def _get_all_servers_list(self=None, *args, **kwargs):
        if not isinstance(self, GovtServerAPI):
            from .api_client import APIClient
            return APIClient.get_default().govt_server._get_all_servers_list(*args, **kwargs)

        user_id = self._client.get_user_id()
        endpoint = GET_ALL_STATE_SERVERS.format(user_id=user_id)
        response = self._client.get(endpoint)
        servers = response.get("data", [])
        if not servers:
            raise ValueError("No servers found in API response")
        server_id = servers[0].get("id")
        return servers, server_id, user_id

    def get_all_firmware(self=None, *args, **kwargs):
        """Fetch all firmware versions."""
        if not isinstance(self, GovtServerAPI):
            from .api_client import APIClient
            return APIClient.get_default().govt_server.get_all_firmware(*args, **kwargs)

        response = self._client.get(GET_ALL_FIRMWARES)
        return response.get("data", [])

    def _get_firmwares_by_type(self, firmware_type="OC", added_in_state=False, state_server_id=None):
        if state_server_id is None:
            _, state_server_id, user_id = self._get_all_servers_list()
        else:
            user_id = self._client.get_user_id()

        if added_in_state:
            endpoint = GET_STATE_FIRMWARES.format(
                firmware_type=firmware_type, user_id=user_id, state_server_id=state_server_id
            )
        else:
            endpoint = GET_FIRMWARES_NOT_ADDED_IN_STATE.format(
                firmware_type=firmware_type, state_server_id=state_server_id
            )
        response = self._client.get(endpoint)
        return response.get("data", [])

    def get_oc_firmwares_not_added(self=None, *args, **kwargs):
        """Fetch OC firmware list not added."""
        if not isinstance(self, GovtServerAPI):
            from .api_client import APIClient
            return APIClient.get_default().govt_server.get_oc_firmwares_not_added(*args, **kwargs)

        return self._get_firmwares_by_type("OC", added_in_state=False)

    def get_oc_firmwares_added_in_state(self=None, state_name=None, *args, **kwargs):
        """Fetch OC firmware list added in state."""
        if not isinstance(self, GovtServerAPI):
            from .api_client import APIClient
            return APIClient.get_default().govt_server.get_oc_firmwares_added_in_state(state_name, *args, **kwargs)

        for a in args:
            if isinstance(a, str):
                state_name = a
                break

        state_server_id = kwargs.get("state_server_id")
        if state_name and not state_server_id:
            servers, _, _ = self._get_all_servers_list()
            match = next((s for s in servers if s.get("state") == state_name), None)
            if match:
                state_server_id = match.get("id")

        return self._get_firmwares_by_type("OC", added_in_state=True, state_server_id=state_server_id)

    def get_d_firmwares_not_added(self=None, *args, **kwargs):
        """Fetch D firmware list not added."""
        if not isinstance(self, GovtServerAPI):
            from .api_client import APIClient
            return APIClient.get_default().govt_server.get_d_firmwares_not_added(*args, **kwargs)

        return self._get_firmwares_by_type("D", added_in_state=False)

    def get_d_firmwares_added_in_state(self=None, *args, **kwargs):
        """Fetch D firmware list added in state."""
        if not isinstance(self, GovtServerAPI):
            from .api_client import APIClient
            return APIClient.get_default().govt_server.get_d_firmwares_added_in_state(*args, **kwargs)

        return self._get_firmwares_by_type("D", added_in_state=True)

    def get_state_server_details_by_name(self=None, state_name=None, *args, **kwargs):
        """Fetch state server details by state name."""
        if not isinstance(self, GovtServerAPI):
            from .api_client import APIClient
            return APIClient.get_default().govt_server.get_state_server_details_by_name(state_name, *args, **kwargs)

        for a in args:
            if isinstance(a, str):
                state_name = a
                break

        servers, _, _ = self._get_all_servers_list()
        match = next((s for s in servers if s.get("state") == state_name), None)
        assert match, f"No server found with state name: {state_name}"
        server_id = match.get("id")

        endpoint = GET_STATE_SERVER_DETAILS.format(server_id=server_id)
        details = self._client.get(endpoint).get("data", {})
        oc = self.get_oc_firmwares_not_added()
        d = self.get_d_firmwares_not_added()
        return details, oc, d

    def get_state_server_details_by_id(self=None, server_id=None, *args, **kwargs):
        """Fetch state server details by server ID."""
        if not isinstance(self, GovtServerAPI):
            from .api_client import APIClient
            return APIClient.get_default().govt_server.get_state_server_details_by_id(server_id, *args, **kwargs)

        for a in args:
            if isinstance(a, (int, str)) and not hasattr(a, "request"):
                server_id = a
                break
        if server_id is None:
            _, server_id, _ = self._get_all_servers_list()

        endpoint = GET_STATE_SERVER_DETAILS.format(server_id=server_id)
        details = self._client.get(endpoint).get("data", {})
        oc = self.get_oc_firmwares_not_added()
        d = self.get_d_firmwares_not_added()
        return details, oc, d
