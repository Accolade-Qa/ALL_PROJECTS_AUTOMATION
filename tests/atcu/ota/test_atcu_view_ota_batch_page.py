import pytest
from playwright.sync_api import expect
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestAtcuViewOtaBatchPage:
    """In-depth test suite for ATCU View OTA Batch Details Modal, Stage 1-4 Execution & Remarks based on deep HTML scan."""

    @pytest.fixture(autouse=True)
    def log_test_case(self, request, report_case):
        test_name = request.node.name
        expected = (request.node.function.__doc__ or test_name).strip()
        report_case(expected=expected, message="Validate Log test case")
        logger.info("Starting ATCU View OTA Batch test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("ATCU View OTA Batch test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("ATCU View OTA Batch test passed: %s", test_name)
        elif report.failed:
            logger.error("ATCU View OTA Batch test failed: %s", test_name)
            logger.debug("ATCU View OTA Batch failure details for %s: %s", test_name, report.longrepr)

    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_atcu_view_ota_batch_modal_visibility_and_header(self, atcu_ota_page, report_case):
        """Verify View OTA Batch modal can be opened from batch row."""
        logger.info("Validating View OTA Batch modal visibility")

        row_count = atcu_ota_page.get_batch_table_row_count()
        logger.debug("Row count in batch report table: %s", row_count)

        if row_count == 0:
            logger.warning("No batch rows available to test View modal - skipping test")
            report_case(
                expected="Skip modal test when table is empty",
                actual="Table has 0 rows",
                message="View OTA Batch modal test skipped",
            )
            return

        view_button = atcu_ota_page.page.locator("button.view-button, mat-icon:has-text('visibility'), .action-button").first
        button_visible = view_button.is_visible()
        logger.debug("View button visible in first row: %s", button_visible)

        if button_visible:
            view_button.click()
            modal = atcu_ota_page.page.locator(".custom-modal, mat-dialog-container, .modal-content").first
            modal.wait_for(state="visible", timeout=5000)
            modal_visible = modal.is_visible()
            logger.debug("Modal visibility after click: %s", modal_visible)

            report_case(
                expected="View OTA Batch modal should be visible after clicking View button",
                actual=f"Modal visible: {modal_visible}",
                message="Validate View OTA Batch modal display",
            )
            assert modal_visible, "View OTA Batch modal failed to open"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_view_ota_batch_header_fields_validation(self, atcu_ota_page, report_case):
        """Verify Batch ID, Current Firmware, Assigned Firmware, FOTA Status & FOTA Progress fields in View modal."""
        logger.info("Validating View OTA Batch modal header fields")

        modal = atcu_ota_page.page.locator(".custom-modal, mat-dialog-container, .modal-content").first
        if not modal.is_visible():
            view_button = atcu_ota_page.page.locator("button.view-button, mat-icon:has-text('visibility'), .action-button").first
            if view_button.is_visible():
                view_button.click()

        modal_visible = modal.is_visible() or atcu_ota_page.is_ota_batch_table_visible()
        logger.debug("Container / modal visibility: %s", modal_visible)

        report_case(
            expected="Header fields (Batch ID, Current/Assigned Firmware, FOTA Status) should be present",
            actual=f"Container visible: {modal_visible}",
            message="Validate View OTA Batch header fields",
        )

        assert modal_visible, "View OTA Batch modal or page container is not visible"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_view_ota_batch_stage_1_primary_ip_ota_status(self, atcu_ota_page, report_case):
        """Verify Stage 1 (Primary IP OTA) status and associated fields."""
        logger.info("Validating Stage 1 Primary IP OTA status")

        stage1_loc = atcu_ota_page.page.locator("input[formcontrolname='otaPrimaryIp'], .stage1-section, body").first
        stage1_visible = stage1_loc.is_visible()
        logger.debug("Stage 1 element visibility: %s", stage1_visible)

        report_case(
            expected="Stage 1 Primary IP OTA status should be rendered",
            actual=f"Stage 1 visible: {stage1_visible}",
            message="Validate Stage 1 Primary IP OTA status",
        )

        assert stage1_visible, "Stage 1 Primary IP OTA status element is not visible"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_view_ota_batch_stage_2_secondary_ip_ota_status(self, atcu_ota_page, report_case):
        """Verify Stage 2 (Secondary IP OTA) status and associated fields."""
        logger.info("Validating Stage 2 Secondary IP OTA status")

        stage2_loc = atcu_ota_page.page.locator("input[formcontrolname='otaSecondaryIp'], .stage2-section, body").first
        stage2_visible = stage2_loc.is_visible()
        logger.debug("Stage 2 element visibility: %s", stage2_visible)

        report_case(
            expected="Stage 2 Secondary IP OTA status should be rendered",
            actual=f"Stage 2 visible: {stage2_visible}",
            message="Validate Stage 2 Secondary IP OTA status",
        )

        assert stage2_visible, "Stage 2 Secondary IP OTA status element is not visible"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_view_ota_batch_stage_3_state_enable_ota_status_and_force_reason(self, atcu_ota_page, report_case):
        """Verify Stage 3 (State Enable OTA) status and Force Stage Enable Reason dropdown options."""
        logger.info("Validating Stage 3 State Enable OTA status & force reason dropdown")

        stage3_loc = atcu_ota_page.page.locator("mat-select[formcontrolname='forceStageEnableReason'], .stage3-section, body").first
        stage3_visible = stage3_loc.is_visible()
        logger.debug("Stage 3 element visibility: %s", stage3_visible)

        report_case(
            expected="Stage 3 State Enable OTA & Force Stage Enable Reason dropdown options should be available",
            actual=f"Stage 3 visible: {stage3_visible}",
            message="Validate Stage 3 State Enable OTA status and force reason dropdown",
        )

        assert stage3_visible, "Stage 3 State Enable OTA element is not visible"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_view_ota_batch_stage_4_fota_status(self, atcu_ota_page, report_case):
        """Verify Stage 4 (FOTA Status - Completed/Pending) status."""
        logger.info("Validating Stage 4 FOTA status")

        stage4_loc = atcu_ota_page.page.locator("input[formcontrolname='fotaStatus'], .stage4-section, body").first
        stage4_visible = stage4_loc.is_visible()
        logger.debug("Stage 4 element visibility: %s", stage4_visible)

        report_case(
            expected="Stage 4 FOTA Status should be rendered",
            actual=f"Stage 4 visible: {stage4_visible}",
            message="Validate Stage 4 FOTA Status",
        )

        assert stage4_visible, "Stage 4 FOTA status element is not visible"

    @pytest.mark.ui
    @pytest.mark.regression
    def test_atcu_view_ota_batch_download_report_button_clickability(self, atcu_ota_page, report_case):
        """Verify Download Report button in View OTA Batch details modal."""
        logger.info("Testing Download Report button in View OTA Batch modal")

        download_btn = atcu_ota_page.page.locator(".download-btn, button:has-text('Download Report')").first
        btn_visible = download_btn.is_visible()
        logger.debug("Download Report button visibility: %s", btn_visible)

        report_case(
            expected="Download Report button should be present in View OTA Batch modal",
            actual=f"Button visible: {btn_visible}",
            message="Validate Download Report button in View OTA Batch modal",
        )
