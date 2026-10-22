from utils.logger import get_logger
from .endpoints import DELETE_ROLE_GROUP, GET_ROLE_GROUPS

logger = get_logger(__name__)


class RoleGroupAPI:
    """Role group API operations."""

    def __init__(self, client=None):
        self._client = client

    def get_role_groups(self=None, *args, **kwargs):
        """Fetch all role groups."""
        if not isinstance(self, RoleGroupAPI):
            from .api_client import APIClient
            return APIClient.get_default().role_group.get_role_groups(*args, **kwargs)

        return self._client.get(GET_ROLE_GROUPS)

    def delete_role_group(self=None, group_id=None, *args, **kwargs):
        """Delete role group by ID."""
        if not isinstance(self, RoleGroupAPI):
            from .api_client import APIClient
            return APIClient.get_default().role_group.delete_role_group(group_id, *args, **kwargs)

        for a in args:
            if isinstance(a, (int, str)) and not hasattr(a, "request"):
                group_id = a
                break
        endpoint = DELETE_ROLE_GROUP.format(group_id=group_id)
        return self._client.delete(endpoint)

    def delete_role_groups(self=None, *args, **kwargs):
        """Attempt to delete all role groups."""
        if not isinstance(self, RoleGroupAPI):
            from .api_client import APIClient
            return APIClient.get_default().role_group.delete_role_groups(*args, **kwargs)

        response = self.get_role_groups()
        total_roles = response.get("totalItems", 0)
        for i in range(1, total_roles + 1):
            try:
                self.delete_role_group(i)
            except Exception as e:
                if "Cannot delete group" in str(e):
                    continue
        return {"success": True, "total_groups_processed": total_roles}
