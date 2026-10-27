"""API operations used by the role-management page."""

from .api_service import APIService


GET_ROLES = "/roles/getRoles?page=0&size=1000&search=&userRole="
DELETE_ROLE = "/roles/deleteRole?roleId={role_id}"


class RoleManagementAPI(APIService):
    def get_roles(self):
        return self._client.get(GET_ROLES)

    def delete_role(self, role_id):
        endpoint = DELETE_ROLE.format(role_id=role_id)
        return self._client.delete(endpoint)

    def delete_roles(self):
        total, failed_ids = self._delete_items(
            self.get_roles(),
            self.delete_role,
            "role",
        )
        return {
            "success": not failed_ids,
            "total_roles_processed": total,
            "failed_role_ids": failed_ids,
        }
