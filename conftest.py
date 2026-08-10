import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib
import json
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from pages.atcu.atcu_aepl_response_log_page import AtcuAeplResponseLogPage

import config.config as config_module
from config.global_var import (
    get_project_logs_path,
    get_project_screenshot_path,
    prepare_project_artifact_dirs,
)
from pages.common_base_page import BasePage

# Screenshot directories are created lazily when a failure screenshot is captured.

# Path to cached authenticated storage state to avoid UI login every test
STORAGE_STATE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "storage_state.json"
)

from utils.logger import enable_file_logging, get_logger

logger = get_logger(__name__)

VALID_PROJECTS = ("atcu", "lct", "sampark", "swaraj", "trio", "all")

ZOOM_SCRIPT = """
() => {
    const applyZoom = () => {
        const zoomLevel = '1';

        if (document.documentElement) {
            document.documentElement.style.zoom = zoomLevel;
        }

        if (document.body) {
            document.body.style.zoom = zoomLevel;
        }
    };

    applyZoom();

    new MutationObserver(applyZoom).observe(document.documentElement, {
        childList: true,
        subtree: true
    });
}
"""


# Playwright instance
@pytest.fixture(scope="session")
def playwright_instance():
    logger.info("Starting Playwright session")
    with sync_playwright() as p:
        yield p
    logger.info("Playwright session ended")


# Browser
@pytest.fixture(scope="session")
def browser(playwright_instance, request):
    browser_type = getattr(playwright_instance, config_module.BROWSER)

    cli_headless = request.config.getoption("--headless")
    effective_headless = True if cli_headless else config_module.HEADLESS

    launch_args = []
    if effective_headless:
        launch_args = [
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--window-size=1920,1080",
        ]
    else:
        launch_args = ["--start-maximized"]

    browser = browser_type.launch(
        headless=effective_headless,
        args=launch_args,
    )
    logger.info(
        "Launched browser instance (%s) headless=%s args=%s",
        config_module.BROWSER,
        effective_headless,
        launch_args,
    )

    yield browser
    logger.info("Browser instance closed")


# Context with zoom applied
def _new_context_with_zoom(browser, **kwargs):
    context = browser.new_context(viewport=None)

    context.add_init_script(ZOOM_SCRIPT)
    logger.debug("Created new browser context with zoom applied")
    return context


def pytest_addoption(parser):
    parser.addoption(
        "--iterations",
        action="store",
        default=1,
        type=int,
        help="Number of times to run the loop test",
    )
    parser.addoption(
        "--project",
        action="store",
        default=os.getenv("PROJECT"),
        help="Project name to select the configuration (atcu, lct, sampark, swaraj, trio, all)",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )


def pytest_configure(config):
    if config.getoption("collectonly", default=False) or os.getenv("TEST_RUN_PIPE"):
        return

    cli_project = config.getoption("--project")
    env_project = os.getenv("PROJECT")

    project = cli_project or env_project
    if not project:
        for arg in config.args:
            arg_clean = str(arg).replace("\\", "/").lower()
            for proj in ("atcu", "lct", "sampark", "swaraj", "trio"):
                if f"tests/{proj}/" in arg_clean or f"tests/{proj}" in arg_clean:
                    project = proj
                    break
            if project:
                break

    if not project or project.lower().strip() == "all":
        project = "lct"

    project = project.lower().strip()
    if project not in VALID_PROJECTS:
        raise pytest.UsageError(
            f"Invalid project '{project}'. Must be one of: {', '.join(VALID_PROJECTS)}"
        )

    os.environ["PROJECT"] = project
    importlib.reload(config_module)

    artifact_dirs = prepare_project_artifact_dirs(project=project)
    enable_file_logging(project)
    os.makedirs(get_project_logs_path(project=project), exist_ok=True)
    os.makedirs(get_project_screenshot_path(project=project), exist_ok=True)

    required_configs = ("BASE_URL", "USERNAME", "PASSWORD", "BROWSER")
    missing = [key for key in required_configs if not getattr(config_module, key, None)]
    if missing:
        raise ValueError(
            f"Missing required config values for project '{project}': "
            f"{', '.join(missing)}. Check config/{project}.yaml"
        )

    logger.info("=" * 60)
    logger.info("PYTEST STARTUP - Project Configuration")
    logger.info("=" * 60)
    logger.info("PROJECT: %s", project)
    logger.info("BASE_URL: %s", config_module.BASE_URL)
    logger.info(
        "BROWSER: %s (headless=%s)", config_module.BROWSER, config_module.HEADLESS
    )
    logger.info("=" * 60)


def pytest_collection_modifyitems(config, items):
    if config.getoption("collectonly", default=False) or os.getenv("TEST_RUN_PIPE"):
        return

    cli_project = config.getoption("--project")
    env_project = os.getenv("PROJECT")

    current_project = cli_project or env_project
    if current_project and current_project.lower().strip() == "all":
        return

    if not current_project:
        detected_projects = set()
        for item in items:
            item_path_str = str(item.fspath).replace("\\", "/").lower()
            for proj in ("atcu", "lct", "sampark", "swaraj", "trio"):
                if f"/tests/{proj}/" in item_path_str:
                    detected_projects.add(proj)
        if len(detected_projects) == 1:
            current_project = detected_projects.pop()
        else:
            return

    current_project = current_project.lower().strip()
    project_markers = set(VALID_PROJECTS) - {"all"}

    selected = []
    deselected = []

    for item in items:
        item_markers = {marker.name for marker in item.iter_markers()}
        test_projects = item_markers & project_markers

        item_path_str = str(item.fspath).replace("\\", "/").lower()
        path_project = None
        for proj in ("atcu", "lct", "sampark", "swaraj", "trio"):
            if f"/tests/{proj}/" in item_path_str:
                path_project = proj
                break

        if test_projects:
            if current_project in test_projects:
                selected.append(item)
            else:
                deselected.append(item)
        elif path_project:
            if current_project == path_project:
                selected.append(item)
            else:
                deselected.append(item)
        else:
            selected.append(item)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
    items[:] = selected


@pytest.fixture(scope="session")
def project_config():
    return {
        "project": os.getenv("PROJECT", "lct").lower(),
        "base_url": config_module.BASE_URL,
        "username": config_module.USERNAME,
        "password": config_module.PASSWORD,
        "invalid_username": config_module.INVALID_USERNAME,
        "invalid_password": config_module.INVALID_PASSWORD,
        "dashboard_url": config_module.DASHBOARD_URL,
        "sim_data_details_url": config_module.SIM_DATA_DETAILS_URL,
        "role_management_url": config_module.ROLE_MANAGEMENT_URL,
        "role_group_url": config_module.ROLE_GROUP_URL,
        "device_details_url": config_module.DEVICE_DETAILS_URL,
        "ota_url": config_module.OTA_URL,
        "manual_ota_url" : config_module.MANUAL_OTA_URL,
        "create_new_ota_batch": config_module.CREATE_NEW_OTA_BATCH,
        "production_page_url": config_module.PRODUCTION_PAGE_URL,
        "create_production_url": config_module.CREATE_PRODUCTION_URL,
        "add_production_url": config_module.ADD_PRODUCTION_URL,
        "user_management_url": config_module.USER_MANAGEMENT_URL,
        "government_servers_url": config_module.GOVERNMENT_SERVERS_URL,
        "dispatched_device_url": config_module.DISPATCHED_DEVICE_URL,
        "dealer_fota_url": config_module.DEALER_FOTA_URL,
        "profile_url": config_module.PROFILE_URL,
        "customer_master_url": config_module.CUSTOMER_MASTER_URL,
        "model_url": config_module.MODEL_URL,
        "create_new_model": config_module.CREATE_NEW_MODEL,
        "update_model": config_module.UPDATE_MODEL,
        "ticket_dashboard_url": config_module.TICKET_DASHBOARD_URL,
        "my_ais_ticket_url": config_module.MY_AIS_TICKET_URL,
        "fota_url": config_module.FOTA_URL,
        "tml_request_log_url": config_module.TML_REQUEST_LOG_URL,
        "aepl_response_log_url": config_module.AEPL_RESPONSE_LOG_URL,
        "status_update_log_url": config_module.STATUS_UPDATE_LOG_URL,
        "device_state_config_url": config_module.DEVICE_STATE_CONFIG_URL,
        "device_vin_config_url": config_module.DEVICE_VIN_CONFIG_URL,
        "device_activity_log_url": config_module.DEVICE_ACTIVITY_LOG_URL,
        "api_base_url": config_module.API_BASE_URL,
        "page_title": config_module.PAGE_TITLE,
        "imei": config_module.IMEI,
        "browser": config_module.BROWSER,
        "headless": config_module.HEADLESS,
        "video_recording": config_module.VIDEO_RECORDING,
        "screenshot_on_failure": config_module.SCREENSHOT_ON_FAILURE,
        "log_level": config_module.LOG_LEVEL,
        "api_username": config_module.API_USERNAME,
        "api_password": config_module.API_PASSWORD,
        "customer": config_module.CUSTOMER,
        "login_user": config_module.LOGIN_USER,
        "valid_uid": config_module.VALID_UID,
        "valid_uin": config_module.VALID_UIN,
        "command_to_search": config_module.COMMAND_TO_SEARCH,
        "vin": config_module.VIN,
        "iccid": config_module.ICCID,
    }


@pytest.fixture(scope="session")
def test_data(project_config):
    project = project_config["project"]
    combined_data = {
        "username": project_config.get("username"),
        "password": project_config.get("password"),
        "login_user": project_config.get("login_user"),
        "valid_uid": project_config.get("valid_uid"),
        "valid_uin": project_config.get("valid_uin"),
        "command_to_search": project_config.get("command_to_search"),
        "vin": project_config.get("vin"),
        "iccid": project_config.get("iccid"),
        "customer": project_config.get("customer"),
        "valid_imei": project_config.get("imei"),
    }

    logger.info("Loaded test data for project %s", project)
    return combined_data


@pytest.fixture(scope="session", autouse=True)
def validate_project_config(project_config):
    required_keys = (
        "base_url",
        "username",
        "password",
        "browser",
        "api_base_url",
        "api_username",
        "api_password",
    )
    missing_keys = [key for key in required_keys if not project_config.get(key)]

    if missing_keys:
        raise ValueError(
            f"Missing required config keys for project "
            f"'{project_config['project']}': {', '.join(missing_keys)}"
        )

    logger.info("Project config validation passed for %s", project_config["project"])


@pytest.fixture
def login_page(browser):
    context = _new_context_with_zoom(browser, accept_downloads=True)
    page = context.new_page()

    from pages.common_login_page import LoginPage

    login = LoginPage(page)
    yield login

    page.close()
    context.close()


# Authenticated Page Fixture
@pytest.fixture(scope="function")
def page(browser, project_config):
    context = _new_context_with_zoom(
        browser,
        accept_downloads=True,
    )

    page = context.new_page()
    logger.info("New page opened")

    # Debugging listeners to log network errors and console issues
    # def log_console(msg):
    #     if msg.type in ["error", "warning"]:
    #         logger.warning(f"Browser console {msg.type}: {msg.text}")


    def log_response(response):
        if response.status >= 400:
            logger.error(f"HTTP Response error: {response.status} {response.url}")
            try:
                logger.error(f"Response body: {response.text()}")
            except Exception:
                pass

    # page.on("console", log_console)
    page.on("response", log_response)


    from pages.common_login_page import LoginPage

    login = LoginPage(page)
    login.load(project_config["base_url"])
    login.login(project_config["username"], project_config["password"])

    page.wait_for_load_state("networkidle")
    logger.info("Authenticated context ready: %s", page.url)

    yield page

    page.close()
    context.close()


def clean_error_message(err_str: str) -> str:
    """Consistently sanitize error strings to remove raw exception/stack trace verbosity."""
    if not err_str:
        return ""
    # If the string doesn't look like an exception/traceback/error, return it directly
    lower_str = err_str.lower()
    if "traceback" not in lower_str and "exception" not in lower_str and "error" not in lower_str:
        return err_str.strip()

    lines = err_str.strip().splitlines()
    if not lines:
        return ""

    # Look for standard pytest/python assertion formats
    for line in lines:
        line_strip = line.strip()
        if line_strip.startswith("E   assert ") or line_strip.startswith("E   AssertionError"):
            return line_strip[4:].strip()
        if line_strip.startswith("E "):
            return line_strip[2:].strip()

    # Fallback to the last line containing exception/assertion info
    last_line = lines[-1].strip()
    if last_line.startswith("E "):
        return last_line[2:].strip()
    return last_line


@pytest.fixture
def report_case(record_property):
    def _report_case(expected="", actual="", result="", message=""):
        # Always record properties, even if empty, to ensure they're in the report
        clean_expected = clean_error_message(str(expected)) if expected != "" else ""
        clean_actual = clean_error_message(str(actual)) if actual != "" else ""
        record_property("expected", clean_expected)
        record_property("actual", clean_actual)

        # 🔹 Determine result conditionally if not explicitly passed
        if not result:
            if clean_expected == clean_actual:
                result = "PASS"
            elif clean_expected != "" and clean_actual != "":
                if str(clean_expected).strip() == str(clean_actual).strip():
                    result = "PASS"
                else:
                    result = ""
            else:
                result = ""

        if result:
            record_property("result", result)
        if message:
            record_property("message", message)

    return _report_case


# Screenshot on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call":
        # Extract existing properties as a dict for easier manipulation
        props_dict = {name: val for name, val in item.user_properties}

        # 🔹 Extract expected from docstring or test name
        expected = (getattr(item.function, "__doc__", "") or "").strip()
        if not expected:
            expected = item.name.strip()

        # 🔹 Extract actual based on test outcome
        if report.passed:
            actual = "Test passed"
        elif report.skipped:
            actual = "Test skipped"
        else:
            # For failed tests, use the cleaned failure reason (no full stack trace)
            actual = clean_error_message(str(report.longrepr)) if report.longrepr else "Test failed"

        # Determine the final result value: failed tests always override to "failed"
        final_result = props_dict.get("result", "")
        failure_reason = ""
        if report.failed:
            final_result = "failed"
            failure_reason = clean_error_message(str(report.longrepr)) if report.longrepr else "Test failed"
        elif not final_result:
            final_result = report.outcome

        # Re-build user_properties to update values cleanly (update result, actual, message on failure)
        updated_properties = []
        for name, val in item.user_properties:
            if name == "result":
                continue
            if report.failed:
                if name == "actual" and failure_reason:
                    # Append failure reason to actual if actual was already recorded
                    val = f"{val} | Failure: {failure_reason}" if val and val != failure_reason else failure_reason
                elif name == "message" and failure_reason:
                    val = f"{val} | Failure: {failure_reason}"
            updated_properties.append((name, val))
        
        # Add result (either updated or original)
        updated_properties.append(("result", final_result))

        # Add expected/actual/message if they were not explicitly recorded
        has_expected = any(name == "expected" for name, _ in updated_properties)
        has_actual = any(name == "actual" for name, _ in updated_properties)
        has_message = any(name == "message" for name, _ in updated_properties)

        if not has_expected and expected:
            updated_properties.append(("expected", expected))
        if not has_actual and actual:
            updated_properties.append(("actual", actual))
        if not has_message and failure_reason:
            updated_properties.append(("message", f"Test failed: {failure_reason}"))

        item.user_properties = updated_properties

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            logger.warning("Test %s failed, capturing screenshot", item.name)
            screenshot_path = get_project_screenshot_path()
            os.makedirs(screenshot_path, exist_ok=True)
            safe_nodeid = item.nodeid
            safe_nodeid = (
                safe_nodeid.replace("::", "__").replace("/", "_").replace("\\", "_")
            )
            safe_nodeid = safe_nodeid.replace(" ", "_")
            import re

            safe_nodeid = re.sub(r'[<>:"\\|?*]+', "_", safe_nodeid)
            if len(safe_nodeid) > 100:
                safe_nodeid = safe_nodeid[-100:]
            page.screenshot(
                path=os.path.join(screenshot_path, f"{safe_nodeid}.png"),
                full_page=True,
            )


# Page Fixtures
@pytest.fixture
def dashboard_page(page, project_config):
    from pages.common_dashboard_page import DashboardPage

    dashboard = DashboardPage(page)
    dashboard.go_to_dashboard(project_config["dashboard_url"])
    logger.info("Dashboard page fixture ready")
    return dashboard


@pytest.fixture
def sim_data_details_page(page, project_config):
    from pages.common_sim_data_details_page import SimDataDetailsPage

    sim_data_details = SimDataDetailsPage(page)
    sim_data_details.go_to_simbatchpage(project_config["sim_data_details_url"])
    logger.info("SIM data details fixture ready")
    return sim_data_details


@pytest.fixture
def role_management_page(page, project_config):
    from pages.common_role_management_page import RoleManagementPage

    role_management = RoleManagementPage(page)
    role_management.go_to_rolemanagementpage(project_config["role_management_url"])
    logger.info("Role Management page fixture ready")
    return role_management


@pytest.fixture
def role_group_page(page, project_config):
    from pages.common_role_group_page import RoleGroupPage

    role_group = RoleGroupPage(page)
    role_group.go_to_role_group_page(project_config["role_group_url"])
    logger.info("Role Group page fixture ready")
    return role_group


@pytest.fixture
def device_details_page(page, project_config, test_data):
    # Prefer IMEI defined in project-specific test_data, otherwise fall back to project config
    device = test_data.get("valid_imei") or project_config.get(
        "imei", "866677075606341"
    )

    from pages.common_dashboard_page import DashboardPage
    from pages.common_device_details_page import DeviceDetailsPage

    base = BasePage(page)
    dashboard = DashboardPage(page)
    device_details = DeviceDetailsPage(page)

    base.navigate_to(project_config["dashboard_url"])

    result = dashboard.search_helper.run_search(device)
    assert result["success"], f"Search failed: {result['error']}"
    assert result["results_found"] == 1

    dashboard.click_on_view_device_in_table(device)

    page.wait_for_url("**/device-details")
    page.wait_for_load_state("networkidle")

    return device_details


@pytest.fixture
def ota_page(page, project_config):
    from pages.common_ota_page import OtaPage
    from pages.common_base_page import BasePage

    ota = OtaPage(page)
    base = BasePage(page)

    base.navigate_to(project_config["ota_url"])
    return ota


@pytest.fixture
def dispatched_device_page(page, project_config):
    from pages.common_dispatched_device_page import DispatchedDevicePage
    from pages.common_base_page import BasePage

    dispatched_device = DispatchedDevicePage(page)
    base = BasePage(page)
    base.navigate_to(project_config["dispatched_device_url"])
    logger.info("Dispatched Device page fixture ready")
    return dispatched_device


@pytest.fixture
def govt_server_page(page, project_config):
    from pages.common_govt_server_page import GovtServerPage
    from pages.common_base_page import BasePage

    govtserver = GovtServerPage(page)
    base = BasePage(page)
    base.navigate_to(project_config["government_servers_url"])

    logger.info("Government Server page ready via UI navigation")

    return govtserver


@pytest.fixture
def profile_page(page, project_config):
    from pages.common_profile_page import ProfilePage
    from pages.common_base_page import BasePage

    profile = ProfilePage(page)
    base = BasePage(page)

    base.navigate_to(project_config["profile_url"])

    logger.info("Profile page fixture ready")
    return profile


@pytest.fixture
def customer_master(page, project_config):
    from pages.common_customer_master_page import CustomerMasterPage

    customermaster = CustomerMasterPage(page)
    customermaster.go_to_customer(project_config["customer_master_url"])
    return customermaster


@pytest.fixture
def user_management(page, project_config):
    from pages.common_user_management_page import UserManagementPage

    usermanagement = UserManagementPage(page)
    usermanagement.go_to_user(project_config["user_management_url"])
    return usermanagement


@pytest.fixture
def model_page(page, project_config):
    from pages.common_model_page import DeviceModel

    model = DeviceModel(page)
    model.go_to_model(project_config["model_url"])
    logger.info("Model page fixture ready")
    return model


@pytest.fixture
def production_devices_page(page, project_config):
    from pages.common_production_devices_page import ProductionDevices

    production = ProductionDevices(page)
    base = BasePage(page)
    base.navigate_to(project_config["production_page_url"])
    logger.info("Production devices page fixture ready")
    return production


@pytest.fixture
def tml_request_log_page(page, project_config):
    from pages.atcu.atcu_tml_request_log_page import AtcuTmlRequestLogPage

    tml_request_log = AtcuTmlRequestLogPage(page)
    base = BasePage(page)
    base.navigate_to(project_config["tml_request_log_url"])
    logger.info("TML Request Log page fixture ready")
    return tml_request_log

@pytest.fixture
def aepl_response_log_page(page, project_config):
    from pages.atcu.atcu_aepl_response_log_page import AtcuAeplResponseLogPage

    aepl_response_log = AtcuAeplResponseLogPage(page)
    base = BasePage(page)
    base.navigate_to(project_config["aepl_response_log_url"])
    logger.info("AEPL Response Log page fixture ready")
    return aepl_response_log

@pytest.fixture
def atcu_device_state_config_page(page, project_config):
    from pages.atcu.atcu_device_state_config_page import AtcuDeviceStateConfigPage

    device_state_config = AtcuDeviceStateConfigPage(page)
    base = BasePage(page)
    base.navigate_to(project_config["device_state_config_url"])
    logger.info("Device State Config page fixture ready")
    return device_state_config


@pytest.fixture
def atcu_device_vin_config_page(page, project_config):
    from pages.atcu.atcu_device_vin_config_page import AtcuDeviceVinConfigPage

    device_vin_config = AtcuDeviceVinConfigPage(page)
    base = BasePage(page)
    base.navigate_to(project_config["device_vin_config_url"])
    logger.info("Device VIN Config page fixture ready")
    return device_vin_config


@pytest.fixture
def atcu_dealer_fota_page(page, project_config):
    from pages.atcu.atcu_dealer_fota_page import AtcuDealerFotaPage

    dealer_fota = AtcuDealerFotaPage(page)
    base = BasePage(page)
    base.navigate_to(project_config["dealer_fota_url"])
    logger.info("Dealer FOTA page fixture ready")
    return dealer_fota


@pytest.fixture
def atcu_model_page(page, project_config):
    from pages.atcu.atcu_model_page import AtcuModelPage

    model_page = AtcuModelPage(page)
    base = BasePage(page)
    base.navigate_to(project_config["model_url"])
    logger.info("ATCU Device Model page fixture ready")
    return model_page


@pytest.fixture
def atcu_govt_server_page(page, project_config):
    from pages.atcu.atcu_govt_server_page import AtcuGovtServerPage

    govt_server_page = AtcuGovtServerPage(page)
    base = BasePage(page)
    base.navigate_to(project_config["government_servers_url"])
    logger.info("ATCU Government Servers page fixture ready")
    return govt_server_page


@pytest.fixture
def atcu_device_activity_log_page(page, project_config):
    from pages.atcu.atcu_device_activity_log_page import AtcuDeviceActivityLogPage

    activity_log_page = AtcuDeviceActivityLogPage(page)
    base = BasePage(page)
    base.navigate_to(project_config["device_activity_log_url"])
    logger.info("ATCU Device System Activity Log page fixture ready")
    return activity_log_page


@pytest.fixture
def atcu_status_update_log_page(page, project_config):
    from pages.atcu.atcu_status_update_log_page import AtcuStatusUpdateLogPage

    status_log_page = AtcuStatusUpdateLogPage(page)
    base = BasePage(page)
    base.navigate_to(project_config["status_update_log_url"])
    logger.info("ATCU AIS140 Ticket Status Update Logs page fixture ready")
    return status_log_page


@pytest.fixture
def atcu_dispatched_device_page(page, project_config):
    from pages.atcu.atcu_dispatched_device_page import AtcuDispatchedDevicePage

    dispatched_device_page = AtcuDispatchedDevicePage(page)
    base = BasePage(page)
    base.navigate_to(project_config["dispatched_device_url"])
    logger.info("ATCU Dispatched Devices page fixture ready")
    return dispatched_device_page


@pytest.fixture
def atcu_dashboard_page(page, project_config):
    from pages.atcu.atcu_dashboard_page import AtcuDashboardPage

    dashboard_page = AtcuDashboardPage(page)
    base = BasePage(page)
    dash_url = project_config.get("atcu_dashboard_url") or project_config.get("dashboard_url")
    base.navigate_to(dash_url)
    logger.info("ATCU Dashboard page fixture ready")
    return dashboard_page


@pytest.fixture
def atcu_ticket_dashboard_page(page, project_config):
    from pages.atcu.atcu_ticket_dashboard_page import AtcuTicketDashboardPage

    ticket_dashboard_page = AtcuTicketDashboardPage(page)
    base = BasePage(page)
    base.navigate_to(project_config["ticket_dashboard_url"])
    logger.info("ATCU Ticket Dashboard page fixture ready")
    return ticket_dashboard_page


@pytest.fixture
def atcu_ota_page(page, project_config):
    from pages.atcu.atcu_ota_page import AtcuOtaPage

    ota_page = AtcuOtaPage(page)
    base = BasePage(page)
    ota_url = project_config.get("ota_batch_report_url") or project_config.get("ota_url") or "https://aepl-tcu4g-qa.accoladeelectronics.com/Ota-batch-report"
    base.navigate_to(ota_url)
    logger.info("ATCU OTA page fixture ready at %s", ota_url)
    return ota_page


@pytest.fixture
def atcu_create_ota_batch_page(page, project_config):
    from pages.atcu.atcu_ota_page import AtcuOtaPage

    ota_page = AtcuOtaPage(page)
    base = BasePage(page)
    create_url = project_config.get("create_new_ota_batch") or "https://aepl-tcu4g-qa.accoladeelectronics.com/ota-batch-create"
    base.navigate_to(create_url)
    logger.info("ATCU Create OTA Batch page fixture ready at %s", create_url)
    return ota_page


@pytest.fixture
def atcu_manual_ota_page(page, project_config):
    from pages.atcu.atcu_ota_page import AtcuOtaPage

    ota_page = AtcuOtaPage(page)
    base = BasePage(page)
    manual_url = project_config.get("manual_ota_url") or "https://aepl-tcu4g-qa.accoladeelectronics.com/manual-ota"
    base.navigate_to(manual_url)
    logger.info("ATCU Manual OTA page fixture ready at %s", manual_url)
    return ota_page


@pytest.fixture
def atcu_ota_master_page(page, project_config):
    from pages.atcu.atcu_ota_page import AtcuOtaPage

    ota_page = AtcuOtaPage(page)
    base = BasePage(page)
    master_url = project_config.get("ota_master_url") or "https://aepl-tcu4g-qa.accoladeelectronics.com/ota-master"
    base.navigate_to(master_url)
    logger.info("ATCU OTA Master page fixture ready at %s", master_url)
    return ota_page



# API Fixtures
@pytest.fixture
def api_context(project_config):
    """Provide API context with credentials for API tests."""
    return {
        "api_base_url": project_config["api_base_url"],
        "api_username": project_config["api_username"],
        "api_password": project_config["api_password"],
    }


@pytest.fixture
def sim_batch_api(page, api_context):
    from api.sim_batch_api import SIMBatchAPI

    return SIMBatchAPI


@pytest.fixture
def customer_api(page, api_context):
    from api.customer_api import CustomerAPI

    return CustomerAPI


@pytest.fixture
def device_dashboard_api(page, api_context):
    from api.device_dashboard_api import DeviceDashboardAPI

    return DeviceDashboardAPI


@pytest.fixture
def login_api_fixture(page, api_context):
    from api.login_api import LoginAPI

    return LoginAPI


@pytest.fixture
def govt_server_api(page, api_context):
    from api.government_server_api import GovtServerAPI

    return GovtServerAPI
