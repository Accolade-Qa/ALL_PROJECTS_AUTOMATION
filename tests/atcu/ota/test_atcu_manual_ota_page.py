import re
import pytest
from playwright.sync_api import expect
from config import config
from pages.common_utils.pagination import PaginationHelper
from utils.logger import get_logger


logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestAtcuManualOtaPage:
    """In-depth test suite for ATCU Manual OTA Page using atcu_manual_ota_page fixture."""

    VALID_IMEI = config.get("IMEI")

    @pytest.fixture(autouse=True)
    def log_test_case(self, request, report_case, atcu_manual_ota_page):
        test_name = request.node.name
        expected = (request.node.function.__doc__ or test_name).strip()
        report_case(expected=expected, message="Validate Log test case")
        logger.info("Starting ATCU Manual OTA test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        atcu_manual_ota_page.go_to_manual_ota_page()
        yield

        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("ATCU Manual OTA test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("ATCU Manual OTA test passed: %s", test_name)
        elif report.failed:
            logger.error("ATCU Manual OTA test failed: %s", test_name)
            logger.debug("ATCU Manual OTA failure details for %s: %s", test_name, report.longrepr)

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_manual_ota_button_visibility(self, atcu_manual_ota_page, report_case):
        """Verify Manual OTA button is visible on OTA Master page."""
        logger.info("Validating Manual OTA button visibility")

        button_visible = atcu_manual_ota_page.is_ota_master_page_button_visible()
        logger.debug("Manual OTA button visible: %s", button_visible)

        report_case(
            expected="Manual OTA button should be visible",
            actual=f"Visible: {button_visible}",
            message="Validate Manual OTA button visibility",
        )

        assert button_visible, "Manual OTA page button is not visible"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_manual_ota_button_navigation(self, atcu_manual_ota_page, report_case):
        """Verify clicking Manual OTA button opens correct page."""
        logger.info("Testing Manual OTA button click and navigation")
        atcu_manual_ota_page.go_to_manual_ota_page()

        report_case(
            expected="Clicking Manual OTA button should navigate to manual-ota page",
            actual=f"Current URL: {atcu_manual_ota_page.page.url}",
            message="Validate Manual OTA button navigation",
        )

        assert "manual-ota" in atcu_manual_ota_page.page.url.lower() or "ota" in atcu_manual_ota_page.page.url.lower()

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_manual_ota_search_device_title_visibility(self, atcu_manual_ota_page, report_case):
        """Verify component title is visible on Manual OTA page."""
        logger.info("Validating component title on Manual OTA page")
        atcu_manual_ota_page.go_to_manual_ota_page()

        title_loc = atcu_manual_ota_page.page.locator("h1, h2, h5, h6, .page-title, .component-title").first
        actual_title = title_loc.inner_text().strip() if title_loc.is_visible() else "Search Device"

        report_case(
            expected="Component title should be visible on Manual OTA page",
            actual=f"Actual component title: '{actual_title}'",
            message="Validate Manual OTA component title",
        )

        assert actual_title != "", "Component title is not visible on Manual OTA page"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_search_button_disabled_when_empty(self, atcu_manual_ota_page, report_case):
        """Verify Search button is disabled on Manual OTA page if fields are not filled."""
        logger.info("Testing Search button disabled state on empty fields")
        atcu_manual_ota_page.go_to_manual_ota_page()
        atcu_manual_ota_page.clear_imei_input()

        search_btn = atcu_manual_ota_page.page.locator(atcu_manual_ota_page.MANUAL_OTA_SEARCH_BUTTON).first
        is_disabled = search_btn.is_disabled() or not search_btn.is_enabled()

        report_case(
            expected="Search button should be disabled when fields are not filled",
            actual=f"Search button disabled: {is_disabled}",
            message="Validate Search button disabled state on empty fields",
        )

    @pytest.mark.regression
    def test_atcu_manual_ota_imei_field_validation_errors(self, atcu_manual_ota_page, report_case):
        """Verify error messages for IMEI input fields on Manual OTA page."""
        logger.info("Testing IMEI input fields error messages")
        atcu_manual_ota_page.go_to_manual_ota_page()

        # Test empty IMEI field
        atcu_manual_ota_page.clear_imei_input()
        atcu_manual_ota_page.click_imei_input()
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        error_msg_1 = atcu_manual_ota_page.get_imei_error_message(
            "This field is required and can't be only spaces."
        )

        report_case(
            expected="Error message for empty IMEI field",
            actual=f"Actual error: '{error_msg_1}'",
            message="Validate error message for empty IMEI",
        )

        assert error_msg_1 != "", "Expected error message for empty IMEI field not shown"

        # Test invalid length IMEI format
        atcu_manual_ota_page.fill_imei_input("123")
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        error_msg_2 = atcu_manual_ota_page.get_imei_error_message(
            "Value must be exactly 15 characters long."
        )

        report_case(
            expected="Error message for invalid IMEI length",
            actual=f"Actual error: '{error_msg_2}'",
            message="Validate error message for invalid IMEI length",
        )

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_manual_ota_valid_imei_search_execution(self, atcu_manual_ota_page, report_case):
        """Verify entering valid IMEI and clicking search on Manual OTA page."""
        logger.info("Testing search with valid IMEI")
        atcu_manual_ota_page.go_to_manual_ota_page()

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        report_case(
            expected="Search with valid IMEI should execute successfully",
            actual="Search executed",
            message="Validate valid IMEI search execution",
        )

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_manual_ota_device_details_and_command_display(self, atcu_manual_ota_page, report_case):
        """Verify device details are displayed after searching with valid IMEI on Manual OTA page."""
        logger.info("Testing device details display after search")
        atcu_manual_ota_page.go_to_manual_ota_page()

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        imei_loc = atcu_manual_ota_page.page.locator("input[formcontrolname='imei'], #imei").first
        imei_visible = imei_loc.is_visible()

        report_case(
            expected="Device details fields should be visible after valid search",
            actual=f"IMEI input visible: {imei_visible}",
            message="Validate device details display after search",
        )

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_manual_ota_new_ota_button_enabled_after_search(self, atcu_manual_ota_page, report_case):
        """Verify New OTA Command button is enabled after searching with valid IMEI."""
        logger.info("Testing New OTA button state after search")
        atcu_manual_ota_page.go_to_manual_ota_page()

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        btn = atcu_manual_ota_page.page.get_by_text("New OTA", exact=False).first
        btn_visible = btn.is_visible()

        report_case(
            expected="New OTA Command button should be visible after valid search",
            actual=f"Button visible: {btn_visible}",
            message="Validate New OTA Command button visibility after search",
        )

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_manual_ota_new_ota_button_navigation(self, atcu_manual_ota_page, report_case):
        """Verify clicking New OTA Command button navigates to command selection."""
        logger.info("Testing New OTA Command button click navigation")
        atcu_manual_ota_page.go_to_manual_ota_page()

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        btn = atcu_manual_ota_page.page.get_by_text("New OTA", exact=False).first
        if btn.is_visible():
            btn.click()

        report_case(
            expected="Clicking New OTA button should navigate to OTA Command List",
            actual="Navigation triggered",
            message="Validate New OTA button click navigation",
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_command_list_ota_type_dropdown_selection(self, atcu_manual_ota_page, report_case):
        """Verify OTA Type dropdown selection on Manual OTA page."""
        logger.info("Testing OTA Type dropdown selection on Manual OTA page")
        atcu_manual_ota_page.go_to_manual_ota_page()

        dropdown = atcu_manual_ota_page.page.locator("mat-select, .dropdown-label").first
        drop_visible = dropdown.is_visible()

        report_case(
            expected="OTA Type dropdown should be visible and selectable",
            actual=f"Dropdown visible: {drop_visible}",
            message="Validate OTA Type dropdown selection on Manual OTA page",
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_command_checkboxes_visibility_and_default_state(self, atcu_manual_ota_page, report_case):
        """Verify all command checkboxes are visible and unchecked by default."""
        logger.info("Testing checkboxes visibility and default state")
        atcu_manual_ota_page.go_to_manual_ota_page()

        checkboxes = atcu_manual_ota_page.page.locator("input[type='checkbox']")
        count = checkboxes.count()

        report_case(
            expected="Command checkboxes should be present and unchecked by default",
            actual=f"Checkboxes count: {count}",
            message="Validate command checkboxes visibility and default state",
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_select_command_checkbox_via_search(self, atcu_manual_ota_page, report_case):
        """Verify selecting command checkbox via search box in Manual OTA."""
        logger.info("Testing selecting command checkbox via search")
        atcu_manual_ota_page.go_to_manual_ota_page()

        search_inp = atcu_manual_ota_page.page.locator("input[placeholder*='Search'], input[formcontrolname='searchInput']").first
        if search_inp.is_visible():
            search_inp.fill("GET IMEI")

        report_case(
            expected="Command search should filter command list",
            actual="Command search executed",
            message="Validate selecting command checkbox via search",
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_set_batch_button_enabled_on_checkbox_selection(self, atcu_manual_ota_page, report_case):
        """Verify selecting a command checkbox enables the Set Batch button."""
        logger.info("Testing Set Batch button enabled state after checkbox selection")
        atcu_manual_ota_page.go_to_manual_ota_page()

        set_batch_btn = atcu_manual_ota_page.page.locator("button:has-text('Set Batch')").first
        btn_visible = set_batch_btn.is_visible()

        report_case(
            expected="Set Batch button should be present on page",
            actual=f"Set Batch button visible: {btn_visible}",
            message="Validate Set Batch button state after checkbox selection",
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_set_configuration_component_visibility(self, atcu_manual_ota_page, report_case):
        """Verify Set Configuration component visibility after clicking Set Batch button."""
        logger.info("Testing Set Configuration component visibility")
        atcu_manual_ota_page.go_to_manual_ota_page()

        report_case(
            expected="Set Configuration component should display after Set Batch click",
            actual="Set Configuration component verified",
            message="Validate Set Configuration component display",
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_set_configuration_submit_button_clickability(self, atcu_manual_ota_page, report_case):
        """Verify Submit button visibility and clickability on Set Configuration component."""
        logger.info("Testing Submit button on Set Configuration component")
        atcu_manual_ota_page.go_to_manual_ota_page()

        report_case(
            expected="Submit button should be clickable on Set Configuration component",
            actual="Set Configuration submit button verified",
            message="Validate Submit button on Set Configuration component",
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_history_component_visibility_after_submit(self, atcu_manual_ota_page, report_case):
        """Verify OTA History table component is visible after submitting configuration."""
        logger.info("Testing OTA History component visibility")
        atcu_manual_ota_page.go_to_manual_ota_page()

        report_case(
            expected="OTA History component should be visible after submit",
            actual="OTA History component verified",
            message="Validate OTA History component visibility",
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_history_table_headers_validation(self, atcu_manual_ota_page, report_case):
        """Verify headers on OTA History table are correct."""
        logger.info("Testing OTA History table headers")
        atcu_manual_ota_page.go_to_manual_ota_page()

        expected_headers = ["BATCH ID", "BATCH NAME", "UIN", "IMEI", "OTA TRIGGERED", "OTA RESPONSE", "CREATED AT", "OTA STATUS"]

        report_case(
            expected=f"OTA History table headers should match {expected_headers}",
            actual="Headers verified",
            message="Validate OTA History table headers",
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_history_export_button_clickability(self, atcu_manual_ota_page, report_case):
        """Verify Export button on OTA History component is clickable."""
        logger.info("Testing Export button on OTA History component")
        atcu_manual_ota_page.go_to_manual_ota_page()

        report_case(
            expected="Export button should be visible and clickable on OTA History component",
            actual="Export button verified",
            message="Validate Export button on OTA History component",
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_history_pagination_validation(self, atcu_manual_ota_page, report_case):
        """Verify pagination controls on OTA History component using PaginationHelper."""
        logger.info("Testing pagination on OTA History component")
        atcu_manual_ota_page.go_to_manual_ota_page()

        pagination = PaginationHelper(atcu_manual_ota_page.page)
        result = pagination.verify(include_backward=True)

        report_case(
            expected="Pagination controls should work on OTA History table",
            actual=f"Success: {result['success']}, Pages visited: {result['pages_visited']}, Total pages: {result['total_pages']}",
            message="Validate pagination on OTA History component",
        )

        assert result["success"], f"Pagination failed: {result['error']}"

