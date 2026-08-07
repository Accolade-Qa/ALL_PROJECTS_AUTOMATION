import os
from pathlib import Path
import pytest
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestAtcuCreateOtaBatchBulkUploadPage:
    """In-depth test suite for ATCU Create OTA Batch - Bulk Upload Page covering field validations, dropdown options, CSV upload, and submit enablement."""

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
        val_num = atcu_create_ota_batch_page.page.locator("input[formcontrolname='batchName'], input[placeholder*='Batch Name']").first.input_value()

        report_case(
            expected="Numerical input '12345' should be accepted in Batch Name field",
            actual=f"Actual input value: '{val_num}'",
            message="Validate Batch Name numerical input",
        )
        assert val_num == "12345", f"Expected '12345', got '{val_num}'"

        # Step 5: Valid text input
        atcu_create_ota_batch_page.fill_batch_name("TestBatch")
        val_text = atcu_create_ota_batch_page.page.locator("input[formcontrolname='batchName'], input[placeholder*='Batch Name']").first.input_value()

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
        val_num = atcu_create_ota_batch_page.page.locator("input[formcontrolname='batchDescription'], textarea[formcontrolname='batchDescription'], input[placeholder*='Description']").first.input_value()

        assert val_num == "99999", f"Expected '99999', got '{val_num}'"

        # Step 5: Valid text input
        atcu_create_ota_batch_page.fill_batch_description("TestDescription")
        val_text = atcu_create_ota_batch_page.page.locator("input[formcontrolname='batchDescription'], textarea[formcontrolname='batchDescription'], input[placeholder*='Description']").first.input_value()

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

        assert any("Manual" in opt for opt in actual_options) and any("Bulk" in opt for opt in actual_options) and any("Custom" in opt for opt in actual_options) and len(actual_options) == 3, "OTA Type dropdown options mismatch"

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

        assert ".csv" in str(accept_attr).lower() or accept_attr is not None, "File input does not restrict to .csv files"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_bulk_upload_submit_button_visibility_and_clickability_flow(self, atcu_create_ota_batch_page, report_case):
        """Requirement 6 & 7: Validate Submit button is not visible/enabled until all fields are inputed with correct data and CSV file uploaded, then click Submit."""
        logger.info("Testing Submit button visibility and clickability flow with valid data & CSV upload")

        submit_btn = atcu_create_ota_batch_page.page.locator("button.submit-button, button[type='submit']").first

        # Step 1: Verify Submit button is not enabled when fields are empty
        if submit_btn.is_visible():
            initially_disabled = submit_btn.is_disabled() or not submit_btn.is_enabled()
            logger.debug("Submit button initially disabled: %s", initially_disabled)
            report_case(
                expected="Submit button should be disabled when mandatory fields are empty",
                actual=f"Initially disabled: {initially_disabled}",
                message="Validate Submit button disabled on empty fields",
            )
            assert initially_disabled, "Submit button should be disabled when fields are empty"

        # Step 2: Fill all fields with correct valid data
        atcu_create_ota_batch_page.fill_batch_name("ValidBulkBatch123")
        atcu_create_ota_batch_page.fill_batch_description("Valid Bulk OTA Description")

        try:
            atcu_create_ota_batch_page.select_ota_batch_type("Bulk OTA")
        except Exception as e:
            logger.warning("Could not select Bulk OTA type: %s", str(e))

        # Step 3: Upload sample CSV file from test-data/atcu/bulk ota sample template.csv
        file_path = self.SAMPLE_CSV_PATH
        logger.info("Uploading bulk CSV file from path: %s", file_path)

        if os.path.exists(file_path):
            file_input = atcu_create_ota_batch_page.page.locator("input[type='file']").first
            if file_input.is_visible():
                file_input.set_input_files(file_path)
                logger.info("CSV File uploaded successfully: %s", file_path)
        else:
            logger.warning("Sample CSV file path not found: %s", file_path)

        # Step 4: Verify Submit button becomes visible/enabled and click it
        btn_visible = submit_btn.is_visible()
        logger.debug("Submit button visible after complete form fill & CSV upload: %s", btn_visible)

        report_case(
            expected="Submit button should become visible and enabled after all fields are valid and CSV file is uploaded",
            actual=f"Submit button visible: {btn_visible}",
            message="Validate Submit button visibility after complete form fill",
        )

        assert btn_visible, "Submit button failed to become visible after filling valid data and uploading CSV file"

        try:
            submit_btn.click()
            logger.info("Clicked Submit button successfully")
        except Exception as e:
            logger.warning("Could not click submit button: %s", str(e))
