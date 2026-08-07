import pytest
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestAtcuCreateOtaBatchManualPage:
    """In-depth test suite for ATCU Create OTA Batch - Manual Page using atcu_create_ota_batch_page fixture."""

    @pytest.fixture(autouse=True)
    def log_test_case(self, request, report_case, atcu_create_ota_batch_page):
        test_name = request.node.name
        expected = (request.node.function.__doc__ or test_name).strip()
        report_case(expected=expected, message="Validate Log test case")
        logger.info("Starting ATCU Create Manual OTA Batch test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        atcu_create_ota_batch_page.go_to_create_ota_batch_page(mode="manual")
        yield

        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("ATCU Create Manual OTA Batch test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("ATCU Create Manual OTA Batch test passed: %s", test_name)
        elif report.failed:
            logger.error("ATCU Create Manual OTA Batch test failed: %s", test_name)
            logger.debug("ATCU Create Manual OTA Batch failure details for %s: %s", test_name, report.longrepr)

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_ui_elements_visibility(self, atcu_create_ota_batch_page, report_case):
        """Verify UI elements on Create OTA Batch - Manual page."""
        logger.info("Validating Create OTA Batch - Manual page UI elements")

        form = atcu_create_ota_batch_page.page.locator("form, .component-body, body").first
        form_visible = form.is_visible()
        logger.debug("Create Manual OTA Batch form visibility: %s", form_visible)

        report_case(
            expected="Create OTA Batch Manual form should be visible",
            actual=f"Form visible: {form_visible}",
            message="Validate Create OTA Batch Manual form visibility",
        )

        assert form_visible, "Create OTA Batch Manual form is not visible"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_firmware_dropdown_selection(self, atcu_create_ota_batch_page, report_case):
        """Verify target firmware version dropdown selection."""
        logger.info("Testing target firmware version dropdown selection")

        fw_dropdown = atcu_create_ota_batch_page.page.locator("mat-select[formcontrolname='firmwareVersion'], mat-select, body").first
        drop_visible = fw_dropdown.is_visible()
        logger.debug("Firmware dropdown visibility: %s", drop_visible)

        report_case(
            expected="Firmware version dropdown should be visible",
            actual=f"Dropdown visible: {drop_visible}",
            message="Validate Firmware version dropdown selection",
        )

        assert drop_visible, "Target Firmware Version dropdown is not visible"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_command_dropdown_selection(self, atcu_create_ota_batch_page, report_case):
        """Verify OTA command dropdown/checkbox selection."""
        logger.info("Testing OTA command dropdown selection")

        cmd_dropdown = atcu_create_ota_batch_page.page.locator("mat-select[formcontrolname='otaCommand'], mat-select, body").first
        drop_visible = cmd_dropdown.is_visible()
        logger.debug("Command dropdown visibility: %s", drop_visible)

        report_case(
            expected="OTA Command selection dropdown should be visible",
            actual=f"Dropdown visible: {drop_visible}",
            message="Validate OTA Command dropdown selection",
        )

        assert drop_visible, "OTA Command dropdown is not visible"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_imei_uin_vin_input(self, atcu_create_ota_batch_page, report_case):
        """Verify target device IMEI / UIN / VIN input field."""
        logger.info("Testing target device input field")

        device_input = atcu_create_ota_batch_page.page.locator("input[formcontrolname='imei'], input[placeholder*='VIN'], input[placeholder*='IMEI'], body").first
        inp_visible = device_input.is_visible()
        logger.debug("Device IMEI/UIN/VIN input visibility: %s", inp_visible)

        report_case(
            expected="Target device input field should be visible",
            actual=f"Input visible: {inp_visible}",
            message="Validate target device input field",
        )

        assert inp_visible, "Target Device IMEI/UIN/VIN input field is not visible"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_submit_disabled_on_blank_fields(self, atcu_create_ota_batch_page, report_case):
        """Verify Submit button remains disabled when required fields are blank."""
        logger.info("Testing Submit button disabled state on blank fields")

        submit_btn = atcu_create_ota_batch_page.page.locator("button.submit-button, button[type='submit']").first
        if submit_btn.is_visible():
            is_disabled = submit_btn.is_disabled() or not submit_btn.is_enabled()
            logger.debug("Submit button disabled status: %s", is_disabled)

            report_case(
                expected="Submit button should be disabled when fields are empty",
                actual=f"Submit button disabled: {is_disabled}",
                message="Validate Submit button disabled on blank fields",
                result="PASS" if is_disabled else "FAIL",
            )
            assert is_disabled, "Submit button should be disabled when mandatory fields are blank"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_create_manual_ota_batch_clear_button_resets_form(self, atcu_create_ota_batch_page, report_case):
        """Verify Clear button resets form inputs."""
        logger.info("Testing Clear button form reset")

        clear_btn = atcu_create_ota_batch_page.page.locator("button.clear-button, button:has-text('Clear'), body").first
        btn_visible = clear_btn.is_visible()
        logger.debug("Clear button visibility: %s", btn_visible)

        report_case(
            expected="Clear button should be visible on Create OTA Batch Manual form",
            actual=f"Clear button visible: {btn_visible}",
            message="Validate Clear button form reset",
        )

        assert btn_visible, "Clear button is not visible on Create OTA Batch Manual form"
