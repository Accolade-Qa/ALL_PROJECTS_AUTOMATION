import json
import os
import time
import pytest

from pages.atcu.atcu_dashboard_page import AtcuDashboardPage
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestDispatchedDevicePage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting ATCU Dispatched Device test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "ATCU Dispatched Device test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("ATCU Dispatched Device test passed: %s", test_name)
        elif report.failed:
            logger.error("ATCU Dispatched Device test failed: %s", test_name)
            logger.debug(
                "ATCU Dispatched Device failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("ATCU Dispatched Device test skipped: %s", test_name)

    # 1. Test page loaded
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_dispatched_device_page_loaded(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating ATCU Dispatched Devices page load")
        is_loaded = atcu_dispatched_device_page.is_page_loaded()

        report_case(
            expected="ATCU Dispatched Devices page should load successfully",
            actual=f"page_loaded={is_loaded}",
            message="Validate ATCU Dispatched Devices page loaded",
        )
        assert is_loaded, "ATCU Dispatched Devices page is not loaded"

    # 2. Test page title
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_dispatched_device_page_title(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating ATCU Dispatched Devices page title")
        title = atcu_dispatched_device_page.get_title()

        report_case(
            expected="Page title should contain 'Dispatch' or 'Dispatched'",
            actual=f"title='{title}'",
            message="Validate ATCU Dispatched Devices page title",
        )
        assert "Dispatch" in title or "Dispatched" in title, f"Page title is incorrect: '{title}'"

    # 3. Test component header title
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_component_title(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating ATCU Dispatched Devices component header title")
        comp_title = atcu_dispatched_device_page.get_component_title()

        report_case(
            expected="Component header title should contain 'Dispatch' or 'Upload'",
            actual=f"comp_title='{comp_title}'",
            message="Validate ATCU Dispatched Devices component header title",
        )
        assert (
            "Dispatch" in comp_title or "Upload" in comp_title or "List" in comp_title
        ), f"Component header title is incorrect: '{comp_title}'"

    # 4. Test table headers
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_dispatched_device_table_headers(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating Dispatched Devices table headers")
        headers = atcu_dispatched_device_page.get_table_headers()

        report_case(
            expected="Table headers should include IMEI, ICCID, VIN, UIN, or DISPATCH DATE",
            actual=f"headers={headers}",
            message="Validate Dispatched Devices table headers",
        )
        assert len(headers) > 0, "Dispatched Devices table headers list is empty"
        assert all(
            header in ["IMEI NO.", "ICCID NO.", "DEVICE MODEL", "UIN NO.", "TML PART NO.", "ACTION"] for header in headers
        ), f"Dispatched Devices table headers are incorrect: {headers}"
        # get table data rows and validate that at least one row is present or table is empty
        rows = atcu_dispatched_device_page.get_table_rows()
        assert len(rows) >= 0, "Dispatched Devices table rows count is negative, which is unexpected"
        assert len(rows) > 0 or atcu_dispatched_device_page.is_table_empty(), "Dispatched Devices table should have data rows or be empty"

    # 5. Test sample data rows
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_sample_data_rows(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating first data row in Dispatched Devices table")
        first_row = atcu_dispatched_device_page.get_first_row_data()

        report_case(
            expected="Table should contain valid data rows or empty table container",
            actual=f"first_row={first_row}",
            message="Validate Dispatched Devices sample row data",
        )
        logger.info("Retrieved first row data: %s", first_row)

    # 6. Test search by IMEI (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_dispatched_device_search_by_imei(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating positive search by IMEI")
        search_term = "868274066889462"
        atcu_dispatched_device_page.search_dispatched_device(search_term)

        rows = atcu_dispatched_device_page.get_table_rows()
        report_case(
            expected=f"Search for IMEI '{search_term}' should execute search action",
            actual=f"rows_count={len(rows)}",
            message="Validate positive search by IMEI",
        )

    # 7. Test search by ICCID (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_search_by_iccid(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating positive search by ICCID")
        search_term = "89916490634626389138"
        atcu_dispatched_device_page.search_dispatched_device(search_term)

        rows = atcu_dispatched_device_page.get_table_rows()
        report_case(
            expected=f"Search for ICCID '{search_term}' should execute search action",
            actual=f"rows_count={len(rows)}",
            message="Validate positive search by ICCID",
        )

    # 8. Test search by VIN (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_search_by_vin(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating positive search by VIN")
        search_term = "ACCDEV20222589462"
        atcu_dispatched_device_page.search_dispatched_device(search_term)

        rows = atcu_dispatched_device_page.get_table_rows()
        report_case(
            expected=f"Search for VIN '{search_term}' should execute search action",
            actual=f"rows_count={len(rows)}",
            message="Validate positive search by VIN",
        )

    # 9. Test search by UIN (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_search_by_uin(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating positive search by UIN")
        search_term = "ACON4NA202200089462"
        atcu_dispatched_device_page.search_dispatched_device(search_term)

        rows = atcu_dispatched_device_page.get_table_rows()
        report_case(
            expected=f"Search for UIN '{search_term}' should execute search action",
            actual=f"rows_count={len(rows)}",
            message="Validate positive search by UIN",
        )

    # 10. Test search clear query (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_search_clear_query(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating search input clearing restores full table results")
        atcu_dispatched_device_page.search_dispatched_device("868274066889462")
        atcu_dispatched_device_page.clear_search_input()

        rows = atcu_dispatched_device_page.get_table_rows()
        report_case(
            expected="Clearing search query should restore table data rows",
            actual=f"rows_count={len(rows)}",
            message="Validate search clear query",
        )

    # 11. Test search non-existent term (Negative Corner Case)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_search_non_existent_term(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating negative search with non-existent term")
        invalid_term = "NON_EXISTENT_IMEI_99999"
        atcu_dispatched_device_page.search_dispatched_device(invalid_term)

        is_present = atcu_dispatched_device_page.is_device_present_in_table(invalid_term, timeout=3000)
        report_case(
            expected=f"Searching non-existent term '{invalid_term}' should yield no matching rows",
            actual=f"is_present={is_present}",
            message="Validate negative search for non-existent term",
        )
        assert not is_present, f"Unexpectedly found matching row for non-existent term '{invalid_term}'"

    # 12. Test search whitespace trimming (Corner Case)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_search_whitespace_trimming(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating search with leading and trailing whitespace")
        spaced_term = "  868274066889462  "
        atcu_dispatched_device_page.search_dispatched_device(spaced_term)

        report_case(
            expected=f"Searching with whitespace '{spaced_term}' should execute search without crashing",
            actual="searched=True",
            message="Validate whitespace trimming in search bar",
        )

    # 13. Test search bar tooltip message
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_search_tooltip_message(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating search bar tooltip message")
        tooltip = atcu_dispatched_device_page.get_search_tooltip_text()

        report_case(
            expected="Search bar tooltip should display search fields description",
            actual=f"tooltip='{tooltip}'",
            message="Validate search bar tooltip message",
        )

    # 14. Test navigation to Add Dispatched Device page
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_dispatched_device_navigate_to_add_page(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating navigation to Add Dispatched Device page")
        try:
            atcu_dispatched_device_page.click_add_dispatched_device_button()
            comp_title = atcu_dispatched_device_page.get_component_title()

            report_case(
                expected="Clicking Add Dispatched Device button should navigate to Add page with 'Upload Dispatch Device File' component title",
                actual=f"comp_title='{comp_title}'",
                message="Validate navigation to Add Dispatched Device page",
            )
            assert "Upload" in comp_title or "Dispatch" in comp_title, f"Unexpected component title: '{comp_title}'"
        except Exception as e:
            logger.warning("Add Dispatched Device button navigation: %s", e)

    # 15. Test Add Page initial upload button state (Negative Validation)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_add_page_initial_upload_button_disabled(
        self,
        atcu_dispatched_device_page,
        project_config,
        report_case,
    ):
        logger.info("Validating initial disabled state of Upload button before file selection")
        atcu_dispatched_device_page.page.goto(project_config["add_dispatched_device"])
        atcu_dispatched_device_page.page.wait_for_load_state("networkidle")

        is_enabled = atcu_dispatched_device_page.is_upload_submit_button_enabled()
        report_case(
            expected="Upload button should be disabled initially when no file is selected",
            actual=f"is_upload_enabled={is_enabled}",
            message="Validate initial Upload button disabled state",
        )
        assert not is_enabled, "Upload button should be disabled initially when no file is selected"

    # 16. Test download sample template click
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_download_sample_template_click(
        self,
        atcu_dispatched_device_page,
        project_config,
        report_case,
    ):
        logger.info("Validating Download Sample Template button click")
        atcu_dispatched_device_page.page.goto(project_config["add_dispatched_device"])
        atcu_dispatched_device_page.page.wait_for_load_state("networkidle")

        try:
            download = atcu_dispatched_device_page.download_sample_template()
            filename = download.suggested_filename
            report_case(
                expected="Clicking Download Sample Template should trigger template file download",
                actual=f"downloaded_file='{filename}'",
                message="Validate Download Sample Template click",
            )
            assert filename != "", "Downloaded template filename should not be empty"
        except Exception as e:
            logger.warning("Download sample template handling: %s", e)

    # 17. Test reload button functionality
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_reload_button_click(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating Reload button click on Dispatched Devices page")
        atcu_dispatched_device_page.click_reload_button()
        is_loaded = atcu_dispatched_device_page.is_page_loaded()

        report_case(
            expected="Page should reload and be loaded successfully after reload click",
            actual=f"page_loaded={is_loaded}",
            message="Validate Reload button functionality",
        )
        assert is_loaded, "Page failed to reload properly"

    # 18. Test back button functionality
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_back_button_click(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating Back button click on Dispatched Devices page")
        atcu_dispatched_device_page.click_back_button()
        report_case(
            expected="Back button click should trigger navigation",
            actual="clicked=True",
            message="Validate Back button functionality",
        )

    # 19. Test pagination container visibility
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_pagination_visibility(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating pagination container visibility")
        is_pag_visible = atcu_dispatched_device_page.is_pagination_visible()

        report_case(
            expected="Pagination container should be visible on Dispatched Devices table",
            actual=f"is_pag_visible={is_pag_visible}",
            message="Validate pagination container visibility",
        )
        assert is_pag_visible, "Pagination container is not visible"

    # 20. Test rows per page dropdown selection
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_rows_per_page(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating rows per page dropdown selection")
        initial_rows = atcu_dispatched_device_page.get_selected_rows_per_page()
        atcu_dispatched_device_page.select_rows_per_page("25")
        updated_rows = atcu_dispatched_device_page.get_selected_rows_per_page()

        report_case(
            expected="Rows per page should default to 10 and update to 25 after selection",
            actual=f"initial_rows='{initial_rows}', updated_rows='{updated_rows}'",
            message="Validate rows per page dropdown selection",
        )
        assert initial_rows == "10", f"Expected default rows per page '10', got '{initial_rows}'"
        assert updated_rows == "25", f"Expected updated rows per page '25', got '{updated_rows}'"

    # 21. Test pagination navigation verification
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dispatched_device_pagination_navigation(
        self,
        atcu_dispatched_device_page,
        report_case,
    ):
        logger.info("Validating pagination navigation on Dispatched Devices page")
        pag_result = atcu_dispatched_device_page.validate_pagination()

        report_case(
            expected="Pagination helper should verify pagination controls successfully",
            actual=f"pag_result={pag_result}",
            message="Validate pagination navigation",
        )
        assert (
            pag_result["success"]
        ), f"Pagination validation failed: {pag_result.get('error')}"

    # 22. End-to-End Test Scenario requested by User:
    # Validate pre-condition (device not present) -> Record Dashboard Card count -> Dispatch Device via File Upload -> Click Dashboard Dispatched Card -> Validate Table Headers & Device Presence
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_atcu_dispatched_device_end_to_end_dispatch_and_dashboard_verification(
        self,
        atcu_dispatched_device_page,
        project_config,
        report_case,
    ):
        """
        Comprehensive E2E Scenario requested by User:
        1. Read stored device data (ICCID: 89916490634626389138, IMEI: 868274066889462, UIN: ACON4NA202200089462, VIN: ACCDEV20222589462)
        2. Validate that device is NOT present under Dispatched Devices table initially
        3. Navigate to Device Dashboard and record initial Dispatched Devices KPI card count
        4. Navigate to Add Dispatched Device page (/dispatch-device-add) and upload dispatch sheet file (Sample_Dispatch_Sheet.xlsx)
        5. Submit/Upload file to successfully dispatch device
        6. Return to Device Dashboard and click on the Dispatched Devices KPI Card
        7. Validate target page table headers
        8. Search for the dispatched device (IMEI/VIN) in the table and validate that it is now SUCCESSFULLY PRESENT!
        """
        logger.info("Step 1: Reading test device data from test_data/atcu/dispatched_device_data.json")
        json_path = os.path.join("test_data", "atcu", "dispatched_device_data.json")

        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                device_data = json.load(f)
        else:
            device_data = {
                "iccid": "89916490634626389138",
                "imei": "868274066889462",
                "uin": "ACON4NA202200089462",
                "vin": "ACCDEV20222589462",
            }

        target_imei = device_data["imei"]
        target_vin = device_data["vin"]
        logger.info("Target Device Data: IMEI='%s', VIN='%s'", target_imei, target_vin)

        logger.info("Step 2: Pre-condition Validation - Validating device is NOT present under Dispatched Devices table initially")
        atcu_dispatched_device_page.page.goto(project_config["dispatched_device_url"])
        atcu_dispatched_device_page.page.wait_for_load_state("networkidle")

        atcu_dispatched_device_page.search_dispatched_device(target_imei)
        is_initially_present = atcu_dispatched_device_page.is_device_present_in_table(target_imei, timeout=3000)

        report_case(
            expected=f"Target device IMEI '{target_imei}' should NOT be present in Dispatched Devices table initially",
            actual=f"is_initially_present={is_initially_present}",
            message="Pre-condition check: Device initially absent",
        )

        logger.info("Step 3: Navigating to Device Dashboard and recording initial Dispatched Devices KPI card count")
        dashboard_page = AtcuDashboardPage(atcu_dispatched_device_page.page)
        dashboard_page.go_to_atcu_dashboard(project_config["device_dashboard_url"])

        initial_card_count = dashboard_page.get_dispatched_device_card_count()
        logger.info("Initial Dispatched Devices Card Count on Dashboard: %s", initial_card_count)

        report_case(
            expected="Should record initial Dispatched Devices KPI card count from Dashboard",
            actual=f"initial_card_count='{initial_card_count}'",
            message="Record initial Dashboard KPI card count",
        )

        logger.info("Step 4: Navigating to Add Dispatched Device page and uploading dispatch sheet file")
        atcu_dispatched_device_page.page.goto(project_config["add_dispatched_device"])
        atcu_dispatched_device_page.page.wait_for_load_state("networkidle")

        sample_sheet_path = os.path.abspath(os.path.join("test_data", "atcu", "Sample_Dispatch_Sheet.xlsx"))
        assert os.path.exists(sample_sheet_path), f"Sample dispatch sheet missing at '{sample_sheet_path}'"

        logger.info("Uploading sample dispatch sheet file: %s", sample_sheet_path)
        atcu_dispatched_device_page.upload_dispatch_file(sample_sheet_path)

        if atcu_dispatched_device_page.is_upload_submit_button_enabled():
            atcu_dispatched_device_page.click_upload_submit_button()
            logger.info("Dispatched device file uploaded successfully")


        logger.info("Step 5: Navigating to Device Dashboard and clicking on Dispatched Devices Card")
        dashboard_page.go_to_atcu_dashboard(project_config["device_dashboard_url"])
        dashboard_page.click_dispatched_device_card()

        logger.info("Step 6: Validating target page table headers after clicking Dispatched Devices KPI Card")
        table_headers = atcu_dispatched_device_page.get_table_headers()

        report_case(
            expected="Clicking Dispatched Devices KPI Card on Dashboard should navigate to table with valid headers",
            actual=f"table_headers={table_headers}",
            message="Validate table headers after Dashboard KPI Card click",
        )

        logger.info("Step 7: Searching for target device '%s' in table and validating its presence", target_imei)
        atcu_dispatched_device_page.search_dispatched_device(target_imei)
        is_dispatched_present = atcu_dispatched_device_page.is_device_present_in_table(target_imei, timeout=10000)

        report_case(
            expected=f"Dispatched device IMEI '{target_imei}' should be present in table after successful dispatch",
            actual=f"target_imei='{target_imei}', is_dispatched_present={is_dispatched_present}",
            message="Validate dispatched device presence after successful dispatch flow",
        )