"""API operations used by common and ATCU role-group pages."""

from .api_service import APIService


GET_ROLE_GROUPS = "/roleGroup/getRolesGroup?page=0&size=1000&search="
GET_ATCU_ROLE_GROUPS = "/api/roleGroup/fetchRoleGroup"
DELETE_ROLE_GROUP = "/roleGroup/deleteRoleGroup?id={group_id}"
DELETE_ATCU_ROLE_GROUP = "/api/roleGroup/deleteRoleGroup?id={group_id}"


class RoleGroupAPI(APIService):
    def get_role_groups(self):
        try:
            return self._client.get(GET_ROLE_GROUPS)
        except Exception:
            return self.get_atcu_role_groups()

    def delete_role_group(self, group_id):
        try:
            endpoint = DELETE_ROLE_GROUP.format(group_id=group_id)
            return self._client.delete(endpoint)
        except Exception:
            return self.delete_atcu_role_group(group_id)

    def delete_role_groups(self):
        try:
            res = self._client.get(GET_ROLE_GROUPS)
            total, failed_ids = self._delete_items(
                res,
                self.delete_role_group,
                "group",
            )
            return {
                "success": not failed_ids,
                "total_groups_processed": total,
                "failed_group_ids": failed_ids,
            }
        except Exception:
            res = self.get_atcu_role_groups()
            data = res.get("data", [])
            total = len(data)
            failed_ids = []
            for item in data:
                group_id = item.get("_id")
                group_name = item.get("groupName", "")
                if group_name.startswith("Test"):
                    try:
                        self.delete_atcu_role_group(group_id)
                    except Exception:
                        failed_ids.append(group_id)
            return {
                "success": not failed_ids,
                "total_groups_processed": total,
                "failed_group_ids": failed_ids,
            }

    def get_atcu_role_groups(self):
        return self._client.get(GET_ATCU_ROLE_GROUPS)

    def delete_atcu_role_group(self, group_id):
        endpoint = DELETE_ATCU_ROLE_GROUP.format(group_id=group_id)
        return self._client.delete(endpoint)

    def delete_atcu_role_groups(self):
        return self.delete_role_groups()
