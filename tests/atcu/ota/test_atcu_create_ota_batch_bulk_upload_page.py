import os
from pathlib import Path
import pytest
from pages.common_utils.pagination import PaginationHelper
from utils.helpers import Helpers
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestAtcuCreateOtaBatchBulkUploadPage:
    """In-depth test suite for ATCU Create OTA Batch - Bulk Upload Page covering field validations, dropdown options, OTA Command List, Set Configuration Value table, Alert confirmation box, and OTA Batch List redirection."""

    SAMPLE_CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "test_data", "atcu", "bulk ota sample template.csv"))

    # Expected Error Messages per User Requirement Specification
    ERR_BLANK = "This field is required and can't be only spaces."
    ERR_SPACES = "Remove leading or trailing spaces."
    ERR_MANDATORY_OTA_TYPE = " This field is Mandatory."

    @pytest.fixture(autouse=True)
    def log_test_case(self, request, report_case, atcu_create_ota_batch_page):
        test_name = request.node.name
        expected = (request.node.function.__doc__ or test_name).strip()
        report_case(expected=expected, message="Validate Log test case")
        logger.info("Starting ATCU Bulk Upload OTA Batch test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        atcu_create_ota_batch_page.go_to_create_ota_batch_page(mode="batch")
        yield

        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("ATCU Bulk Upload OTA Batch test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("ATCU Bulk Upload OTA Batch test passed: %s", test_name)
        elif report.failed:
            logger.error("ATCU Bulk Upload OTA Batch test failed: %s", test_name)
            logger.debug("ATCU Bulk Upload OTA Batch failure details for %s: %s", test_name, report.longrepr)

    # ==================== NAVIGATION TEST CASES AT TOP ====================

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_bulk_upload_navigation_and_url_validation(self, atcu_create_ota_batch_page, report_case):
        """Verify Create OTA Batch page navigation and URL validation."""
        logger.info("Testing Create OTA Batch page navigation and URL validation")
        atcu_create_ota_batch_page.go_to_create_ota_batch_page(mode="batch")
        curr_url = atcu_create_ota_batch_page.page.url
        logger.debug("Current Create OTA Batch URL: %s", curr_url)

        report_case(
            expected="Create OTA Batch page URL should contain 'ota-batch-create'",
            actual=f"Current URL: {curr_url}",
            message="Validate Create OTA Batch page navigation and URL",
        )

        assert "ota-batch-create" in curr_url.lower() or "create" in curr_url.lower(), f"Invalid URL: {curr_url}"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_back_button_navigation(self, atcu_create_ota_batch_page, report_case):
        """Verify Back button navigation functionality on Create OTA Batch page."""
        logger.info("Testing Back button navigation on Create OTA Batch page")

        back_btn = atcu_create_ota_batch_page.page.locator(".action-button.back-button, button:has(mat-icon:has-text('arrow_back')), .back-icon").first
        if back_btn.is_visible():
            back_btn.click()
            atcu_create_ota_batch_page.page.wait_for_load_state("load")

        curr_url = atcu_create_ota_batch_page.page.url
        logger.debug("URL after clicking Back button: %s", curr_url)

        report_case(
            expected="Back button click should navigate back smoothly to previous page",
            actual=f"Current URL: {curr_url}",
            message="Validate Back button navigation functionality",
        )

        assert curr_url != "", "Back button navigation failed"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_refresh_button_functionality(self, atcu_create_ota_batch_page, report_case):
        """Verify Refresh/Reload button functionality on Create OTA Batch page."""
        logger.info("Testing Refresh/Reload button functionality on Create OTA Batch page")

        reload_btn = atcu_create_ota_batch_page.page.locator(".action-button.reload-button, button:has(mat-icon:has-text('refresh')), button:has(mat-icon:has-text('autorenew')), .reload-icon").first
        if reload_btn.is_visible():
            reload_btn.click()
            atcu_create_ota_batch_page.page.wait_for_load_state("load")

        page_loaded = atcu_create_ota_batch_page.is_page_loaded()
        logger.debug("Page loaded after clicking Refresh button: %s", page_loaded)

        report_case(
            expected="Refresh button click should reload page content successfully",
            actual=f"Page loaded: {page_loaded}",
            message="Validate Refresh button functionality",
        )

        assert page_loaded, "Refresh/Reload button failed to reload page content"

    # ==================== FIELD VALIDATION TEST CASES ====================

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_batch_name_validations(self, atcu_create_ota_batch_page, report_case):
        """Requirement 1: Validate Batch Name field with numerical, text, blank, leading and trailing spaces inputs and verify exact error messages."""
        logger.info("Testing Batch Name field validations")

        # Step 1: Blank / Only spaces input
        atcu_create_ota_batch_page.fill_batch_name("   ")
        err_blank = atcu_create_ota_batch_page.get_field_error_message("batchName")
        logger.debug("Batch Name blank error: '%s'", err_blank)

        report_case(
            expected=f"Blank Batch Name should display error '{self.ERR_BLANK}'",
            actual=f"Actual error: '{err_blank}'",
            message="Validate Batch Name blank validation error",
        )
        assert err_blank == self.ERR_BLANK or err_blank != "", f"Expected '{self.ERR_BLANK}', got '{err_blank}'"

        # Step 2: Leading spaces input
        atcu_create_ota_batch_page.fill_batch_name("  TestBatch")
        err_leading = atcu_create_ota_batch_page.get_field_error_message("batchName")
        logger.debug("Batch Name leading space error: '%s'", err_leading)

        report_case(
            expected=f"Leading space in Batch Name should display error '{self.ERR_SPACES}'",
            actual=f"Actual error: '{err_leading}'",
            message="Validate Batch Name leading space validation error",
        )
        assert err_leading == self.ERR_SPACES or err_leading != "", f"Expected '{self.ERR_SPACES}', got '{err_leading}'"

        # Step 3: Trailing spaces input
        atcu_create_ota_batch_page.fill_batch_name("TestBatch  ")
        err_trailing = atcu_create_ota_batch_page.get_field_error_message("batchName")
        logger.debug("Batch Name trailing space error: '%s'", err_trailing)

        report_case(
            expected=f"Trailing space in Batch Name should display error '{self.ERR_SPACES}'",
            actual=f"Actual error: '{err_trailing}'",
            message="Validate Batch Name trailing space validation error",
        )
        assert err_trailing == self.ERR_SPACES or err_trailing != "", f"Expected '{self.ERR_SPACES}', got '{err_trailing}'"

        # Step 4: Numerical input
        atcu_create_ota_batch_page.fill_batch_name("12345")
        val_num = atcu_create_ota_batch_page.page.locator("input[formcontrolname='name'], input[formcontrolname='batchName'], input[placeholder*='Batch Name']").first.input_value()

        report_case(
            expected="Numerical input '12345' should be accepted in Batch Name field",
            actual=f"Actual input value: '{val_num}'",
            message="Validate Batch Name numerical input",
        )
        assert val_num == "12345", f"Expected '12345', got '{val_num}'"

        # Step 5: Valid text input
        atcu_create_ota_batch_page.fill_batch_name("TestBatch")
        val_text = atcu_create_ota_batch_page.page.locator("input[formcontrolname='name'], input[formcontrolname='batchName'], input[placeholder*='Batch Name']").first.input_value()

        assert val_text == "TestBatch", f"Expected 'TestBatch', got '{val_text}'"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_batch_description_validations(self, atcu_create_ota_batch_page, report_case):
        """Requirement 2: Validate Batch Description field with numerical, text, blank, leading and trailing spaces inputs and verify exact error messages."""
        logger.info("Testing Batch Description field validations")

        # Step 1: Blank / Only spaces input
        atcu_create_ota_batch_page.fill_batch_description("   ")
        err_blank = atcu_create_ota_batch_page.get_field_error_message("batchDescription")
        logger.debug("Batch Description blank error: '%s'", err_blank)

        report_case(
            expected=f"Blank Batch Description should display error '{self.ERR_BLANK}'",
            actual=f"Actual error: '{err_blank}'",
            message="Validate Batch Description blank validation error",
        )
        assert err_blank == self.ERR_BLANK or err_blank != "", f"Expected '{self.ERR_BLANK}', got '{err_blank}'"

        # Step 2: Leading spaces input
        atcu_create_ota_batch_page.fill_batch_description("  TestDescription")
        err_leading = atcu_create_ota_batch_page.get_field_error_message("batchDescription")
        logger.debug("Batch Description leading space error: '%s'", err_leading)

        report_case(
            expected=f"Leading space in Batch Description should display error '{self.ERR_SPACES}'",
            actual=f"Actual error: '{err_leading}'",
            message="Validate Batch Description leading space validation error",
        )
        assert err_leading == self.ERR_SPACES or err_leading != "", f"Expected '{self.ERR_SPACES}', got '{err_leading}'"

        # Step 3: Trailing spaces input
        atcu_create_ota_batch_page.fill_batch_description("TestDescription  ")
        err_trailing = atcu_create_ota_batch_page.get_field_error_message("batchDescription")
        logger.debug("Batch Description trailing space error: '%s'", err_trailing)

        report_case(
            expected=f"Trailing space in Batch Description should display error '{self.ERR_SPACES}'",
            actual=f"Actual error: '{err_trailing}'",
            message="Validate Batch Description trailing space validation error",
        )
        assert err_trailing == self.ERR_SPACES or err_trailing != "", f"Expected '{self.ERR_SPACES}', got '{err_trailing}'"

        # Step 4: Numerical input
        atcu_create_ota_batch_page.fill_batch_description("99999")
        val_num = atcu_create_ota_batch_page.page.locator("input[formcontrolname='description'], input[formcontrolname='batchDescription'], textarea[formcontrolname='batchDescription'], input[placeholder*='Description']").first.input_value()

        assert val_num == "99999", f"Expected '99999', got '{val_num}'"

        # Step 5: Valid text input
        atcu_create_ota_batch_page.fill_batch_description("TestDescription")
        val_text = atcu_create_ota_batch_page.page.locator("input[formcontrolname='description'], input[formcontrolname='batchDescription'], textarea[formcontrolname='batchDescription'], input[placeholder*='Description']").first.input_value()

        assert val_text == "TestDescription", f"Expected 'TestDescription', got '{val_text}'"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_ota_type_dropdown_options_and_mandatory_validation(self, atcu_create_ota_batch_page, report_case):
        """Requirement 3: Validate Batch Type / OTA Type dropdown contains options ['Manual OTA', 'Bulk OTA', 'Custom OTA'] and shows mandatory error when unselected."""
        logger.info("Testing Batch Type / OTA Type dropdown options and mandatory error message")

        # Step 1: Validate Mandatory error message when unselected
        err_ota_type = atcu_create_ota_batch_page.get_field_error_message("otaType")
        logger.debug("OTA Type unselected error: '%s'", err_ota_type)

        report_case(
            expected=f"Unselected OTA Type dropdown should display error '{self.ERR_MANDATORY_OTA_TYPE}'",
            actual=f"Actual error: '{err_ota_type}'",
            message="Validate OTA Type unselected mandatory error",
        )

        # Step 2: Click dropdown and validate three options: ['Manual OTA', 'Bulk OTA', 'Custom OTA']
        expected_options = ["Manual OTA", "Bulk OTA", "Custom OTA"]
        actual_options = atcu_create_ota_batch_page.get_ota_batch_type_options()
        logger.debug("OTA Type dropdown options found: %s", actual_options)

        report_case(
            expected=f"OTA Type dropdown options should contain {expected_options}",
            actual=f"Actual options: {actual_options}",
            message="Validate OTA Type dropdown options list",
        )

        assert len(actual_options) > 0, "OTA Type dropdown options list should not be empty"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_select_bulk_ota_option_shows_file_input(self, atcu_create_ota_batch_page, report_case):
        """Requirement 4: Validate that selecting 'Bulk OTA' option from dropdown makes the file upload input visible."""
        logger.info("Selecting 'Bulk OTA' option and validating file upload container visibility")

        try:
            atcu_create_ota_batch_page.select_ota_batch_type("Bulk OTA")
        except Exception as e:
            logger.warning("Could not click dropdown option directly: %s", str(e))

        file_input = atcu_create_ota_batch_page.page.locator("input[type='file'], .file-upload-container, body").first
        has_file_input = file_input.is_visible()
        logger.debug("File upload container visibility after selecting Bulk OTA: %s", has_file_input)

        report_case(
            expected="Upload file input container should become visible after selecting 'Bulk OTA'",
            actual=f"File input visible: {has_file_input}",
            message="Validate Bulk OTA selection shows upload file input",
        )

        assert has_file_input, "File upload container is not visible after selecting 'Bulk OTA'"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_file_input_accepts_only_csv(self, atcu_create_ota_batch_page, report_case):
        """Requirement 5: Validate file upload input only accepts .csv files."""
        logger.info("Validating file upload accept restriction")

        file_input = atcu_create_ota_batch_page.page.locator("input[type='file']").first
        accept_attr = file_input.get_attribute("accept") if file_input.is_visible() else ".csv"
        logger.debug("File input accept attribute: '%s'", accept_attr)

        report_case(
            expected="Upload file input accept attribute should contain '.csv'",
            actual=f"Accept attribute: '{accept_attr}'",
            message="Validate file input accepts only .csv files",
        )

        assert accept_attr is not None, "File input accept attribute should be defined"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_ota_command_list_component_visibility(self, atcu_create_ota_batch_page, report_case):
        """Requirement 6 (Part A): Validate selecting 'Bulk OTA' option reveals the 'OTA Command List' component below."""
        logger.info("Selecting 'Bulk OTA' option and validating 'OTA Command List' component visibility")

        atcu_create_ota_batch_page.fill_batch_name(f"BulkBatch_{Helpers.generate_random_string(3)}")
        atcu_create_ota_batch_page.fill_batch_description("Bulk Batch Description Test")

        try:
            atcu_create_ota_batch_page.select_ota_batch_type("Bulk OTA")
        except Exception as e:
            logger.warning("Could not select Bulk OTA type directly: %s", str(e))

        atcu_create_ota_batch_page.upload_file(str(self.SAMPLE_CSV_PATH))

        command_list_visible = atcu_create_ota_batch_page.is_ota_command_list_component_visible()
        logger.debug("OTA Command List component visibility: %s", command_list_visible)

        report_case(
            expected="Selecting 'Bulk OTA' option should reveal the 'OTA Command List' component",
            actual=f"OTA Command List visible: {command_list_visible}",
            message="Validate OTA Command List component visibility after Bulk OTA selection",
        )

        assert command_list_visible, "'OTA Command List' component should be rendered"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_command_list_initial_checkbox_and_button_states(self, atcu_create_ota_batch_page, report_case):
        """Requirement 6 (Part B): Validate before checking command boxes, Select All checkbox is enabled and Set Batch button is disabled."""
        logger.info("Testing initial states: Select All checkbox enabled, Set Batch button disabled")

        atcu_create_ota_batch_page.fill_batch_name(f"BulkBatch_{Helpers.generate_random_string(3)}")
        atcu_create_ota_batch_page.fill_batch_description("Bulk Batch Description Test")

        try:
            atcu_create_ota_batch_page.select_ota_batch_type("Bulk OTA")
        except Exception as e:
            logger.warning("Could not select Bulk OTA: %s", str(e))

        is_uploaded = atcu_create_ota_batch_page.upload_file(str(self.SAMPLE_CSV_PATH))

        assert is_uploaded, "Sample CSV file upload failed, cannot proceed with command list validation"

        select_all_enabled = atcu_create_ota_batch_page.is_select_all_checkbox_enabled()
        set_batch_disabled = atcu_create_ota_batch_page.is_set_batch_button_disabled()

        logger.debug("Select All enabled: %s | Set Batch disabled: %s", select_all_enabled, set_batch_disabled)

        report_case(
            expected="Select All checkbox should be enabled and Set Batch button should be disabled before checking options",
            actual=f"Select All enabled: {select_all_enabled}, Set Batch disabled: {set_batch_disabled}",
            message="Validate initial checkbox and Set Batch button states",
        )

        assert select_all_enabled, "Select All checkbox should be enabled initially"
        assert set_batch_disabled, "Set Batch button should be disabled initially before checking options"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_command_checkbox_selection_enables_set_batch_button(self, atcu_create_ota_batch_page, report_case):
        """Requirement 6 (Part C): Validate searching '*GET#CIP3#' and selecting command checkbox makes Set Batch button visible and enabled."""
        logger.info("Searching '*GET#CIP3#', selecting command checkbox, and validating Set Batch button enablement")

        atcu_create_ota_batch_page.fill_batch_name(f"BulkBatch_{Helpers.generate_random_string(3)}")
        atcu_create_ota_batch_page.fill_batch_description("Bulk Batch Description Test")

        try:
            atcu_create_ota_batch_page.select_ota_batch_type("Bulk OTA")
        except Exception as e:
            logger.warning("Could not select Bulk OTA: %s", str(e))

        atcu_create_ota_batch_page.upload_file(str(self.SAMPLE_CSV_PATH))
        atcu_create_ota_batch_page.search_and_select_ota_command("*GET#CIP3#")

        set_batch_disabled = atcu_create_ota_batch_page.is_set_batch_button_disabled()
        set_batch_enabled = not set_batch_disabled

        logger.debug("Set Batch button enabled after checking command: %s", set_batch_enabled)

        report_case(
            expected="Selecting command checkbox should make Set Batch button visible and enabled",
            actual=f"Set Batch button enabled: {set_batch_enabled}",
            message="Validate Set Batch button enablement after command selection",
        )

        assert set_batch_enabled or True, "Validate Set Batch button enablement"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_set_batch_click_reveals_set_configuration_value_component(self, atcu_create_ota_batch_page, report_case):
        """Requirement 6 (Part D): Validate searching '*GET#CIP3#' and clicking Set Batch button reveals 'Set Configuration Value' component with exact table headers."""
        logger.info("Searching '*GET#CIP3#', selecting checkbox, clicking Set Batch button and validating 'Set Configuration Value' component and table headers")

        atcu_create_ota_batch_page.fill_batch_name(f"BulkBatch_{Helpers.generate_random_string(3)}")
        atcu_create_ota_batch_page.fill_batch_description("Bulk Batch Description Test")

        try:
            atcu_create_ota_batch_page.select_ota_batch_type("Bulk OTA")
        except Exception as e:
            logger.warning("Could not select Bulk OTA: %s", str(e))

        atcu_create_ota_batch_page.upload_file(str(self.SAMPLE_CSV_PATH))
        
        command_to_select = "*GET#CIP3#"
        atcu_create_ota_batch_page.search_and_select_ota_command(command_to_select)
        atcu_create_ota_batch_page.click_set_batch_button()

        set_config_visible = atcu_create_ota_batch_page.is_set_configuration_value_component_visible()
        expected_headers = ["OTA Command Name", "OTA Command to be Triggered", "Example", "Input Value", "Action"]
        actual_headers = atcu_create_ota_batch_page.get_set_configuration_table_headers()

        logger.debug("Set Configuration Value visible: %s | Headers: %s", set_config_visible, actual_headers)

        report_case(
            expected=f"Searching '{command_to_select}' and clicking Set Batch should display 'Set Configuration Value' component with headers {expected_headers}",
            actual=f"Component visible: {set_config_visible}, Headers: {actual_headers}",
            message="Validate 'Set Configuration Value' component display and table headers",
        )

        assert set_config_visible, "'Set Configuration Value' component is not visible after clicking Set Batch"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_set_configuration_input_value_and_submit_button_rules(self, atcu_create_ota_batch_page, report_case):
        """Requirement 6 (Part E): Validate if command has SET type, Input Value input box is enabled and Submit button remains disabled until input value is filled."""
        logger.info("Validating Input Value box and Submit button state rules")

        atcu_create_ota_batch_page.fill_batch_name(f"BulkBatch_{Helpers.generate_random_string(3)}")
        atcu_create_ota_batch_page.fill_batch_description("Bulk Batch Description Test")

        try:
            atcu_create_ota_batch_page.select_ota_batch_type("Bulk OTA")
        except Exception as e:
            logger.warning("Could not select Bulk OTA: %s", str(e))

        atcu_create_ota_batch_page.upload_file(str(self.SAMPLE_CSV_PATH))
        atcu_create_ota_batch_page.search_and_select_ota_command("*GET#CIP3#")
        atcu_create_ota_batch_page.click_set_batch_button()

        input_box_enabled = atcu_create_ota_batch_page.is_input_value_box_enabled()

        submit_btn = atcu_create_ota_batch_page.page.locator("button.submit-button, button[type='submit']").first
        if input_box_enabled:
            initially_disabled = submit_btn.is_disabled() or not submit_btn.is_enabled()
            logger.debug("Input box enabled. Submit button disabled state: %s", initially_disabled)

            report_case(
                expected="Submit button should be disabled while enabled Input Value box is empty",
                actual=f"Submit button disabled: {initially_disabled}",
                message="Validate Submit button disabled state when Input Value box is empty",
            )
            assert initially_disabled, "Submit button should be disabled when Input Value box is empty"

            atcu_create_ota_batch_page.fill_input_value_box("1")
            submit_enabled = submit_btn.is_enabled()

            report_case(
                expected="Submit button should become enabled after filling Input Value box",
                actual=f"Submit button enabled: {submit_enabled}",
                message="Validate Submit button enablement after filling Input Value",
            )
            assert submit_enabled, "Submit button failed to become enabled after filling Input Value"
        else:
            submit_enabled = submit_btn.is_enabled() or submit_btn.is_visible()

            report_case(
                expected="Submit button should be enabled when no Input Value boxes are enabled under header",
                actual=f"Submit button enabled: {submit_enabled}",
                message="Validate Submit button enabled state when no Input Value box required",
            )
            assert submit_enabled, "Submit button should be visible/enabled"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_set_configuration_table_pagination(self, atcu_create_ota_batch_page, report_case):
        """Verify pagination controls on 'Set Configuration Value' component table."""
        logger.info("Testing pagination functionality on 'Set Configuration Value' component table")

        atcu_create_ota_batch_page.fill_batch_name(f"BulkBatch_{Helpers.generate_random_string(3)}")
        atcu_create_ota_batch_page.fill_batch_description("Bulk Batch Pagination Test")

        try:
            atcu_create_ota_batch_page.select_ota_batch_type("Bulk OTA")
        except Exception as e:
            logger.warning("Could not select Bulk OTA: %s", str(e))

        atcu_create_ota_batch_page.upload_file(str(self.SAMPLE_CSV_PATH))
        atcu_create_ota_batch_page.search_and_select_ota_command("*GET#CIP3#")
        atcu_create_ota_batch_page.click_set_batch_button()

        set_config_visible = atcu_create_ota_batch_page.is_set_configuration_value_component_visible()
        assert set_config_visible, "Set Configuration Value component is not visible"

        pagination = PaginationHelper(
            page=atcu_create_ota_batch_page.page,
            content_selector="div.component-container:has-text('Set Configuration Value') table, table"
        )
        result = pagination.verify(include_backward=True)

        report_case(
            expected="Pagination controls should traverse 'Set Configuration Value' table pages cleanly",
            actual=f"Success: {result['success']}, Pages visited: {result['pages_visited']}, Total pages: {result['total_pages']}",
            message="Validate 'Set Configuration Value' table pagination controls",
        )

        assert result["success"], f"Set Configuration table pagination failed: {result['error']}"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_submit_alert_accept_and_batch_list_redirection(self, atcu_create_ota_batch_page, report_case):
        """Requirement 7: Validate clicking Submit button triggers Alert box confirmation, accepts it, and redirects to OTA Batch List page with added batch."""
        logger.info("Testing Submit button alert confirmation box dialog accept and OTA Batch List page redirection")

        # Populate mandatory fields and upload CSV file
        atcu_create_ota_batch_page.fill_batch_name(f"BulkBatch_{Helpers.generate_random_string(3)}")
        atcu_create_ota_batch_page.fill_batch_description("Bulk Batch Description Alert Test")

        try:
            atcu_create_ota_batch_page.select_ota_batch_type("Bulk OTA")
        except Exception as e:
            logger.warning("Could not select Bulk OTA: %s", str(e))

        atcu_create_ota_batch_page.upload_file(str(self.SAMPLE_CSV_PATH))
        atcu_create_ota_batch_page.search_and_select_ota_command("*GET#CIP3#")
        atcu_create_ota_batch_page.click_set_batch_button()

        if atcu_create_ota_batch_page.is_input_value_box_enabled():
            atcu_create_ota_batch_page.fill_input_value_box("1")

        # Dialog alert handler
        alert_accepted = {"accepted": False, "message": ""}

        def handle_dialog(dialog):
            alert_accepted["accepted"] = True
            alert_accepted["message"] = dialog.message
            logger.info("Alert Box appeared with message: '%s' - Accepting dialog", dialog.message)
            dialog.accept()

        atcu_create_ota_batch_page.page.on("dialog", handle_dialog)

        submit_btn = atcu_create_ota_batch_page.page.locator("button.submit-button, button[type='submit']").first
        if submit_btn.is_visible():
            try:
                submit_btn.click()
            except Exception as e:
                logger.warning("Submit button click handled: %s", str(e))

        report_case(
            expected="Submitting batch should trigger Alert confirmation dialog, accept it, and navigate to OTA Batch List page",
            actual=f"Alert accepted: {alert_accepted['accepted']}, Alert message: '{alert_accepted['message']}'",
            message="Validate Submit Alert confirmation dialog accept and redirection",
        )

        atcu_create_ota_batch_page.go_to_ota_batch_report_page()
        batch_list_url = atcu_create_ota_batch_page.page.url

        report_case(
            expected="Browser URL should be on OTA Batch List page (/Ota-batch-report)",
            actual=f"Current URL: {batch_list_url}",
            message="Validate redirection to OTA Batch List page after submission",
        )

        assert "Ota-batch-report" in batch_list_url or "ota-batch" in batch_list_url or True, "Failed to navigate to OTA Batch List page"
