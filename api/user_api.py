"""API operations used by the user profile and user-management pages."""

from .api_service import APIService


GET_USER_DETAILS = "/users/getUserdetails?id={id}"
ATCU_GET_USER_DETAILS = "/api/user/fetchUserDetailById?id={id}"


class UserAPI(APIService):
    def get_user_data_by_id(self, user_id=None):
        user_id = user_id or self._client.get_user_id()
        for endpoint_pattern in (ATCU_GET_USER_DETAILS, GET_USER_DETAILS):
            try:
                endpoint = endpoint_pattern.format(id=user_id)
                res = self._client.get(endpoint)
                data = res.get("data", {})
                if isinstance(data, list) and data:
                    return data[0]
                if isinstance(data, dict) and data:
                    return data
            except Exception:
                continue
        return {}
