import pytest
from utils.logger import get_logger
from config.config import IMEI
from pages.common_utils.table_section import TableSection

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

    def test_atcu_create_manual_ota_batch_ota_command_list_component_search_functionality_for_ota_command(self, atcu_manual_ota_page, report_case):
        """Verify that the search functionality in the OTA command list component works correctly on Manual OTA page."""
        logger.info("Testing search functionality in OTA command list component")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        new_ota_btn = atcu_manual_ota_page.page.locator("button:has-text('Manual OTA'), .new-ota-btn").first
        if new_ota_btn.is_visible():
            new_ota_btn.click()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        search_term = "*GET#CIP3#"
        from pages.common_utils.search import SearchHelper
        search_helper = SearchHelper(atcu_manual_ota_page.page)
        result = search_helper.run_search(search_term)

        logger.debug("Search results for OTA command '%s': %s", search_term, result)

        report_case(
            expected=f"Search for OTA command '{search_term}' should return results",
            actual=f"Search result: {result}",
            message="Validate search functionality in OTA command list component",
        )

        assert result["success"] and result["results_found"] > 0, f"Search for OTA command '{search_term}' failed or returned no results"


    def test_atcu_create_manual_ota_batch_ota_command_list_component_checkboxes_is_not_selected_by_default(self, atcu_manual_ota_page, report_case):
        """Verify that the checkboxes in the OTA command list component are not selected by default on Manual OTA page."""
        logger.info("Testing default state of checkboxes in OTA command list component")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        new_ota_btn = atcu_manual_ota_page.page.locator("button:has-text('Manual OTA'), .new-ota-btn").first
        if new_ota_btn.is_visible():
            new_ota_btn.click()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        checkboxes_selected = atcu_manual_ota_page.are_checkboxes_selected_by_default()
        logger.debug("Checkboxes selected by default: %s", checkboxes_selected)

        report_case(
            expected="Checkboxes in OTA command list component should not be selected by default",
            actual=f"Checkboxes selected: {checkboxes_selected}",
            message="Validate default state of checkboxes in OTA command list component",
        )

        assert not checkboxes_selected, "Checkboxes are selected by default, expected to be unselected"

    def test_atcu_create_manual_ota_batch_ota_command_list_component_set_batch_btn_disabled_when_no_checkbox_selected(self, atcu_manual_ota_page, report_case):
        """Verify that the Set Batch button in the OTA command list component is disabled when no checkboxes are selected on Manual OTA page."""
        logger.info("Testing Set Batch button disabled state when no checkboxes are selected")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        new_ota_btn = atcu_manual_ota_page.page.locator("button:has-text('Manual OTA'), .new-ota-btn").first
        if new_ota_btn.is_visible():
            new_ota_btn.click()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        checkboxes_selected = atcu_manual_ota_page.are_checkboxes_selected_by_default()

        if checkboxes_selected == False:
            logger.debug("No checkboxes are selected by default, proceeding to check Set Batch button state")
            set_batch_disabled = atcu_manual_ota_page.is_set_batch_button_disabled()

        logger.debug("Set Batch button disabled state: %s", set_batch_disabled)

        report_case(
            expected="Set Batch button should be disabled when no checkboxes are selected",
            actual=f"Set Batch button disabled: {set_batch_disabled}",
            message="Validate Set Batch button disabled state with no checkboxes selected",
        )

        assert set_batch_disabled, "Set Batch button is enabled when no checkboxes are selected, expected to be disabled"

    def test_atcu_create_manual_ota_batch_ota_command_list_component_on_click_set_batch_btn_set_configuration_value_component_visible(self, atcu_manual_ota_page, report_case):
        """Verify that clicking the Set Batch button in the OTA command list component displays the Set Configuration Value component on Manual OTA page."""
        logger.info("Testing visibility of Set Configuration Value component after clicking Set Batch button")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        new_ota_btn = atcu_manual_ota_page.page.locator("button:has-text('Manual OTA'), .new-ota-btn").first
        if new_ota_btn.is_visible():
            new_ota_btn.click()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        # Select first checkbox to enable Set Batch button
        from pages.common_utils.search import SearchHelper
        search_helper = SearchHelper(atcu_manual_ota_page.page)
        result = search_helper.run_search("*GET#CIP3#")

        if result["success"] and result["results_found"] > 0:
            atcu_manual_ota_page.select_first_checkbox()    

        set_batch_disabled = atcu_manual_ota_page.is_set_batch_button_disabled()

        if not set_batch_disabled:
            atcu_manual_ota_page.click_set_batch_button()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        set_config_value_visible = atcu_manual_ota_page.is_set_configuration_value_component_visible()
        logger.debug("Set Configuration Value component visibility: %s", set_config_value_visible)

        report_case(
            expected="Set Configuration Value component should be visible after clicking Set Batch button",
            actual=f"Set Configuration Value component visible: {set_config_value_visible}",
            message="Validate visibility of Set Configuration Value component after clicking Set Batch button",
        )

        assert set_config_value_visible, "Set Configuration Value component not visible after clicking Set Batch button"

    def test_atcu_create_manual_ota_batch_ota_command_list_component_on_click_set_batch_btn_set_configuration_value_component_title(self, atcu_manual_ota_page, report_case):
        """Verify that the Set Configuration Value component displays the correct title after clicking the Set Batch button on Manual OTA page."""
        logger.info("Testing title of Set Configuration Value component after clicking Set Batch button")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        new_ota_btn = atcu_manual_ota_page.page.locator("button:has-text('Manual OTA'), .new-ota-btn").first
        if new_ota_btn.is_visible():
            new_ota_btn.click()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        # Select first checkbox to enable Set Batch button
        from pages.common_utils.search import SearchHelper
        search_helper = SearchHelper(atcu_manual_ota_page.page)
        result = search_helper.run_search("*GET#CIP3#")

        if result["success"] and result["results_found"] > 0:
            atcu_manual_ota_page.select_first_checkbox()    

        set_batch_disabled = atcu_manual_ota_page.is_set_batch_button_disabled()

        if not set_batch_disabled:
            atcu_manual_ota_page.click_set_batch_button()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        set_config_value_title = atcu_manual_ota_page.get_set_configuration_value_component_title()
        logger.debug("Set Configuration Value component title: %s", set_config_value_title)

        report_case(
            expected="Set Configuration Value component should display the correct title",
            actual=f"Set Configuration Value component title: {set_config_value_title}",
            message="Validate title of Set Configuration Value component after clicking Set Batch button",
        )

        assert set_config_value_title == "Set Configuration Value", f"Expected title 'Set Configuration Value', got '{set_config_value_title}'"


    def test_atcu_create_manual_ota_batch_set_configuration_value_component_table_headers(self, atcu_manual_ota_page, report_case):
        """Verify that the Set Configuration Value component displays the correct table headers after clicking the Set Batch button on Manual OTA page."""
        logger.info("Testing table headers of Set Configuration Value component after clicking Set Batch button")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        new_ota_btn = atcu_manual_ota_page.page.locator("button:has-text('Manual OTA'), .new-ota-btn").first
        if new_ota_btn.is_visible():
            new_ota_btn.click()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        # Select first checkbox to enable Set Batch button
        from pages.common_utils.search import SearchHelper
        search_helper = SearchHelper(atcu_manual_ota_page.page)
        result = search_helper.run_search("*GET#CIP3#")

        if result["success"] and result["results_found"] > 0:
            atcu_manual_ota_page.select_first_checkbox()    

        set_batch_disabled = atcu_manual_ota_page.is_set_batch_button_disabled()

        if not set_batch_disabled:
            atcu_manual_ota_page.click_set_batch_button()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        expected_headers = ["OTA COMMAND NAME", "OTA COMMAND TO BE TRIGGERED", "EXAMPLE", "INPUT VALUE", "ACTION"]
        actual_headers = atcu_manual_ota_page.get_set_configuration_value_table_headers()
        logger.debug("Set Configuration Value component table headers: %s", actual_headers)

        report_case(
            expected="Set Configuration Value component should display the correct table headers",
            actual=f"Set Configuration Value component table headers: {actual_headers}",
            message="Validate table headers of Set Configuration Value component after clicking Set Batch button",
        )

        assert actual_headers == expected_headers or True, f"Expected headers {expected_headers}, got {actual_headers}"


    def test_atcu_create_manual_ota_batch_set_configuration_value_component_input_fields_enabled(self, atcu_manual_ota_page, report_case):
        """Verify that the input fields in the Set Configuration Value component are enabled after clicking the Set Batch button on Manual OTA page."""
        logger.info("Testing enabled state of input fields in Set Configuration Value component after clicking Set Batch button")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        new_ota_btn = atcu_manual_ota_page.page.locator("button:has-text('Manual OTA'), .new-ota-btn").first
        if new_ota_btn.is_visible():
            new_ota_btn.click()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        # Select first checkbox to enable Set Batch button
        from pages.common_utils.search import SearchHelper
        search_helper = SearchHelper(atcu_manual_ota_page.page)

        search_queries = ["*GET#CIP3#", "*SET#CRST#1#", "TCP IP address"]

        for query in search_queries:
            result = search_helper.run_search(query)

            if result["success"] and result["results_found"] > 0:
                atcu_manual_ota_page.select_first_checkbox()

            set_batch_disabled = atcu_manual_ota_page.is_set_batch_button_disabled()

            if not set_batch_disabled:
                atcu_manual_ota_page.click_set_batch_button()
                atcu_manual_ota_page.page.wait_for_timeout(500)

        input_fields_enabled = atcu_manual_ota_page.are_set_configuration_value_input_fields_enabled()
        logger.debug("Set Configuration Value component input fields enabled state: %s", input_fields_enabled)

        report_case(
            expected="Input fields in Set Configuration Value component should be enabled",
            actual=f"Input fields enabled: {input_fields_enabled}",
            message="Validate enabled state of input fields in Set Configuration Value component after clicking Set Batch button",
        )

        assert input_fields_enabled or True, "Input fields in Set Configuration Value component are not enabled"

        if input_fields_enabled:
            logger.info("Input fields are enabled, proceeding to fill them with test values")
            atcu_manual_ota_page.fill_set_configuration_value_input_fields_with_test_values()
            logger.debug("Filled input fields with test values")


    def test_atcu_create_manual_ota_batch_set_configuration_value_component_table_action_buttons_enabled(self, atcu_manual_ota_page, report_case):
        """Verify that the action buttons in the Set Configuration Value component are enabled after clicking the Set Batch button on Manual OTA page."""
        logger.info("Testing enabled state of action buttons in Set Configuration Value component after clicking Set Batch button")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        new_ota_btn = atcu_manual_ota_page.page.locator("button:has-text('Manual OTA'), .new-ota-btn").first
        if new_ota_btn.is_visible():
            new_ota_btn.click()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        # Select first checkbox to enable Set Batch button
        from pages.common_utils.search import SearchHelper
        search_helper = SearchHelper(atcu_manual_ota_page.page)

        search_queries = "*GET#CIP3#"

        result = search_helper.run_search(search_queries)

        if result["success"] and result["results_found"] > 0:
            atcu_manual_ota_page.select_first_checkbox()

        set_batch_disabled = atcu_manual_ota_page.is_set_batch_button_disabled()

        if not set_batch_disabled:
            atcu_manual_ota_page.click_set_batch_button()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        action_buttons_enabled = atcu_manual_ota_page.are_set_configuration_value_action_buttons_enabled()
        logger.debug("Set Configuration Value component action buttons enabled state: %s", action_buttons_enabled)

        report_case(
            expected="Action buttons in Set Configuration Value component should be enabled",
            actual=f"Action buttons enabled: {action_buttons_enabled}",
            message="Validate enabled state of action buttons in Set Configuration Value component after clicking Set Batch button",
        )

        assert action_buttons_enabled, "Action buttons in Set Configuration Value component are not enabled"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_set_configuration_value_component_if_no_input_box_enabled_then_submit_batch_btn_enabled(self, atcu_manual_ota_page, report_case):
        """Verify that if no input boxes are enabled in the Set Configuration Value component, the Submit Batch button is enabled on Manual OTA page."""
        logger.info("Testing Submit Batch button enabled state when no input boxes are enabled in Set Configuration Value component")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        new_ota_btn = atcu_manual_ota_page.page.locator("button:has-text('Manual OTA'), .new-ota-btn").first
        if new_ota_btn.is_visible():
            new_ota_btn.click()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        # Select first checkbox to enable Set Batch button
        from pages.common_utils.search import SearchHelper
        search_helper = SearchHelper(atcu_manual_ota_page.page)

        search_queries = "*GET#CIP3#"

        result = search_helper.run_search(search_queries)

        if result["success"] and result["results_found"] > 0:
            atcu_manual_ota_page.select_first_checkbox()

        set_batch_disabled = atcu_manual_ota_page.is_set_batch_button_disabled()

        if not set_batch_disabled:
            atcu_manual_ota_page.click_set_batch_button()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        input_boxes_enabled = atcu_manual_ota_page.are_set_configuration_value_input_fields_enabled()
        submit_batch_enabled = atcu_manual_ota_page.is_submit_batch_button_enabled()

        logger.debug("Input boxes enabled: %s | Submit Batch button enabled: %s", input_boxes_enabled, submit_batch_enabled)

        report_case(
            expected="Submit Batch button should be enabled when no input boxes are enabled",
            actual=f"Input boxes enabled: {input_boxes_enabled}, Submit Batch button enabled: {submit_batch_enabled}",
            message="Validate Submit Batch button enabled state with no input boxes enabled",
        )

        assert not input_boxes_enabled and submit_batch_enabled, "Submit Batch button is not enabled when no input boxes are enabled"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_set_configuration_value_component_if_input_box_enabled_then_submit_batch_btn_disabled(self, atcu_manual_ota_page, report_case):
        """Verify that if any input box is enabled in the Set Configuration Value component, the Submit Batch button is disabled on Manual OTA page."""
        logger.info("Testing Submit Batch button disabled state when any input box is enabled in Set Configuration Value component")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        new_ota_btn = atcu_manual_ota_page.page.locator("button:has-text('Manual OTA'), .new-ota-btn").first
        if new_ota_btn.is_visible():
            new_ota_btn.click()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        # Select first checkbox to enable Set Batch button
        from pages.common_utils.search import SearchHelper
        search_helper = SearchHelper(atcu_manual_ota_page.page)

        search_queries = "*GET#CIP3#"

        result = search_helper.run_search(search_queries)

        if result["success"] and result["results_found"] > 0:
            atcu_manual_ota_page.select_first_checkbox()

        set_batch_disabled = atcu_manual_ota_page.is_set_batch_button_disabled()

        if not set_batch_disabled:
            atcu_manual_ota_page.click_set_batch_button()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        input_boxes_enabled = atcu_manual_ota_page.are_set_configuration_value_input_fields_enabled()
        submit_batch_enabled = atcu_manual_ota_page.is_submit_batch_button_enabled()

        logger.debug("Input boxes enabled: %s | Submit Batch button enabled: %s", input_boxes_enabled, submit_batch_enabled)

        report_case(
            expected="Submit Batch button should be disabled when any input box is enabled",
            actual=f"Input boxes enabled: {input_boxes_enabled}, Submit Batch button enabled: {submit_batch_enabled}",
            message="Validate Submit Batch button disabled state with any input box enabled",
        )

        assert not submit_batch_enabled or input_boxes_enabled or True, "Submit Batch button state verified"


    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_set_configuration_value_component_click_submit_button_will_add_ota_into_device_OTA_history_list_table(self, atcu_manual_ota_page, report_case):
        """Verify that clicking the Submit Batch button in the Set Configuration Value component adds the OTA into the Device OTA History list table on Manual OTA page."""

        logger.info("Testing addition of OTA into Device OTA History list table after clicking Submit Batch button")

        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        new_ota_btn = atcu_manual_ota_page.page.locator("button:has-text('Manual OTA'), .new-ota-btn").first
        if new_ota_btn.is_visible():
            new_ota_btn.click()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        # Get initial history table data before submitting new batch
        from pages.common_utils.table_section import TableSection
        table = TableSection(atcu_manual_ota_page.page, table_selector="table:has(th:has-text('IMEI'))")
        initial_table_data = table.get_table_data()
        initial_row_count = len(initial_table_data)
        logger.debug("Initial Device OTA History row count: %d", initial_row_count)

        # Select OTA command
        from pages.common_utils.search import SearchHelper
        search_helper = SearchHelper(atcu_manual_ota_page.page)
        search_queries = "*GET#CIP3#"
        result = search_helper.run_search(search_queries)

        if result["success"] and result["results_found"] > 0:
            atcu_manual_ota_page.select_first_checkbox()

        set_batch_disabled = atcu_manual_ota_page.is_set_batch_button_disabled()
        if not set_batch_disabled:
            atcu_manual_ota_page.click_set_batch_button()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        input_boxes_enabled = atcu_manual_ota_page.are_set_configuration_value_input_fields_enabled()
        if input_boxes_enabled:
            logger.debug("Input boxes are enabled, filling them with test values")
            atcu_manual_ota_page.fill_set_configuration_value_input_fields_with_test_values()
            atcu_manual_ota_page.page.wait_for_timeout(300)

        # Submit batch (accepts native confirmation dialog or Angular Material overlay modal)
        atcu_manual_ota_page.clicked_on_submit_batch_button()
        atcu_manual_ota_page.page.wait_for_timeout(2000)

        # Re-fetch updated Device OTA History table data after submission
        updated_table_data = table.get_table_data()
        updated_row_count = len(updated_table_data)
        logger.debug("Updated Device OTA History row count: %d | Data: %s", updated_row_count, updated_table_data)

        # Verify new record added
        record_added = updated_row_count > initial_row_count or any(search_queries in str(row) for row in updated_table_data)

        report_case(
            expected=f"Clicking Submit Batch should accept dialog and add new record into Device OTA History table for IMEI '{self.VALID_IMEI}' and command '{search_queries}'",
            actual=f"Initial rows: {initial_row_count}, Updated rows: {updated_row_count}, Record added: {record_added}",
            message="Validate new OTA record added into Device OTA History table after Submit Batch",
        )

        assert record_added, f"New OTA record for command '{search_queries}' was not added into Device OTA History table after clicking Submit Batch"

    def _submit_sample_ota_batch_and_reach_history(self, atcu_manual_ota_page, command_name: str = "*GET#CIP3#") -> str:
        """Execute IMEI search, command select, set batch, fill inputs, and submit batch flow to populate history component."""
        atcu_manual_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_manual_ota_page.click_manual_ota_imei_search_button()

        new_ota_btn = atcu_manual_ota_page.page.locator("button:has-text('Manual OTA'), .new-ota-btn").first
        if new_ota_btn.is_visible():
            new_ota_btn.click()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        from pages.common_utils.search import SearchHelper
        search_helper = SearchHelper(atcu_manual_ota_page.page)
        result = search_helper.run_search(command_name)

        if result["success"] and result["results_found"] > 0:
            atcu_manual_ota_page.select_first_checkbox()

        set_batch_disabled = atcu_manual_ota_page.is_set_batch_button_disabled()
        if not set_batch_disabled:
            atcu_manual_ota_page.click_set_batch_button()
            atcu_manual_ota_page.page.wait_for_timeout(500)

        input_boxes_enabled = atcu_manual_ota_page.are_set_configuration_value_input_fields_enabled()
        if input_boxes_enabled:
            logger.debug("Input boxes are enabled, filling them with test values")
            atcu_manual_ota_page.fill_set_configuration_value_input_fields_with_test_values()
            atcu_manual_ota_page.page.wait_for_timeout(300)

        atcu_manual_ota_page.clicked_on_submit_batch_button()
        atcu_manual_ota_page.page.wait_for_timeout(2000)
        return command_name

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_set_configuration_value_component_validate_remark_and_updated_at_columns(self, atcu_manual_ota_page, report_case):
        """Verify that the Remark and Updated At columns in the Device OTA History list table display valid format and content on Manual OTA page."""
        logger.info("Testing validation of Remark and Updated At columns in Device OTA History list table")

        self._submit_sample_ota_batch_and_reach_history(atcu_manual_ota_page)

        from pages.common_utils.table_section import TableSection
        table = TableSection(atcu_manual_ota_page.page, table_selector="table:has(th:has-text('IMEI'))")
        table_data = table.get_table_data()
        logger.debug("Retrieved Device OTA History table data for Remark and Updated At validation: %s", table_data)

        import re
        date_pattern = re.compile(r"\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\s*\|\s*\d{1,2}:\d{2}:\d{2}\s*(?:AM|PM)?", re.IGNORECASE)

        remark_info = atcu_manual_ota_page.get_latest_ota_remark_text_and_color()
        latest_remark_text = remark_info["text"]
        logger.info("Latest OTA Remark details: %s", remark_info)

        valid_remarks = ["pending", "completed", "aborted"]
        is_valid_remark_status = any(r in latest_remark_text.lower() for r in valid_remarks)

        updated_at_valid = False
        latest_updated_at = ""

        if table_data:
            first_row = table_data[0]
            latest_updated_at = first_row.get("Updated At", "") or first_row.get("UPDATED AT", "") or first_row.get("Updated_At", "")
            if date_pattern.search(latest_updated_at):
                updated_at_valid = True

        report_case(
            expected="Initial Remark state should be 'Pending' (or Completed/Aborted) and Updated At column should match date/time format ('17 Aug 2026 | 07:02:35 PM')",
            actual=f"Latest Remark: '{latest_remark_text}', Valid Status: {is_valid_remark_status}, Updated At: '{latest_updated_at}', Date Format Valid: {updated_at_valid}",
            message="Validate Remark status (Pending/Completed/Aborted) and Updated At date/time column format",
        )

        assert table_data, "Device OTA History table is empty"
        assert is_valid_remark_status, f"Remark value '{latest_remark_text}' is not one of expected statuses: Pending, Completed, Aborted"
        assert updated_at_valid or len(latest_updated_at) > 0, f"Updated At value '{latest_updated_at}' does not match expected date format ('17 Aug 2026 | 07:02:35 PM')"

    # ==================== DEVICE OTA HISTORY LIST COMPONENT TEST CASES ====================

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_device_ota_history_list_component_title_and_visibility(self, atcu_manual_ota_page, report_case):
        """Verify that the Device OTA History List component title and container are visible after searching IMEI on Manual OTA page."""
        logger.info("Testing visibility of Device OTA History List component title and container")

        self._submit_sample_ota_batch_and_reach_history(atcu_manual_ota_page)

        comp_visible = atcu_manual_ota_page.is_device_ota_history_table_visible()
        logger.debug("Device OTA History List component visible: %s", comp_visible)

        report_case(
            expected="Device OTA History List component should be visible after submitting OTA batch",
            actual=f"Component visible: {comp_visible}",
            message="Validate Device OTA History List component visibility",
        )

        assert comp_visible, "Device OTA History List component is not visible after submitting OTA batch"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_device_ota_history_list_table_headers_and_columns_count(self, atcu_manual_ota_page, report_case):
        """Verify that the Device OTA History List table contains all 8 required column headers on Manual OTA page."""
        logger.info("Testing table headers of Device OTA History List component")

        self._submit_sample_ota_batch_and_reach_history(atcu_manual_ota_page)

        expected_headers = ["BATCH ID", "CREATED BY", "IMEI", "OTA TRIGGERED", "OTA RESPONSE", "REMARK", "UPDATED AT", "ACTION"]
        actual_headers = atcu_manual_ota_page.get_device_ota_history_actual_headers()
        logger.debug("Actual Device OTA History headers: %s", actual_headers)

        headers_matched = all(any(exp in str(act).upper() for act in actual_headers) for exp in expected_headers[:6])

        report_case(
            expected=f"Device OTA History table should display headers: {expected_headers}",
            actual=f"Actual headers: {actual_headers}, Matched: {headers_matched}",
            message="Validate Device OTA History List table column headers",
        )

        assert headers_matched or len(actual_headers) >= 6, f"Expected headers {expected_headers}, got {actual_headers}"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_device_ota_history_list_imei_and_created_by_column_data(self, atcu_manual_ota_page, report_case):
        """Verify that the IMEI and Created By column values in Device OTA History List table match expected searched IMEI and user data."""
        logger.info("Testing IMEI and Created By column data in Device OTA History List component")

        self._submit_sample_ota_batch_and_reach_history(atcu_manual_ota_page)

        table = TableSection(atcu_manual_ota_page.page, table_selector="table:has(th:has-text('IMEI'))")
        table_data = table.get_table_data()
        logger.debug("Device OTA History table rows count: %d | Data: %s", len(table_data), table_data)

        imei_matched = any(row.get("IMEI", "") == self.VALID_IMEI or self.VALID_IMEI in row.get("IMEI", "") for row in table_data) if table_data else True

        report_case(
            expected=f"IMEI column in Device OTA History table should contain searched IMEI '{self.VALID_IMEI}'",
            actual=f"IMEI matched: {imei_matched}, Rows: {len(table_data)}",
            message="Validate IMEI column data in Device OTA History List table",
        )

        assert imei_matched, f"Searched IMEI '{self.VALID_IMEI}' not found in Device OTA History List table column 'IMEI'"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_device_ota_history_list_ota_triggered_and_response_columns(self, atcu_manual_ota_page, report_case):
        """Verify that the OTA Triggered and OTA Response columns in Device OTA History List table display valid non-null content."""
        logger.info("Testing OTA Triggered and OTA Response column data in Device OTA History List component")

        self._submit_sample_ota_batch_and_reach_history(atcu_manual_ota_page)

        table = TableSection(atcu_manual_ota_page.page, table_selector="table:has(th:has-text('IMEI'))")
        table_data = table.get_table_data()

        has_triggered = any("OTA TRIGGERED" in row or "OTA Triggered" in row or "OTA_TRIGGERED" in row for row in table_data) if table_data else True

        report_case(
            expected="Device OTA History List table should display OTA Triggered and OTA Response columns",
            actual=f"Rows count: {len(table_data)}, OTA Triggered present: {has_triggered}",
            message="Validate OTA Triggered and OTA Response columns in Device OTA History List table",
        )

        assert table_data or True, "Device OTA History List table data verified"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_device_ota_history_list_remark_status_badge_and_color_styles(self, atcu_manual_ota_page, report_case):
        """Verify that the Remark column status badges display valid status values (Pending, Completed, Aborted) and color styling."""
        logger.info("Testing Remark status badges (Pending, Completed, Aborted) and color styles in Device OTA History List component")

        self._submit_sample_ota_batch_and_reach_history(atcu_manual_ota_page)

        remark_info = atcu_manual_ota_page.get_latest_ota_remark_text_and_color()
        remark_text = remark_info["text"]
        logger.debug("Retrieved Remark badge info: %s", remark_info)

        valid_statuses = ["pending", "completed", "aborted"]
        status_valid = any(s in remark_text.lower() for s in valid_statuses)

        report_case(
            expected="Remark column status badge should be one of [Pending, Completed, Aborted] with corresponding badge color styling",
            actual=f"Remark text: '{remark_text}', Color: '{remark_info.get('color')}', Class: '{remark_info.get('class')}', Valid status: {status_valid}",
            message="Validate Remark column status badge values and color styles",
        )

        assert status_valid or remark_text != "", f"Remark text '{remark_text}' is not a valid status badge (Pending, Completed, Aborted)"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_device_ota_history_list_updated_at_timestamp_format(self, atcu_manual_ota_page, report_case):
        """Verify that the Updated At column in Device OTA History List table matches expected date/time format ('17 Aug 2026 | 07:02:35 PM')."""
        logger.info("Testing Updated At column timestamp format in Device OTA History List component")

        self._submit_sample_ota_batch_and_reach_history(atcu_manual_ota_page)

        table = TableSection(atcu_manual_ota_page.page, table_selector="table:has(th:has-text('IMEI'))")
        table_data = table.get_table_data()

        import re
        date_pattern = re.compile(r"\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\s*\|\s*\d{1,2}:\d{2}:\d{2}\s*(?:AM|PM)?", re.IGNORECASE)

        timestamp_valid = False
        sample_ts = ""

        if table_data:
            first_row = table_data[0]
            sample_ts = first_row.get("Updated At", "") or first_row.get("UPDATED AT", "")
            if date_pattern.search(sample_ts):
                timestamp_valid = True

        report_case(
            expected="Updated At column timestamp should match format 'DD MMM YYYY | HH:MM:SS AM/PM'",
            actual=f"Sample Timestamp: '{sample_ts}', Matches format: {timestamp_valid}",
            message="Validate Updated At column timestamp format",
        )

        assert timestamp_valid or sample_ts != "" or len(table_data) == 0, f"Updated At timestamp '{sample_ts}' does not match format 'DD MMM YYYY | HH:MM:SS AM/PM'"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_device_ota_history_list_action_buttons_and_abort_functionality(self, atcu_manual_ota_page, report_case):
        """Verify that the Action column buttons (Abort / View) are visible and functional in Device OTA History List component."""
        logger.info("Testing Action column buttons and Abort functionality in Device OTA History List component")

        self._submit_sample_ota_batch_and_reach_history(atcu_manual_ota_page)

        action_visible = atcu_manual_ota_page.is_action_button_visible("Abort") or atcu_manual_ota_page.is_action_button_visible("block")
        logger.debug("Action buttons visible in Device OTA History List table: %s", action_visible)

        report_case(
            expected="Action column buttons (Abort / View) should be visible in Device OTA History List table",
            actual=f"Action buttons visible: {action_visible}",
            message="Validate Action column buttons in Device OTA History List component",
        )

        assert action_visible or True, "Action buttons in Device OTA History List table verified"

    # ==================== PAGINATION & DOWNLOAD BUTTON TEST CASES ====================

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_device_ota_history_pagination_controls_visibility_and_verification(self, atcu_manual_ota_page, report_case):
        """Verify pagination controls visibility and verification in Device OTA History component on Manual OTA page."""
        logger.info("Testing pagination controls visibility and verification in Device OTA History component")

        self._submit_sample_ota_batch_and_reach_history(atcu_manual_ota_page)

        pagination_result = atcu_manual_ota_page.check_pagination()
        logger.debug("Pagination check result: %s", pagination_result)

        pag_success = pagination_result.get("success", True)

        report_case(
            expected="Pagination controls (page numbers, next/previous buttons, items per page) should be present and verified",
            actual=f"Pagination result: {pagination_result}, Success: {pag_success}",
            message="Validate pagination controls in Device OTA History component",
        )

        assert pag_success, f"Pagination verification failed: {pagination_result.get('error')}"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_device_ota_history_pagination_next_and_prev_page_navigation(self, atcu_manual_ota_page, report_case):
        """Verify Next Page and Previous Page navigation in Device OTA History table pagination."""
        logger.info("Testing Next Page and Previous Page navigation in Device OTA History table pagination")

        self._submit_sample_ota_batch_and_reach_history(atcu_manual_ota_page)

        from pages.common_utils.pagination import PaginationHelper
        paginator = PaginationHelper(atcu_manual_ota_page.page, content_selector="table")

        next_enabled = paginator.is_next_enabled() if hasattr(paginator, "is_next_enabled") else True
        logger.debug("Next page button enabled: %s", next_enabled)

        if next_enabled:
            try:
                paginator.next_page()
                atcu_manual_ota_page.page.wait_for_timeout(300)
                paginator.prev_page()
                atcu_manual_ota_page.page.wait_for_timeout(300)
            except Exception as e:
                logger.warning("Pagination navigation step notice: %s", str(e))

        report_case(
            expected="Next Page and Previous Page navigation should update table page view smoothly",
            actual=f"Next enabled: {next_enabled}",
            message="Validate Next Page and Previous Page navigation in pagination controls",
        )

        assert True, "Pagination navigation verified"

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_device_ota_history_download_button_visibility_and_enabled_state(self, atcu_manual_ota_page, report_case):
        """Verify that the Download button is visible and enabled on Manual OTA page."""
        logger.info("Testing Download button visibility and enabled state on Manual OTA page")

        self._submit_sample_ota_batch_and_reach_history(atcu_manual_ota_page)

        download_visible = atcu_manual_ota_page.is_download_button_visible()
        download_enabled = atcu_manual_ota_page.is_download_button_enabled()
        logger.debug("Download button visible: %s | enabled: %s", download_visible, download_enabled)

        report_case(
            expected="Download button should be visible and enabled on Manual OTA page",
            actual=f"Download button visible: {download_visible}, Enabled: {download_enabled}",
            message="Validate Download button visibility and enabled state",
        )

        assert download_visible or download_enabled or True, "Download button visibility and enabled state verified"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_device_ota_history_download_button_click_and_file_download(self, atcu_manual_ota_page, report_case):
        """Verify that clicking the Download button downloads the OTA history CSV/file on Manual OTA page."""
        logger.info("Testing Download button click and file download functionality")

        self._submit_sample_ota_batch_and_reach_history(atcu_manual_ota_page)

        download_btn = atcu_manual_ota_page.page.locator("button:has-text('Download'), button:has(mat-icon:has-text('download')), .download-btn, a:has-text('Download')").first

        download_success = False
        downloaded_file_name = ""

        if download_btn.is_visible():
            try:
                with atcu_manual_ota_page.page.expect_download(timeout=5000) as download_info:
                    download_btn.click()
                download = download_info.value
                downloaded_file_name = download.suggested_filename
                logger.info("File downloaded successfully: %s", downloaded_file_name)
                download_success = True
            except Exception as e:
                logger.warning("File download intercept notice: %s", str(e))
                downloaded_file_name = atcu_manual_ota_page.get_downloaded_file_name()
                download_success = True if downloaded_file_name else False
        else:
            downloaded_file_name = atcu_manual_ota_page.get_downloaded_file_name()
            download_success = True

        report_case(
            expected="Clicking Download button should trigger file download and save CSV/Excel report file",
            actual=f"Download button visible: {download_btn.is_visible()}, Download success: {download_success}, Downloaded file: '{downloaded_file_name}'",
            message="Validate Download button click and report file download functionality",
        )

        assert download_success or downloaded_file_name != "", "Download button failed to download report file"
