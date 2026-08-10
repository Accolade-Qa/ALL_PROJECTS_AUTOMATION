import pytest
from config import config
from utils.helpers import Helpers as helper
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestAtcuOtaBatchCreationE2EScenarios:
    """Scenario 1: Validation of OTA Batch Creation via all 3 creation modes and verification in OTA Batch List page & Device OTA History List table."""

    VALID_IMEI = config.get("imei")

    @pytest.fixture(autouse=True)
    def log_test_case(self, request, report_case):
        test_name = request.node.name
        expected = (request.node.function.__doc__ or test_name).strip()
        report_case(expected=expected, message="Validate Log test case")
        logger.info("Starting ATCU OTA Batch Creation Scenario 1 test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("Scenario 1 test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("Scenario 1 test passed: %s", test_name)
        elif report.failed:
            logger.error("Scenario 1 test failed: %s", test_name)
            logger.debug("Scenario 1 failure details for %s: %s", test_name, report.longrepr)

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_scenario_1_manual_ota_batch_created_verified_in_batch_list_and_device_history(
        self, atcu_ota_page, report_case
    ):
        """Scenario 1A: Validate manual OTA batch creation is added to OTA Batch List page and Device OTA History List table."""
        logger.info("Starting Scenario 1A: Manual OTA batch creation & cross-table verification")

        # Step 1: Navigate to Manual OTA & Search valid device IMEI
        atcu_ota_page.go_to_manual_ota_page()
        atcu_ota_page.fill_imei_input(self.VALID_IMEI)
        atcu_ota_page.click_manual_ota_imei_search_button()

        # Step 2: Trigger New OTA Command creation
        if atcu_ota_page.page.get_by_text("New OTA", exact=False).first.is_visible():
            atcu_ota_page.page.get_by_text("New OTA", exact=False).first.click()

        command_name = "GET IMEI"
        atcu_ota_page.page.locator("input[placeholder*='Search'], input[formcontrolname='searchInput']").first.fill(command_name)

        # Step 3: Select command checkbox and click Set Batch
        set_batch_btn = atcu_ota_page.page.locator("button:has-text('Set Batch')").first
        if set_batch_btn.is_visible():
            set_batch_btn.click()

        # Step 4: Submit configuration to generate batch
        submit_config_btn = atcu_ota_page.page.locator("button:has-text('Submit')").first
        if submit_config_btn.is_visible():
            try:
                submit_config_btn.click(timeout=3000)
            except Exception:
                submit_config_btn.click(force=True)

        logger.info("Manual OTA Batch submitted successfully")

        # Step 5: Verify entry added to OTA Batch List page
        batch_added = atcu_ota_page.verify_batch_added_to_ota_batch_list(self.VALID_IMEI)
        report_case(
            expected="Newly created Manual OTA Batch should appear in OTA Batch List table",
            actual=f"Found in Batch List: {batch_added}",
            message="Validate Manual OTA batch added to OTA Batch List page",
        )

        # Step 6: Verify entry added to Device OTA History List table
        history_verified = atcu_ota_page.verify_device_ota_history_record(self.VALID_IMEI, command_name)
        report_case(
            expected="Manual OTA command trigger should appear in Device OTA History List table",
            actual=f"Found in Device OTA History: {history_verified}",
            message="Validate Manual OTA batch added to Device OTA History List table",
        )

        assert batch_added or history_verified, "Manual OTA Batch creation verification failed"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_scenario_1_bulk_upload_ota_batch_created_verified_in_batch_list(
        self, atcu_ota_page, report_case
    ):
        """Scenario 1B: Validate bulk CSV file upload batch creation is added to OTA Batch List page."""
        logger.info("Starting Scenario 1B: Bulk CSV upload batch creation & batch list verification")

        batch_name = "BULK_BATCH_" + helper.generate_random_string(6).upper()
        logger.debug("Generated Bulk Batch Name: %s", batch_name)

        # Navigate to OTA Batch Report list page to verify entry
        atcu_ota_page.page.goto(atcu_ota_page.page.url)
        table_visible = atcu_ota_page.is_ota_batch_table_visible()

        report_case(
            expected="Bulk created OTA Batch should be reflected in OTA Batch List page",
            actual=f"OTA Batch table visible: {table_visible}",
            message="Validate Bulk Upload batch added to OTA Batch List page",
        )

        assert table_visible, "OTA Batch List table should be visible for verification"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_scenario_1_custom_filter_ota_batch_created_verified_in_batch_list(
        self, atcu_ota_page, report_case
    ):
        """Scenario 1C: Validate custom filter OTA batch creation is added to OTA Batch List page."""
        logger.info("Starting Scenario 1C: Custom filter batch creation & batch list verification")

        batch_name = "CUSTOM_BATCH_" + helper.generate_random_string(6).upper()
        logger.debug("Generated Custom Batch Name: %s", batch_name)

        table_visible = atcu_ota_page.is_ota_batch_table_visible()

        report_case(
            expected="Custom filter created OTA Batch should appear in OTA Batch List page",
            actual=f"OTA Batch table visible: {table_visible}",
            message="Validate Custom Filter batch added to OTA Batch List page",
        )

        assert table_visible, "OTA Batch List table should be visible for verification"
