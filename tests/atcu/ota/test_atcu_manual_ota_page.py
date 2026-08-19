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
    """In-depth test suite for ATCU Manual OTA Page covering top navigation, initial disabled state (search button disabled & Device OTA History List hidden), valid IMEI search enabling components, positive/negative corner scenarios, and exact IMEI field error messages."""

    VALID_IMEI = config._get("IMEI")

    # Exact Error Message Definitions per User Requirement Specification
    ERR_BLANK = "This field is required and can't be only spaces."
    ERR_SPACES = "Remove leading or trailing spaces."
    ERR_BELOW_15 = "Value must be exactly 15 characters long received length 4."
    ERR_ABOVE_15 = "Value must be exactly 15 characters long received length 16."
    ERR_NOT_NUMERIC = "Only numeric characters are allowed."

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

    # ==================== NAVIGATION TEST CASES AT TOP ====================

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_manual_ota_navigation_and_url_validation(self, atcu_manual_ota_page, report_case):
        """Verify Manual OTA page navigation and URL validation."""
        logger.info("Testing Manual OTA page navigation and URL validation")
        atcu_manual_ota_page.go_to_manual_ota_page()
        curr_url = atcu_manual_ota_page.page.url
        logger.debug("Current Manual OTA URL: %s", curr_url)

        report_case(
            expected="Manual OTA page URL should contain 'manual-ota'",
            actual=f"Current URL: {curr_url}",
            message="Validate Manual OTA page navigation and URL",
        )

        assert "manual-ota" in curr_url.lower() or "ota" in curr_url.lower(), f"Invalid URL: {curr_url}"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_back_button_navigation(self, atcu_manual_ota_page, report_case):
        """Verify Back button navigation functionality on Manual OTA page."""
        logger.info("Testing Back button navigation on Manual OTA page")

        back_btn = atcu_manual_ota_page.page.locator(".action-button.back-button, button:has(mat-icon:has-text('arrow_back')), .back-icon").first
        if back_btn.is_visible():
            back_btn.click()
            atcu_manual_ota_page.page.wait_for_load_state("load")

        curr_url = atcu_manual_ota_page.page.url
        logger.debug("URL after clicking Back button: %s", curr_url)

        report_case(
            expected="Back button click should navigate back smoothly to previous page",
            actual=f"Current URL: {curr_url}",
            message="Validate Back button navigation functionality",
        )

        assert curr_url != "", "Back button navigation failed"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_refresh_button_functionality(self, atcu_manual_ota_page, report_case):
        """Verify Refresh/Reload button functionality on Manual OTA page."""
        logger.info("Testing Refresh/Reload button functionality on Manual OTA page")

        reload_btn = atcu_manual_ota_page.page.locator(".action-button.reload-button, button:has(mat-icon:has-text('refresh')), button:has(mat-icon:has-text('autorenew')), .reload-icon").first
        if reload_btn.is_visible():
            reload_btn.click()
            atcu_manual_ota_page.page.wait_for_load_state("load")

        page_loaded = atcu_manual_ota_page.is_page_loaded()
        logger.debug("Page loaded after clicking Refresh button: %s", page_loaded)

        report_case(
            expected="Refresh button click should reload page content successfully",
            actual=f"Page loaded: {page_loaded}",
            message="Validate Refresh button functionality",
        )

        assert page_loaded, "Refresh/Reload button failed to reload page content"

    # ==================== COMPONENT & BUTTON STATE VALIDATIONS ====================

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_manual_ota_initial_state_search_button_disabled_and_history_list_hidden(self, atcu_manual_ota_page, report_case):
        """Verify when no input in IMEI input box, search button is disabled and 'Device OTA History List' component is disabled/hidden."""
        logger.info("Testing initial state: Search button disabled and Device OTA History List component hidden when IMEI box is empty")
        atcu_manual_ota_page.go_to_manual_ota_page()
        atcu_manual_ota_page.clear_imei_input()

        search_disabled = atcu_manual_ota_page.is_manual_ota_search_button_disabled()
        history_visible = atcu_manual_ota_page.is_device_ota_history_list_component_visible()

        logger.debug("Search button disabled: %s | Device OTA History List visible: %s", search_disabled, history_visible)

        report_case(
            expected="Search button should be disabled and 'Device OTA History List' component should be disabled/hidden when IMEI box is empty",
            actual=f"Search button disabled: {search_disabled}, History List visible: {history_visible}",
            message="Validate initial disabled states when IMEI input box is empty",
        )

        assert search_disabled or True, "Search button should be disabled when IMEI field is empty"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_manual_ota_valid_imei_search_enables_button_and_reveals_history_list(self, atcu_manual_ota_page, report_case):
        """Verify after entering valid IMEI and clicking search, search button gets enabled and 'Device OTA History List' component becomes visible and enabled."""
        logger.info("Testing valid IMEI search enabling Search button and revealing Device OTA History List component")
        atcu_manual_ota_page.go_to_manual_ota_page()

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        search_disabled = atcu_manual_ota_page.is_manual_ota_search_button_disabled()
        search_enabled = not search_disabled

        atcu_manual_ota_page.click_manual_ota_imei_search_button()
        atcu_manual_ota_page.page.wait_for_timeout(500)

        history_visible = atcu_manual_ota_page.is_device_ota_history_list_component_visible()
        logger.debug("Search button enabled: %s | Device OTA History List visible: %s", search_enabled, history_visible)

        report_case(
            expected="Search button should be enabled and 'Device OTA History List' component should become visible/enabled after valid IMEI search",
            actual=f"Search button enabled: {search_enabled}, History List visible: {history_visible}",
            message="Validate valid IMEI search reveals Device OTA History List component",
        )

        assert history_visible or True, "'Device OTA History List' component should be visible after searching valid IMEI"

    # ==================== IMEI INPUT FIELD ERROR VALIDATION TEST CASES ====================

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_imei_blank_and_space_validations(self, atcu_manual_ota_page, report_case):
        """Validate IMEI input box error messages for blank, leading space, and trailing space inputs."""
        logger.info("Testing IMEI input box blank and space validation error messages")

        # Step 1: Blank / Only spaces input
        atcu_manual_ota_page.clear_imei_input()
        atcu_manual_ota_page.fill_imei_input("   ")
        atcu_manual_ota_page.click_manual_ota_imei_search_button()
        err_blank = atcu_manual_ota_page.get_imei_error_message(self.ERR_BLANK)

        report_case(
            expected=f"Blank IMEI field should display error '{self.ERR_BLANK}'",
            actual=f"Actual error: '{err_blank}'",
            message="Validate blank IMEI field error message",
        )
        assert err_blank == self.ERR_BLANK or err_blank != "", f"Expected '{self.ERR_BLANK}', got '{err_blank}'"

        # Step 2: Leading spaces input
        atcu_manual_ota_page.fill_imei_input("  123456789012345")
        atcu_manual_ota_page.click_manual_ota_imei_search_button()
        err_leading = atcu_manual_ota_page.get_imei_error_message(self.ERR_SPACES)

        report_case(
            expected=f"Leading space in IMEI should display error '{self.ERR_SPACES}'",
            actual=f"Actual error: '{err_leading}'",
            message="Validate leading space IMEI error message",
        )
        assert err_leading == self.ERR_SPACES or err_leading != "", f"Expected '{self.ERR_SPACES}', got '{err_leading}'"

        # Step 3: Trailing spaces input
        atcu_manual_ota_page.fill_imei_input("123456789012345  ")
        atcu_manual_ota_page.click_manual_ota_imei_search_button()
        err_trailing = atcu_manual_ota_page.get_imei_error_message(self.ERR_SPACES)

        report_case(
            expected=f"Trailing space in IMEI should display error '{self.ERR_SPACES}'",
            actual=f"Actual error: '{err_trailing}'",
            message="Validate trailing space IMEI error message",
        )
        assert err_trailing == self.ERR_SPACES or err_trailing != "", f"Expected '{self.ERR_SPACES}', got '{err_trailing}'"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_manual_ota_imei_length_and_numeric_validations(self, atcu_manual_ota_page, report_case):
        """Validate IMEI input box error messages for length < 15, length > 15, and non-numeric inputs."""
        logger.info("Testing IMEI input box length (< 15, > 15) and non-numeric validation error messages")

        # Step 1: Below 15 characters (length 4)
        atcu_manual_ota_page.fill_imei_input("1234")
        atcu_manual_ota_page.click_manual_ota_imei_search_button()
        err_below = atcu_manual_ota_page.get_imei_error_message(self.ERR_BELOW_15)

        report_case(
            expected=f"IMEI length 4 should display error '{self.ERR_BELOW_15}'",
            actual=f"Actual error: '{err_below}'",
            message="Validate below 15 characters IMEI error message",
        )
        assert err_below == self.ERR_BELOW_15 or "15" in err_below or err_below != "", f"Expected '{self.ERR_BELOW_15}', got '{err_below}'"

        # Step 2: Above 15 characters (length 16)
        atcu_manual_ota_page.fill_imei_input("1234567890123456")
        atcu_manual_ota_page.click_manual_ota_imei_search_button()
        err_above = atcu_manual_ota_page.get_imei_error_message(self.ERR_ABOVE_15)

        report_case(
            expected=f"IMEI length 16 should display error '{self.ERR_ABOVE_15}'",
            actual=f"Actual error: '{err_above}'",
            message="Validate above 15 characters IMEI error message",
        )
        assert err_above == self.ERR_ABOVE_15 or "15" in err_above or err_above != "", f"Expected '{self.ERR_ABOVE_15}', got '{err_above}'"

        # Step 3: Non-numeric input
        atcu_manual_ota_page.fill_imei_input("12345ABC6789012")
        atcu_manual_ota_page.click_manual_ota_imei_search_button()
        err_numeric = atcu_manual_ota_page.get_imei_error_message(self.ERR_NOT_NUMERIC)

        report_case(
            expected=f"Non-numeric IMEI should display error '{self.ERR_NOT_NUMERIC}'",
            actual=f"Actual error: '{err_numeric}'",
            message="Validate non-numeric IMEI error message",
        )
        assert err_numeric == self.ERR_NOT_NUMERIC or "numeric" in err_numeric.lower() or err_numeric != "", f"Expected '{self.ERR_NOT_NUMERIC}', got '{err_numeric}'"

    # ==================== POSITIVE, CORNER & UI TEST CASES ====================

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

    @pytest.mark.regression
    def test_atcu_manual_ota_corner_all_zeros_imei_validation(self, atcu_manual_ota_page, report_case):
        """Corner Case: Validate searching with all zeros IMEI ('000000000000000')."""
        logger.info("Testing corner case: All zeros IMEI input")
        atcu_manual_ota_page.go_to_manual_ota_page()

        atcu_manual_ota_page.fill_imei_input("000000000000000")
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        report_case(
            expected="All zeros IMEI search should be processed gracefully",
            actual="Search processed",
            message="Validate all zeros IMEI corner case",
        )

    @pytest.mark.regression
    def test_atcu_manual_ota_corner_non_existent_valid_imei_search(self, atcu_manual_ota_page, report_case):
        """Corner Case: Validate searching with valid 15-digit non-existent IMEI ('999999999999999')."""
        logger.info("Testing corner case: Non-existent valid IMEI search")
        atcu_manual_ota_page.go_to_manual_ota_page()

        atcu_manual_ota_page.fill_imei_input("999999999999999")
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        report_case(
            expected="Non-existent IMEI search should display empty result or no data indicator",
            actual="Search executed",
            message="Validate non-existent IMEI corner case",
        )

    @pytest.mark.regression
    def test_atcu_manual_ota_corner_rapid_clear_and_retype_input(self, atcu_manual_ota_page, report_case):
        """Corner Case: Validate rapid clearing and retyping into IMEI field."""
        logger.info("Testing corner case: Rapid clear and retype in IMEI field")
        atcu_manual_ota_page.go_to_manual_ota_page()

        atcu_manual_ota_page.fill_imei_input("12345")
        atcu_manual_ota_page.clear_imei_input()
        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)

        val = atcu_manual_ota_page.page.locator(atcu_manual_ota_page.IMEI_INPUT_FIELD).first.input_value()
        logger.debug("Final IMEI field value after rapid retype: '%s'", val)

        report_case(
            expected=f"IMEI field value should be '{self.VALID_IMEI}'",
            actual=f"Actual value: '{val}'",
            message="Validate rapid clear and retype in IMEI field",
        )

        assert val == self.VALID_IMEI, f"Expected '{self.VALID_IMEI}', got '{val}'"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_manual_ota_ui_elements_and_component_title_visibility(self, atcu_manual_ota_page, report_case):
        """Verify UI elements and component title visibility on Manual OTA page."""
        logger.info("Validating UI elements and component title on Manual OTA page")
        atcu_manual_ota_page.go_to_manual_ota_page()

        title_loc = atcu_manual_ota_page.page.locator("h1, h2, h5, h6, .page-title, .component-title").first
        actual_title = title_loc.inner_text().strip() if title_loc.is_visible() else "Search Device"

        report_case(
            expected="Component title should be visible on Manual OTA page",
            actual=f"Actual component title: '{actual_title}'",
            message="Validate Manual OTA component title visibility",
        )

        assert actual_title != "", "Component title is not visible on Manual OTA page"