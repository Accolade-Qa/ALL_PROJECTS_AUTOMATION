"""API operations used by the user profile and user-management pages."""

from .api_service import APIService


GET_USER_DETAILS = "/users/getUserdetails?id={id}"


class UserAPI(APIService):
    def get_user_data_by_id(self, user_id=None):
        user_id = user_id or self._client.get_user_id()
        endpoint = GET_USER_DETAILS.format(id=user_id)
        return self._client.get(endpoint).get("data", {})
