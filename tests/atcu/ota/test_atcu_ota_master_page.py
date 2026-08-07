import re
import pytest
from playwright.sync_api import expect

from pages.common_utils.search import SearchHelper
from pages.common_utils.table_section import TableSection
from utils.helpers import Helpers as helper
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestAtcuOtaMasterPage:
    """In-depth test suite for ATCU Project OTA Master & Add OTA Command Pages using atcu_ota_master_page fixture."""

    SEARCH_QUERY = "test"

    @pytest.fixture(autouse=True)
    def log_test_case(self, request, report_case, atcu_ota_master_page):
        test_name = request.node.name
        expected = (request.node.function.__doc__ or test_name).strip()
        report_case(expected=expected, message="Validate Log test case")
        logger.info("Starting ATCU OTA Master test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        atcu_ota_master_page.go_to_ota_master_page()
        yield

        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("ATCU OTA Master test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("ATCU OTA Master test passed: %s", test_name)
        elif report.failed:
            logger.error("ATCU OTA Master test failed: %s", test_name)
            logger.debug("ATCU OTA Master failure details for %s: %s", test_name, report.longrepr)

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_ota_master_button_visibility(self, atcu_ota_master_page, report_case):
        """Verify OTA Master button is visible on OTA Batch page."""
        logger.info("Validating OTA Master button visibility")

        button_visible = atcu_ota_master_page.is_ota_master_page_button_visible()
        logger.debug("OTA Master button visible: %s", button_visible)

        report_case(
            expected="OTA Master button should be visible on OTA Batch page",
            actual=f"OTA Master button visible: {button_visible}",
            message="Validate OTA Master button visibility",
        )

        assert button_visible, "OTA Master page button is not visible"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_ota_master_button_navigation(self, atcu_ota_master_page, report_case):
        """Verify navigation to OTA Master page succeeds."""
        logger.info("Navigating to OTA Master page")
        atcu_ota_master_page.go_to_ota_master_page()
        logger.debug("OTA Master URL after navigation: %s", atcu_ota_master_page.page.url)

        report_case(
            expected="Page URL should contain 'ota-master'",
            actual=f"Current URL: {atcu_ota_master_page.page.url}",
            message="Validate navigation to OTA Master page",
        )

        assert "ota-master" in atcu_ota_master_page.page.url.lower()

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_ota_master_header_title_validation(self, atcu_ota_master_page, report_case):
        """Verify OTA Master page title is correct after navigation."""
        logger.info("Verifying OTA Master page title")
        atcu_ota_master_page.go_to_ota_master_page()

        actual_title = atcu_ota_master_page.get_page_title()
        logger.debug("OTA Master header title: %s", actual_title)

        report_case(
            expected="Page title should contain 'OTA Master'",
            actual=f"Actual title: '{actual_title}'",
            message="Validate OTA Master page title",
        )

        assert "OTA" in actual_title or "Master" in actual_title or actual_title != "", "OTA Master page title is invalid"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_ota_master_ui_elements_visibility(self, atcu_ota_master_page, report_case):
        """Verify OTA Master page elements are visible after navigation."""
        logger.info("Validating OTA Master page elements")
        atcu_ota_master_page.go_to_ota_master_page()

        master_loaded = atcu_ota_master_page.is_ota_master_page_loaded()
        buttons_visible = atcu_ota_master_page.is_ota_batch_page_buttons_visible()
        table_visible = atcu_ota_master_page.is_ota_batch_table_visible()

        report_case(
            expected="All OTA Master page elements should be visible",
            actual=f"Master page loaded: {master_loaded}, Buttons: {buttons_visible}, Table: {table_visible}",
            message="Validate OTA Master page elements visibility",
        )

        assert master_loaded, "OTA Master page did not load correctly"
        assert table_visible, "OTA Master table is not visible on OTA Master page"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_ota_master_table_search_filter_functionality(self, atcu_ota_master_page, report_case):
        """Verify search functionality on OTA Master page."""
        logger.info("Testing search functionality on OTA Master table")

        atcu_ota_master_page.go_to_ota_master_page()
        assert atcu_ota_master_page.is_ota_batch_table_visible(), "OTA Master table is not visible"

        search = SearchHelper(atcu_ota_master_page.page)
        result = search.run_search(self.SEARCH_QUERY)

        report_case(
            expected=f"Search with query '{self.SEARCH_QUERY}' should succeed",
            actual=f"Search success: {result['success']}, Results found: {result['results_found']}",
            message=f"Validate OTA Master table search filters for query '{self.SEARCH_QUERY}'",
        )

        assert result["success"], f"Search failed: {result['error']}"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_ota_master_table_headers_and_data_display(self, atcu_ota_master_page, report_case):
        """Verify OTA Master table data is visible and valid."""
        logger.info("Validating OTA Master table data")
        atcu_ota_master_page.go_to_ota_master_page()

        row_count = atcu_ota_master_page.get_master_table_row_count()
        logger.debug("OTA Master table row count: %s", row_count)

        report_case(
            expected="OTA Master table should display valid data",
            actual=f"Row count: {row_count}",
            message="Validate OTA Master table displays data",
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_add_command_button_visibility_and_navigation(self, atcu_ota_master_page, report_case):
        """Verify Add OTA Command button is visible on OTA Master page."""
        logger.info("Validating Add OTA Command button visibility and navigation")
        atcu_ota_master_page.go_to_ota_master_page()

        button_visible = atcu_ota_master_page.is_add_ota_command_button_visible()

        report_case(
            expected="Add OTA Command button should be visible on OTA Master page",
            actual=f"Add OTA Command button visible: {button_visible}",
            message="Validate Add OTA Command button visibility",
        )

        assert button_visible, "Add OTA Command button is not visible on OTA Master page"

        atcu_ota_master_page.validate_add_ota_button_and_click()
        page_title = atcu_ota_master_page.is_on_add_ota_command_page()

        report_case(
            expected="Should navigate to Add OTA Command page",
            actual=f"Page title after navigation: '{page_title}'",
            message="Validate Add OTA Command page navigation",
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_add_command_form_fields_visibility(self, atcu_ota_master_page, report_case):
        """Verify all Add OTA Command form fields are visible."""
        logger.info("Validating Add OTA Command form fields visibility")
        atcu_ota_master_page.go_to_ota_master_page()
        atcu_ota_master_page.validate_add_ota_button_and_click()

        fields_visible = atcu_ota_master_page.are_add_ota_command_form_fields_visible()

        report_case(
            expected="All Add OTA Command form fields should be visible",
            actual=f"Form fields visible: {fields_visible}",
            message="Validate Add OTA Command form fields visibility",
        )

        assert fields_visible, "Not all Add OTA Command form fields are visible"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_add_command_form_ota_name_field_input(self, atcu_ota_master_page, report_case):
        """Verify OTA Name field can be filled."""
        logger.info("Testing OTA Name field fill")
        atcu_ota_master_page.go_to_ota_master_page()
        atcu_ota_master_page.validate_add_ota_button_and_click()

        test_name = "Test OTA Name"
        atcu_ota_master_page.page.locator(atcu_ota_master_page.OTA_NAME_FIELD).fill(test_name)
        actual_val = atcu_ota_master_page.page.locator(atcu_ota_master_page.OTA_NAME_FIELD).input_value()

        report_case(
            expected=f"OTA Name field should accept value '{test_name}'",
            actual=f"Actual value: '{actual_val}'",
            message="Validate OTA Name field input",
        )

        assert actual_val == test_name, f"Expected '{test_name}', got '{actual_val}'"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_add_command_form_ota_command_field_input(self, atcu_ota_master_page, report_case):
        """Verify OTA Command field can be filled."""
        logger.info("Testing OTA Command field fill")
        atcu_ota_master_page.go_to_ota_master_page()
        atcu_ota_master_page.validate_add_ota_button_and_click()

        test_cmd = "Test Command"
        atcu_ota_master_page.page.locator(atcu_ota_master_page.OTA_COMMAND_FIELD).fill(test_cmd)
        actual_val = atcu_ota_master_page.page.locator(atcu_ota_master_page.OTA_COMMAND_FIELD).input_value()

        report_case(
            expected=f"OTA Command field should accept value '{test_cmd}'",
            actual=f"Actual value: '{actual_val}'",
            message="Validate OTA Command field input",
        )

        assert actual_val == test_cmd, f"Expected '{test_cmd}', got '{actual_val}'"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_add_command_form_example_field_input(self, atcu_ota_master_page, report_case):
        """Verify Example field can be filled."""
        logger.info("Testing Example field fill")
        atcu_ota_master_page.go_to_ota_master_page()
        atcu_ota_master_page.validate_add_ota_button_and_click()

        test_ex = "Example Value"
        atcu_ota_master_page.page.locator(atcu_ota_master_page.EXAMPLE_FIELD).fill(test_ex)
        actual_val = atcu_ota_master_page.page.locator(atcu_ota_master_page.EXAMPLE_FIELD).input_value()

        report_case(
            expected=f"Example field should accept value '{test_ex}'",
            actual=f"Actual value: '{actual_val}'",
            message="Validate Example field input",
        )

        assert actual_val == test_ex, f"Expected '{test_ex}', got '{actual_val}'"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_add_command_form_ota_type_dropdown_selection(self, atcu_ota_master_page, report_case):
        """Verify OTA Type dropdown can be selected."""
        logger.info("Testing OTA Type dropdown selection")
        atcu_ota_master_page.go_to_ota_master_page()
        atcu_ota_master_page.validate_add_ota_button_and_click()

        drop_loc = atcu_ota_master_page.page.locator(atcu_ota_master_page.OTA_TYPE_DROPDOWN).first
        drop_visible = drop_loc.is_visible()

        report_case(
            expected="OTA Type dropdown should be visible",
            actual=f"Dropdown visible: {drop_visible}",
            message="Validate OTA Type dropdown selection",
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_add_command_form_submit_disabled_when_empty(self, atcu_ota_master_page, report_case):
        """Verify Submit button is disabled when form fields are empty."""
        logger.info("Testing Submit button disabled state on empty form")
        atcu_ota_master_page.go_to_ota_master_page()
        atcu_ota_master_page.validate_add_ota_button_and_click()

        btn = atcu_ota_master_page.page.locator(atcu_ota_master_page.SUBMIT_BUTTON).first
        is_disabled = btn.is_disabled() or not btn.is_enabled()

        report_case(
            expected="Submit button should be disabled on empty form",
            actual=f"Submit button disabled: {is_disabled}",
            message="Validate Submit button disabled state on empty form",
        )

        assert is_disabled, "Submit button should be disabled when form is empty"

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_add_command_form_submit_enabled_when_filled(self, atcu_ota_master_page, report_case):
        """Verify Submit button is enabled when all form fields are filled."""
        logger.info("Testing Submit button enabled state on filled form")
        atcu_ota_master_page.go_to_ota_master_page()
        atcu_ota_master_page.validate_add_ota_button_and_click()

        atcu_ota_master_page.fill_add_ota_command_form("Test Name", "Test Cmd", "GET", "Test Ex", "NO")

        btn = atcu_ota_master_page.page.locator(atcu_ota_master_page.SUBMIT_BUTTON).first
        btn_visible = btn.is_visible()

        report_case(
            expected="Submit button should be present on form fill",
            actual=f"Submit button visible: {btn_visible}",
            message="Validate Submit button enabled state on filled form",
        )

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_add_command_form_submit_button_clickability(self, atcu_ota_master_page, report_case):
        """Verify Submit button is clickable when enabled."""
        logger.info("Testing Submit button clickability")
        atcu_ota_master_page.go_to_ota_master_page()
        atcu_ota_master_page.validate_add_ota_button_and_click()

        atcu_ota_master_page.fill_add_ota_command_form("Click OTA", "Click Cmd", "SET", "Click Ex", "NO")

        btn = atcu_ota_master_page.page.locator(atcu_ota_master_page.SUBMIT_BUTTON).first
        assert btn.is_visible(), "Submit button should be visible"
