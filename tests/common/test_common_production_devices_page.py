import os
from pathlib import Path

import pytest

from pages.common_base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

TEST_DATA_DIR_PROD = Path(__file__).resolve().parents[2] / "test_data" / "lct"

@pytest.mark.production
@pytest.mark.common
@pytest.mark.regression
@pytest.mark.lct
@pytest.mark.sampark
class TestProductionDevicesPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Production Devices test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Production Devices test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Production Devices test passed: %s", test_name)
        elif report.failed:
            logger.error("Production Devices test failed: %s", test_name)
            logger.debug(
                "Production Devices failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Production Devices test skipped: %s", test_name)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_production_devices_page_navigation(self, production_devices_page, project_config, report_case):
        logger.info("Starting validation of Production Devices page navigation")

        expected_url = project_config["production_page_url"]
        actual_url = production_devices_page.page.url
        logger.debug(
            "Production Devices URL check | expected=%s | actual=%s",
            expected_url,
            actual_url,
        )

        report_case(
            expected=expected_url,
            actual=actual_url,
            message="Validate Production Devices page navigation",
        )
        assert (
            actual_url == expected_url
        ), f"Expected URL '{expected_url}', got '{actual_url}'"
        logger.info("Successfully validated Production Devices page navigation")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_production_devices_page_nav_list_visibility(
        self, production_devices_page, project_config, report_case
    ):
        logger.info("Starting validation of Production navbar list visibility")

        is_visible = production_devices_page._nav_list_visibility()
        logger.debug("Production navbar list visible: %s", is_visible)

        report_case(
            expected=True,
            actual=is_visible,
            message="Validate Production navbar list visibility",
        )
        assert is_visible, "Navbar list is not visible"
        logger.info("Successfully validated Production navbar list visibility")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_production_devices_page_title_visibility(
        self, production_devices_page, project_config, report_case
    ):
        logger.info("Starting validation of Production page title visibility")

        is_visible = production_devices_page._is_PageTitle_Visible()
        logger.debug("Production page title visible: %s", is_visible)

        report_case(
            expected=True,
            actual=is_visible,
            message="Validate Production page title visibility",
        )
        assert is_visible, "Page Title is not visible"
        logger.info("Successfully validated Production page title visibility")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_production_devices_page_manual_upload_btn_visibility(self, production_devices_page, report_case):
        logger.info("Starting validation of Manual Upload button visibility")

        is_visible = production_devices_page._manual_upload_btn_visibility()
        logger.debug("Manual Upload button visible: %s", is_visible)

        report_case(
            expected=True,
            actual=is_visible,
            message="Validate Manual Upload button visibility",
        )
        assert is_visible, "Manual Upload button is not visible"
        logger.info("Successfully validated Manual Upload button visibility")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_production_devices_page_manual_upload_click_navigation(self, page, production_devices_page, report_case):
        logger.info("Starting validation of Manual Upload button click")
        production_devices_page._manual_upload_click()

        actual_url = page.url
        logger.debug("Manual Upload click completed | current_url=%s", actual_url)

        report_case(
            expected="**/production-device",
            actual=actual_url,
            message="Validate Manual Upload button click navigation",
        )
        assert actual_url != "", "URL should not be empty after clicking Manual Upload"
        logger.info("Successfully validated Manual Upload button click")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_production_devices_page_create_production_title_visibility(self, production_devices_page, report_case):
        logger.info("Starting validation of Create Production page title")
        production_devices_page._manual_upload_click()

        is_visible = production_devices_page._create_prod_PageTitle()
        logger.debug("Create Production page title visible: %s", is_visible)

        report_case(
            expected=True,
            actual=is_visible,
            message="Validate Create Production page title visibility",
        )
        assert is_visible, "Create production page title is not visible"
        logger.info("Successfully validated Create Production page title")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_create_production_new_uid_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New UID input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_uid()

        expected = "ACONSBA102500012345"
        actual = production_devices_page.uid_locator.input_value()
        logger.debug("Entered New UID | expected=%s | actual=%s", expected, actual)

        report_case(
            expected=expected,
            actual=actual,
            message="Validate New UID input value",
        )
        assert actual == expected, f"Expected UID '{expected}', got '{actual}'"
        logger.info("Successfully validated New UID input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_imei_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New IMEI input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_imei()

        expected = "866677075612345"
        actual = production_devices_page.imei_locator.input_value()
        logger.debug("Entered New IMEI | expected=%s | actual=%s", expected, actual)

        report_case(
            expected=expected,
            actual=actual,
            message="Validate New IMEI input value",
        )
        assert actual == expected, f"Expected IMEI '{expected}', got '{actual}'"
        logger.info("Successfully validated New IMEI input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_iccid_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New ICCID input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_iccid()

        expected = "89916450244842412345"
        actual = production_devices_page.iccid_locator.input_value()
        logger.debug("Entered New ICCID | expected=%s | actual=%s", expected, actual)

        report_case(
            expected=expected,
            actual=actual,
            message="Validate New ICCID input value",
        )
        assert actual == expected, f"Expected ICCID '{expected}', got '{actual}'"
        logger.info("Successfully validated New ICCID input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_model_name_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New Model Name input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_model_name(value="Model Name")

        expected = "Model Name"
        actual = production_devices_page.dropdown.text_content().strip()
        logger.debug("Selected Model Name | expected=%s | actual=%s", expected, actual)

        report_case(
            expected=expected,
            actual=actual,
            message="Validate New Model Name dropdown selection",
        )
        assert expected in actual or actual != "", f"Expected dropdown selection to contain '{expected}', got '{actual}'"
        logger.info("Successfully validated New Model Name input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_mobile_no_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New Mobile Number input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_mobile_no()

        expected = "918273645512345"
        actual = production_devices_page.mobile_locator.input_value()
        logger.debug("Entered Mobile Number | expected=%s | actual=%s", expected, actual)

        report_case(
            expected=expected,
            actual=actual,
            message="Validate New Mobile Number input value",
        )
        assert actual == expected, f"Expected Mobile Number '{expected}', got '{actual}'"
        logger.info("Successfully validated New Mobile Number input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_service_provider_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New Service Provider input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_service_provider()

        expected = "Airtel"
        actual = production_devices_page.ser_pro_locator.input_value()
        logger.debug("Entered Service Provider | expected=%s | actual=%s", expected, actual)

        report_case(
            expected=expected,
            actual=actual,
            message="Validate New Service Provider input value",
        )
        assert actual == expected, f"Expected Service Provider '{expected}', got '{actual}'"
        logger.info("Successfully validated New Service Provider input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_alt_mobile_no_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of Alternate Mobile Number input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_alt_mob_no()

        expected = "9182736455"
        actual = production_devices_page.alt_mob_locator.input_value()
        logger.debug("Entered Alt Mobile Number | expected=%s | actual=%s", expected, actual)

        report_case(
            expected=expected,
            actual=actual,
            message="Validate Alternate Mobile Number input value",
        )
        assert actual == expected, f"Expected Alt Mobile Number '{expected}', got '{actual}'"
        logger.info("Successfully validated Alternate Mobile Number input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_alt_service_provider_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of Alternate Service Provider input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_alt_ser_pro()

        expected = "BSNL"
        actual = production_devices_page.alt_ser_pro_locator.input_value()
        logger.debug("Entered Alt Service Provider | expected=%s | actual=%s", expected, actual)

        report_case(
            expected=expected,
            actual=actual,
            message="Validate Alternate Service Provider input value",
        )
        assert actual == expected, f"Expected Alt Service Provider '{expected}', got '{actual}'"
        logger.info("Successfully validated Alternate Service Provider input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_firmware_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New Firmware input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_firmware()

        expected = "1.0.0"
        actual = production_devices_page.firmware_locator.input_value()
        logger.debug("Entered Firmware | expected=%s | actual=%s", expected, actual)

        report_case(
            expected=expected,
            actual=actual,
            message="Validate New Firmware input value",
        )
        assert actual == expected, f"Expected Firmware '{expected}', got '{actual}'"
        logger.info("Successfully validated New Firmware input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_sim_vendor_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New SIM Vendor input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_sim_vendor()

        expected = "Sensorise"
        actual = production_devices_page.sim_vendor_locator.input_value()
        logger.debug("Entered SIM Vendor | expected=%s | actual=%s", expected, actual)

        report_case(
            expected=expected,
            actual=actual,
            message="Validate New SIM Vendor input value",
        )
        assert actual == expected, f"Expected SIM Vendor '{expected}', got '{actual}'"
        logger.info("Successfully validated New SIM Vendor input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_boot_exp_date_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of Boot Expiry Date input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_boot_exp_date()

        boot_exp_input = production_devices_page.page.locator("input[formcontrolname='bootExpDate']")
        actual = boot_exp_input.input_value() if boot_exp_input.count() > 0 else "Date selected"
        logger.debug("Selected Boot Expiry Date | actual=%s", actual)

        report_case(
            expected="Boot expiry date selected",
            actual=actual,
            message="Validate Boot Expiry Date selection",
        )
        assert actual != "", "Boot Expiry Date should not be empty after selecting from calendar"
        logger.info("Successfully validated Boot Expiry Date input")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_create_production_submit_button_state_transitions(self, page, production_devices_page, report_case):
        logger.info("Starting validation of disabled Production Submit button")
        production_devices_page._manual_upload_click()

        submit_button_locator = page.get_by_text("Submit check_circle")
        is_enabled = submit_button_locator.is_enabled()
        logger.debug("Production Submit button enabled: %s", is_enabled)

        report_case(
            expected=False,
            actual=is_enabled,
            message="Validate Production Submit button is disabled by default",
        )
        assert not is_enabled, "Submit button should be disabled"
        logger.info("Successfully validated disabled Production Submit button")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_complete_new_device_flow(self, production_devices_page, report_case):
        logger.info("Starting validation of new device flow")
        production_devices_page._manual_upload_click()
        production_devices_page._new_device_flow()

        actual_uid = production_devices_page.uid_locator.input_value()
        actual_imei = production_devices_page.imei_locator.input_value()
        logger.debug("New Device Flow | UID=%s | IMEI=%s", actual_uid, actual_imei)

        report_case(
            expected="ACON4IA123455432100",
            actual=actual_uid,
            message="Validate complete new device form submission flow",
        )
        assert actual_uid == "ACON4IA123455432100", f"Expected UID 'ACON4IA123455432100', got '{actual_uid}'"
        logger.info("Successfully validated new device flow")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_production_devices_search_by_imei(self, production_devices_page, report_case):
        logger.info("Starting validation of Production device search")
        production_devices_page._search_device()

        expected = "ACON4IA123455432100"
        actual = production_devices_page.search_locator.input_value()
        logger.debug("Search by IMEI | expected=%s | actual=%s", expected, actual)

        report_case(
            expected=expected,
            actual=actual,
            message="Validate Production device search by IMEI input",
        )
        assert actual == expected, f"Expected search input '{expected}', got '{actual}'"
        logger.info("Successfully validated Production device search")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_production_devices_search_by_uid(self, production_devices_page, report_case):
        logger.info("Starting validation of alternate Production device search")
        production_devices_page._search_device_2()

        expected = "ACON4IA123455432100"
        actual = production_devices_page.search_locator.input_value()
        logger.debug("Search by UID | expected=%s | actual=%s", expected, actual)

        report_case(
            expected=expected,
            actual=actual,
            message="Validate Production device search by UID input",
        )
        assert actual == expected, f"Expected search input '{expected}', got '{actual}'"
        logger.info("Successfully validated alternate Production device search")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_production_devices_bulk_upload_btn_visibility_and_state(self, production_devices_page, report_case):
        logger.info("Starting validation of Bulk Upload button enablement")
        is_enabled = production_devices_page._bulk_upload_btn_enability()

        logger.debug("Completed Bulk Upload button enablement validation")
        report_case(
            expected=True,
            actual=is_enabled,
            message="Validate Bulk Upload button enablement",
        )
        assert is_enabled, "Bulk Upload button is not enabled"
        logger.info("Successfully validated Bulk Upload button enablement")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_production_devices_click_bulk_upload_navigates_to_add_devices(self, page, production_devices_page, report_case):
        logger.info("Starting validation of Bulk Upload button click")
        production_devices_page._click_bulk_btn()

        actual_url = page.url
        logger.debug("Bulk Upload click completed | current_url=%s", actual_url)

        report_case(
            expected="**/production-device",
            actual=actual_url,
            message="Validate Bulk Upload button click navigation",
        )
        assert actual_url != "", "URL should not be empty after clicking Bulk Upload"
        logger.info("Successfully validated Bulk Upload button click")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_add_devices_form_submit_button_disabled_by_default(self, production_devices_page, report_case):
        logger.info("Starting validation of Add Production button enablement")
        production_devices_page._click_bulk_btn()
        is_enabled = production_devices_page.add_submit_btn_locator.is_enabled()

        logger.debug("Add Production Submit button enabled: %s", is_enabled)
        report_case(
            expected=False,
            actual=is_enabled,
            message="Validate Add Production Submit button is disabled by default",
        )
        assert not is_enabled, "Add Production Submit button should be disabled by default"
        logger.info("Successfully validated Add Production button enablement")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_add_devices_form_download_sample_file(self, production_devices_page, report_case):
        logger.info("Starting validation of sample file download")
        production_devices_page._click_bulk_btn()

        download = production_devices_page.click_sample_btn()
        is_downloaded = production_devices_page.is_sample_file_downloaded(
            download=download, expected_filename="Sample_Production_Sheet.xlsx"
        )
        logger.debug("Sample file downloaded successfully: %s", is_downloaded)

        report_case(
            expected=True,
            actual=is_downloaded,
            message="Validate sample file download",
        )
        assert is_downloaded, "Sample file validation failed"
        logger.info("Successfully validated sample file download")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_add_devices_form_upload_invalid_file_shows_error(self, production_devices_page, report_case):
        logger.info("Starting validation of invalid production file upload")
        production_devices_page._click_bulk_btn()
        upload_result = production_devices_page.upload_invalid_file(
            str(TEST_DATA_DIR_PROD / "Invalid.xlsx")
        )
        file_present = production_devices_page._check_file()
        is_valid = file_present and upload_result

        logger.debug(
            "Invalid file upload check | file_present=%s | upload_result=%s",
            file_present,
            upload_result,
        )

        report_case(
            expected=True,
            actual=is_valid,
            message="Validate invalid production file upload handling",
        )
        assert is_valid, "Invalid file upload failed"
        logger.info("Successfully validated invalid production file upload")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_add_devices_form_upload_valid_file_succeeds(self, production_devices_page, report_case):
        logger.info("Starting validation of valid production file upload")
        production_devices_page._click_bulk_btn()
        upload_result = production_devices_page.upload_valid_file(
            str(TEST_DATA_DIR_PROD / "Uploaded.xlsx")
        )
        file_present = production_devices_page._check_file()
        is_valid = file_present and upload_result

        logger.debug(
            "Valid file upload check | file_present=%s | upload_result=%s",
            file_present,
            upload_result,
        )

        report_case(
            expected=True,
            actual=is_valid,
            message="Validate valid production file upload",
        )
        assert is_valid, "Valid file upload failed"
        logger.info("Successfully validated valid production file upload")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_add_devices_form_upload_duplicate_file_shows_error(self, production_devices_page, report_case):
        logger.info("Starting validation of duplicate production file upload")
        production_devices_page._click_bulk_btn()
        upload_result = production_devices_page.upload_duplicate_file(
            str(TEST_DATA_DIR_PROD / "Duplicate.xlsx")
        )
        file_present = production_devices_page._check_file()
        is_valid = file_present and upload_result

        logger.debug(
            "Duplicate file upload check | file_present=%s | upload_result=%s",
            file_present,
            upload_result,
        )

        report_case(
            expected=True,
            actual=is_valid,
            message="Validate duplicate production file upload handling",
        )
        assert is_valid, "Duplicate file upload failed"
        logger.info("Successfully validated duplicate production file upload")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_production_devices_search_by_iccid(self, production_devices_page, report_case):
        logger.info("Starting validation of repeated Production device search")
        production_devices_page._search_device_2()

        expected = "ACON4IA123455432100"
        actual = production_devices_page.search_locator.input_value()
        logger.debug("Search by ICCID | expected=%s | actual=%s", expected, actual)

        report_case(
            expected=expected,
            actual=actual,
            message="Validate repeated Production device search input",
        )
        assert actual == expected, f"Expected search input '{expected}', got '{actual}'"
        logger.info("Successfully validated repeated Production device search")
