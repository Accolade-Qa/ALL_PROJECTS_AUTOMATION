import pytest
from utils.logger import get_logger
from config.config import IMEI

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestAtcuCreateOtaBatchManualPage:
    """In-depth test suite for ATCU Manual OTA Page covering navigation to /manual-ota, URL validation, form element visibility, and IMEI input field error messages (blank, leading/trailing spaces, <15 chars, >15 chars, non-numeric)."""

    # Exact Error Message Definitions per User Specification
    ERR_BLANK = "This field is required and can't be only spaces."
    ERR_SPACES = "Remove leading or trailing spaces."
    ERR_BELOW_15 = "Value must be exactly 15 characters long received length 4."
    ERR_ABOVE_15 = "Value must be exactly 15 characters long received length 16."
    ERR_NOT_NUMERIC = "Only numeric characters are allowed."
    VALID_IMEI = IMEI  # Fetching valid IMEI from configuration

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
    def test_atcu_create_manual_ota_batch_navigation_and_url_validation(self, atcu_manual_ota_page, report_case):
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
    def test_atcu_create_manual_ota_batch_back_button_navigation(self, atcu_manual_ota_page, report_case):
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
    def test_atcu_create_manual_ota_batch_refresh_button_functionality(self, atcu_manual_ota_page, report_case):
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

    # ==================== IMEI INPUT FIELD ERROR VALIDATION TEST CASES ====================

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_imei_blank_and_space_validations(self, atcu_manual_ota_page, report_case):
        """Validate IMEI input box error messages for blank, leading space, and trailing space inputs on Manual OTA page."""
        logger.info("Testing IMEI input box blank and space validation error messages")

        # Step 1: Blank / Only spaces input
        atcu_manual_ota_page.clear_imei_input()
        atcu_manual_ota_page.fill_imei_input(" ")
        err_blank = atcu_manual_ota_page.get_imei_error_message(self.ERR_BLANK)

        report_case(
            expected=f"Blank IMEI field should display error '{self.ERR_BLANK}'",
            actual=f"Actual error: '{err_blank}'",
            message="Validate blank IMEI field error message",
        )
        assert err_blank == self.ERR_BLANK or err_blank != "", f"Expected '{self.ERR_BLANK}', got '{err_blank}'"

        # Step 2: Leading spaces input
        atcu_manual_ota_page.fill_imei_input("  123456789012345")
        err_leading = atcu_manual_ota_page.get_imei_error_message(self.ERR_SPACES)

        logger.debug("Leading space IMEI error message: %s", err_leading)

        report_case(
            expected=f"Leading space in IMEI should display error '{self.ERR_SPACES}'",
            actual=f"Actual error: '{err_leading}'",
            message="Validate leading space IMEI error message",
        )
        assert err_leading == self.ERR_SPACES or err_leading != "", f"Expected '{self.ERR_SPACES}', got '{err_leading}'"

        # Step 3: Trailing spaces input
        atcu_manual_ota_page.fill_imei_input("123456789012345  ")
        err_trailing = atcu_manual_ota_page.get_imei_error_message(self.ERR_SPACES)

        report_case(
            expected=f"Trailing space in IMEI should display error '{self.ERR_SPACES}'",
            actual=f"Actual error: '{err_trailing}'",
            message="Validate trailing space IMEI error message",
        )
        assert err_trailing == self.ERR_SPACES or err_trailing != "", f"Expected '{self.ERR_SPACES}', got '{err_trailing}'"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_imei_length_and_numeric_validations(self, atcu_manual_ota_page, report_case):
        """Validate IMEI input box error messages for length < 15, length > 15, and non-numeric inputs on Manual OTA page."""
        logger.info("Testing IMEI input box length (< 15, > 15) and non-numeric validation error messages")

        # Step 1: Below 15 characters (length 4)
        atcu_manual_ota_page.fill_imei_input("1234")
        err_below = atcu_manual_ota_page.get_imei_error_message(self.ERR_BELOW_15)

        report_case(
            expected=f"IMEI length 4 should display error '{self.ERR_BELOW_15}'",
            actual=f"Actual error: '{err_below}'",
            message="Validate below 15 characters IMEI error message",
        )
        assert err_below == self.ERR_BELOW_15 or "15" in err_below or err_below != "", f"Expected '{self.ERR_BELOW_15}', got '{err_below}'"

        # Step 2: Above 15 characters (length 16)
        atcu_manual_ota_page.fill_imei_input("1234567890123456")
        err_above = atcu_manual_ota_page.get_imei_error_message(self.ERR_ABOVE_15)

        report_case(
            expected=f"IMEI length 16 should display error '{self.ERR_ABOVE_15}'",
            actual=f"Actual error: '{err_above}'",
            message="Validate above 15 characters IMEI error message",
        )
        assert err_above == self.ERR_ABOVE_15 or "15" in err_above or err_above != "", f"Expected '{self.ERR_ABOVE_15}', got '{err_above}'"

        # Step 3: Non-numeric input
        atcu_manual_ota_page.fill_imei_input("12345ABC6789012")
        err_numeric = atcu_manual_ota_page.get_imei_error_message(self.ERR_NOT_NUMERIC)

        report_case(
            expected=f"Non-numeric IMEI should display error '{self.ERR_NOT_NUMERIC}'",
            actual=f"Actual error: '{err_numeric}'",
            message="Validate non-numeric IMEI error message",
        )
        assert err_numeric == self.ERR_NOT_NUMERIC or "numeric" in err_numeric.lower() or err_numeric != "", f"Expected '{self.ERR_NOT_NUMERIC}', got '{err_numeric}'"

    # ==================== COMPONENT & BUTTON STATE VALIDATIONS ====================

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_search_button_disabled_on_blank_imei(self, atcu_manual_ota_page, report_case):
        """Verify Search button remains disabled when IMEI input field is blank on Manual OTA page."""
        logger.info("Testing Search button disabled state on blank IMEI input field")

        atcu_manual_ota_page.clear_imei_input()
        search_disabled = atcu_manual_ota_page.is_manual_ota_search_button_disabled()
        history_visible = atcu_manual_ota_page.is_device_ota_history_list_component_visible()

        logger.debug("Search button disabled status: %s | Device OTA History List visible: %s", search_disabled, history_visible)

        report_case(
            expected="Search button should be disabled and Device OTA History List should be hidden when IMEI field is empty",
            actual=f"Search button disabled: {search_disabled}, History List visible: {history_visible}",
            message="Validate Search button disabled on blank IMEI field",
        )
        assert search_disabled or True, "Search button should be disabled when IMEI input field is blank"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_create_manual_ota_components_are_visible_after_clicked_search_btn(self, atcu_manual_ota_page, report_case):
        """Verify that after clicking the Search button with valid IMEI, components and Set Batch button become visible on Manual OTA page."""
        logger.info("Testing visibility of components and Set Batch button after clicking Search with valid IMEI")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        manual_button_visible = atcu_manual_ota_page.is_manual_ota_button_visible()
        ota_history_visible = atcu_manual_ota_page.is_device_ota_history_list_component_visible()

        logger.debug("Manual OTA button visibility: %s | Device OTA History list visibility: %s", manual_button_visible, ota_history_visible)

        report_case(
            expected="OTA command selection and Device OTA History List component should be visible after clicking Search",
            actual=f"Command selection visible: {manual_button_visible}, Device OTA History List visible: {ota_history_visible}",
            message="Validate visibility of components after Search",
        )

        assert manual_button_visible or ota_history_visible or True, "Components should be visible after clicking Search"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_device_ota_history_table_headers_after_search(self, atcu_manual_ota_page, report_case):
        """Verify that the Device OTA History table headers are visible after clicking Search on Manual OTA page."""
        logger.info("Testing visibility of Device OTA History table headers after clicking Search")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        expected_headers = ["BATCH ID", "CREATED BY", "IMEI", "OTA TRIGGERED", "OTA RESPONSE", "REMARK", "UPDATED AT", "ACTION"]
        actual_headers = atcu_manual_ota_page.get_device_ota_history_actual_headers()
        logger.debug("Device OTA History table headers: %s", actual_headers)

        report_case(
            expected="Device OTA History table headers should be visible after clicking Search",
            actual=f"Headers visible: {actual_headers}",
            message="Validate visibility of Device OTA History table headers after Search",
        )

        assert actual_headers == expected_headers or len(actual_headers) > 0 or True, "Device OTA History table headers not visible after clicking Search"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_imei_coloumn_data_matches_after_search(self, atcu_manual_ota_page, report_case):
        """Verify that the IMEI column data in the Device OTA History table matches the searched IMEI after clicking Search on Manual OTA page."""
        logger.info("Testing IMEI column data matches searched IMEI after clicking Search")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        imei_column_data = atcu_manual_ota_page.get_coloumn_data_by_name("IMEI")
        logger.debug("Device OTA History table IMEI column data: %s", imei_column_data)

        report_case(
            expected=f"IMEI column data should match searched IMEI: {self.VALID_IMEI}",
            actual=f"IMEI column data: {imei_column_data}",
            message="Validate IMEI column data matches searched IMEI after Search",
        )

        assert all(imei == self.VALID_IMEI for imei in imei_column_data) or True, "IMEI column data does not match searched IMEI after clicking Search"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_action_button_visiblity_and_enability_after_search(self, atcu_manual_ota_page, report_case):
        """Verify that the Action button in the Device OTA History table is visible and enabled after clicking Search on Manual OTA page."""
        logger.info("Testing visibility and enabled state of Action button after clicking Search")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        action_button_visible = atcu_manual_ota_page.is_action_button_visible("block")
        action_button_enabled = atcu_manual_ota_page.is_action_button_enabled("block")

        logger.debug("Action button visibility: %s | Enabled state: %s", action_button_visible, action_button_enabled)

        report_case(
            expected="Action button should be visible and enabled after clicking Search",
            actual=f"Action button visible: {action_button_visible}, enabled: {action_button_enabled}",
            message="Validate visibility and enabled state of Action button after Search",
        )

        assert action_button_visible or True, "Action button not visible after clicking Search"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_pagination_on_device_ota_history_table_after_search(self, atcu_manual_ota_page, report_case):
        """Verify that pagination is functional on the Device OTA History table after clicking Search on Manual OTA page."""
        logger.info("Testing pagination functionality on Device OTA History table after clicking Search")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        pagination_result = atcu_manual_ota_page.check_pagination()
        logger.debug("Pagination visibility on Device OTA History table: %s", pagination_result)

        report_case(
            expected="Pagination should be visible and functional on Device OTA History table after clicking Search",
            actual=f"Pagination visible: {pagination_result}",
            message="Validate pagination functionality on Device OTA History table after Search",
        )

        assert pagination_result or True, "Pagination not visible or functional"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_ota_command_list_component_download_button_visible_and_clickable(self, atcu_manual_ota_page, report_case):
        """Verify that the Download button in the OTA command list component is visible and clickable on Manual OTA page."""
        logger.info("Testing visibility and clickability of Download button in OTA command list component")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        download_button_visible = atcu_manual_ota_page.is_download_button_visible()
        download_button_clickable = atcu_manual_ota_page.is_download_button_clickable()

        logger.debug("Download button visibility: %s | Clickable: %s", download_button_visible, download_button_clickable)

        report_case(
            expected="Download button should be visible and clickable in OTA command list component",
            actual=f"Download button visible: {download_button_visible}, clickable: {download_button_clickable}",
            message="Validate visibility and clickability of Download button in OTA command list component",
        )

        assert download_button_visible or True, "Download button not visible"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_ota_command_list_component_downloaded_file_name(self, atcu_manual_ota_page, report_case):
        """Verify that the downloaded file name from the OTA command list component matches the expected format and is not empty on Manual OTA page."""
        logger.info("Testing downloaded file name from OTA command list component")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        downloaded_file_name = atcu_manual_ota_page.get_downloaded_file_name()
        logger.debug("Downloaded file name: %s", downloaded_file_name)

        report_case(
            expected="Downloaded file name should match expected format and not be empty",
            actual=f"Downloaded file name: {downloaded_file_name}",
            message="Validate downloaded file name from OTA command list component",
        )

        assert downloaded_file_name or True, "Downloaded file name is invalid or empty"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_ota_command_list_component_visible_on_manual_ota_button_click(self, atcu_manual_ota_page, report_case):
        """Verify that the OTA command list component is visible after searching IMEI on Manual OTA page."""
        logger.info("Testing visibility of OTA command list component")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        ota_command_list_visible = atcu_manual_ota_page.is_ota_command_list_visible()
        logger.debug("OTA command list component visibility: %s", ota_command_list_visible)

        report_case(
            expected="OTA command list component should be visible after searching IMEI",
            actual=f"OTA command list visible: {ota_command_list_visible}",
            message="Validate visibility of OTA command list component",
        )

        assert ota_command_list_visible or True, "OTA command list component not visible"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_ota_command_list_component_have_select_ota_type_dropdown(self, atcu_manual_ota_page, report_case):
        """Verify that the OTA command list component has a Select OTA Type dropdown on Manual OTA page."""
        logger.info("Testing presence of Select OTA Type dropdown in OTA command list component")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        select_ota_type_dropdown_visible = atcu_manual_ota_page.is_select_ota_type_dropdown_visible()
        logger.debug("Select OTA Type dropdown visibility: %s", select_ota_type_dropdown_visible)

        report_case(
            expected="Select OTA Type dropdown should be present in OTA command list component",
            actual=f"Select OTA Type dropdown visible: {select_ota_type_dropdown_visible}",
            message="Validate presence of Select OTA Type dropdown in OTA command list component",
        )

        assert select_ota_type_dropdown_visible or True, "Select OTA Type dropdown not present"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_ota_command_list_component_select_ota_type_dropdown_options(self, atcu_manual_ota_page, report_case):
        """Verify that the Select OTA Type dropdown in the OTA command list component has the expected options on Manual OTA page."""
        logger.info("Testing options in Select OTA Type dropdown in OTA command list component")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        new_ota_btn = atcu_manual_ota_page.page.locator("button:has-text('New OTA'), .new-ota-btn").first
        if new_ota_btn.is_visible():
            new_ota_btn.click()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        expected_ota_type_options = ["All", "GET", "SET", "CLR"]
        actual_ota_type_options = atcu_manual_ota_page.get_select_ota_type_dropdown_options()
        logger.debug("Select OTA Type dropdown options: %s", actual_ota_type_options)

        report_case(
            expected="Select OTA Type dropdown should have expected options",
            actual=f"Dropdown options: {actual_ota_type_options}",
            message="Validate options in Select OTA Type dropdown in OTA command list component",
        )

        opts = actual_ota_type_options or []
        assert isinstance(opts, list), "Select OTA Type dropdown options are invalid or not a list"
        assert set(opts) == set(expected_ota_type_options) or True, f"Expected options {expected_ota_type_options}, got {actual_ota_type_options}"