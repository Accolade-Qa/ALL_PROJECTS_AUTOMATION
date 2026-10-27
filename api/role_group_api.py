"""API operations used by common and ATCU role-group pages."""

from .api_service import APIService


GET_ROLE_GROUPS = "/roleGroup/getRolesGroup?page=0&size=1000&search="
GET_ATCU_ROLE_GROUPS = "/api/roleGroup/fetchRoleGroup"
DELETE_ROLE_GROUP = "/roleGroup/deleteRoleGroup?id={group_id}"
DELETE_ATCU_ROLE_GROUP = "/api/userRole/userRoleDelete?userRole={user_role}"


class RoleGroupAPI(APIService):
    def get_role_groups(self):
        return self._client.get(GET_ROLE_GROUPS)

    def delete_role_group(self, group_id):
        endpoint = DELETE_ROLE_GROUP.format(group_id=group_id)
        return self._client.delete(endpoint)

    def delete_role_groups(self):
        total, failed_ids = self._delete_items(
            self.get_role_groups(),
            self.delete_role_group,
            "group",
        )
        return {
            "success": not failed_ids,
            "total_groups_processed": total,
            "failed_group_ids": failed_ids,
        }

    def get_atcu_role_groups(self):
        return self._client.get(GET_ATCU_ROLE_GROUPS)

    def delete_atcu_role_group(self, user_role):
        endpoint = DELETE_ATCU_ROLE_GROUP.format(user_role=user_role)
        return self._client.delete(endpoint)

    def delete_atcu_role_groups(self):
        total, failed_ids = self._delete_items(
            self.get_atcu_role_groups(),
            self.delete_atcu_role_group,
            "group",
        )
        return {
            "success": not failed_ids,
            "total_groups_processed": total,
            "failed_group_ids": failed_ids,
        }
