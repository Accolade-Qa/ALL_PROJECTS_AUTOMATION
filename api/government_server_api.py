"""API operations used by the government-server page."""

from .api_service import APIService


GET_ALL_STATE_SERVERS = (
    "/stateServers/getAllStateServerList?page=0&size=1000&search=&userId={user_id}"
)
GET_ALL_FIRMWARES = (
    "/firmwareMaster/getAllFirmwareList?page=0&size=1000&search=&firmwareType="
)
GET_STATE_FIRMWARES = (
    "/firmwareMaster/getStateFirmwares?page=0&size=1000&search="
    "&firmwareType={firmware_type}&userId={user_id}&stateServerId={state_server_id}"
)
GET_FIRMWARES_NOT_ADDED_IN_STATE = (
    "/firmwareMaster/getFirmwaresListNotAddedInState?page=0&size=1000&search="
    "&firmwareType={firmware_type}&stateServerId={state_server_id}"
)
GET_STATE_SERVER_DETAILS = "/stateServers/getStateServerDetails?id={server_id}"


class GovtServerAPI(APIService):
    def _get_all_servers(self):
        user_id = self._client.get_user_id()
        endpoint = GET_ALL_STATE_SERVERS.format(user_id=user_id)
        servers = self._client.get(endpoint).get("data", [])
        if not servers:
            raise ValueError("No servers found in API response")
        return servers, user_id

    def _get_server_id(self, state_name=None):
        servers, _ = self._get_all_servers()
        if state_name is None:
            return servers[0].get("id")

        server = next(
            (item for item in servers if item.get("state") == state_name),
            None,
        )
        if server is None:
            raise ValueError(f"No server found with state name: {state_name}")
        return server.get("id")

    def get_all_firmware(self):
        return self._client.get(GET_ALL_FIRMWARES).get("data", [])

    def _get_firmwares(self, firmware_type, added_to_state, state_server_id=None):
        if state_server_id is None:
            state_server_id = self._get_server_id()
        user_id = self._client.get_user_id() if added_to_state else None

        if added_to_state:
            endpoint = GET_STATE_FIRMWARES.format(
                firmware_type=firmware_type,
                user_id=user_id,
                state_server_id=state_server_id,
            )
        else:
            endpoint = GET_FIRMWARES_NOT_ADDED_IN_STATE.format(
                firmware_type=firmware_type,
                state_server_id=state_server_id,
            )
        return self._client.get(endpoint).get("data", [])

    def get_oc_firmwares_not_added(self):
        return self._get_firmwares("OC", added_to_state=False)

    def get_oc_firmwares_added_in_state(self, state_name=None, state_server_id=None):
        server_id = state_server_id or self._get_server_id(state_name)
        return self._get_firmwares("OC", True, server_id)

    def get_d_firmwares_not_added(self):
        return self._get_firmwares("D", added_to_state=False)

    def get_d_firmwares_added_in_state(self, state_server_id=None):
        return self._get_firmwares("D", True, state_server_id)

    def _get_state_server_details(self, server_id):
        endpoint = GET_STATE_SERVER_DETAILS.format(server_id=server_id)
        details = self._client.get(endpoint).get("data", {})
        return (
            details,
            self.get_oc_firmwares_not_added(),
            self.get_d_firmwares_not_added(),
        )

    def get_state_server_details_by_name(self, state_name):
        return self._get_state_server_details(self._get_server_id(state_name))

    def get_state_server_details_by_id(self, server_id=None):
        server_id = server_id or self._get_server_id()
        return self._get_state_server_details(server_id)
