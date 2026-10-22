from utils.logger import get_logger
from .endpoints import DELETE_ROLE, GET_ROLES

logger = get_logger(__name__)


class RoleManagementAPI:
    """Role management API operations."""

    def __init__(self, client=None):
        self._client = client

    def get_roles(self=None, *args, **kwargs):
        """Fetch all roles."""
        if not isinstance(self, RoleManagementAPI):
            from .api_client import APIClient
            return APIClient.get_default().role_management.get_roles(*args, **kwargs)

        return self._client.get(GET_ROLES)

    def delete_role(self=None, role_id=None, *args, **kwargs):
        """Delete role by ID."""
        if not isinstance(self, RoleManagementAPI):
            from .api_client import APIClient
            return APIClient.get_default().role_management.delete_role(role_id, *args, **kwargs)

        for a in args:
            if isinstance(a, (int, str)) and not hasattr(a, "request"):
                role_id = a
                break
        endpoint = DELETE_ROLE.format(role_id=role_id)
        return self._client.delete(endpoint)

    def delete_roles(self=None, *args, **kwargs):
        """Attempt to delete roles."""
        if not isinstance(self, RoleManagementAPI):
            from .api_client import APIClient
            return APIClient.get_default().role_management.delete_roles(*args, **kwargs)

        response = self.get_roles()
        total_roles = response.get("totalItems", 0)
        for i in range(1, total_roles + 1):
            try:
                self.delete_role(i)
            except Exception as e:
                if "Cannot delete role" in str(e):
                    continue
        return {"success": True, "total_roles_processed": total_roles}
