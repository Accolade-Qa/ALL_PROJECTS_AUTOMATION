"""API module entry point."""

from .api_client import APIClient
from .customer_api import CustomerAPI
from .device_dashboard_api import DeviceDashboardAPI
from .government_server_api import GovtServerAPI
from .login_api import LoginAPI
from .role_group_api import RoleGroupAPI
from .role_management_api import RoleManagementAPI
from .sim_batch_api import SIMBatchAPI
from .tml_request_api import TmlRequestAPI, TmlRequestApi
from .user_api import UserAPI
from .atcu.ota_page_api import AtcuOtaPageAPI

# Default instance so you can also import `api`
api = APIClient.get_default()

__all__ = [
    "api",
    "APIClient",
    "CustomerAPI",
    "DeviceDashboardAPI",
    "GovtServerAPI",
    "LoginAPI",
    "RoleGroupAPI",
    "RoleManagementAPI",
    "SIMBatchAPI",
    "TmlRequestAPI",
    "TmlRequestApi",
    "UserAPI",
    "AtcuOtaPageAPI",
]
