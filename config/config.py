import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(dotenv_path=ROOT.parent / ".env")


def _get_project():
    """Resolve the project before loading its project-specific files."""
    for index, argument in enumerate(sys.argv):
        if argument == "--project" and index + 1 < len(sys.argv):
            return sys.argv[index + 1].lower()
        if argument.startswith("--project="):
            return argument.split("=", 1)[1].lower()

    return os.getenv("PROJECT", "lct").lower()


PROJECT = _get_project()
PROJECT_ENV_PATH = ROOT / f"{PROJECT}.env"
if PROJECT_ENV_PATH.exists():
    load_dotenv(dotenv_path=PROJECT_ENV_PATH, override=True)

PROJECT_CONFIG_PATH = ROOT / f"{PROJECT}.yaml" 

_PROJECT_CONFIG = {}
if PROJECT_CONFIG_PATH.exists():
    with PROJECT_CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        _PROJECT_CONFIG = yaml.safe_load(config_file) or {}


def _get(key, default=None):
    env_val = os.getenv(key)
    if env_val is not None and str(env_val).strip() != "":
        return env_val

    project_value = _PROJECT_CONFIG.get(key.lower())
    if project_value is not None:
        return project_value

    return default



def _get_bool(key, default=False):
    env_value = os.getenv(key)
    if env_value is not None:
        return str(env_value).lower() == "true"

    project_value = _PROJECT_CONFIG.get(key.lower())
    if isinstance(project_value, bool):
        return project_value
    if project_value is not None:
        return str(project_value).lower() == "true"

    return default


BASE_URL = _get("BASE_URL")
USERNAME = _get("USERNAME", _get("APP_USERNAME"))
PASSWORD = _get("PASSWORD", _get("APP_PASSWORD"))
LOGIN_USER = _get("LOGIN_USER", USERNAME)
VALID_UID = _get("VALID_UID")
VALID_UIN = _get("VALID_UIN")
COMMAND_TO_SEARCH = _get("COMMAND_TO_SEARCH")
VIN = _get("VIN")
ICCID = _get("ICCID")
TICKET_BASE_URL = _get(
    "TICKET_BASE_URL", "https://aepl-tcu4g-qa.accoladeelectronics.com:6109"
)
TICKET_USERNAME = _get("TICKET_USERNAME", _get("APP_USERNAME"))
TICKET_PASSWORD = _get("TICKET_PASSWORD", _get("APP_PASSWORD"))
BROWSER = _get("BROWSER", "chromium")
HEADLESS = _get_bool("HEADLESS", True)
SCREENSHOT_ON_FAILURE = _get_bool("SCREENSHOT_ON_FAILURE", True)
LOG_LEVEL = _get("LOG_LEVEL", "INFO")
VIDEO_RECORDING = _get_bool("VIDEO_RECORDING", False)
INVALID_USERNAME = _get("INVALID_USERNAME", "ABCD")
INVALID_PASSWORD = _get("INVALID_PASSWORD", "12345")
API_USERNAME = _get("API_USERNAME", _get("APP_USERNAME", USERNAME))
API_PASSWORD = _get("API_PASSWORD", _get("APP_PASSWORD", PASSWORD))
CUSTOMER = _get("CUSTOMER", "Accolade")
# Compute a sensible default page title per-project when not provided in YAML or env
_project_page_title = _PROJECT_CONFIG.get("page_title")
if _project_page_title:
    PAGE_TITLE = _get("PAGE_TITLE", _project_page_title)
else:
    # Use a project-specific display name: keep legacy 'LCT-A4G' for 'lct',
    # otherwise capitalize the project key (e.g., 'sampark' -> 'Sampark').
    display_name = (
        PROJECT.upper() + " a4g - tarang" if PROJECT == "lct" else PROJECT.capitalize()
    )
    PAGE_TITLE = _get("PAGE_TITLE", f"AEPL {display_name} QA Diagnostic Cloud")
IMEI = _get("IMEI", "866677075606341")


# -----------------------------------------------
#               URLs
# -----------------------------------------------
DASHBOARD_URL = _get(
    "DASHBOARD_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/device-dashboard-page",
)
SIM_DATA_DETAILS_URL = _get(
    "SIM_DATA_DETAILS_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/sensorise-sim-data-details",
)
ROLE_MANAGEMENT_URL = _get(
    "ROLE_MANAGEMENT_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/user-role",
)
ROLE_GROUP_URL = _get(
    "ROLE_GROUP_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/role-group",
)
DEVICE_DETAILS_URL = _get(
    "DEVICE_DETAILS_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/device-details",
)
OTA_URL = _get(
    "OTA_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/ota-batch-page",
)
PRODUCTION_PAGE_URL = _get(
    "PRODUCTION_PAGE_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/production-device-page",
)
CREATE_PRODUCTION_URL = _get(
    "CREATE_PRODUCTION_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/create-production-device",
)
ADD_PRODUCTION_URL = _get(
    "ADD_PRODUCTION_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/add-production-device",
)
USER_MANAGEMENT_URL = _get(
    "USER_MANAGEMENT_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/user-tab",
)
API_BASE_URL = _get(
    "API_BASE_URL",
    "http://lct-a4g-qa.accoladeelectronics.com:9090",
)
API_LOGIN_ENDPOINT = _get("API_LOGIN_ENDPOINT", "/users/login")
GOVERNMENT_SERVERS_URL = _get(
    "GOVERNMENT_SERVERS_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/govt-servers",
)
DISPATCHED_DEVICE_URL = _get(
    "DISPATCHED_DEVICE_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/dispatch-device-page",
)
PROFILE_URL = _get(
    "PROFILE_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/profile",
)
CUSTOMER_MASTER_URL = _get(
    "CUSTOMER_MASTER_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/customer-master",
)
MODEL_URL = _get(
    "MODEL_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/model",
)
CREATE_NEW_MODEL = _get(
    "CREATE_NEW_MODEL",
    "http://lct-a4g-qa.accoladeelectronics.com/model-firmware",
)
UPDATE_MODEL = _get(
    "UPDATE_MODEL",
    "http://lct-a4g-qa.accoladeelectronics.com/model-firmware/11",
)
TICKET_DASHBOARD_URL = _get(
    "TICKET_DASHBOARD_URL",
    "https://aepl-tcu4g-qa.accoladeelectronics.com/ticket-dashboard-page",
)
MY_AIS_TICKET_URL = _get(
    "MY_AIS_TICKET_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/my-ais-ticket",
)
FOTA_URL = _get(
    "FOTA_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/fota",
)
TML_REQUEST_LOG_URL = _get(
    "TML_REQUEST_LOG_URL",
    "https://aepl-tcu4g-qa.accoladeelectronics.com/ais140-api-req-logs",
)
AEPL_RESPONSE_LOG_URL = _get(
    "AEPL_RESPONSE_LOG_URL",
    "https://aepl-tcu4g-qa.accoladeelectronics.com/ais140-api-res-logs",
)
STATUS_UPDATE_LOG_URL = _get(
    "STATUS_UPDATE_LOG_URL",
    "https://aepl-tcu4g-qa.accoladeelectronics.com/ais140-tml-api-logs",
)

DEALER_FOTA_URL = _get(
    "DEALER_FOTA_URL", "https://aepl-tcu4g-qa.accoladeelectronics.com/dealer-fota",
)

DEVICE_STATE_CONFIG_URL = _get(
    "DEVICE_STATE_CONFIG_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/device-state-config",
)
DEVICE_VIN_CONFIG_URL = _get(
    "DEVICE_VIN_CONFIG_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/device-vin-config",
)
DEVICE_ACTIVITY_LOG_URL = _get(
    "DEVICE_ACTIVITY_LOG_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/device-activity-log",
)

CREATE_NEW_OTA_BATCH = _get(
    "CREATE_NEW_OTA_BATCH",
    "https://aepl-tcu4g-qa.accoladeelectronics.com/ota-batch-create",
)

MANUAL_OTA_URL = _get(
    "MANUAL_OTA_URL",
    "https://aepl-tcu4g-qa.accoladeelectronics.com/manual-ota",
)
# Expected permission counts per project (can be overridden in project YAML)
EXPECTED_PERMISSION_COUNT = int(_get("EXPECTED_PERMISSION_COUNT", 16))
